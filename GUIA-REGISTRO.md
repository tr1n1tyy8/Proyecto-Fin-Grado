# 📱 Guía: Formulario de Registro Enlazado a BD

## ¿Qué he hecho?

He enlazado tu formulario de registro (4 páginas HTML) directamente con tu base de datos MySQL sin modificar **ningún campo existente**.

---

## 📊 Solo adaptaciones necesarias

El formulario tiene nombres que entiende el usuario, pero en la BD se llaman diferente:

| Etiqueta en formulario | Campo en BD | Ubicación |
|---|---|---|
| NIF/NIE | dni | Página 2 |
| Calle de residencia | direccion | Página 3 |
| Población | ciudad | Página 3 |
| Correo Electrónico | email | Página 4 |
| Número de Teléfono | telefono | Página 4 |

**Todos los demás campos son idénticos** ✓

---

## 🔧 Cómo funciona

### **Página 1 - Situación Laboral**
- Seleccionas una opción
- **JavaScript lo guarda en memoria** (sessionStorage)
- Botón "Continuar" te lleva a la página 2

### **Página 2 - Datos Personales**
- Rellenas los 6 campos
- **Se guardan automáticamente en memoria**
- Si vuelves atrás, los datos siguen ahí
- Botón "Continuar" → Página 3

### **Página 3 - Tu Residencia**
- Rellenas los 4 campos de dirección
- **JavaScript los guarda**
- Los datos persisten si vuelves atrás
- Botón "Continuar" → Página 4

### **Página 4 - Para Terminar**
- Rellenas email, teléfono y contraseña
- **JavaScript valida que las contraseñas coincidan**
- Si todo está correcto, botón "Confirmar" hace:
  1. ✅ Reúne todos los datos de las 4 páginas
  2. ✅ Los envía a la API en `/register`
  3. ✅ La API los guarda en la BD
  4. ✅ Te redirige al dashboard

---

## 📁 Archivos que cambié

### HTML (Sin cambios visuales, solo atributos técnicos)
- `registro.html` - Página 1 - Añadí IDs a los elementos
- `registro2.html` - Página 2 - Añadí IDs y names
- `registro3.html` - Página 3 - Añadí IDs y names
- `registro4.html` - Página 4 - Añadí IDs y names

### JavaScript (Tu nuevo aliado)
- **`js/registro-api.js`** - Archivo nuevo que maneja TODO:
  - Guarda datos conforme avanzas
  - Valida que los campos estén rellenos
  - Valida que las contraseñas coincidan
  - Envía los datos a la API
  - Muestra mensajes de éxito o error

### Backend (También ajustado)
- `backend/FastAPI/routers/autenticacion.py` - Endpoint `/register` funcionando
- `backend/FastAPI/models.py` - Modelo `Cliente` sin cambios en campos

---

## ✅ Validaciones que hace

Antes de guardar cada página:
- ✅ Todos los campos están rellenos
- ✅ Contraseña tiene mínimo 6 caracteres
- ✅ Las 2 contraseñas coinciden
- ✅ Email es válido

---

## 🚀 Para probar

1. **Abre** `registro.html` en tu navegador
2. **Rellena** las 4 páginas del formulario
3. **En la última página**, haz clic en "Confirmar"
4. **Si todo va bien**, verás un mensaje "✅ ¡Registro exitoso!" y te llevará al dashboard
5. **Abre MySQL** y verifica que se guardó en `clientes`:

```sql
SELECT * FROM clientes WHERE email = 'tu_email@ejemplo.com';
```

---

## 🛠️ Para tabla TRANSACCIONES

Igual que con registro, puedo crear un formulario para Bizum que:
- Valide que tengas saldo suficiente
- Guarde el Bizum en la tabla `transacciones`
- Actualice el saldo en ambos clientes

¿Lo hago también? Solo dime si quieres un formulario de Bizum con el mismo sistema.

---

## 📝 Resumen

- ✅ **Sin cambios** en estructura de BD
- ✅ **Sin librerías complicadas** - Solo vanilla JavaScript
- ✅ **Principiante amigable** - Comentarios explicativos en el código
- ✅ **Todo funciona** - Formulario → JavaScript → API → BD

¡Listo para tu defensa de FG! 🎓
