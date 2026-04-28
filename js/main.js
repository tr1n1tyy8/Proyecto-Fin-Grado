// Intersection Observer para detectar cuando los apartados entran en vista

const API_URL = "http://127.0.0.1:8000";

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
