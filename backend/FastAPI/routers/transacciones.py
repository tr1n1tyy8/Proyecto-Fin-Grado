# TRANSACCIONES BANCARIAS - BIZUM

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from ..bbdd import get_db
from ..models import Cliente, Transaccion
from ..schemas import TransaccionBizum, HistorialResponse, TransaccionResponse
from .autenticacion import get_current_user

router = APIRouter(
    prefix="/transacciones",
    tags=["transacciones"],
    responses={404: {"description": "Transacción no encontrada"}}
)


# RUTA: POST /transferir (hacer bizum)

@router.post("/transferir", response_model=dict, status_code=201)
async def transferir_bizum(
    transferencia: TransaccionBizum,
    usuario_autenticado: Cliente = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # VALIDACIÓN 1: No transferir a sí mismo
    if usuario_autenticado.telefono == transferencia.numero_receptor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes transferir dinero a tu propia cuenta"
        )
    
    # VALIDACIÓN 2: Cantidad válida (> 0)
    if transferencia.cantidad <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La cantidad debe ser mayor a 0"
        )
    
    # VALIDACIÓN 3: Máximo 500€ por transferencia
    if transferencia.cantidad > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El máximo por transferencia es de 500€"
        )
    
    # VALIDACIÓN 4: Saldo suficiente
    if usuario_autenticado.saldo < transferencia.cantidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Saldo insuficiente. Tienes {usuario_autenticado.saldo}€"
        )
    
    # VALIDACIÓN 5: Buscar receptor por teléfono
    receptor = db.query(Cliente).filter(
        Cliente.telefono == transferencia.numero_receptor
    ).first()
    
    if not receptor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receptor no encontrado. Verifica el número de teléfono"
        )
    
    # VALIDACIÓN 6: Verificar que el nombre coincide
    if receptor.nombre.lower() != transferencia.nombre_receptor.lower():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El nombre no coincide. El usuario con ese teléfono es: {receptor.nombre}"
        )
    
    # TRANSACCIÓN ATÓMICA: Actualizar saldos (se ejecuta todo o nada, si falla una parte, se revierte todo)

    try:
        # 1. Restar del emisor
        usuario_autenticado.saldo -= transferencia.cantidad
        
        # 2. Sumar al receptor
        receptor.saldo += transferencia.cantidad
        
        # 3. Crear registro de transacción en el historial
        nueva_transaccion = Transaccion(
            id_emisor=usuario_autenticado.id,
            id_receptor=receptor.id,
            cantidad=transferencia.cantidad,
            concepto=transferencia.concepto or "Transferencia Bizum"
        )
        
        # 4. Guardar todo en la BD
        db.add(nueva_transaccion)
        db.commit()  # Si llega aquí, la transacción se guarda
        
    except Exception as e:
        # Si hay error, revertir todos los cambios
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar la transferencia. Vuelva a intentarlo"
        )
    
    # Transferencia exitosa
    return {
        "estado": "éxito",
        "mensaje": f"Transferencia de {transferencia.cantidad}€ a {receptor.nombre} realizada",
        "nuevo_saldo": usuario_autenticado.saldo,
        "id_transaccion": nueva_transaccion.id,
        "receptor": receptor.nombre
    }


# RUTA: GET /ultimas (obtener últimas 5 transacciones del usuario)

@router.get("/ultimas", response_model=list[TransaccionResponse])
async def obtener_ultimas_transacciones(
    usuario_autenticado: Cliente = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    usuario_id = usuario_autenticado.id
    print(f"Buscando transacciones para usuario ID: {usuario_id}")
    
    # Obtener todas las transacciones del usuario (enviadas + recibidas) ordenadas por fecha
    transacciones = db.query(Transaccion).options(
        joinedload(Transaccion.emisor),
        joinedload(Transaccion.receptor)
    ).filter(
        (Transaccion.id_emisor == usuario_id) | (Transaccion.id_receptor == usuario_id)
    ).order_by(Transaccion.fecha.desc()).limit(5).all()
    
    print(f"Encontradas {len(transacciones)} transacciones")
    
    if not transacciones:
        print("Sin transacciones encontradas")
        return []
    
    # Convertir a schemas de respuesta con información adicional
    resultado = []
    for t in transacciones:
        try:
            # Obtener datos del emisor y receptor
            email_emisor = t.emisor.email if t.emisor else None
            email_receptor = t.receptor.email if t.receptor else None
            nombre_emisor = t.emisor.nombre if t.emisor else None
            nombre_receptor = t.receptor.nombre if t.receptor else None
            
            print(f"Trans #{t.id}: {email_emisor} → {email_receptor} | {t.cantidad}€")
            
            # Crear el diccionario para TransaccionResponse
            trans_dict = {
                "id": t.id,
                "id_emisor": t.id_emisor,
                "id_receptor": t.id_receptor,
                "cantidad": t.cantidad,
                "concepto": t.concepto,
                "fecha": t.fecha,
                "emisor": email_emisor,
                "receptor": email_receptor,
                "nombre_emisor": nombre_emisor,
                "nombre_receptor": nombre_receptor
            }
            
            trans_response = TransaccionResponse(**trans_dict)
            resultado.append(trans_response)
        except Exception as e:
            print(f"Error procesando transacción: {e}")
    
    print(f"Retornando {len(resultado)} transacciones")
    return resultado


# RUTA: GET /transacciones/{cliente_id} (historial de movimientos)

@router.get("/{cliente_id}", response_model=HistorialResponse)
async def obtener_historial(
    cliente_id: int,
    usuario_autenticado: Cliente = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Verificar que solo ve su propio historial
    if usuario_autenticado.id != cliente_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver el historial de otros usuarios"
        )
    
    # Buscar el cliente
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    # Obtener transacciones (ordenadas por fecha, más recientes primero)
    transacciones_enviadas = db.query(Transaccion).filter(
        Transaccion.id_emisor == cliente_id
    ).order_by(Transaccion.fecha.desc()).all()
    
    transacciones_recibidas = db.query(Transaccion).filter(
        Transaccion.id_receptor == cliente_id
    ).order_by(Transaccion.fecha.desc()).all()
    
    # Convertir a schemas de respuesta
    return HistorialResponse(
        saldo_actual=cliente.saldo,
        transacciones_enviadas=[
            TransaccionResponse.from_orm(t) for t in transacciones_enviadas
        ],
        transacciones_recibidas=[
            TransaccionResponse.from_orm(t) for t in transacciones_recibidas
        ]
    )