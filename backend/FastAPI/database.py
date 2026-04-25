# ============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS CON SQLALCHEMY
# ============================================================================
# Este archivo establece la conexión con MySQL usando SQLAlchemy como ORM.
# ORM = Object Relational Mapping (mapeo de objetos a tablas SQL)
# ============================================================================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# CONFIGURACIÓN DE CONEXIÓN A MYSQL
# ====================================
# Formato: mysql+pymysql://usuario:contraseña@host:puerto/nombre_bbdd
# 
# ⚠️ IMPORTANTE: Cambia estos valores según tu configuración local:
# - usuario: generalmente 'root' en desarrollo local
# - contraseña: tu contraseña de MySQL (vacía si no tienes)
# - localhost: dirección del servidor (localhost para desarrollo local)
# - 3306: puerto por defecto de MySQL
# - proyecto_fin_grado: nombre de tu base de datos

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
    """
    Generador que proporciona una sesión de BD para cada petición.
    Usado con Depends() en las rutas de FastAPI.
    
    Ejemplo:
        @app.post("/users")
        def crear_usuario(db: Session = Depends(get_db)):
            # aquí se usa db para hacer operaciones
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Siempre cerramos la sesión (incluso si hay error)
