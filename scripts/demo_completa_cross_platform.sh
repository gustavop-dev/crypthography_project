#!/bin/bash

# ============================================
# DEMO COMPLETA - HTTP vs HTTPS
# Proyecto de Criptografía - UNAL Medellín
# Compatible: Linux, macOS, Windows (Git Bash/WSL)
# ============================================

# Detectar sistema operativo
detect_os() {
    case "$(uname -s)" in
        Linux*)     OS="Linux";;
        Darwin*)    OS="macOS";;
        CYGWIN*|MINGW*|MSYS*) OS="Windows";;
        *)          OS="Unknown";;
    esac
}

# Determinar si necesitamos sudo
setup_docker_command() {
    detect_os
    
    if [ "$OS" = "Linux" ]; then
        # En Linux, verificar si el usuario está en el grupo docker
        if groups | grep -q docker; then
            DOCKER_CMD="docker"
            DOCKER_COMPOSE_CMD="docker compose"
        else
            echo "  En Linux necesitas sudo o estar en el grupo docker"
            DOCKER_CMD="sudo docker"
            DOCKER_COMPOSE_CMD="sudo docker compose"
        fi
    else
        # macOS y Windows con Docker Desktop no necesitan sudo
        DOCKER_CMD="docker"
        DOCKER_COMPOSE_CMD="docker compose"
    fi
}

# Verificar que Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo " Docker no está instalado"
        echo ""
        case "$OS" in
            Linux)
                echo "Instala Docker: https://docs.docker.com/engine/install/"
                ;;
            macOS)
                echo "Instala Docker Desktop: https://docs.docker.com/desktop/install/mac-install/"
                ;;
            Windows)
                echo "Instala Docker Desktop: https://docs.docker.com/desktop/install/windows-install/"
                ;;
        esac
        exit 1
    fi
    
    # Verificar que Docker está corriendo
    if ! $DOCKER_CMD ps &> /dev/null; then
        echo " Docker no está corriendo"
        echo ""
        case "$OS" in
            Linux)
                echo "Inicia Docker: sudo systemctl start docker"
                ;;
            macOS|Windows)
                echo "Abre Docker Desktop y espera a que inicie"
                ;;
        esac
        exit 1
    fi
}

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# Setup
setup_docker_command
check_docker

clear

echo -e "${CYAN}"
cat << "EOF"

           DEMOSTRACIÓN COMPARATIVA                         
           HTTP vs HTTPS - Ataque MitM                      
                                                            
     Universidad Nacional de Colombia - Sede Medellín      
           Criptografía y Seguridad - Grupo 6              

EOF
echo -e "${NC}"

echo -e "${CYAN}Sistema detectado: ${GREEN}$OS${NC}"
echo -e "${CYAN}Comando Docker: ${GREEN}$DOCKER_CMD${NC}"
echo ""

echo -e "${RED}  ADVERTENCIA: USO EDUCATIVO ÚNICAMENTE${NC}"
echo -e "${YELLOW}Esta demostración muestra vulnerabilidades en un entorno controlado${NC}"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "mitm-demo/docker-compose.yml" ]; then
    echo -e "${RED} Error: Ejecuta desde el directorio raíz del proyecto${NC}"
    exit 1
fi

cd mitm-demo

echo -e "${BLUE}${NC}"
echo -e "${GREEN}PARTE 1: DEMOSTRACIÓN CON HTTP (VULNERABLE)${NC}"
echo -e "${BLUE}${NC}"
echo ""

echo -e "${YELLOW}Presiona ENTER para continuar...${NC}"
read

# Limpiar entorno previo
echo -e "${YELLOW} Limpiando entorno previo...${NC}"
$DOCKER_COMPOSE_CMD down -v 2>/dev/null

# Levantar contenedores
echo -e "${YELLOW} Levantando contenedores...${NC}"
$DOCKER_COMPOSE_CMD up -d

# Esperar a que el webserver esté listo
echo -e "${YELLOW}⏳ Esperando a que el servidor esté listo...${NC}"
sleep 5

# Verificar que el contenedor está corriendo
if ! $DOCKER_CMD ps | grep -q mitm-webserver; then
    echo -e "${RED} Error: El contenedor webserver no está corriendo${NC}"
    echo -e "${YELLOW}Logs del error:${NC}"
    $DOCKER_COMPOSE_CMD logs webserver
    exit 1
fi

echo ""
echo -e "${GREEN} Servidor HTTP listo${NC}"
echo ""

cat << "EOF"


           PARTE 1: DEMOSTRACIÓN CON HTTP                   
                    (VULNERABLE)                            

EOF

echo ""
echo -e "${BLUE}${NC}"
echo -e "${CYAN}PARTE 1: DEMOSTRACIÓN CON HTTP (VULNERABLE)${NC}"
echo -e "${BLUE}${NC}"
echo ""

echo -e "${GREEN} Servidor HTTP corriendo en: ${CYAN}http://localhost:8080${NC}"
echo ""
echo -e "${YELLOW} INSTRUCCIONES:${NC}"
echo -e "   1. Abre tu navegador"
echo -e "   2. Ve a: ${CYAN}http://localhost:8080${NC}"
echo -e "   3. Haz login con:"
echo -e "      ${GREEN}Usuario:${NC} admin"
echo -e "      ${GREEN}Contraseña:${NC} password123"
echo ""

