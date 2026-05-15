# ============================================================================
# AUTENTICACIÓN SEGURA CON JWT Y BASE DE DATOS
# ============================================================================
# Este módulo gestiona:
# 1. Registro de nuevos usuarios (POST /register)
# 2. Login con JWT (POST /login)
# 3. Obtener usuario autenticado (GET /users/me)
# 4. Protección de rutas con OAuth2PasswordBearer
# ============================================================================

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Importar desde nuestros módulos
from ..database import get_db
from ..models import Cliente, InitioSesion
from ..schemas import ClienteRegistro, ClienteResponse, Token, ClienteActualizarCompleto

# ============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================================================

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 30  # Subido a 30 min para que no se te cierre la sesión tan rápido probando

SECRET = "ceaad262e916ec4fff4df3c3f7679e7913d209bcaad56df1cfa9612f5665c00a"

# Contexto de cifrado con bcrypt
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Security Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(tags=["autenticación"])

# ============================================================================
# FUNCIONES AUXILIARES DE SEGURIDAD
# ============================================================================

def hash_password(password: str) -> str:
    """Convierte texto plano en un hash seguro"""
    return crypt.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara la contraseña del login con el hash de la BD"""
    return crypt.verify(plain_password, hashed_password)

def create_access_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token

# ============================================================================
# DEPENDENCIAS (PARA PROTEGER RUTAS)
# ============================================================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Cliente:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado o sesión expirada",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(Cliente).filter(Cliente.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user

# ============================================================================
# RUTAS DE AUTENTICACIÓN
# ============================================================================

@router.post("/registro", response_model=ClienteResponse, status_code=201)
async def register(
    client: ClienteRegistro,
    db: Session = Depends(get_db)
):
    # ✓ VALIDACIONES DE EXISTENCIA
    if db.query(Cliente).filter(Cliente.email == client.email).first():
        raise HTTPException(status_code=400, detail="Este email ya está registrado")
    
    if db.query(Cliente).filter(Cliente.dni == client.dni).first():
        raise HTTPException(status_code=400, detail="Este DNI ya está registrado")

    # ✓ PROCESAR FECHA
    # Pydantic ya convierte el string a date, solo necesitamos convertirlo a datetime
    fecha_nac = datetime.combine(client.fecha_nacimiento, datetime.min.time())
    
    # ✓ CREAR CLIENTE CON CONTRASEÑA HASHEADA
    nuevo_cliente = Cliente(
        nombre=client.nombre,
        apellidos=client.apellidos,
        fecha_nacimiento=fecha_nac,
        dni=client.dni,
        telefono=client.telefono,
        email=client.email,
        nacionalidad=client.nacionalidad,
        direccion=client.direccion,
        provincia=client.provincia,
        ciudad=client.ciudad,
        codigo_postal=client.codigo_postal,
        pais_residencia=client.pais_residencia,
        situacion_laboral=client.situacion_laboral,
        saldo=0.00,
        # AQUÍ ESTÁ LA MAGIA: Hasheamos la contraseña que viene del Pydantic
        password=hash_password(client.password) 
    )
    
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


@router.post("/login", response_model=Token)
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # 1. Buscar usuario por email
    user = db.query(Cliente).filter(Cliente.email == credentials.username).first()
    
    # 2. Verificar usuario y CONTRASEÑA
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Registrar el inicio de sesión
    nuevo_inicio = InitioSesion(id_cliente=user.id)
    db.add(nuevo_inicio)
    db.commit()
    
    # 4. Generar token si todo es correcto
    access_token = create_access_token(email=user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=ClienteResponse)
async def get_current_user_info(user: Cliente = Depends(get_current_user)):
    return user


@router.get("/usuarios/{email}", response_model=ClienteResponse)
async def get_usuario_por_email(
    email: str,
    user: Cliente = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtiene los datos de un usuario por su email (requiere estar autenticado)"""
    # Solo permite obtener datos del usuario autenticado
    if user.email != email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a otros usuarios"
        )
    
    return user


@router.get("/inicios-sesion/ultimos", response_model=list[dict])
async def obtener_ultimos_inicios_sesion(
    user: Cliente = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GET /inicios-sesion/ultimos - Obtener los 5 últimos inicios de sesión del usuario autenticado.
    
    ⚠️ PROTEGIDA: Requiere JWT token
    
    Returns:
        Lista de hasta 5 diccionarios con fecha_hora de los inicios de sesión
    """
    
    # Obtener los 5 últimos inicios de sesión del usuario autenticado
    inicios = db.query(InitioSesion).filter(
        InitioSesion.id_cliente == user.id
    ).order_by(InitioSesion.fecha_hora.desc()).limit(5).all()
    
    # Convertir a lista de diccionarios
    resultado = [
        {"fecha_hora": inicio.fecha_hora}
        for inicio in inicios
    ]
    
    return resultado


@router.put("/usuarios/actualizar/{email}", response_model=ClienteResponse)
async def actualizar_usuario(
    email: str,
    datos: ClienteActualizarCompleto,
    user: Cliente = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    PUT /usuarios/actualizar/{email} - Actualizar datos de un usuario.
    
    ⚠️ PROTEGIDA: Requiere JWT token
    ⚠️ AUTORIZACIÓN: Solo el usuario autenticado puede editar su propio perfil
    
    Campos que se actualizan:
    - nombre, apellidos, telefono, fecha_nacimiento
    - nacionalidad, direccion, provincia, ciudad
    - codigo_postal, pais_residencia, situacion_laboral
    
    Campos PROTEGIDOS (no se pueden cambiar):
    - email, dni, saldo, password
    
    Args:
        email: Email del usuario a actualizar (debe coincidir con usuario autenticado)
        datos: Schema ClienteActualizarCompleto con los datos a actualizar
        user: Usuario autenticado (obtenido de JWT)
        db: Sesión de base de datos
    
    Returns:
        ClienteResponse con los datos actualizados
    """
    
    # ✓ VERIFICAR PERMISO: Solo puede editar su propio perfil
    if user.email != email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar este usuario"
        )
    
    # ✓ ACTUALIZAR CAMPOS
    user.nombre = datos.nombre
    user.apellidos = datos.apellidos
    user.telefono = datos.telefono
    # Convertir date a datetime
    user.fecha_nacimiento = datetime.combine(datos.fecha_nacimiento, datetime.min.time())
    user.nacionalidad = datos.nacionalidad
    user.direccion = datos.direccion
    user.provincia = datos.provincia
    user.ciudad = datos.ciudad
    user.codigo_postal = datos.codigo_postal
    user.pais_residencia = datos.pais_residencia
    user.situacion_laboral = datos.situacion_laboral
    
    # ✓ GUARDAR CAMBIOS
    db.commit()
    db.refresh(user)
    
    return user







