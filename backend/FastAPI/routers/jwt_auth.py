# AUTENTICACIÓN SEGURA CON JWT (usuario y contraseña)

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta # trabajar con la fecha del sistema y cálculos de fecha (seguridad con la duración del token)

# función de hash para las contraseñas
ALGORITHM = "HS256" #constante
ACCESS_TOKEN_DURATION = 1   # duración del token (en minutos)
SECRET = "ceaad262e916ec4fff4df3c3f7679e7913d209bcaad56df1cfa9612f5665c00a" # clave secreta generada con openssl rand -hex 32 para encriptar el token

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")    # criterio de autenticación
crypt = CryptContext(schemes=["bcrypt"])    # algoritmo que va a usar para encriptar las contraseñas


class User(BaseModel):
    usuario: str
    nombre_completo: str
    email: str
    desactivado: bool

class UserDB(User):
    contraseña: str

bd_usuarios = {
    "sandra": {
        "usuario": "sandra", 
        "nombre_completo": "Sandra García", 
        "email": "sandra@example.com", 
        "desactivado": False, 
        "contraseña": crypt.hash("1234") #1234 encriptada con bcrypt
    },
    "juan": {
        "usuario": "juan", 
        "nombre_completo": "Juan Pérez", 
        "email": "juan@example.com", 
        "desactivado": True,
        "contraseña": crypt.hash("5678")
    }
}

def search_user(usuario: str):
    if usuario in bd_usuarios:
        return UserDB(**bd_usuarios[usuario])   
    return None

async def auth_user(token: str = Depends(oauth2)):   # dependencia pq el token depende de la búsqueda en el sistema de autenticación

    exception = HTTPException(status_code=401, detail="Credenciales inválidas")

    try:
        user = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")   #decodificar el token para obtener la información del usuario
        if user is None:
            raise exception
    except JWTError:
        raise exception
    
    return search_user(user)

async def usuario_actual(user: User = Depends(auth_user)): 
    if user.desactivado:
        raise HTTPException(status_code=400, detail="Cuenta desactivada")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = bd_usuarios.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    user = search_user(form.username)

    if not crypt.verify(form.password, user.contraseña):    #comprobar que la contraseña introducida coincide con la contraseña encriptada en la base de datos
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    # generar el token JWT con la información del usuario para que se autentique (en este caso, el nombre de usuario)
    access_token = {"sub": user.usuario,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}   #sub: identificador del usuario (nombre de usuario) // exp: fecha de expiración del token

    return{"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(usuario_actual)): # Esto en el proyecto sería el equivalente a no dejar pasar al dashboard a cualquiera
    return user