echo -e "${YELLOW}Presiona ENTER cuando estés listo para ver el tráfico interceptado...${NC}"
read

echo ""
echo -e "${RED}  INTERCEPTANDO TRÁFICO HTTP...${NC}"
echo ""

# Iniciar monitor en background
$DOCKER_COMPOSE_CMD exec -T webserver python /app/monitor_traffic.py &
MONITOR_PID=$!

echo ""
cat << "EOF"

 AHORA HAZ LOGIN EN TU NAVEGADOR


   URL: http://localhost:8080
   Usuario: admin
   Contraseña: password123

  Presiona Ctrl+C después de hacer login

EOF

# Esperar a que el usuario haga Ctrl+C
trap 'echo ""; echo "Deteniendo monitor..."; kill $MONITOR_PID 2>/dev/null; break' INT
wait $MONITOR_PID 2>/dev/null
trap - INT

echo ""
echo -e "${BLUE}${NC}"
echo -e "${RED} RESULTADO: CREDENCIALES INTERCEPTADAS${NC}"
echo -e "${BLUE}${NC}"
echo ""

echo -e "${YELLOW}Presiona ENTER para continuar con HTTPS...${NC}"
read

# ============================================
# PARTE 2: HTTPS
# ============================================

clear

cat << "EOF"


           PARTE 2: DEMOSTRACIÓN CON HTTPS                  
                    (SEGURO)                                

EOF

echo ""
echo -e "${BLUE}${NC}"
echo -e "${CYAN}PARTE 2: DEMOSTRACIÓN CON HTTPS (SEGURO)${NC}"
echo -e "${BLUE}${NC}"
echo ""

echo -e "${YELLOW} Generando certificado SSL...${NC}"
$DOCKER_COMPOSE_CMD exec -T webserver bash /app/generate_cert.sh

echo ""
echo -e "${YELLOW} Deteniendo servidor HTTP y iniciando HTTPS...${NC}"
$DOCKER_COMPOSE_CMD exec -T webserver pkill -f "python.*manage.py" 2>/dev/null || true
sleep 2
$DOCKER_COMPOSE_CMD exec -d webserver bash /app/start_https.sh
sleep 3

echo -e "${GREEN} Servidor HTTPS listo${NC}"
echo ""
echo -e "${GREEN} Servidor HTTPS corriendo en: ${CYAN}https://localhost:8443${NC}"
echo -e "${RED}  Tu navegador mostrará advertencia de certificado (es normal)${NC}"
echo -e "   Haz clic en 'Avanzado' → 'Continuar de todos modos'"
echo ""

echo -e "${YELLOW}Presiona ENTER cuando estés listo para hacer login por HTTPS...${NC}"
read

echo ""
echo -e "${CYAN}  INTENTANDO INTERCEPTAR TRÁFICO HTTPS...${NC}"
echo ""

# Iniciar monitor en background
$DOCKER_COMPOSE_CMD exec -T webserver python /app/monitor_traffic.py &
MONITOR_PID=$!

cat << "EOF"

 AHORA HAZ LOGIN POR HTTPS EN TU NAVEGADOR


   URL: https://localhost:8443
   Usuario: admin
   Contraseña: password123

 El atacante NO podrá ver las credenciales

  Presiona Ctrl+C después de hacer login

EOF

# Esperar a que el usuario haga Ctrl+C
trap 'echo ""; echo "Deteniendo monitor..."; kill $MONITOR_PID 2>/dev/null; break' INT
wait $MONITOR_PID 2>/dev/null
trap - INT

echo ""
echo -e "${BLUE}${NC}"
echo -e "${GREEN} RESULTADO: CREDENCIALES CIFRADAS - NO INTERCEPTADAS${NC}"
echo -e "${BLUE}${NC}"

# ============================================
# COMPARACIÓN FINAL
# ============================================

echo ""
echo -e "${BLUE}${NC}"
echo -e "${MAGENTA} COMPARACIÓN FINAL${NC}"
echo -e "${BLUE}${NC}"
echo ""

echo -e "${RED} HTTP (Puerto 8080):${NC}"
echo -e "   • Credenciales en texto plano"
echo -e "   • Fácilmente interceptables"
echo -e "   • Vulnerable a MitM"
echo ""

echo -e "${GREEN} HTTPS (Puerto 8443):${NC}"
echo -e "   • Credenciales cifradas"
echo -e "   • Imposible de interceptar sin certificado"
echo -e "   • Protegido contra MitM"
echo ""

echo -e "${BLUE}${NC}"
echo -e "${CYAN} CONCLUSIÓN${NC}"
echo -e "${BLUE}${NC}"
echo ""
echo -e "${GREEN}SIEMPRE usa HTTPS para proteger información sensible${NC}"
echo ""

echo -e "${YELLOW}Presiona ENTER para finalizar y limpiar...${NC}"
read

# Limpieza
echo ""
echo -e "${YELLOW} Limpiando entorno...${NC}"
$DOCKER_COMPOSE_CMD down

echo ""
echo -e "${GREEN} Demo completada y entorno limpio${NC}"
echo -e "${CYAN}Gracias por usar la demostración${NC}"
echo ""
echo -e "${BLUE} Para volver a ejecutar: bash scripts/demo_completa_cross_platform.sh${NC}"
echo ""
