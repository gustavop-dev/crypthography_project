#!/bin/bash

# ============================================
# Script de Instalación de Docker
# Proyecto de Criptografía - UNAL Medellín
# ============================================

set -e  # Salir si hay algún error

echo " Instalando Docker y Docker Compose..."
echo ""

# Detectar distribución de Linux
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VERSION=$VERSION_ID
else
    echo " No se pudo detectar la distribución de Linux"
    exit 1
fi

echo " Sistema detectado: $OS $VERSION"
echo ""

# Función para Ubuntu/Debian
install_docker_ubuntu() {
    echo " Instalando Docker en Ubuntu/Debian..."
    
    # Actualizar repositorios
    sudo apt-get update
    
    # Instalar dependencias
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Añadir clave GPG oficial de Docker
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # Configurar repositorio
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Instalar Docker Engine
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    echo " Docker instalado correctamente"
}

# Función para Arch Linux
install_docker_arch() {
    echo " Instalando Docker en Arch Linux..."
    
    sudo pacman -Syu --noconfirm
    sudo pacman -S --noconfirm docker docker-compose
    
    echo " Docker instalado correctamente"
}

# Instalar según la distribución
case $OS in
    ubuntu|debian)
        install_docker_ubuntu
        ;;
    arch|manjaro)
        install_docker_arch
        ;;
    *)
        echo " Distribución no soportada: $OS"
        echo "Por favor, instala Docker manualmente desde: https://docs.docker.com/engine/install/"
        exit 1
        ;;
esac

# Iniciar y habilitar Docker
echo ""
echo " Iniciando servicio Docker..."
sudo systemctl start docker
sudo systemctl enable docker

# Añadir usuario actual al grupo docker
echo ""
echo " Añadiendo usuario al grupo docker..."
sudo usermod -aG docker $USER

# Verificar instalación
echo ""
echo " Verificando instalación..."
docker --version
docker compose version

echo ""
echo " ¡Docker instalado correctamente!"
echo ""
echo "  IMPORTANTE: Debes cerrar sesión y volver a entrar para que los cambios surtan efecto."
echo "    O ejecuta: newgrp docker"
echo ""
echo "Para verificar que funciona, ejecuta:"
echo "    docker run hello-world"
echo ""
