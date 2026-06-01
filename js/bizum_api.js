// SCRIPT PARA BIZUM - VALIDACIONES Y TRANSFERENCIAS

let datosTransferencia = null; // Guardar datos mientras se confirma

// FUNCIÓN: MOSTRAR ERROR INLINE

function mostrarErrorInline(campo, mensaje) {
    const errorElement = document.getElementById(`error-${campo}`);
    if (errorElement) {
        errorElement.textContent = mensaje;
        errorElement.classList.add('visible');
    }
}

// FUNCIÓN: LIMPIAR ERRORES

function limpiarErrores() {
    const errores = document.querySelectorAll('[id^="error-"]');
    errores.forEach(error => {
        error.textContent = '';
        error.classList.remove('visible');
    });
}

// FUNCIÓN: VALIDAR Y PREPARAR TRANSFERENCIA

document.addEventListener('submit', function(e) {
    if (!window.location.href.includes('/bizum')) {
        return;
    }
    
    if (e.target.id !== 'formulario-bizum') {
        return;
    }
    
    e.preventDefault();
    validarYPrepararTransferencia();
}, true);

async function validarYPrepararTransferencia() {
    console.log('📋 Validando datos de transferencia...');
    
    // Limpiar errores previos
    limpiarErrores();
    
    // Recoger datos del formulario
    const numero_receptor = document.getElementById('numero_receptor').value.trim();
    const nombre_receptor = document.getElementById('nombre_receptor').value.trim();
    const cantidad = parseFloat(document.getElementById('cantidad').value);
    const concepto = document.getElementById('concepto').value.trim();
    
    // VALIDACIÓN 1: Campos requeridos
    if (!numero_receptor || !nombre_receptor || !cantidad) {
        if (!numero_receptor) mostrarErrorInline('numero_receptor', 'Por favor, ingresa el teléfono del receptor');
        if (!nombre_receptor) mostrarErrorInline('nombre_receptor', 'Por favor, ingresa el nombre del receptor');
        if (!cantidad) mostrarErrorInline('cantidad', 'Por favor, ingresa la cantidad');
        return;
    }
    
    // VALIDACIÓN 2: Formato de teléfono (9 dígitos)
    const telefonoLimpio = numero_receptor.replace(/\D/g, ''); // Elimina caracteres no dígitos
    if (telefonoLimpio.length !== 9) {
        mostrarErrorInline('numero_receptor', 'El teléfono debe tener 9 dígitos');
        return;
    }
    
    // Guardar solo los 9 dígitos del teléfono
    const numeroFinal = telefonoLimpio;
    
    // VALIDACIÓN 3: Verificar que no se envía a sí mismo
    const miTelefono = localStorage.getItem('telefono');
    if (miTelefono && numeroFinal === miTelefono) {
        mostrarErrorInline('numero_receptor', 'No puedes enviar Bizum a tu propio número');
        return;
    }
    
    // VALIDACIÓN 4: Cantidad válida
    if (cantidad <= 0) {
        mostrarErrorInline('cantidad', 'La cantidad debe ser mayor a 0€');
        return;
    }
    
    // VALIDACIÓN 5: Máximo 500€
    if (cantidad > 500) {
        mostrarErrorInline('cantidad', 'El máximo por transferencia es de 500€');
        return;
    }
    
    // VALIDACIÓN 6: Máximo 2 decimales
    if (cantidad.toString().split('.')[1]?.length > 2) {
        mostrarErrorInline('cantidad', 'La cantidad solo puede tener máximo 2 decimales');
        return;
    }
    
    console.log('Validaciones frontend pasadas');
    console.log('Datos a enviar:', {
        numero_receptor: numeroFinal,
        nombre_receptor: nombre_receptor,
        cantidad: cantidad,
        concepto: concepto || '(Sin concepto)'
    });
    
    // Guardar datos para confirmar después
    datosTransferencia = {
        numero_receptor: numeroFinal,
        nombre_receptor: nombre_receptor,
        cantidad: cantidad,
        concepto: concepto
    };
    
    // Mostrar pantalla de confirmación
    mostrarConfirmacion();
}

// FUNCIÓN: MOSTRAR CONFIRMACIÓN

