from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
import os
from pathlib import Path

# Importar routers
from .routers import autenticacion, transacciones

# Importar BD
from .bbdd import engine
from .models import Base


# INICIALIZACIÓN DE LA APLICACIÓN

app = FastAPI(
    title="Capitalia API",
    description="API segura para banca online con JWT y Bizum",
    version="1.0.0"
)

# Evento de arranque controlado para crear tablas sin bloquear la compilación
@app.on_event("startup")
def startup_event():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"No se pudieron sincronizar las tablas al arrancar: {e}")


# CONFIGURACIÓN DE RUTAS ABSOLUTAS PARA ARCHIVOS ESTÁTICOS

BASE_DIR = Path(__file__).resolve().parent.parent.parent  

CSS_DIR = BASE_DIR / "css"
IMAGES_DIR = BASE_DIR / "images"
JS_DIR = BASE_DIR / "js"
FRONTEND_DIR = BASE_DIR / "frontend"


# CONFIGURACIÓN DE CORS: permite peticiones desde el frontend en Vercel y el middleware centraliza la autenticación JWT en cada petición

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# MONTAR ARCHIVOS ESTÁTICOS

if CSS_DIR.exists():
    app.mount("/css", StaticFiles(directory=CSS_DIR), name="css")
if IMAGES_DIR.exists():
    app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")
if JS_DIR.exists():
    app.mount("/js", StaticFiles(directory=JS_DIR), name="js")


# INCLUIR ROUTERS

app.include_router(autenticacion.router)           
app.include_router(transacciones.router)  


# SERVIR ARCHIVOS HTML DEL FRONTEND / REDIRECCIONES

@app.get("/")
async def index():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file, media_type="text/html")
    return RedirectResponse(url="/docs")

@app.get("/compromiso_social")
async def compromiso_social():
    archivo = FRONTEND_DIR / "compromiso_social.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/novedades")
async def novedades():
    archivo = FRONTEND_DIR / "novedades.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/mas_informacion")
async def mas_informacion():
    archivo = FRONTEND_DIR / "mas_informacion.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/registro")
async def registro():
    archivo = FRONTEND_DIR / "registro.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/registro2")
async def registro2():
    archivo = FRONTEND_DIR / "registro2.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/registro3")
async def registro3():
    archivo = FRONTEND_DIR / "registro3.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/registro4")
async def registro4():
    archivo = FRONTEND_DIR / "registro4.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/acceso")
async def login_page():
    archivo = FRONTEND_DIR / "login.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/dashboard")
async def dashboard():
    archivo = FRONTEND_DIR / "dashboard.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/bizum")
async def bizum_page():
    archivo = FRONTEND_DIR / "bizum.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/avisos")
async def avisos_page():
    archivo = FRONTEND_DIR / "avisos.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/informacion")
async def informacion_page():
    archivo = FRONTEND_DIR / "informacion.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/politicas_privacidad")
async def politicas_privacidad_page():
    archivo = FRONTEND_DIR / "politicas_privacidad.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/condiciones_uso")
async def condiciones_uso_page():
    archivo = FRONTEND_DIR / "condiciones_uso.html"
    if archivo.exists(): return FileResponse(archivo, media_type="text/html")
    return {"error": "No encontrado"}

@app.get("/api")
async def api_root():
    return {
        "mensaje": "Bienvenido a Capitalia API",
        "documentacion": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}