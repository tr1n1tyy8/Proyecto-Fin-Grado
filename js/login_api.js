// SCRIPT PARA LOGIN Y CERRAR SESIÓN

// FUNCIÓN: INICIAR SESIÓN (login.html)

async function iniciarSesion(event) {
    event.preventDefault(); // No recargar la página
    
    // Recoger datos del formulario
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Validar que fueron rellenados
    if (!email || !password) {
        alert('Por favor, rellena email y contraseña');
        return false;
    }
    
    console.log('Intentando login con:', email);
    
    try {
        // Enviar login a la API
        const respuesta = await fetch(API_URL + '/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${email}&password=${password}`
        });
        
        const datos = await respuesta.json();
        
        if (respuesta.ok) {
            // Login exitoso
            console.log('Login exitoso, token recibido');
            
            // 1. Guardar token en localStorage (memoria del navegador)
            localStorage.setItem('token', datos.access_token);
            localStorage.setItem('email', email);
            
            // 2. Obtener datos del usuario (incluyendo teléfono)
            try {
                const usuarioResponse = await fetch(API_URL + '/usuarios/' + email, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${datos.access_token}`,
                        'Content-Type': 'application/json',
                    }
                });
                
                if (usuarioResponse.ok) {
                    const usuarioData = await usuarioResponse.json();
                    if (usuarioData.telefono) {
                        localStorage.setItem('telefono', usuarioData.telefono);
                        console.log('Teléfono guardado en localStorage');
                    }
                }
            } catch (err) {
                console.warn('No se pudo obtener el teléfono:', err);
            }
            
            // 3. Ir al dashboard
            console.log('Redirigiendo al dashboard...');
            window.location.href = '/dashboard';
        } else {
            // Credenciales inválidas
            alert('Email o contraseña incorrectos');
            console.error('Error:', datos);
        }
    } catch (error) {
        // Error de conexión
        alert('Error de conexión: ' + error.message);
        console.error('Error:', error);
    }
    
    return false;
}

// FUNCIÓN: CERRAR SESIÓN (dashboard.html)

function cerrarSesion() {

    // Confirmar que quiere cerrar sesión
    if (!confirm('¿Estás seguro/a de que quieres cerrar sesión?')) {
        return;
    }
    
    // Borrar token del navegador
    localStorage.removeItem('token');
    localStorage.removeItem('email');
    sessionStorage.clear(); 
    
    console.log('Sesión cerrada');
    alert('Sesión cerrada. ¡Hasta pronto!');
    
    // Ir a login
    window.location.href = '/acceso';
}

// FUNCIÓN: VERIFICAR SI ESTÁ AUTENTICADO

function estaAutenticado() {
    return localStorage.getItem('token') !== null;
}

// FUNCIÓN: CARGAR DATOS DEL USUARIO EN DASHBOARD

async function cargarDashboard() {

    // Verificar que está autenticado
    if (!estaAutenticado()) {
        alert('Necesitas iniciar sesión primero');
        window.location.href = '/acceso';
        return;
    }
    
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('email');
    
    console.log('Cargando datos del dashboard para:', email);
    
    try {

        // Llamar a /users/me para obtener datos del usuario
        const respuesta = await fetch(API_URL + '/users/me', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });
        
        if (respuesta.ok) {
            const usuario = await respuesta.json();
            
            console.log('Datos del usuario:', usuario);
            
            // Actualizar el HTML del dashboard con los datos reales
            actualizarDashboard(usuario);
        } else if (respuesta.status === 401) {

            // Token expirado o inválido
            alert('Tu sesión ha expirado. Inicia sesión de nuevo');
            localStorage.removeItem('token');
            localStorage.removeItem('email');
            window.location.href = '/acceso';
        } else {
            throw new Error('Error al cargar datos');
        }
    } catch (error) {
        alert('Error al cargar datos: ' + error.message);
        console.error('Error:', error);
    }
}

// FUNCIÓN: ACTUALIZAR DATOS EN EL HTML DEL DASHBOARD

function actualizarDashboard(usuario) {

    // Mostrar nombre del usuario
    const h2 = document.querySelector('h2');
    if (h2) {
        h2.textContent = `Hola, ${usuario.nombre}`;
    }
    
    // Mostrar saldo
    const saldoP = document.querySelector('.saldo p');
    if (saldoP) {
        saldoP.textContent = `${usuario.saldo}€ en tu cuenta de ahorros`;
    }
    
    // Mostrar información de cuenta
    const infoDiv = document.querySelector('.informacion-usuario');
    if (infoDiv) {
        infoDiv.innerHTML = `
            <h3>Tu Información</h3>
            <p><strong>Email:</strong> ${usuario.email}</p>
            <p><strong>Teléfono:</strong> ${usuario.telefono}</p>
            <p><strong>Ciudad:</strong> ${usuario.ciudad}</p>
            <p><strong>DNI:</strong> ${usuario.dni}</p>
        `;
    }
}

// CUANDO CARGA LA PÁGINA

console.log('Script login-api.js cargado');

// Capturar TODOS los submits de formularios
document.addEventListener('submit', function(e) {

    // Verificar si estamos en /acceso
    if (!window.location.href.includes('/acceso')) {
        return;
    }
    
    console.log('Submit de formulario detectado en /acceso');
    e.preventDefault(); // Prevenir comportamiento por defecto
    
    // Llamar a iniciarSesion
    iniciarSesion(e);
}, true);

// Cargar dashboard cuando sea necesario
window.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded disparado');
    
    if (window.location.href.includes('/dashboard')) {
        console.log('Cargando datos del dashboard...');
        cargarDashboard();
    }
});