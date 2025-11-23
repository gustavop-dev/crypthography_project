#!/bin/bash

# ============================================
# Script de Configuración de 2FA para SSH
# Proyecto de Criptografía - UNAL Medellín
# ============================================
#
# Este script configura autenticación de dos factores
# usando Google Authenticator PAM
#
# ⚠️  ADVERTENCIA: Asegúrate de tener otra forma de acceso
#     antes de habilitar 2FA, por si algo sale mal.
# ============================================

set -e

echo "🔐 Configuración de 2FA para SSH"
echo "=================================="
echo ""

# Verificar si se ejecuta como root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Este script debe ejecutarse como root (sudo)"
    exit 1
fi

# Verificar distribución
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "❌ No se pudo detectar la distribución"
    exit 1
fi

echo "📋 Sistema detectado: $OS"
echo ""

# Función para instalar en Ubuntu/Debian
install_ubuntu() {
    echo "📦 Instalando Google Authenticator PAM..."
    apt-get update
    apt-get install -y libpam-google-authenticator
}

# Función para instalar en Arch
install_arch() {
    echo "📦 Instalando Google Authenticator PAM..."
    pacman -Syu --noconfirm
    pacman -S --noconfirm libpam-google-authenticator
}

# Instalar según distribución
case $OS in
    ubuntu|debian)
        install_ubuntu
        ;;
    arch|manjaro)
        install_arch
        ;;
    *)
        echo "❌ Distribución no soportada: $OS"
        exit 1
        ;;
esac

echo ""
echo "✅ Google Authenticator PAM instalado"
echo ""

# Configurar PAM
echo "🔧 Configurando PAM para SSH..."

PAM_SSHD="/etc/pam.d/sshd"

# Backup del archivo PAM
cp $PAM_SSHD ${PAM_SSHD}.backup.$(date +%Y%m%d_%H%M%S)

# Verificar si ya está configurado
if grep -q "pam_google_authenticator.so" $PAM_SSHD; then
    echo "⚠️  Google Authenticator ya está configurado en PAM"
else
    # Añadir configuración al inicio del archivo
    sed -i '1i# Google Authenticator 2FA' $PAM_SSHD
    sed -i '2iauth required pam_google_authenticator.so nullok' $PAM_SSHD
    echo "✅ PAM configurado correctamente"
fi

echo ""

# Configurar SSH
echo "🔧 Configurando SSH para 2FA..."

SSHD_CONFIG="/etc/ssh/sshd_config"

# Backup del archivo SSH
cp $SSHD_CONFIG ${SSHD_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)

# Habilitar ChallengeResponseAuthentication
if grep -q "^ChallengeResponseAuthentication" $SSHD_CONFIG; then
    sed -i 's/^ChallengeResponseAuthentication.*/ChallengeResponseAuthentication yes/' $SSHD_CONFIG
else
    echo "ChallengeResponseAuthentication yes" >> $SSHD_CONFIG
fi

# Habilitar UsePAM
if grep -q "^UsePAM" $SSHD_CONFIG; then
    sed -i 's/^UsePAM.*/UsePAM yes/' $SSHD_CONFIG
else
    echo "UsePAM yes" >> $SSHD_CONFIG
fi

# Configurar AuthenticationMethods (clave pública + 2FA)
if grep -q "^AuthenticationMethods" $SSHD_CONFIG; then
    sed -i 's/^AuthenticationMethods.*/AuthenticationMethods publickey,keyboard-interactive/' $SSHD_CONFIG
else
    echo "AuthenticationMethods publickey,keyboard-interactive" >> $SSHD_CONFIG
fi

echo "✅ SSH configurado para 2FA"
echo ""

# Verificar configuración
echo "🔍 Verificando configuración de SSH..."
if sshd -t; then
    echo "✅ Configuración de SSH válida"
else
    echo "❌ Error en la configuración de SSH"
    echo "Restaurando backup..."
    cp ${SSHD_CONFIG}.backup.* $SSHD_CONFIG
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 2FA configurado correctamente"
echo "=========================================="
echo ""
echo "📝 IMPORTANTE - Próximos pasos:"
echo ""
echo "1. Cada usuario debe ejecutar (sin sudo):"
echo "   google-authenticator"
echo ""
echo "2. Responder a las preguntas:"
echo "   - Do you want authentication tokens to be time-based? (y)"
echo "   - Do you want me to update your ~/.google_authenticator file? (y)"
echo "   - Do you want to disallow multiple uses of the same token? (y)"
echo "   - Do you want to do so? (n) [rate limiting]"
echo "   - Do you want to enable rate-limiting? (y)"
echo ""
echo "3. Escanear el código QR con Google Authenticator app"
echo ""
echo "4. Guardar los códigos de emergencia en lugar seguro"
echo ""
echo "5. Reiniciar SSH:"
echo "   sudo systemctl restart sshd"
echo ""
echo "6. ⚠️  PROBAR en una nueva sesión ANTES de cerrar esta"
echo ""
echo "Para restaurar configuración anterior:"
echo "   sudo cp ${SSHD_CONFIG}.backup.* $SSHD_CONFIG"
echo "   sudo cp ${PAM_SSHD}.backup.* $PAM_SSHD"
echo "   sudo systemctl restart sshd"
echo ""
