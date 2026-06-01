// SCRIPT PARA AVISOS - CARGAR ÚLTIMOS INICIOS DE SESIÓN

async function cargarUltimosInicisSesion() {
    console.log('Cargando últimos inicios de sesión...');
    
    if (!estaAutenticado()) {
        console.log('No autenticado');
        return;
    }
    
    const token = localStorage.getItem('token');
    
    try {

        // Llamar a GET /inicios-sesion/ultimos
        const respuesta = await fetch(API_URL + '/inicios-sesion/ultimos', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });
        
        if (respuesta.ok) {
            const inicios = await respuesta.json();
            console.log('Inicios de sesión cargados:', inicios);
            
            mostrarInicisSesion(inicios);
        } else if (respuesta.status === 401) {
            console.log('Sesión expirada');
            localStorage.removeItem('token');
            window.location.href = '/acceso';
        } else {
            console.error('Error al cargar inicios de sesión');
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}

// FUNCIÓN: MOSTRAR INICIOS DE SESIÓN EN EL HTML

function mostrarInicisSesion(inicios) {
    const divLista = document.querySelector('.lista-inicios-sesion');
    
    if (!divLista) {
        console.error('No se encontró el div .lista-inicios-sesion');
        return;
    }
    
    if (inicios.length === 0) {
        divLista.innerHTML = '<p style="text-align: center; color: #999;">No hay inicios de sesión registrados</p>';
        return;
    }
    
    let html = '';
    
    inicios.forEach((inicio, index) => {

        // Formatea la fecha y hora
        const fechaObj = new Date(inicio.fecha_hora);
        const fecha = fechaObj.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
        const hora = fechaObj.toLocaleTimeString('es-ES', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        
        const label = index === 0 ? '(Actual)' : '';
        
        html += `
            <div class="inicio-sesion-item">
                <div class="inicio-sesion-numero">
                    <span>${index + 1}</span>
                </div>
                <div class="inicio-sesion-info">
                    <div class="inicio-sesion-fecha">${fecha} a las ${hora} ${label}</div>
                </div>
            </div>
        `;
    });
    
    divLista.innerHTML = html;
    console.log('Inicios de sesión mostrados');
}

// CUANDO CARGA LA PÁGINA DE AVISOS

window.addEventListener('DOMContentLoaded', function() {
    if (window.location.href.includes('/avisos')) {
        console.log('Página de avisos cargada. Mostrando inicios de sesión');
        
        // Esperar un poco a que cargueDashboard() haya terminado
        setTimeout(() => {
            cargarUltimosInicisSesion();
        }, 500);
    }
});
