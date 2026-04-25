# 🚀 FASTAPI SERVIENDO ARCHIVOS ESTÁTICOS Y FRONTEND COMPLETO

## ¿QUÉ CAMBIÓ?

Tu `main.py` ahora:

✅ **Monta archivos estáticos** (CSS, JS, imágenes)
✅ **Sirve archivos HTML** (registro, login, dashboard)  
✅ **Configura CORS correctamente** para peticiones POST desde frontend
✅ **Funciona todo desde `localhost:8000`** sin necesidad de servidor separado

---

## 📁 ESTRUCTURA DE CARPETAS (SIN CAMBIOS)

```
proyecto_fin_grado/
├── backend/
│   └── FastAPI/
│       └── main.py  ← 🔧 ACTUALIZADO
├── css/          ← 📦 Montado en /css
├── images/       ← 📦 Montado en /images  
├── js/           ← 📦 Montado en /js
├── frontend/
│   ├── registro.html      ← ✅ Ahora con rutas absolutas
│   ├── registro2.html     ← ✅ Actualizado
│   ├── registro3.html     ← ✅ Actualizado
│   ├── registro4.html     ← ✅ Actualizado
│   ├── login.html         ← ✅ Actualizado
│   └── dashboard.html     ← ✅ Actualizado
```

---

## 🎯 LO QUE FASTAPI AHORA SIRVE

### **Archivos Estáticos - Rutas Automáticas**

```
GET /css/styles.css      → Sirve: proyecto_fin_grado/css/styles.css
GET /images/logo.png     → Sirve: proyecto_fin_grado/images/logo.png
GET /js/registro-api.js  → Sirve: proyecto_fin_grado/js/registro-api.js
```

### **Archivos HTML - Rutas Específicas**

```
GET /                    → index.html
GET /registro            → registro.html (página 1)
GET /registro2           → registro2.html (página 2)
GET /registro3           → registro3.html (página 3)
GET /registro4           → registro4.html (página 4)
GET /login               → login.html
GET /dashboard           → dashboard.html
```

### **API - Rutas Existentes**

```
POST /register           → Crear usuario
POST /login              → Iniciar sesión
GET  /users/me           → Obtener datos usuario
GET  /docs               → Swagger UI (documentación)
GET  /health             → Health check
```

---

## 🌐 CÓMO USAR AHORA

### **Opción 1: SOLO FASTAPI (SIN servidor frontend separado)**

1. **Abre navegador**:
```
http://localhost:8000/registro
```

2. **Llena las 4 páginas del formulario**
3. **Haz clic "Confirmar"**
4. **¡Listo! Se registra y va a dashboard**

### **Opción 2: Si quieres un servidor separado (como antes)**

Sigue usando:
```bash
cd frontend
python3 -m http.server 3000
```

Y abre:
```
http://localhost:3000/registro.html
```

---

## 📝 RUTAS EN HTML - QUÉ CAMBIÓ

### **ANTES** (Rutas relativas)
```html
<link rel="stylesheet" href="../css/styles.css">
<img src="../images/logo.png">
<script src="../js/registro-api.js"></script>
```

### **AHORA** (Rutas absolutas)
```html
<link rel="stylesheet" href="/css/styles.css">
<img src="/images/logo.png">
<script src="/js/registro-api.js"></script>
```

**¿Por qué?** Porque las páginas ahora se sirven desde diferentes rutas (`/registro2`, `/dashboard`, etc), así que las rutas relativas no funcionan.

---

## 🔧 CÓDIGO CLAVE EN main.py

### **1. Importaciones nuevas**
```python
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
```

### **2. Rutas base calculadas**
```python
BASE_DIR = Path(__file__).resolve().parent.parent.parent

CSS_DIR = BASE_DIR / "css"
IMAGES_DIR = BASE_DIR / "images"
JS_DIR = BASE_DIR / "js"
FRONTEND_DIR = BASE_DIR / "frontend"
```

### **3. Montaje de archivos estáticos**
```python
app.mount("/css", StaticFiles(directory=CSS_DIR), name="css")
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")
app.mount("/js", StaticFiles(directory=JS_DIR), name="js")
```

### **4. CORS actualizado**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

### **5. Rutas para servir HTML**
```python
@app.get("/registro")
async def registro():
    archivo = FRONTEND_DIR / "registro.html"
    if archivo.exists():
        return FileResponse(archivo, media_type="text/html")
    return {"error": "registro.html no encontrado"}
```

---

## 🧪 PRUEBAS RÁPIDAS

### **Verificar que el servidor funciona**
```bash
curl http://localhost:8000/health
# Resultado: {"status":"ok"}
```

### **Verificar CSS**
```bash
curl -I http://localhost:8000/css/styles.css
# Resultado: HTTP/1.1 200 OK
```

### **Verificar imagen**
```bash
curl -I http://localhost:8000/images/logo.png
# Resultado: HTTP/1.1 200 OK
```

### **Verificar página HTML**
```bash
curl -I http://localhost:8000/registro
# Resultado: HTTP/1.1 200 OK
```

---

## ✅ FLUJO COMPLETO DESDE FASTAPI

```
Usuario abre: http://localhost:8000/registro
    ↓
FastAPI sirve: /frontend/registro.html
    ↓
HTML carga CSS: <link href="/css/styles.css">
    ↓
FastAPI sirve: /css/styles.css
    ↓
HTML carga JS: <script src="/js/registro-api.js">
    ↓
FastAPI sirve: /js/registro-api.js
    ↓
Usuario llena formulario en 4 páginas
    ↓
Hace clic "Confirmar" en registro4
    ↓
JavaScript llama: POST /register (a la API)
    ↓
API crea usuario en BD
    ↓
Redirige a: /dashboard
    ↓
FastAPI sirve: /frontend/dashboard.html
    ↓
Dashboard carga con datos del usuario
✅ ¡TODO FUNCIONA DESDE LOCALHOST:8000!
```

---

## 🎯 RESUMEN

| Antes | Ahora |
|---|---|
| Necesitabas 2 servidores | ✅ Un único servidor (FastAPI) |
| Frontend en puerto 3000 | ✅ Todo en puerto 8000 |
| Rutas relativas `../css/` | ✅ Rutas absolutas `/css/` |
| Problemas CORS | ✅ CORS configurado automáticamente |
| Archivos estáticos no servidos | ✅ CSS, JS, imágenes servidas desde FastAPI |

---

## 🚀 PRÓXIMOS PASOS

1. **Abre navegador**: `http://localhost:8000/registro`
2. **Prueba a registrarte** con datos completos
3. **Ve al dashboard** automáticamente
4. **Cierra sesión**
5. **Inicia sesión de nuevo** desde login

---

## 🔗 RUTAS ÚTILES

```
Documentación API:    http://localhost:8000/docs
Swagger UI:          http://localhost:8000/redoc
Página inicial:       http://localhost:8000/
Registro paso 1:      http://localhost:8000/registro
Login:              http://localhost:8000/login
Dashboard:          http://localhost:8000/dashboard
```

---

**¡Listo! FastAPI ahora es tu servidor completo. 🎉**
