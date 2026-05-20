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

# Obtenemos la URL de la BD desde variables de entorno
# En local se mantiene un fallback, pero en Vercel debe configurarse DATABASE_URL.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:@localhost:3306/proyecto_fin_grado",
)

# Aiven MySQL funciona mejor con TLS habilitado. Permitimos desactivarlo en local.
DB_SSL_DISABLED = os.getenv("DB_SSL_DISABLED", "false").lower() == "true"

# Creamos el motor de conexión
# pool_pre_ping/pool_recycle ayudan en entornos serverless con conexiones cortadas.
engine_kwargs = {
    "echo": False,
    "pool_pre_ping": True,
    "pool_recycle": 280,
}

if not DB_SSL_DISABLED and "localhost" not in DATABASE_URL and "127.0.0.1" not in DATABASE_URL:
    # En PyMySQL, pasar un dict vacío en ssl fuerza TLS.
    engine_kwargs["connect_args"] = {"ssl": {}}

engine = create_engine(DATABASE_URL, **engine_kwargs)

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
