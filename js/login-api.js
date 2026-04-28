// ============================================================================
// SCRIPT PARA LOGIN Y CERRAR SESIÓN
// ============================================================================
// Maneja todo lo relacionado con la autenticación del usuario
// ============================================================================

const API_URL = 'http://localhost:8000';

// ============================================================================
// FUNCIÓN: INICIAR SESIÓN (login.html)
// ============================================================================
async function iniciarSesion(event) {
    event.preventDefault(); // No recargar la página
    
    // Recoger datos del formulario
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // Validar que fueron rellenados
    if (!email || !password) {
        alert('⚠️ Por favor, rellena email y contraseña');
        return;
    }
    
    console.log('📤 Intentando login con:', email);
    
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
            // ✅ Login exitoso
            console.log('✅ Login exitoso, token recibido');
            
            // 1. Guardar token en localStorage (memoria del navegador)
            localStorage.setItem('token', datos.access_token);
            localStorage.setItem('email', email);
            
            // 2. Ir al dashboard
            alert('✅ ¡Sesión iniciada! Bienvenido/a');
            window.location.href = '/dashboard';
        } else {
            // ❌ Credenciales inválidas
            alert('❌ Email o contraseña incorrectos');
            console.error('Error:', datos);
        }
    } catch (error) {
        // ❌ Error de conexión
        alert('❌ Error de conexión: ' + error.message);
        console.error('Error:', error);
    }
}

// ============================================================================
// FUNCIÓN: CERRAR SESIÓN (dashboard.html)
// ============================================================================
function cerrarSesion() {
    // Confirmar que quiere cerrar sesión
    if (!confirm('¿Estás seguro/a de que quieres cerrar sesión?')) {
        return;
    }
    
    // Borrar token del navegador
    localStorage.removeItem('token');
    localStorage.removeItem('email');
    sessionStorage.clear(); // También limpiamos datos del registro
    
    console.log('✅ Sesión cerrada');
    alert('Sesión cerrada. Hasta pronto!');
    
    // Ir a login
    window.location.href = '/acceso';
}

// ============================================================================
// FUNCIÓN: VERIFICAR SI ESTÁ AUTENTICADO
// ============================================================================
function estaAutenticado() {
    return localStorage.getItem('token') !== null;
}

// ============================================================================
// FUNCIÓN: CARGAR DATOS DEL USUARIO EN DASHBOARD
// ============================================================================
async function cargarDashboard() {
    // Verificar que está autenticado
    if (!estaAutenticado()) {
        alert('⚠️ Necesitas iniciar sesión primero');
        window.location.href = '/acceso';
        return;
    }
    
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('email');
    
    console.log('📥 Cargando datos del dashboard para:', email);
    
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
            
            console.log('✅ Datos del usuario:', usuario);
            
            // Actualizar el HTML del dashboard con los datos reales
            actualizarDashboard(usuario);
        } else if (respuesta.status === 401) {
            // Token expirado o inválido
            alert('⚠️ Tu sesión ha expirado. Inicia sesión de nuevo');
            localStorage.removeItem('token');
            localStorage.removeItem('email');
            window.location.href = '/acceso';
        } else {
            throw new Error('Error al cargar datos');
        }
    } catch (error) {
        alert('❌ Error al cargar datos: ' + error.message);
        console.error('Error:', error);
    }
}

// ============================================================================
// FUNCIÓN: ACTUALIZAR DATOS EN EL HTML DEL DASHBOARD
// ============================================================================
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

// ============================================================================
// CUANDO CARGA LA PÁGINA
// ============================================================================
window.addEventListener('DOMContentLoaded', function() {
    // Si estamos en dashboard.html
    if (window.location.href.includes('dashboard.html')) {
        cargarDashboard();
    }
    
    // Si estamos en login.html, conectar el formulario
    if (window.location.href.includes('login.html')) {
        const formulario = document.querySelector('form');
        if (formulario) {
            // Buscar los inputs por placeholder o type
            const inputs = document.querySelectorAll('input');
            
            // Darles IDs si no los tienen
            if (inputs[0]) {
                inputs[0].id = 'email';
                inputs[0].name = 'email';
            }
            if (inputs[1]) {
                inputs[1].id = 'password';
                inputs[1].name = 'password';
            }
            
            // Conectar el formulario al evento de envío
            formulario.addEventListener('submit', iniciarSesion);
        }
    }
    
    // Conectar botones de cerrar sesión (pueden estar en varios sitios)
    document.querySelectorAll('a[href="login.html"]').forEach(link => {
        // Si el texto del link contiene "Cerrar" o "logout", hacerlo un botón de logout
        if (link.textContent.toLowerCase().includes('cerrar') || 
            link.textContent.toLowerCase().includes('logout')) {
            link.href = '#';
            link.onclick = function(e) {
                e.preventDefault();
                cerrarSesion();
            };
        }
    });
});

// ============================================================================
