# ⚡ INICIO RÁPIDO - 5 pasos

## Paso 1: Crear la base de datos
```bash
mysql -u root << 'EOF'
CREATE DATABASE banco_ficticio CHARACTER SET utf8mb4;
EOF
```

## Paso 2: Instalar dependencias
```bash
cd backend
pip install -r requirements.txt
```

## Paso 3: Ejecutar la API
```bash
# Desde carpeta backend
uvicorn FastAPI.main:app --reload
```

Espera a que veas:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## Paso 4: Abrir la documentación interactiva
Ve a: **http://localhost:8000/docs**

## Paso 5: Probar un endpoint
1. Haz clic en "POST /register"
2. Haz clic en "Try it out"
3. Rellena con esto:
```json
{
  "nombre": "Test User",
  "email": "test@example.com",
  "dni": "12345678Z",
  "telefono": "650123456",
  "password": "TestPass123!"
}
```
4. Click "Execute"

✅ ¡Listo! Ya creaste tu primer usuario.

---

## Siguiente: Ver [API-DOCS.md](API-DOCS.md) para entender qué hacen las rutas
