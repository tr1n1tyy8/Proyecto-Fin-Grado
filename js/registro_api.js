// ============================================================================
// SCRIPT PARA ENLAZAR FORMULARIO DE REGISTRO CON LA BASE DE DATOS
// ============================================================================
// Este archivo maneja:
// 1. Guardar datos conforme rellenas cada página
// 2. Validar que las contraseñas coincidan
// 3. Enviar todo a la API cuando das a "Confirmar"
// ============================================================================

// ============================================================================
// PASO 1: GUARDAR SITUACIÓN LABORAL (Página 1)
// ============================================================================

function guardarSituacionLaboral() {
    const situacion = document.getElementById('situacion_laboral').value;
    
    // Validar que seleccionó algo
    if (!situacion) {
        alert('⚠️ Por favor, selecciona tu situación laboral');
        return;
    }
    
    // Guardar en sessionStorage (memoria temporal del navegador)
    sessionStorage.setItem('situacion_laboral', situacion);
    
    // Ir a la siguiente página
    window.location.href = '/registro2';
}

// ============================================================================
// PASO 2: GUARDAR DATOS PERSONALES (Página 2)
// ============================================================================
function guardarPersonales() {
    // Recoger todos los datos del formulario
    const nombre = document.getElementById('nombre').value;
    const apellidos = document.getElementById('apellidos').value;
    const fecha_nacimiento = document.getElementById('fecha_nacimiento').value;
    const dni = document.getElementById('dni').value;
    const pais_residencia = document.getElementById('pais_residencia').value;
    const nacionalidad = document.getElementById('nacionalidad').value;
    
    // Validar que todos los campos estén rellenos
    if (!nombre || !apellidos || !fecha_nacimiento || !dni || !pais_residencia || !nacionalidad) {
        alert('⚠️ Por favor, rellena todos los campos');
        return;
    }

    // --- Validaciones Página 2 ---
    // Validación Página 2 - Campos "nombre", "apellidos", "nacionalidad" y "pais_residencia":
    // sólo letras y espacios (sin números ni caracteres especiales)
    const letrasEspaciosRegex = /^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$/;
    let erroresP2 = 0;

    if (!letrasEspaciosRegex.test(nombre)) {
        window.alert('Nombre: sólo se permiten letras y espacios');
        erroresP2++;
    }

    if (!letrasEspaciosRegex.test(apellidos)) {
        window.alert('Apellidos: sólo se permiten letras y espacios');
        erroresP2++;
    }

    if (!letrasEspaciosRegex.test(nacionalidad)) {
        window.alert('Nacionalidad: sólo se permiten letras y espacios');
        erroresP2++;
    }

    if (!letrasEspaciosRegex.test(pais_residencia)) {
        window.alert('País: sólo se permiten letras y espacios');
        erroresP2++;
    }

    // Validación Página 2 - Campo "dni": formato español estándar (8 dígitos + letra)
    const dniRegex = /^\d{8}[A-Za-z]$/;
    if (!dniRegex.test(dni)) {
        window.alert('DNI: formato inválido. Debe ser 8 dígitos seguidos de una letra, sin espacios ni guiones');
        erroresP2++;
    }

    // Si hubo errores en las validaciones de la Página 2, no avanzamos
    if (erroresP2 > 0) return;
    
    // Guardar en sessionStorage
    sessionStorage.setItem('nombre', nombre);
    sessionStorage.setItem('apellidos', apellidos);
    sessionStorage.setItem('fecha_nacimiento', fecha_nacimiento);
    sessionStorage.setItem('dni', dni);
    sessionStorage.setItem('pais_residencia', pais_residencia);
    sessionStorage.setItem('nacionalidad', nacionalidad);
    
    // Ir a la siguiente página
    window.location.href = '/registro3';
}

// ============================================================================
// PASO 3: GUARDAR RESIDENCIA (Página 3)
// ============================================================================
function guardarResidencia() {
    // Recoger datos
    const direccion = document.getElementById('direccion').value;
    const ciudad = document.getElementById('ciudad').value;
    const provincia = document.getElementById('provincia').value;
    const codigo_postal = document.getElementById('codigo_postal').value;
    
    // Validar
    if (!direccion || !ciudad || !provincia || !codigo_postal) {
        alert('⚠️ Por favor, rellena todos los campos');
        return;
    }

    // --- Validaciones Página 3 ---
    // Validación Página 3 - Campos de localización ("direccion", "ciudad", "provincia"):
    // sólo letras y espacios (sin números ni caracteres especiales)
    const letrasEspaciosRegexLoc = /^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$/;
    let erroresP3 = 0;

    if (!letrasEspaciosRegexLoc.test(direccion)) {
        window.alert('Dirección: sólo se permiten letras y espacios');
        erroresP3++;
    }

    if (!letrasEspaciosRegexLoc.test(ciudad)) {
        window.alert('Ciudad: sólo se permiten letras y espacios');
        erroresP3++;
    }

    if (!letrasEspaciosRegexLoc.test(provincia)) {
        window.alert('Provincia: sólo se permiten letras y espacios');
        erroresP3++;
    }

    // Si hubo errores en las validaciones de la Página 3, no avanzamos
    if (erroresP3 > 0) return;

    // Guardar
    sessionStorage.setItem('direccion', direccion);
    sessionStorage.setItem('ciudad', ciudad);
    sessionStorage.setItem('provincia', provincia);
    sessionStorage.setItem('codigo_postal', codigo_postal);

    // Ir a la siguiente página
    window.location.href = '/registro4';
}

