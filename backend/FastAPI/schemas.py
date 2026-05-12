# ============================================================================
# SCHEMAS PYDANTIC - VALIDACIÓN DE DATOS EN PETICIONES
# ============================================================================
# Los Schemas validan y transforman los datos que recibimos del cliente.
# Se usan para: validar emails, contraseñas, saldos, etc.
# ============================================================================

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional

# ==================== SCHEMAS DE CLIENTE ====================

class ClienteRegistro(BaseModel):
    """Datos requeridos para registrar un nuevo cliente"""
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    dni: str
    telefono: str
    email: EmailStr
    password: str = Field(..., min_length=6)
    nacionalidad: str
    direccion: str
    provincia: str
    ciudad: str
    codigo_postal: str
    pais_residencia: str
    situacion_laboral: str

class ClienteLogin(BaseModel):
    """Datos para login (POST /login) - Solo email y contraseña"""
    email: str = Field(..., description="Email del cliente")
    password: str = Field(..., description="Contraseña")

class ClienteActualizar(BaseModel):
    """Datos para actualizar perfil del cliente (PUT /clientes/{id})"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    telefono: Optional[str] = None
    # Email y DNI NO se pueden cambiar (por seguridad)

class ClienteResponse(BaseModel):
    """Datos de cliente (sin password por seguridad)"""
    id: int
    nombre: str
    apellidos: str
    email: str
    dni: str
    telefono: str
    saldo: float
    nacionalidad: str
    ciudad: str
    provincia: str
    
    class Config:
        from_attributes = True


# ==================== SCHEMAS DE TRANSACCIONES ====================

class TransaccionBizum(BaseModel):
    """
    Datos para realizar un Bizum (POST /transferir).
    
    Validaciones:
    - cantidad > 0 (no se puede enviar dinero negativo)
    - cantidad <= 500 (máximo por transferencia)
    - concepto opcional (por qué se envía el dinero)
    - numero_receptor: número de teléfono del receptor (para identificarlo)
    - nombre_receptor: nombre del receptor (para verificar que es correcto)
    """
    cantidad: float = Field(..., gt=0, description="Cantidad a transferir (mayor que 0)")
    numero_receptor: str = Field(..., description="Teléfono del receptor")
    nombre_receptor: str = Field(..., min_length=1, description="Nombre del receptor (para verificar)")
    concepto: Optional[str] = Field(None, max_length=255, description="Motivo del Bizum (opcional)")

class TransaccionResponse(BaseModel):
    """Datos de una transacción en respuestas (GET /transacciones/{cliente_id})"""
    id: int
    id_emisor: int
    id_receptor: int
    cantidad: float
    concepto: Optional[str]
    fecha: datetime
    emisor: Optional[str] = None  # Email del emisor
    receptor: Optional[str] = None  # Email del receptor
    nombre_receptor: Optional[str] = None  # Nombre del receptor (si está disponible)
    
    class Config:
        from_attributes = True

class HistorialResponse(BaseModel):
    """
    Respuesta completa del historial de transacciones de un cliente.
    Incluye tanto transacciones enviadas como recibidas.
    """
    saldo_actual: float
    transacciones_recibidas: list[TransaccionResponse]
    transacciones_enviadas: list[TransaccionResponse]


# ==================== SCHEMAS DE RESPUESTAS JWT ====================

class Token(BaseModel):
    """Respuesta después del login exitoso"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Datos dentro del JWT token decodificado"""
    email: Optional[str] = None
    exp: Optional[datetime] = None
