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
