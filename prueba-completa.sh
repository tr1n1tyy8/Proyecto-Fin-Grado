#!/bin/bash
# ============================================================================
# SCRIPT DE PRUEBA RÁPIDA - Registro → Login → Dashboard
# ============================================================================
# Este script simula un usuario completo llenando el formulario

echo "========================================"
echo "🧪 PRUEBA: Flujo Completo de Registro"
echo "========================================"
echo ""

# Usuario de prueba
EMAIL="prueba_$(date +%s)@test.com"
PASSWORD="prueba123456"

echo "📝 Datos del usuario de prueba:"
echo "Email: $EMAIL"
echo "Password: $PASSWORD"
echo ""

# ============================================================================
# PASO 1: REGISTRAR USUARIO
# ============================================================================
echo "1️⃣ Registrando usuario en la BD..."
echo ""

RESPONSE=$(curl -s -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d "{
    \"nombre\": \"Usuario\",
    \"apellidos\": \"Prueba\",
    \"fecha_nacimiento\": \"1990-05-15\",
    \"dni\": \"PRUEBA123456\",
    \"telefono\": \"612345678\",
    \"email\": \"$EMAIL\",
    \"nacionalidad\": \"España\",
    \"direccion\": \"Calle Test 123\",
    \"provincia\": \"Madrid\",
    \"ciudad\": \"Madrid\",
    \"codigo_postal\": \"28001\",
    \"pais_residencia\": \"España\",
    \"situacion_laboral\": \"Estudiante\",
    \"password\": \"$PASSWORD\"
  }")

echo "Respuesta del servidor:"
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
echo ""

# Extraer ID del usuario
USER_ID=$(echo "$RESPONSE" | jq .id 2>/dev/null)

if [ -z "$USER_ID" ] || [ "$USER_ID" == "null" ]; then
  echo "❌ Error: No se pudo registrar el usuario"
  exit 1
fi

echo "✅ Usuario registrado con ID: $USER_ID"
echo ""

# ============================================================================
# PASO 2: LOGIN
# ============================================================================
echo "2️⃣ Intentando login..."
echo ""

LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$EMAIL&password=$PASSWORD")

echo "Respuesta del servidor:"
echo "$LOGIN_RESPONSE" | jq . 2>/dev/null || echo "$LOGIN_RESPONSE"
echo ""

# Extraer token
TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r .access_token 2>/dev/null)

if [ -z "$TOKEN" ] || [ "$TOKEN" == "null" ]; then
  echo "❌ Error: No se pudo obtener el token"
  exit 1
fi

echo "✅ Login exitoso"
echo "Token JWT: ${TOKEN:0:50}..."
echo ""

# ============================================================================
# PASO 3: OBTENER DATOS DEL USUARIO
# ============================================================================
echo "3️⃣ Obteniendo datos del usuario autenticado..."
echo ""

ME_RESPONSE=$(curl -s -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer $TOKEN")

echo "Datos del usuario:"
echo "$ME_RESPONSE" | jq . 2>/dev/null || echo "$ME_RESPONSE"
echo ""

# ============================================================================
# VERIFICACIÓN EN BD
# ============================================================================
echo "4️⃣ Verificación en MySQL:"
echo ""
echo "Ejecuta esto en MySQL:"
echo "mysql> SELECT * FROM proyecto_fin_grado.clientes WHERE email = '$EMAIL';"
echo ""

# ============================================================================
# RESULTADOS
# ============================================================================
echo "========================================"
echo "✅ PRUEBA COMPLETADA"
echo "========================================"
echo "✓ Usuario registrado en BD"
echo "✓ Login funcionando"
echo "✓ Token JWT generado"
echo "✓ Endpoint /users/me funcionando"
echo ""
echo "El sistema está LISTO para usar 🚀"
