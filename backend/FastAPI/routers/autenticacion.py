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
from ..models import Cliente
from ..schemas import ClienteRegistro, ClienteResponse, Token

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
    try:
        fecha_nac = datetime.strptime(client.fecha_nacimiento, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido (YYYY-MM-DD)")
    
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
        hashed_password=hash_password(client.password) 
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
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generar token si todo es correcto
    access_token = create_access_token(email=user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=ClienteResponse)
async def get_current_user_info(user: Cliente = Depends(get_current_user)):
    return user



















"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Importar desde nuestros módulos
from ..database import get_db
from ..models import Cliente
from ..schemas import ClienteRegistro, ClienteLogin, ClienteResponse, Token

# ============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================================================

# JWT: Algoritmo y duración del token
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 5  # Duración en minutos

# ⚠️ IMPORTANTE: Genera una clave secreta nueva con: openssl rand -hex 32
# NUNCA uses esta en producción. Está aquí solo como ejemplo.
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
    return crypt.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt.verify(plain_password, hashed_password)

def create_access_token(email: str) -> str:
    # Datos a incluir en el token
    payload = {
        "sub": email,  # Subject = email del usuario
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)  # Expiración
    }
    
    # Codificar el JWT
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token

# ============================================================================
# DEPENDENCIAS (PARA PROTEGER RUTAS)
# ============================================================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Cliente:
    # Mensaje de error genérico (por seguridad)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar el JWT
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Buscar el usuario en la BD
    user = db.query(Cliente).filter(Cliente.email == email).first()
    
    if user is None:
        raise credentials_exception
    
    return user

# ============================================================================
# RUTAS DE AUTENTICACIÓN
# ============================================================================

@router.post("/register", response_model=ClienteResponse, status_code=201)
async def register(
    client: ClienteRegistro,
    db: Session = Depends(get_db)
):

    # ✓ VALIDACIÓN 1: Email no existe
    existing_email = db.query(Cliente).filter(Cliente.email == client.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email ya está registrado"
        )
    
    # ✓ VALIDACIÓN 2: DNI no existe
    existing_dni = db.query(Cliente).filter(Cliente.dni == client.dni).first()
    if existing_dni:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este DNI ya está registrado"
        )
    
    # ✓ VALIDACIÓN 3: Teléfono no existe
    existing_telefono = db.query(Cliente).filter(Cliente.telefono == client.telefono).first()
    if existing_telefono:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este teléfono ya está registrado"
        )
    
    # ✓ Crear nuevo cliente con todos los campos
    try:
        fecha_nac = datetime.strptime(client.fecha_nacimiento, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de fecha inválido. Use YYYY-MM-DD"
        )
    
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
        saldo=0.00
        # ultimo_inicio_sesion se establece automáticamente con el datetime actual
    )
    
    # Guardar en la BD
    db.add(nuevo_cliente)
    db.commit()  # Confirmar cambios
    db.refresh(nuevo_cliente)  # Recargar el objeto para obtener el ID generado
    
    return nuevo_cliente


@router.post("/login", response_model=Token)
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # Buscar usuario por email (username en OAuth2)
    user = db.query(Cliente).filter(Cliente.email == credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # ✓ Generar JWT token (sin validar contraseña por ahora)
    access_token = create_access_token(email=user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=ClienteResponse)
async def get_current_user_info(user: Cliente = Depends(get_current_user)):
    return user
"""