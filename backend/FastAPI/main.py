from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

# Importar routers
from .routers import autenticacion, transacciones

# Importar BD (para crear las tablas)
from .database import engine
from .models import Base

# ============================================================================
# INICIALIZACIÓN DE LA APLICACIÓN
# ============================================================================

app = FastAPI(
    title="Capitalia API",
    description="API segura para banca online con JWT y Bizum",
    version="1.0.0"
)

# ============================================================================
# CONFIGURACIÓN DE RUTAS ABSOLUTAS PARA ARCHIVOS ESTÁTICOS
# ============================================================================
# Obtener ruta base del proyecto (subir 2 niveles desde backend/FastAPI/)

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # /Users/sandra/PROYECTO/proyecto_fin_grado/

CSS_DIR = BASE_DIR / "css"
IMAGES_DIR = BASE_DIR / "images"
JS_DIR = BASE_DIR / "js"
FRONTEND_DIR = BASE_DIR / "frontend"

# ============================================================================
# CONFIGURACIÓN DE CORS (Para permitir peticiones desde el frontend)
# ============================================================================
# CORS = Cross-Origin Resource Sharing
# Permite que tu frontend acceda al backend sin bloqueos de seguridad

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Servidor frontend (puerto 3000)
        "http://localhost:8000",      # Servidor frontend desde FastAPI
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "file://",                     # Archivos locales (opcional)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ============================================================================
# MONTAR ARCHIVOS ESTÁTICOS
# ============================================================================
# Esto permite que FastAPI sirva archivos CSS, JS, imágenes directamente

# CSS estáticos
if CSS_DIR.exists():
    app.mount("/css", StaticFiles(directory=CSS_DIR), name="css")
else:
    print(f"⚠️  Carpeta CSS no encontrada: {CSS_DIR}")

# Imágenes estáticas
if IMAGES_DIR.exists():
    app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")
else:
    print(f"⚠️  Carpeta images no encontrada: {IMAGES_DIR}")

# JavaScript estático
if JS_DIR.exists():
    app.mount("/js", StaticFiles(directory=JS_DIR), name="js")
else:
    print(f"⚠️  Carpeta js no encontrada: {JS_DIR}")

# ============================================================================
# CREAR TABLAS EN LA DDBB
# ============================================================================
# Esta línea crea todas las tablas definidas en models.py
# Si ya existen, no hace nada (idempotente)

Base.metadata.create_all(bind=engine)

# ============================================================================
# INCLUIR ROUTERS
# ============================================================================

app.include_router(autenticacion.router)           # Rutas de autenticación
app.include_router(transacciones.router)  # Rutas de Bizum y historial

# ============================================================================
# SERVIR ARCHIVOS HTML DEL FRONTEND
# ============================================================================
# Rutas para acceder a los archivos HTML del formulario de registro y login

@app.get("/")
async def index():
    """Servir la página de inicio"""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file, media_type="text/html")
    return {"error": "index.html no encontrado"}

@app.get("/registro")
async def registro():
    """Servir página de registro"""
    archivo = FRONTEND_DIR / "registro.html"
    if archivo.exists():
        return FileResponse(archivo, media_type="text/html")
    return {"error": "registro.html no encontrado"}

@app.get("/registro2")
async def registro2():
    """Servir página 2 de registro"""
    archivo = FRONTEND_DIR / "registro2.html"
    if archivo.exists():
        return FileResponse(archivo, media_type="text/html")
    return {"error": "registro2.html no encontrado"}

@app.get("/registro3")
async def registro3():
    """Servir página 3 de registro"""
    archivo = FRONTEND_DIR / "registro3.html"
    if archivo.exists():
        return FileResponse(archivo, media_type="text/html")
    return {"error": "registro3.html no encontrado"}

@app.get("/registro4")
async def registro4():
    """Servir página 4 de registro"""
    archivo = FRONTEND_DIR / "registro4.html"
    if archivo.exists():
        return FileResponse(archivo, media_type="text/html")
    return {"error": "registro4.html no encontrado"}

@app.get("/login")
async def login_page():
    """Servir página de login"""
    archivo = FRONTEND_DIR / "login.html"
    if archivo.exists():
        return FileResponse(archivo, media_type="text/html")
    return {"error": "login.html no encontrado"}

@app.get("/dashboard")
async def dashboard():
    """Servir página del dashboard"""
    archivo = FRONTEND_DIR / "dashboard.html"
    if archivo.exists():
        return FileResponse(archivo, media_type="text/html")
    return {"error": "dashboard.html no encontrado"}

# ============================================================================
# RUTA RAÍZ (Documentación)
# ============================================================================

@app.get("/api")
async def api_root():
    """Endpoint raíz para verificar que la API está funcionando"""
    return {
        "mensaje": "Bienvenido a Capitalia API",
        "documentación": "/docs",  # Swagger UI
        "documentación_alternativa": "/redoc"  # ReDoc
    }

@app.get("/health")
async def health_check():
    """Health check para verificar el estado de la API"""
    return {"status": "ok"}
