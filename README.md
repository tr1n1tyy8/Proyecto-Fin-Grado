# Capitalia - App bancaria con FastAPI y frontend estático

## Descripción
Capitalia es una aplicación bancaria web que permite a usuarios registrados iniciar sesión, consultar su saldo, realizar transferencias Bizum y ver su historial de transacciones. El proyecto usa un backend en FastAPI y un frontend en HTML/JavaScript/CSS.

## Tecnologías principales
- Backend: `FastAPI`, `SQLAlchemy`, `JWT`, `bcrypt`
- Base de datos: MySQL (conector `mysqlclient` o `PyMySQL`)
- Frontend: HTML, CSS y JavaScript puro
- Despliegue recomendado: frontend en Vercel y backend en un host Python

## Funcionalidades
- Registro y login de usuarios con JWT
- Protección de rutas para páginas privadas
- Historial de transacciones
- Bizum interno entre usuarios con validaciones
- Prevención de transferencias a sí mismo
- Mensajes de error inline en los formularios
- CORS configurado para permitir el frontend en Vercel

## Estructura del proyecto
- `/backend/requirements.txt` - dependencias Python
- `/backend/FastAPI/main.py` - aplicación FastAPI principal
- `/backend/FastAPI/routers/autenticacion.py` - rutas de registro/login y perfil
- `/backend/FastAPI/routers/transacciones.py` - transferencias y historial
- `/frontend/` - páginas HTML del cliente
- `/css/styles.css` - estilos globales
- `/js/` - lógica de cliente y consumo de API

## Cómo ejecutar localmente
1. Crear un entorno virtual en `backend`:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configurar variables de entorno para la base de datos y JWT.
3. Iniciar la app:
   ```bash
   uvicorn FastAPI.main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Abrir las páginas estáticas desde el frontend con un servidor local, o simplemente abrir los HTML en el navegador.

## Notas de despliegue
- El frontend es estático y puede hospedarse en Vercel.
- El backend debe desplegarse en un servicio capaz de ejecutar Python/FastAPI y conectar a MySQL.
- Asegúrate de configurar correctamente la URL de la API en `/js/main.js` y `/js/api_cliente.js`.

## Puntos clave de seguridad
- Las rutas privadas sólo aceptan requests con token JWT válido.
- Las transacciones requieren autenticación y sólo pueden verse los registros del usuario actual.
- Las transferencias validan que el receptor exista, el nombre coincida y que el usuario tenga saldo suficiente.
- Se evita que un usuario se envíe Bizum a sí mismo.

## Archivos importantes para producción
- `backend/FastAPI/main.py` - CORS y configuración de la app
- `backend/FastAPI/routers/autenticacion.py` - endpoints de auth
- `backend/FastAPI/routers/transacciones.py` - lógica bancaria y validaciones
- `js/main.js` - gestión de rutas protegidas y URL de API
- `js/api_cliente.js` - lógica de consumo de API y fallback

## Uso básico
1. Registrar una nueva cuenta desde `registro.html`.
2. Iniciar sesión en `login.html`.
3. Acceder a `dashboard.html` para ver saldo y transacciones.
4. Usar `bizum.html` para enviar dinero a otro usuario.
5. Consultar el historial en la sección de movimientos.

## Estado actual
- App funcional con login, registro, transferencias y historial.
- Validaciones de formulario y seguridad implementadas.
- Backend preparado para despliegue en una plataforma Python.
- Frontend listo para hospedar como sitio estático.

---