function mostrarConfirmacion() {
    if (!datosTransferencia) return;
    
    // Llenar datos en la confirmación
    document.getElementById('confirmar-nombre').textContent = datosTransferencia.nombre_receptor;
    document.getElementById('confirmar-telefono').textContent = datosTransferencia.numero_receptor;
    document.getElementById('confirmar-cantidad').textContent = datosTransferencia.cantidad.toFixed(2);
    document.getElementById('confirmar-concepto').textContent = datosTransferencia.concepto || '(Sin concepto)';
    
    // Mostrar la pantalla de confirmación
    document.getElementById('confirmar-transferencia').classList.add('visible');
    
    // Desactivar botón de envío
    document.getElementById('btn-enviar').disabled = true;
    
    console.log('Mostrando pantalla de confirmación');
}

// FUNCIÓN: CANCELAR TRANSFERENCIA

function cancelarTransferencia() {
    console.log('Transferencia cancelada');
    
    datosTransferencia = null;
    
    // Ocultar pantalla de confirmación
    document.getElementById('confirmar-transferencia').classList.remove('visible');
    
    // Reactivar botón
    document.getElementById('btn-enviar').disabled = false;
    
    // Limpiar mensaje de éxito si lo hay
    document.getElementById('mensaje-exito').classList.remove('visible');
}

// FUNCIÓN: CONFIRMAR Y ENVIAR TRANSFERENCIA

async function confirmarTransferencia() {
    if (!datosTransferencia) return;
    
    console.log('Enviando transferencia a la API...');
    
    // Desactivar botones durante el envío
    document.getElementById('btn-enviar').disabled = true;
    
    const token = localStorage.getItem('token');
    
    if (!token) {
        mostrarErrorInline('numero_receptor', 'Error: No hay sesión. Por favor, inicia sesión de nuevo');
        setTimeout(() => {
            window.location.href = '/acceso';
        }, 1500);
        return;
    }
    
    try {

        // Enviar datos a la API
        const respuesta = await fetch(API_URL + '/transacciones/transferir', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                numero_receptor: datosTransferencia.numero_receptor,
                nombre_receptor: datosTransferencia.nombre_receptor,
                cantidad: datosTransferencia.cantidad,
                concepto: datosTransferencia.concepto
            })
        });
        
        const datos = await respuesta.json();
        
        if (respuesta.ok) {
            // Transferencia exitosa
            console.log('Transferencia exitosa:', datos);
            
            mostrarMensajeExito(datos);
            limpiarFormulario();
            
            // Ocultar confirmación
            document.getElementById('confirmar-transferencia').classList.remove('visible');
            
            datosTransferencia = null;
            
        } else {
            // Error desde la API
            console.error('Error en la API:', datos);
            mostrarErrorInline('numero_receptor', 'Error: ' + (datos.detail || 'Error desconocido'));
            
            // Mostrar confirmación nuevamente para volver a intentar
            mostrarConfirmacion();
        }
    } catch (error) {
        // Error de conexión
        console.error('Error de conexión:', error);
        mostrarErrorInline('numero_receptor', 'Error de conexión: ' + error.message);
        
        // Mostrar confirmación nuevamente
        mostrarConfirmacion();
    } finally {
        // Reactivar botón
        document.getElementById('btn-enviar').disabled = false;
    }
}

// FUNCIÓN: MOSTRAR MENSAJE DE ÉXITO

function mostrarMensajeExito(datos) {
    const divMensaje = document.getElementById('mensaje-exito');
    
    divMensaje.innerHTML = `
        <strong>${datos.mensaje}</strong><br>
        Tu nuevo saldo: <strong>${datos.nuevo_saldo.toFixed(2)}€</strong><br>
        ID Transacción: <strong>#${datos.id_transaccion}</strong>
    `;
    
    divMensaje.classList.add('visible');
    
    // Ocultar el mensaje después de 5 segundos
    setTimeout(() => {
        divMensaje.classList.remove('visible');
    }, 5000);
}

// FUNCIÓN: LIMPIAR FORMULARIO

function limpiarFormulario() {
    document.getElementById('numero_receptor').value = '';
    document.getElementById('nombre_receptor').value = '';
    document.getElementById('cantidad').value = '';
    document.getElementById('concepto').value = '';
}

// VERIFICAR AUTENTICACIÓN AL CARGAR LA PÁGINA

window.addEventListener('DOMContentLoaded', function() {
    if (window.location.href.includes('/bizum')) {
        console.log('Página de Bizum cargada');
        
        // Verificar que está autenticado
        if (!localStorage.getItem('token')) {
            mostrarErrorInline('numero_receptor', 'Necesitas iniciar sesión');
            setTimeout(() => {
                window.location.href = '/acceso';
            }, 1500);
        }
    }
});
