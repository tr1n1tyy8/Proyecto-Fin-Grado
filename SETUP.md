# � INSTALACIÓN Y CONFIGURACIÓN

## Paso 1: Crear la base de datos

Abre terminal y ejecuta:

```bash
mysql -u root << 'EOF'
CREATE DATABASE banco_ficticio CHARACTER SET utf8mb4;
EOF
```

✅ Listo, base de datos creada.

---

## Paso 2: Instalar dependencias Python

```bash
cd backend
pip install -r requirements.txt
```

Espera a que termine sin errores.

---

## Paso 3: Ejecutar la API

```bash
# Desde carpeta backend
uvicorn FastAPI.main:app --reload
```

Deberías ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## Paso 4: Probar la API

Abre navegador en: **http://localhost:8000/docs**

Verás una página interactiva (Swagger UI) donde puedes probar:

1. Click en "POST /register"
2. Click "Try it out"
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

Si ves un `201`, ¡funciona! ✅

---

## Ahora, ¿qué hago?

- Ver **[INICIO-RAPIDO.md](INICIO-RAPIDO.md)** para los primeros 5 pasos
- Ver **[API-DOCS.md](API-DOCS.md)** para entender qué hace cada ruta
- Para conectar tu HTML, ver la sección "Frontend" abajo

---

## 🌐 Conectar HTML con la API

### Paso 1: Incluir la librería JavaScript
En tu HTML, antes de cerrar `</body>`, añade:
```html
<script src="js/api-cliente.js"></script>
```

### Paso 2: Usa las funciones

**Registro:**
```javascript
// Evento del botón
document.getElementById("btnRegistrar").addEventListener("click", async () => {
  try {
    const usuario = await registrar({
      nombre: "Sandra García",
      email: "sandra@example.com",
      dni: "12345678A",
      telefono: "650123456",
      password: "MiPassword123!"
    });
    alert("¡Registrado! ID: " + usuario.id);
  } catch (error) {
    alert("Error: " + error.message);
  }
});
```

**Login:**
```javascript
document.getElementById("btnLogin").addEventListener("click", async () => {
  try {
    await iniciarSesion("sandra@example.com", "MiPassword123!");
    alert("✓ Sesión iniciada");
    window.location.href = "dashboard.html";
  } catch (error) {
    alert("Error: " + error.message);
  }
});
```

**Ver datos del usuario:**
```javascript
window.addEventListener("load", async () => {
  if (!estaAutenticado()) {
    window.location.href = "login.html";
    return;
  }
  
  const usuario = await obtenerMeDatos();
  document.getElementById("nombre").textContent = usuario.nombre;
  document.getElementById("saldo").textContent = usuario.saldo + "€";
});
```

**Hacer Bizum:**
```javascript
document.getElementById("btnBizum").addEventListener("click", async () => {
  try {
    const resultado = await realizarBizum(
      25.50,              // cantidad
      "650654321",        // teléfono del receptor
      "Cena"              // concepto
    );
    alert("✓ " + resultado.mensaje);
  } catch (error) {
    alert("Error: " + error.message);
  }
});
```

**Ver historial:**
```javascript
const historial = await obtenerHistorial(1);  // 1 = ID del usuario
console.log("Recibidas:", historial.transacciones_recibidas);
console.log("Enviadas:", historial.transacciones_enviadas);
```

---

## ❌ Si algo no funciona

### Error: "Can't connect to MySQL"
```bash
# Inicia MySQL
brew services start mysql
# o en Windows: net start MySQL
```

### Error: "ModuleNotFoundError: No module named 'FastAPI'"
```bash
cd backend
pip install -r requirements.txt
```

### Las tablas no se crean
Reinicia la API:
```bash
# Haz Ctrl+C en la terminal
# Luego:
uvicorn FastAPI.main:app --reload
```

### Si necesitas borrar todo y empezar
```bash
mysql -u root -e "DROP DATABASE banco_ficticio;"
mysql -u root -e "CREATE DATABASE banco_ficticio CHARACTER SET utf8mb4;"
```

---

✅ **Listo**. Ya tienes todo funcionando. Ve a [API-DOCS.md](API-DOCS.md) para entender qué hace cada ruta.
