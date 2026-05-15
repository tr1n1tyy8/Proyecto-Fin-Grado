// ============================================================================
// SCRIPT PARA INFORMACIÓN DEL USUARIO - MOSTRAR Y EDITAR DATOS
// ============================================================================

async function cargarInformacionUsuario() {
    console.log('👤 Cargando información del usuario...');
    
    if (!estaAutenticado()) {
        console.log('⚠️ No autenticado');
        return;
    }
    
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('email');
    
    try {
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
            mostrarInformacionUsuario(usuario);
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

// ============================================================================
// MOSTRAR INFORMACIÓN DEL USUARIO
// ============================================================================
function mostrarInformacionUsuario(usuario) {
    const divDatos = document.getElementById('datos-usuario');
    
    if (!divDatos) {
        console.error('❌ No se encontró el div #datos-usuario');
        return;
    }
    
    let html = '<form id="formulario-informacion" class="formulario-informacion">';
    
    // Array de campos a mostrar (excepto contraseña y último inicio de sesión)
    const campos = [
        { key: 'nombre', label: 'Nombre', type: 'text', required: true },
        { key: 'apellidos', label: 'Apellidos', type: 'text', required: true },
        { key: 'email', label: 'Correo Electrónico', type: 'email', required: true, readonly: true },
        { key: 'dni', label: 'DNI', type: 'text', required: true, readonly: true },
        { key: 'telefono', label: 'Teléfono', type: 'tel', required: true },
        { key: 'fecha_nacimiento', label: 'Fecha de Nacimiento', type: 'date', required: true },
        { key: 'nacionalidad', label: 'Nacionalidad', type: 'text', required: true },
        { key: 'direccion', label: 'Dirección', type: 'text', required: true },
        { key: 'provincia', label: 'Provincia', type: 'text', required: true },
        { key: 'ciudad', label: 'Ciudad', type: 'text', required: true },
        { key: 'codigo_postal', label: 'Código Postal', type: 'text', required: true },
        { key: 'pais_residencia', label: 'País de Residencia', type: 'text', required: true },
        { key: 'situacion_laboral', label: 'Situación Laboral', type: 'text', required: true },
        { key: 'saldo', label: 'Saldo', type: 'number', required: false, readonly: true }
    ];
    
    campos.forEach(campo => {
        let valor = usuario[campo.key] || '';
        
        // Convertir fecha si es necesario
        if (campo.key === 'fecha_nacimiento' && valor) {
            const fecha = new Date(valor);
            valor = fecha.toISOString().split('T')[0]; // YYYY-MM-DD
        }
        
        // Formatear saldo
        if (campo.key === 'saldo' && valor) {
            valor = parseFloat(valor).toFixed(2);
        }
        
        const readonly = campo.readonly ? 'readonly' : '';
        const required = campo.required ? 'required' : '';
        
        html += `
            <div class="campo-informacion">
                <label for="${campo.key}">${campo.label}</label>
                <input 
                    type="${campo.type}" 
                    id="${campo.key}" 
                    name="${campo.key}" 
                    value="${valor}" 
                    ${readonly}
                    ${required}
                    class="input-informacion"
                    data-original="${valor}"
                >
                <span class="error-mensaje" id="error-${campo.key}"></span>
            </div>
        `;
    });
    
    // Botones de acción
    html += `
        <div class="botones-informacion">
            <button type="button" class="btn-editar" onclick="habilitarEdicion()" id="btn-editar">Editar Datos</button>
            <div class="botones-edicion" style="display: none;" id="botones-edicion">
                <button type="submit" class="btn-guardar">💾 Guardar Cambios</button>
                <button type="button" class="btn-cancelar" onclick="cancelarEdicion()">❌ Cancelar</button>
            </div>
        </div>
    `;
    
    html += '</form>';
    
    divDatos.innerHTML = html;
    
    // Agregar listener al formulario
    document.getElementById('formulario-informacion').addEventListener('submit', guardarCambios);
    
    console.log('✅ Información mostrada');
}

// ============================================================================
// HABILITAR EDICIÓN
// ============================================================================
function habilitarEdicion() {
    const inputs = document.querySelectorAll('.input-informacion:not([readonly])');
    const btnEditar = document.getElementById('btn-editar');
    const botonesEdicion = document.getElementById('botones-edicion');
    
    inputs.forEach(input => {
        input.classList.add('editable');
        input.removeAttribute('readonly');
    });
    
    btnEditar.style.display = 'none';
    botonesEdicion.style.display = 'flex';
    
    console.log('✏️ Modo edición habilitado');
}

// ============================================================================
// CANCELAR EDICIÓN
// ============================================================================
function cancelarEdicion() {
    const inputs = document.querySelectorAll('.input-informacion');
    const btnEditar = document.getElementById('btn-editar');
    const botonesEdicion = document.getElementById('botones-edicion');
    
    inputs.forEach(input => {
        input.value = input.getAttribute('data-original');
        input.classList.remove('editable');
        if (input.hasAttribute('readonly')) {
            input.setAttribute('readonly', 'readonly');
        }
    });
    
    btnEditar.style.display = 'block';
    botonesEdicion.style.display = 'none';
    
    // Limpiar mensajes de error
    document.querySelectorAll('.error-mensaje').forEach(msg => msg.textContent = '');
    
    console.log('❌ Edición cancelada');
}

// ============================================================================
// GUARDAR CAMBIOS
// ============================================================================
async function guardarCambios(event) {
    event.preventDefault();
    
    console.log('💾 Guardando cambios...');
    
    if (!estaAutenticado()) {
        alert('⚠️ Sesión expirada');
        return;
    }
    
    const token = localStorage.getItem('token');
    const email = localStorage.getItem('email');
    
    // Recopilar datos del formulario
    const datos = {
        nombre: document.getElementById('nombre').value,
        apellidos: document.getElementById('apellidos').value,
        telefono: document.getElementById('telefono').value,
        fecha_nacimiento: document.getElementById('fecha_nacimiento').value,
        nacionalidad: document.getElementById('nacionalidad').value,
        direccion: document.getElementById('direccion').value,
        provincia: document.getElementById('provincia').value,
        ciudad: document.getElementById('ciudad').value,
        codigo_postal: document.getElementById('codigo_postal').value,
        pais_residencia: document.getElementById('pais_residencia').value,
        situacion_laboral: document.getElementById('situacion_laboral').value
    };
    
    // Validar datos
    const errores = validarDatos(datos);
    if (Object.keys(errores).length > 0) {
        mostrarErrores(errores);
        return;
    }
    
    try {
        const respuesta = await fetch(API_URL + `/usuarios/actualizar/${email}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });
        
        if (respuesta.ok) {
            const usuarioActualizado = await respuesta.json();
            console.log('✅ Datos actualizados:', usuarioActualizado);
            
            // Actualizar la visualización
            mostrarInformacionUsuario(usuarioActualizado);
            alert('✅ Datos actualizados correctamente');
        } else if (respuesta.status === 401) {
            alert('⚠️ Sesión expirada');
            localStorage.removeItem('token');
            window.location.href = '/acceso';
        } else {
            const error = await respuesta.json();
            alert('❌ Error: ' + error.detail);
        }
    } catch (error) {
        console.error('❌ Error de conexión:', error);
        alert('❌ Error al guardar los datos');
    }
}

// ============================================================================
// VALIDAR DATOS
// ============================================================================
function validarDatos(datos) {
    const errores = {};
    
    // Validar nombre
    if (!datos.nombre || datos.nombre.length < 2) {
        errores.nombre = 'El nombre debe tener al menos 2 caracteres';
    }
    
    // Validar apellidos
    if (!datos.apellidos || datos.apellidos.length < 2) {
        errores.apellidos = 'Los apellidos deben tener al menos 2 caracteres';
    }
    
    // Validar teléfono
    if (!datos.telefono || !/^\d{9,15}$/.test(datos.telefono.replace(/\D/g, ''))) {
        errores.telefono = 'El teléfono debe tener entre 9 y 15 dígitos';
    }
    
    // Validar fecha de nacimiento
    if (!datos.fecha_nacimiento) {
        errores.fecha_nacimiento = 'La fecha de nacimiento es requerida';
    } else {
        const fecha = new Date(datos.fecha_nacimiento);
        const hoy = new Date();
        const edad = hoy.getFullYear() - fecha.getFullYear();
        if (edad < 18) {
            errores.fecha_nacimiento = 'Debes tener al menos 18 años';
        }
    }
    
    // Validar campos no vacíos
    const camposRequeridos = ['nacionalidad', 'direccion', 'provincia', 'ciudad', 'codigo_postal', 'pais_residencia', 'situacion_laboral'];
    camposRequeridos.forEach(campo => {
        if (!datos[campo] || datos[campo].trim().length === 0) {
            errores[campo] = 'Este campo es requerido';
        }
    });
    
    return errores;
}

// ============================================================================
// MOSTRAR ERRORES
// ============================================================================
function mostrarErrores(errores) {
    // Limpiar errores anteriores
    document.querySelectorAll('.error-mensaje').forEach(msg => msg.textContent = '');
    
    // Mostrar nuevos errores
    Object.keys(errores).forEach(campo => {
        const elemento = document.getElementById(`error-${campo}`);
        if (elemento) {
            elemento.textContent = '⚠️ ' + errores[campo];
        }
    });
}

// ============================================================================
// CUANDO CARGA LA PÁGINA
// ============================================================================
window.addEventListener('DOMContentLoaded', function() {
    if (window.location.href.includes('/informacion')) {
        console.log('👤 Página de información cargada');
        
        setTimeout(() => {
            cargarInformacionUsuario();
        }, 500);
    }
});
