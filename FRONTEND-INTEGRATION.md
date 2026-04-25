# 🌐 CONECTAR HTML CON LA API

## Paso 1: Incluir la librería

En todas tus páginas HTML, **antes de cerrar `</body>`**, añade:

```html
<script src="js/api-cliente.js"></script>
```

---

## Paso 2: Usar las funciones

Aquí hay ejemplos simples para cada caso:

### Registro
```javascript
// Botón HTML: <button onclick="registro()">Registrarse</button>

async function registro() {
  try {
    const usuario = await registrar({
      nombre: "Sandra",
      apellidos: "García López",
      fecha_nacimiento: "1995-05-15",
      dni: "12345678A",
      telefono: "650123456",
      email: "sandra@example.com",
      password: "MiPassword123!",
      nacionalidad: "Española",
      direccion: "Calle Principal 42",
      provincia: "Madrid",
      ciudad: "Madrid",
      codigo_postal: "28001",
      pais_residencia: "España",
      situacion_laboral: "Empleado"
    });
    alert("¡Registrado!");
    window.location.href = "login.html";
  } catch (error) {
    alert("Error: " + error.message);
  }
}
```

### Login
```javascript
async function login() {
  try {
    await iniciarSesion("tu@email.com", "MiPassword123!");
    window.location.href = "dashboard.html";
  } catch (error) {
    alert("Error: " + error.message);
  }
}
```

### Ver tus datos
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

### Enviar Bizum
```javascript
async function enviarBizum() {
  try {
    const resultado = await realizarBizum(
      100,           // cantidad en €
      "650234567",   // teléfono receptor
      "Cena"         // concepto
    );
    alert("✓ Transferencia enviada!");
    alert("Tu nuevo saldo: " + resultado.nuevo_saldo + "€");
  } catch (error) {
    alert("Error: " + error.message);
  }
}
```

### Ver historial
```javascript
async function verHistorial() {
  const usuario = await obtenerMeDatos();
  const historial = await obtenerHistorial(usuario.id);
  
  console.log("Enviaste:", historial.transacciones_enviadas);
  console.log("Recibiste:", historial.transacciones_recibidas);
}
```

### Logout
```javascript
// Solo funciona con un botón: <button onclick="cerrarSesion()">Logout</button>
```

---

## Funciones disponibles

```javascript
registrar(datos)                    // Crear usuario
iniciarSesion(email, password)      // Login
cerrarSesion()                      // Logout
estaAutenticado()                   // Retorna true/false
obtenerMeDatos()                    // Obtiene dato del usuario
realizarBizum(cantidad, tel, concepto)  // Hacer transferencia
obtenerHistorial(id)                // Ver transacciones
```
