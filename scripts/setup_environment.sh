#!/bin/bash

# ============================================
# Script de Configuración del Entorno
# Proyecto de Criptografía - UNAL Medellín
# ============================================

set -e

echo "🚀 Configurando entorno del proyecto..."
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar comandos
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✅ $1 está instalado${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 NO está instalado${NC}"
        return 1
    fi
}

# Verificar requisitos
echo "📋 Verificando requisitos del sistema..."
echo ""

MISSING_DEPS=0

# Python 3
if check_command python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "   Versión: $PYTHON_VERSION"
else
    MISSING_DEPS=1
fi

# pip
if check_command pip3; then
    PIP_VERSION=$(pip3 --version | cut -d' ' -f2)
    echo "   Versión: $PIP_VERSION"
else
    MISSING_DEPS=1
fi

# Git
if check_command git; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    echo "   Versión: $GIT_VERSION"
else
    MISSING_DEPS=1
fi

# Docker
if check_command docker; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | tr -d ',')
    echo "   Versión: $DOCKER_VERSION"
else
    echo -e "${YELLOW}⚠️  Docker no está instalado${NC}"
    echo "   Ejecuta: bash scripts/install_docker.sh"
    MISSING_DEPS=1
fi

# Docker Compose
if docker compose version &> /dev/null; then
    echo -e "${GREEN}✅ docker compose está disponible${NC}"
    COMPOSE_VERSION=$(docker compose version | cut -d' ' -f4)
    echo "   Versión: $COMPOSE_VERSION"
else
    echo -e "${RED}❌ docker compose NO está disponible${NC}"
    MISSING_DEPS=1
fi

echo ""

if [ $MISSING_DEPS -eq 1 ]; then
    echo -e "${RED}❌ Faltan dependencias. Por favor, instálalas antes de continuar.${NC}"
    exit 1
fi

# Crear entorno virtual Python
echo "🐍 Configurando entorno virtual Python..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Entorno virtual creado${NC}"
else
    echo -e "${YELLOW}⚠️  Entorno virtual ya existe${NC}"
fi

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias Python
echo ""
echo "📦 Instalando dependencias Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo -e "${GREEN}✅ Dependencias Python instaladas correctamente${NC}"

# Verificar permisos de Docker
echo ""
echo "🔐 Verificando permisos de Docker..."
if docker ps &> /dev/null; then
    echo -e "${GREEN}✅ Tienes permisos para usar Docker${NC}"
else
    echo -e "${YELLOW}⚠️  No tienes permisos para usar Docker sin sudo${NC}"
    echo "   Ejecuta: sudo usermod -aG docker $USER"
    echo "   Luego cierra sesión y vuelve a entrar"
fi

# Crear directorios necesarios si no existen
echo ""
echo "📁 Verificando estructura de directorios..."
mkdir -p evidencias/screenshots
mkdir -p evidencias/pcap_files
mkdir -p evidencias/logs
mkdir -p ssh-hardening/resultados
echo -e "${GREEN}✅ Estructura de directorios verificada${NC}"

# Resumen
echo ""
echo "=========================================="
echo -e "${GREEN}✅ Entorno configurado correctamente${NC}"
echo "=========================================="
echo ""
echo "📝 Próximos pasos:"
echo "   1. Activa el entorno virtual: source venv/bin/activate"
echo "   2. Revisa el plan: cat PLAN_PROYECTO.md"
echo "   3. Comienza con la Fase 2: SSH Hardening"
echo ""
echo "🐳 Para trabajar con Docker:"
echo "   cd mitm-demo"
echo "   docker compose up -d"
echo ""
