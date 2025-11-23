#!/bin/bash

# Iniciar servidor Django con HTTPS

echo "🔒 Iniciando servidor HTTPS en puerto 443..."

# Generar certificado si no existe
if [ ! -f /app/ssl/server.crt ]; then
    bash /app/generate_cert.sh
fi

# Instalar gunicorn si no está
pip install gunicorn -q

# Iniciar con gunicorn y SSL
gunicorn webapp.wsgi:application \
    --bind 0.0.0.0:443 \
    --certfile=/app/ssl/server.crt \
    --keyfile=/app/ssl/server.key \
    --access-logfile - \
    --error-logfile -
