# 📚 RUTAS DE LA API

## 🔗 Base URL
```
http://localhost:8000
```

## 📖 Documentación interactiva
Va a http://localhost:8000/docs (después de ejecutar la API)

---

## 🟢 RUTAS PÚBLICAS (Sin token)

### 1. POST /register - Registrar usuario

**Para qué:** Crear una nueva cuenta bancaria

**Qué envías:**
```json
{
  "nombre": "Sandra García",
  "email": "sandra@example.com",
  "dni": "12345678A",
  "telefono": "650123456",
  "password": "MiPassword123!"
}
```

**Qué recibes si funciona (201):**
```json
{
  "id": 1,
  "nombre": "Sandra García",
  "email": "sandra@example.com",
  "saldo": 0.0,
  "fecha_registro": "2026-04-20T10:30:00"
}
```

**Errores:**
- Email ya existe
- DNI ya existe
- Teléfono ya existe
- Email no es válido
- Contraseña menos de 8 caracteres

---

### 2. POST /login - Iniciar sesión

**Para qué:** Obtener un token para usar otras rutas

**Qué envías:**
```
username: sandra@example.com
password: MiPassword123!
```

**Qué recibes si funciona (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errores:**
- Email o contraseña incorrecta

---

## 🔒 RUTAS PROTEGIDAS (Necesitan token)

Para usar estas rutas, envía el token en el header:
```
Authorization: Bearer TU_TOKEN_AQUI
```

### 3. GET /users/me - Ver tus datos

**Para qué:** Ver tu información (nombre, email, saldo, etc.)

**Qué recibes si funciona (200):**
```json
{
  "id": 1,
  "nombre": "Sandra García",
  "email": "sandra@example.com",
  "telefono": "650123456",
  "saldo": 100.50,
  "fecha_registro": "2026-04-20T10:30:00"
}
```

---

### 4. POST /transacciones/transferir - Hacer un Bizum

**Para qué:** Enviar dinero a otro usuario

**Qué envías:**
```json
{
  "cantidad": 25.50,
  "numero_receptor": "650654321",
  "concepto": "Cena en el restaurante"
}
```

**Qué recibes si funciona (201):**
```json
{
  "estado": "éxito",
  "mensaje": "Transferencia de 25.5€ a Juan Pérez realizada",
  "nuevo_saldo": 74.5,
  "id_transaccion": 1,
  "receptor": "Juan Pérez"
}
```

**Errores:**
- "No tienes suficiente saldo"
- "No puedes transferir a tu propia cuenta"
- "Receptor no encontrado"
- Cantidad no es mayor que 0

---

### 5. GET /transacciones/{cliente_id} - Ver historial

**Para qué:** Ver todas tus transacciones (enviadas y recibidas)

**Reemplaza `{cliente_id}` con tu ID** (ej: /transacciones/1)

**Qué recibes si funciona (200):**
```json
{
  "saldo_actual": 74.5,
  "transacciones_recibidas": [
    {
      "id": 2,
      "cantidad": 50.0,
      "concepto": "Pago cena",
      "fecha": "2026-04-20T11:00:00"
    }
  ],
  "transacciones_enviadas": [
    {
      "id": 1,
      "cantidad": 25.5,
      "concepto": "Cena",
      "fecha": "2026-04-20T10:35:00"
    }
  ]
}
```

---

## 🧪 EJEMPLO COMPLETO CON CURL

### 1. Registrar usuario
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Sandra","email":"sandra@test.com","dni":"12345678A","telefono":"650123456","password":"Test1234!"}'
```

### 2. Login y guardar token
```bash
RESPONSE=$(curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=sandra@test.com&password=Test1234!")

# El token está en RESPONSE
```

### 3. Ver datos (reemplaza TOKEN)
```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer TOKEN_AQUI"
```

---

## 🔐 ¿QUÉ SIGNIFICA CADA COSA?

**POST**: Enviar datos (crear, modificar)
**GET**: Obtener información
**Token**: Permiso para acceder a rutas protegidas
**Concepto**: Motivo de la transferencia (dinero para qué)
**Estado 200**: OK, funcionó
**Estado 201**: OK, se creó algo nuevo
**Estado 400**: Error, datos incorrectos
**Estado 401**: No autorizado (token inválido o falta)
**Estado 404**: No encontrado

---

## 💡 RESUMEN

| Ruta | Para qué | Necesita token |
|------|---------|--------|
| POST /register | Crear usuario | ❌ |
| POST /login | Obtener token | ❌ |
| GET /users/me | Ver tus datos | ✅ |
| POST /transferir | Hacer Bizum | ✅ |
| GET /transacciones/{id} | Ver historial | ✅ |

---

Más detalles en http://localhost:8000/docs (Swagger UI)