#!/bin/bash

# Generar certificado SSL autofirmado para HTTPS

echo "🔐 Generando certificado SSL autofirmado..."

mkdir -p /app/ssl

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /app/ssl/server.key \
    -out /app/ssl/server.crt \
    -subj "/C=CO/ST=Antioquia/L=Medellin/O=UNAL/OU=Criptografia/CN=localhost"

chmod 600 /app/ssl/server.key
chmod 644 /app/ssl/server.crt

echo "✅ Certificado generado:"
echo "   Clave privada: /app/ssl/server.key"
echo "   Certificado: /app/ssl/server.crt"
