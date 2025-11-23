#!/bin/bash
# Script de Configuración de Claves SSH
# Proyecto de Criptografía - UNAL Medellín

set -e

echo "🔐 Configuración de Claves SSH"
echo "================================"
echo ""

# Verificar si ya existe una clave
if [ -f ~/.ssh/id_ed25519 ]; then
    echo "⚠️  Ya existe una clave ED25519 en ~/.ssh/id_ed25519"
    read -p "¿Deseas crear una nueva? (s/N): " response
    if [[ ! "$response" =~ ^[Ss]$ ]]; then
        echo "Usando clave existente"
        exit 0
    fi
fi

# Solicitar email
read -p "Ingresa tu email (para identificar la clave): " email

# Generar clave ED25519
echo ""
echo "📝 Generando clave ED25519..."
ssh-keygen -t ed25519 -C "$email" -f ~/.ssh/id_ed25519

# Configurar permisos
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub

echo ""
echo "✅ Clave generada exitosamente"
echo ""
echo "📋 Tu clave pública es:"
echo "---"
cat ~/.ssh/id_ed25519.pub
echo "---"
echo ""
echo "📤 Para copiar la clave a un servidor remoto:"
echo "   ssh-copy-id -i ~/.ssh/id_ed25519.pub usuario@servidor"
echo ""