// ============================================================================
// PASO 4: ENVIAR TODO A LA API (Página 4 - Confirmar)
// ============================================================================
async function enviarRegistro() {
    // Recoger datos de página 4
    const email = document.getElementById('email').value;
    const telefono = document.getElementById('telefono').value;
    const password = document.getElementById('password').value;
    const password_confirm = document.getElementById('password_confirm').value;
    
    // Validar página 4
    if (!email || !telefono || !password || !password_confirm) {
        alert('⚠️ Por favor, rellena todos los campos');
        return;
    }
    
    // Validar que las contraseñas coincidan
    if (password !== password_confirm) {
        alert('⚠️ Las contraseñas no coinciden');
        return;
    }
    
    // Validar que contraseña tenga mínimo 6 caracteres
    if (password.length < 6) {
        alert('⚠️ La contraseña debe tener mínimo 6 caracteres');
        return;
    }

    // --- Validaciones Página 4 ---
    // Validación Página 4 - Campo "telefono": exactamente 9 dígitos, solo números, sin espacios ni guiones
    const telefonoRegex = /^\d{9}$/;
    if (!telefonoRegex.test(telefono)) {
        window.alert('Teléfono: debe contener exactamente 9 dígitos, sin espacios ni guiones');
        return;
    }
    
    // Recoger datos de las páginas anteriores desde sessionStorage
    const situacion_laboral = sessionStorage.getItem('situacion_laboral');
    const nombre = sessionStorage.getItem('nombre');
    const apellidos = sessionStorage.getItem('apellidos');
    const fecha_nacimiento = sessionStorage.getItem('fecha_nacimiento');
    const dni = sessionStorage.getItem('dni');
    const pais_residencia = sessionStorage.getItem('pais_residencia');
    const nacionalidad = sessionStorage.getItem('nacionalidad');
    const direccion = sessionStorage.getItem('direccion');
    const ciudad = sessionStorage.getItem('ciudad');
    const provincia = sessionStorage.getItem('provincia');
    const codigo_postal = sessionStorage.getItem('codigo_postal');
    
    // Validar que todas las páginas anteriores están completas
    if (!situacion_laboral || !nombre || !apellidos || !fecha_nacimiento || !dni) {
        alert('⚠️ Parece que falta completar alguna página anterior. Por favor, vuelve a empezar.');
        return;
    }
    
    // Preparar los datos para enviar a la API
    // Nota: La API espera YYYY-MM-DD, el date input ya lo da en ese formato
    const datosCompletos = {
        nombre: nombre,
        apellidos: apellidos,
        fecha_nacimiento: fecha_nacimiento,  // Ya viene en formato YYYY-MM-DD del input date
        dni: dni,
        telefono: telefono,
        email: email,
        nacionalidad: nacionalidad,
        direccion: direccion,
        provincia: provincia,
        ciudad: ciudad,
        codigo_postal: codigo_postal,
        pais_residencia: pais_residencia,
        situacion_laboral: situacion_laboral,
        password: password
    };
    
    console.log('📤 Enviando datos a la API:', datosCompletos);
    
    try {
        // Enviar POST a /register
        const respuesta = await fetch(API_URL + '/registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datosCompletos)
        });
        
        // Analizar la respuesta
        const datos = await respuesta.json();
        
        if (respuesta.ok) {
            // ✅ Registro exitoso
            alert('✅ ¡Registro exitoso! Bienvenido/a a Capitalia');
            
            // Limpiar sessionStorage
            sessionStorage.clear();
            
            // Ir al dashboard
            window.location.href = '/dashboard';
        } else {
            // ❌ Error en la API
            alert('❌ Error al registrarse: ' + (datos.detail || 'Error desconocido'));
            console.error('Error:', datos);
        }
    } catch (error) {
        // ❌ Error de conexión
        alert('❌ Error de conexión: ' + error.message);
        console.error('Error:', error);
    }
}

// ============================================================================
// CARGAR DATOS SI VUELVES A UNA PÁGINA ANTERIOR
// ============================================================================
// Cuando recargas una página, rellena los campos con lo que guardaste antes

window.addEventListener('DOMContentLoaded', function() {
    // En registro2.html
    if (document.getElementById('nombre')) {
        const nombre = sessionStorage.getItem('nombre');
        if (nombre) document.getElementById('nombre').value = nombre;
        
        const apellidos = sessionStorage.getItem('apellidos');
        if (apellidos) document.getElementById('apellidos').value = apellidos;
        
        const fecha = sessionStorage.getItem('fecha_nacimiento');
        if (fecha) document.getElementById('fecha_nacimiento').value = fecha;
        
        const dni = sessionStorage.getItem('dni');
        if (dni) document.getElementById('dni').value = dni;
        
        const pais = sessionStorage.getItem('pais_residencia');
        if (pais) document.getElementById('pais_residencia').value = pais;
        
        const nacionalidad = sessionStorage.getItem('nacionalidad');
        if (nacionalidad) document.getElementById('nacionalidad').value = nacionalidad;
    }
    
    // En registro3.html
    if (document.getElementById('direccion')) {
        const direccion = sessionStorage.getItem('direccion');
        if (direccion) document.getElementById('direccion').value = direccion;
        
        const ciudad = sessionStorage.getItem('ciudad');
        if (ciudad) document.getElementById('ciudad').value = ciudad;
        
        const provincia = sessionStorage.getItem('provincia');
        if (provincia) document.getElementById('provincia').value = provincia;
        
        const codigo = sessionStorage.getItem('codigo_postal');
        if (codigo) document.getElementById('codigo_postal').value = codigo;
    }
    
    // En registro.html
    if (document.getElementById('situacion_laboral')) {
        const situacion = sessionStorage.getItem('situacion_laboral');
        if (situacion) document.getElementById('situacion_laboral').value = situacion;
    }
});

// ============================================================================
