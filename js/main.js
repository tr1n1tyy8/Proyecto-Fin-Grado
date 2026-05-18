// ============================================================================
// PROTECCIÓN DE RUTAS - Verificar autenticación antes de acceder
// ============================================================================
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
            console.warn('⚠️ Acceso denegado: no hay token. Redirigiendo a login...');
            window.location.href = '/acceso';
        } else {
            console.log('✅ Token verificado, acceso permitido');
        }
    }
}

// Ejecutar protección de rutas al cargar la página
document.addEventListener('DOMContentLoaded', protegerRuta);

// Intersection Observer para detectar cuando los apartados entran en vista

const API_URL = "https://proyectofingrado.vercel.app";

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
