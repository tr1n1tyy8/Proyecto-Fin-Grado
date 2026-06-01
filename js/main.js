// PROTECCIÓN DE RUTAS: Verificar autenticación antes de acceder

function protegerRuta() {
    const rutasProtegidas = ['/dashboard', '/bizum', '/avisos', '/informacion'];
    const rutaActual = window.location.pathname;
    
    // Verificar si la ruta actual está protegida
    const estaProtegida = rutasProtegidas.some(ruta => rutaActual.includes(ruta));
    
    if (estaProtegida) {
        // Verificar si existe token en localStorage
        const token = localStorage.getItem('token');
        
        if (!token) {
            // No hay token, redirigir a login
            console.warn('Acceso denegado: no hay token. Redirigiendo a login...');
            window.location.href = '/acceso';
        } else {
            console.log('Token verificado, acceso permitido');
        }
    }
}

// Ejecutar protección de rutas al cargar la página
document.addEventListener('DOMContentLoaded', protegerRuta);

// Intersection Observer para detectar cuando los apartados entran en vista
const API_URL = window.location.origin;

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observar todos los apartados y formularios
document.addEventListener('DOMContentLoaded', function() {
    const apartados = document.querySelectorAll('[class^="apartado"], .formulario');
    apartados.forEach(apartado => {
        observer.observe(apartado);
    });
});

// Función para los mensajes de error de la página (cambiar alertas del navegador por pop ups en la página)
const _alertContainer = document.createElement('div');
_alertContainer.style.cssText = 'position:fixed;top:16px;right:16px;z-index:9999;display:flex;flex-direction:column;gap:8px';
document.body.appendChild(_alertContainer);

window.alert = function(msg) {
    const box = document.createElement('div');
    box.textContent = msg;
    box.style.cssText = 'background:#fee2e2;color:#991b1b;padding:12px 16px;border-radius:8px;border-left:4px solid #f87171;font-size:14px;max-width:320px;box-shadow:0 2px 8px rgba(0,0,0,0.1)';
    _alertContainer.appendChild(box);
    setTimeout(() => box.remove(), 5000);
};
