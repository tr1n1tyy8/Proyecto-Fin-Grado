// ============================================================================
// SCRIPT PARA DASHBOARD - CARGAR SALDO Y ÚLTIMAS TRANSACCIONES
// ============================================================================

async function cargarSaldoUsuario() {
    console.log('💰 Cargando saldo del usuario...');
    
    if (!estaAutenticado()) {
        console.log('⚠️ No autenticado');
        return;
    }
    
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('email');
    
    try {
        // Llamar a GET /usuarios/{email}
        const respuesta = await fetch(API_URL + `/usuarios/${email}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });
        
        if (respuesta.ok) {
            const usuario = await respuesta.json();
            console.log('✅ Usuario cargado:', usuario);
            
            mostrarSaldo(usuario);
        } else if (respuesta.status === 401) {
            console.log('⚠️ Sesión expirada');
            localStorage.removeItem('token');
            window.location.href = '/acceso';
        } else {
            console.error('❌ Error al cargar usuario');
        }
    } catch (error) {
        console.error('❌ Error de conexión:', error);
    }
}

function mostrarSaldo(usuario) {
    const divSaldo = document.querySelector('.saldo');
    
    if (!divSaldo) {
        console.error('❌ No se encontró el div .saldo');
        return;
    }
    
    const nombre = usuario.nombre || usuario.email;
    const saldoTexto = `${usuario.saldo.toFixed(2)}€ en tu cuenta de ahorros`;
    
    const h2 = divSaldo.querySelector('h2');
    const pMonto = divSaldo.querySelector('.saldo-monto');
    
    if (h2) {
        h2.textContent = `¡Hola, ${nombre}!`;
    }
    if (pMonto) {
        pMonto.textContent = saldoTexto;
    }
    
    console.log('✅ Saldo mostrado');
}

// ============================================================================
// SCRIPT PARA DASHBOARD - CARGAR ÚLTIMAS TRANSACCIONES
// ============================================================================
// Este archivo carga las 5 últimas transacciones del usuario
// ============================================================================

async function cargarUltimasTransacciones() {
    console.log('📋 Cargando últimas transacciones...');
    
    if (!estaAutenticado()) {
        console.log('⚠️ No autenticado');
        return;
    }
    
    const token = localStorage.getItem('token');
    
    try {
        // Llamar a GET /transacciones/ultimas
        const respuesta = await fetch(API_URL + '/transacciones/ultimas', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });
        
        if (respuesta.ok) {
            const transacciones = await respuesta.json();
            console.log('✅ Transacciones cargadas:', transacciones);
            
            mostrarTransacciones(transacciones);
        } else if (respuesta.status === 401) {
            console.log('⚠️ Sesión expirada');
            localStorage.removeItem('token');
            window.location.href = '/acceso';
        } else {
            console.error('❌ Error al cargar transacciones');
        }
    } catch (error) {
        console.error('❌ Error de conexión:', error);
    }
}

// ============================================================================
// FUNCIÓN: MOSTRAR TRANSACCIONES EN EL HTML
// ============================================================================
function mostrarTransacciones(transacciones) {
    const divTransacciones = document.querySelector('.historial-transacciones');
    
    if (!divTransacciones) {
        console.error('❌ No se encontró el div .historial-transacciones');
        return;
    }
    
    if (transacciones.length === 0) {
        divTransacciones.innerHTML = '<p style="text-align: center; color: #999;">No hay transacciones aún</p>';
        return;
    }
    
    let html = '<h3>📊 Tus movimientos</h3>';
    html += '<div class="lista-transacciones">';
    
    const usuarioActual = localStorage.getItem('email');
    
    transacciones.forEach(transaccion => {
        // Formatea la fecha y hora
        const fechaObj = new Date(transaccion.fecha);
        const fecha = fechaObj.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
        const hora = fechaObj.toLocaleTimeString('es-ES', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        // Determinar si es envío o recepción comparando con el email actual
        const esEnvio = transaccion.emisor === usuarioActual;
        
        // Crear la tarjeta de transacción
        const claseTransaccion = esEnvio ? 'transaccion-envio' : 'transaccion-recepcion';
        const icono = esEnvio ? '➡️' : '⬅️';
        const signo = esEnvio ? '-' : '+';
        const colorClase = esEnvio ? 'envio' : 'recepcion';
        
        // Generar el concepto
        let concepto = transaccion.concepto;
        if (!concepto || concepto === 'Transferencia Bizum') {
            if (esEnvio) {
                concepto = `Transferencia a ${transaccion.nombre_receptor || 'usuario'}`;
            } else {
                // Obtener el nombre del emisor (convertir email a algo legible si es necesario)
                const nombreEmisor = transaccion.emisor ? transaccion.emisor.split('@')[0] : 'usuario';
                concepto = `Recibido de ${nombreEmisor}`;
            }
        }
        
        html += `
            <div class="transaccion-item ${claseTransaccion}">
                <div class="transaccion-icono">${icono}</div>
                <div class="transaccion-info">
                    <div class="transaccion-concepto">${concepto}</div>
                    <div class="transaccion-fecha">${fecha} a las ${hora}</div>
                </div>
                <div class="transaccion-cantidad" data-tipo="${colorClase}">
                    ${signo}${transaccion.cantidad.toFixed(2)}€
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    
    divTransacciones.innerHTML = html;
    console.log('✅ Transacciones mostradas');
}

// ============================================================================
// CUANDO CARGA EL DASHBOARD
// ============================================================================
window.addEventListener('DOMContentLoaded', function() {
    if (window.location.href.includes('/dashboard')) {
        console.log('📊 Dashboard cargado');
        
        // Esperar a que carguDashboard() haya terminado
        setTimeout(() => {
            cargarSaldoUsuario();
            cargarUltimasTransacciones();
        }, 500);
    }
});
