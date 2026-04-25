#!/bin/bash
# ============================================================================
# SERVIDOR HTTP PARA EL FRONTEND
# ============================================================================
# Este script inicia un servidor local para que los archivos HTML funcionen
# correctamente con fetch() y la API en localhost:8000

echo "🌐 Iniciando servidor HTTP para el frontend..."
echo ""
echo "Abrirá los archivos en http://localhost:3000"
echo ""

cd /Users/sandra/PROYECTO/proyecto_fin_grado/frontend

# Usar Python 3 para servir los archivos (disponible en Mac)
python3 -m http.server 3000 --bind 127.0.0.1

# Alternativa para Python 2:
# python -m SimpleHTTPServer 3000
