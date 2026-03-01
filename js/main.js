// Intersection Observer para detectar cuando los apartados entran en vista
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

// Observar todos los apartados
document.addEventListener('DOMContentLoaded', function() {
    const apartados = document.querySelectorAll('[class^="apartado"]');
    apartados.forEach(apartado => {
        observer.observe(apartado);
    });
});
