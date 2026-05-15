# ============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS CON SQLALCHEMY
# ============================================================================
# Este archivo establece la conexión con MySQL usando SQLAlchemy como ORM.
# ORM = Object Relational Mapping (mapeo de objetos a tablas SQL)
# ============================================================================

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargamos las variables del archivo .env
load_dotenv()

# Obtenemos la URL de Aiven desde el archivo .env
# Si por alguna razón no la encuentra, intenta usar el localhost por defecto
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root:@localhost:3306/proyecto_fin_grado"
)

# Creamos el motor de conexión
# echo=False para que no ensucie la consola con logs de SQL
engine = create_engine(DATABASE_URL, echo=False)

# Clase para crear las sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos (tablas)
Base = declarative_base()

# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/proyecto_fin_grado"

# Crear el motor (engine) de la base de datos
# echo=True muestra en consola las consultas SQL (útil para debug en desarrollo)
engine = create_engine(
    DATABASE_URL,
    echo=False  # Cambia a True si quieres ver las consultas SQL en consola
)

# SessionLocal es la clase que usaremos para crear sesiones de BD
# Una sesión = conexión a la BD durante operaciones CRUD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase base para todos nuestros modelos SQLAlchemy
# Todos los modelos heredarán de esta clase
Base = declarative_base()

# FUNCIÓN PARA OBTENER LA SESIÓN DE BASE DE DATOS
# ================================================
# Esta función se usará como dependencia en FastAPI
# Yield = permite que FastAPI cierre correctamente la sesión después de cada petición
def get_db():

    Generador que proporciona una sesión de BD para cada petición.
    Usado con Depends() en las rutas de FastAPI.
    
    Ejemplo:
        @app.post("/users")
        def crear_usuario(db: Session = Depends(get_db)):
            # aquí se usa db para hacer operaciones

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Siempre cerramos la sesión (incluso si hay error)
"""