#!/bin/bash

# Iniciar servidor Django con HTTPS

echo "🔒 Iniciando servidor HTTPS en puerto 443..."

# Generar certificado si no existe
if [ ! -f /app/ssl/server.crt ]; then
    bash /app/generate_cert.sh
fi

# Instalar gunicorn si no está
pip install gunicorn -q 2>/dev/null

# Detener cualquier proceso previo en puerto 443
fuser -k 443/tcp 2>/dev/null || true

# Iniciar con gunicorn y SSL
exec gunicorn webapp.wsgi:application \
    --bind 0.0.0.0:443 \
    --certfile=/app/ssl/server.crt \
    --keyfile=/app/ssl/server.key \
    --workers 2 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - 2>&1
