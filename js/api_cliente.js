// ====================================
// API CLIENT - Funciones principales
// ====================================
// Este archivo tiene todas las funciones para comunicarse con el backend.
// Solo copia y pega el código de FRONTEND-INTEGRATION.md para usarlas.
// ====================================

// Dirección de la API (misma URL donde corre el frontend/back en Vercel)
const API_URL = window.location.origin;

// ====================================
// HELPERS (funciones internas)
// ====================================

function obtenerToken() {
  // Lee el token guardado del navegador
  return localStorage.getItem("token");
}

function guardarToken(token) {
  // Guarda el token en el navegador para no perder sesión
  localStorage.setItem("token", token);
}

function eliminarToken() {
  // Borra el token cuando haces logout
  localStorage.removeItem("token");
}

// Hacer peticiones a la API (con autenticación)
async function peticionAutenticada(endpoint, metodo = "GET", datos = null) {
  const token = obtenerToken();
  
  if (!token) {
    throw new Error("Necesitas iniciar sesión primero");
  }
  
  const opciones = {
    method: metodo,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`  // Token de seguridad
    }
  };
  
  if (datos) {
    opciones.body = JSON.stringify(datos);
  }
  
  const respuesta = await fetch(`${API_URL}${endpoint}`, opciones);
  
  if (!respuesta.ok) {
    const error = await respuesta.json();
    throw new Error(error.detail || "Error en la API");
  }
  
  return await respuesta.json();
}

// ====================================
// TUS FUNCIONES (que usarás en HTML)
// ====================================
// REGISTRAR

async function registrar(datos) {
  // datos = {nombre, email, dni, telefono, password}
  const respuesta = await fetch(`${API_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(datos)
  });
  
  if (!respuesta.ok) {
    const error = await respuesta.json();
    throw new Error(error.detail || "Error al registrar");
  }
  
  return await respuesta.json();
}

// LOGIN

async function iniciarSesion(email, password) {
  const formData = new FormData();
  formData.append("username", email);
  formData.append("password", password);
  
  const respuesta = await fetch(`${API_URL}/login`, {
    method: "POST",
    body: formData
  });
  
  if (!respuesta.ok) {
    const error = await respuesta.json();
    throw new Error(error.detail || "Email o contraseña incorrecta");
  }
  
  const datos = await respuesta.json();
  guardarToken(datos.access_token);  // Guardar token para sesión
  return datos;
}

// LOGOUT

function cerrarSesion() {
  eliminarToken();
  window.location.href = "/login";
}

// VERIFICAR SI ESTÁ AUTENTICADO

function estaAutenticado() {
  return !!obtenerToken();
}

// OBTENER MIS DATOS

async function obtenerMeDatos() {
  return await peticionAutenticada("/users/me");
}

// HACER BIZUM

async function realizarBizum(cantidad, numero_receptor, concepto = "") {
  const datos = {
    cantidad: parseFloat(cantidad),
    numero_receptor: numero_receptor,
    concepto: concepto || "Transferencia"
  };
  
  return await peticionAutenticada("/transacciones/transferir", "POST", datos);
}

// VER HISTORIAL DE TRANSACCIONES

async function obtenerHistorial(cliente_id) {
  return await peticionAutenticada(`/transacciones/${cliente_id}`);
}
