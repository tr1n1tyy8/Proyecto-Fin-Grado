# 🏦 BANCO FICTICIO - Proyecto Fin de Grado

Un sistema bancario con **login seguro**, **transferencias Bizum** y **historial de movimientos**.

## 🚀 Empezar en 30 minutos

### Paso 1: Abrir terminal y crear la base de datos
```bash
mysql -u root << 'EOF'
CREATE DATABASE banco_ficticio CHARACTER SET utf8mb4;
EOF
```

### Paso 2: Instalar dependencias
```bash
cd backend
pip install -r requirements.txt
```

### Paso 3: Ejecutar la API
```bash
uvicorn FastAPI.main:app --reload
# Se abrirá en http://localhost:8000/docs
```

### Paso 4: Probar la API en Swagger UI
- Abre **http://localhost:8000/docs**
- Prueba "POST /register" para crear un usuario
- Prueba "POST /login" para obtener token

---

## 📚 Documentación Simple

- **[INICIO-RAPIDO.md](INICIO-RAPIDO.md)** - Cómo empezar (los primeros 5 comandos)
- **[API-DOCS.md](API-DOCS.md)** - Qué hace cada ruta

---

## 🔧 ¿Qué hay en cada carpeta?

```
backend/FastAPI/
├── main.py              ← Arranca la aplicación
├── database.py          ← Se conecta a MySQL
├── models.py            ← Define Cliente y Transacción
├── schemas.py           ← Valida los datos que envían
└── routers/
    ├── auth.py          ← Login y Registro
    └── transacciones.py ← Bizum e Historial
```

---

## ✨ Lo que funciona

✅ **Registro** - Crear usuario con email y contraseña
✅ **Login** - Obtener token JWT
✅ **Ver datos** - GET /users/me (datos del usuario)
✅ **Hacer Bizum** - Transferir dinero a otro usuario
✅ **Ver historial** - Ver todas tus transacciones

---

## 🔐 Seguridad

- Contraseñas encriptadas (bcrypt)
- Login con tokens (JWT)
- Email único
- No puedes transferir dinero a ti mismo

---

## 📁 Archivos importantes

**Backend (Python):**
- `backend/FastAPI/main.py` - Punto de entrada
- `backend/FastAPI/database.py` - Conexión a MySQL
- `backend/FastAPI/models.py` - Estructura de datos
- `backend/requirements.txt` - Dependencias necesarias

**Frontend (JavaScript):**
- `js/api-cliente.js` - Funciones para llamar la API desde HTML

---

Ver [INICIO-RAPIDO.md](INICIO-RAPIDO.md) para empezar ➡️
