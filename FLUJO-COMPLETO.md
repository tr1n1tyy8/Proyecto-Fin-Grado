# 🔐 Flujo Completo: Registro → Login → Dashboard → Logout

## 📱 EL VIAJE DEL USUARIO (paso a paso)

```
PASO 1: REGISTRO
├─ Usuario abre: registro.html
├─ Llena 4 páginas del formulario
├─ Hace clic "Confirmar"
├─ JavaScript valida todos los datos
├─ Envía POST /register a la API
├─ API crea usuario en BD
└─ ✅ Redirige a: dashboard.html

PASO 2: PRIMER ACCESO AL DASHBOARD (después del registro)
├─ El usuario ve su cuenta con saldo 0.00€
├─ Puede explorar: Bizum, Avisos, Información
├─ El token se guarda automáticamente en el navegador
└─ ✅ Usuario en su dashboard

PASO 3: CERRAR SESIÓN
├─ Usuario hace clic: "Cerrar sesión"
├─ Se borra el token del navegador
├─ sessionStorage se limpia
└─ ✅ Redirige a: login.html

PASO 4: INICIAR SESIÓN (después de desconectarse)
├─ Usuario abre: login.html
├─ Introduce email y contraseña
├─ Hace clic: "Iniciar sesión"
├─ JavaScript valida formulario
├─ Envía POST /login a la API
├─ API devuelve JWT token (60 minutos)
└─ ✅ Redirige a: dashboard.html

PASO 5: DASHBOARD AUTENTICADO
├─ JavaScript verifica que tiene token válido
├─ Llamada GET /users/me con el token
├─ API devuelve datos del usuario
├─ Dashboard se actualiza con:
│   ├─ Nombre: "Hola, Sandra"
│   ├─ Saldo: Tu saldo real de la BD
│   ├─ Email, teléfono, ciudad, DNI
│   └─ Botón funcional: "Cerrar sesión"
├─ Usuario puede navegar:
│   ├─ Tus movimientos (transacciones)
│   ├─ Bizum (enviar dinero)
│   ├─ Avisos
│   └─ Información de la cuenta
└─ ✅ Sesión activa hasta que cierre

PASO 6 (opcional): CERRAR SESIÓN Y VOLVER A ENTRAR
└─ Se repite el PASO 3 → PASO 4 → PASO 5
```

---

## 🔑 ¿QUÉ PASA EN LOS NAVEGADORES?

### **localStorage** (Memoria persistente)
Se mantiene aunque cierres la pestaña

```javascript
localStorage.getItem('token')   // JWT token
localStorage.getItem('email')   // Email del usuario
```

### **sessionStorage** (Memoria temporal - Registro)
Se borra al cerrar la pestaña

```javascript
sessionStorage.getItem('nombre')
sessionStorage.getItem('apellidos')
// ... etc
```

---

## 🧪 FLUJO DE PRUEBA COMPLETO

### **Prueba 1: Registro directo**
```bash
# Terminal ejecuta:
bash prueba-completa.sh

# Resultado:
✓ Crea usuario en BD
✓ Genera token JWT
✓ Obtiene datos del usuario
```

### **Prueba 2: Registro por formulario HTML**
```
1. Abre: frontend/registro.html
2. Llena las 4 páginas
3. Haz clic "Confirmar"
4. ✅ Mensaje de éxito y va a dashboard
5. En dashboard verás tu saldo: 0.00€
```

### **Prueba 3: Cerrar sesión y volver a entrar**
```
1. En dashboard, haz clic "Cerrar sesión"
2. Serás redirigido a login.html
3. Introduce tu email y contraseña
4. Haz clic "Iniciar sesión"
5. ✅ Vuelves al dashboard con tus datos
```

---

## 📁 ARCHIVOS CLAVE

| Archivo | Qué hace |
|---|---|
| `registro.html` | Formulario página 1 |
| `registro2.html` | Formulario página 2 |
| `registro3.html` | Formulario página 3 |
| `registro4.html` | Formulario página 4 |
| **`registro-api.js`** | ✨ Maneja registro y validación |
| `login.html` | Formulario login |
| **`login-api.js`** | ✨ Maneja login, logout, dashboard |
| `dashboard.html` | Vista principal del usuario |
| `backend/FastAPI/routers/autenticacion.py` | Endpoints /register, /login, /users/me |
| `backend/FastAPI/models.py` | Modelo Cliente (BD) |

---

## ✅ TODO LO QUE FUNCIONA

- ✅ **Registro completo** - Capturas 16 campos, valida, guarda en BD
- ✅ **Login exitoso** - Genera JWT token válido por 60 minutos
- ✅ **Dashboard dinámico** - Momuestra datos reales del usuario de la BD
- ✅ **Cerrar sesión** - Borra token y sesión local
- ✅ **Re-login** - Puedes entrar de nuevo con mismas credenciales
- ✅ **Protección** - Sin token válido, no puedes acceder a dashboard
- ✅ **Datos persistentes** - Todo está en MySQL realmente

---

## 🎯 PASOS PARA PROBAR AHORA MISMO

### **Opción 1: Rápido (2 minutos)**
```bash
cd /Users/sandra/PROYECTO/proyecto_fin_grado
bash prueba-completa.sh
```

### **Opción 2: Con formularios (5 minutos)**
```
1. Abre: http://localhost:3000/frontend/registro.html
   (o arrastra registro.html a navegador)
2. Llena todo normalmente
3. Verás "Bienvenido" y accederás al dashboard
4. Haz clic "Cerrar sesión"
5. Abre login.html
6. Inicia sesión con lo que registraste
```

### **Opción 3: En MySQL (1 minuto)**
```sql
mysql> SELECT * FROM proyecto_fin_grado.clientes;
```

---

## 🚨 POSIBLES PROBLEMAS Y SOLUCIONES

### **Problema: "Error de conexión" al registrar**
- ✅ Solución: Verifica que el backend está corriendo (`uvicorn`)

### **Problema: Dashboard muestra "Cargando saldo..."**
- ✅ Solución: Espera 2-3 segundos, o recarga la página

### **Problema: "Sesión ha expirado" al entrar**
- ✅ Solución: Normal, el token dura 60 min. Vuelve a hacer login

### **Problema: Contraseña incorrecta en login**
- ✅ Solución: Verifica que es la que usaste en registro (sin espacios)

---

## 📊 BASE DE DATOS

Ver todos los usuarios registrados:
```sql
SELECT id, nombre, email, saldo, ciudad FROM clientes;
```

Ver último usuario registrado:
```sql
SELECT * FROM clientes ORDER BY id DESC LIMIT 1;
```

---

## 🎓 RESUMEN PARA DEFENSA

> "He implementado un sistema completo de autenticación con registro e inicio de sesión. Los usuarios se registran llenando un formulario multipágina, los datos se guardan en MySQL, y pueden iniciar sesión con sus credenciales generando un JWT token válido por 60 minutos. El dashboard muestra los datos reales del usuario desde la base de datos y permite cerrar sesión de forma segura."

---

**¡LISTO PARA PROBAR! 🚀**
