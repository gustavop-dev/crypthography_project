#!/bin/bash

# ============================================
# DEMO COMPLETA - HTTP vs HTTPS
# Proyecto de Criptografía - UNAL Medellín
# ============================================

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

clear

echo -e "${CYAN}"
cat << "EOF"
╔════════════════════════════════════════════════════════════╗
║           DEMOSTRACIÓN COMPARATIVA                         ║
║           HTTP vs HTTPS - Ataque MitM                      ║
║                                                            ║
║     Universidad Nacional de Colombia - Sede Medellín      ║
║           Criptografía y Seguridad - Grupo 6              ║
╚════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${RED}⚠️  ADVERTENCIA: USO EDUCATIVO ÚNICAMENTE${NC}"
echo -e "${YELLOW}Esta demostración muestra vulnerabilidades en un entorno controlado${NC}"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "mitm-demo/docker-compose.yml" ]; then
    echo -e "${RED}❌ Error: Ejecuta desde el directorio raíz del proyecto${NC}"
    exit 1
fi

cd mitm-demo

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}PARTE 1: DEMOSTRACIÓN CON HTTP (VULNERABLE)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Presiona ENTER para continuar...${NC}"
read

echo -e "${CYAN}📦 Preparando entorno...${NC}"
sudo docker compose up -d >/dev/null 2>&1
sleep 3

echo -e "${GREEN}✅ Contenedores listos${NC}"
echo ""

echo -e "${CYAN}🌐 Servidor HTTP corriendo en: ${YELLOW}http://localhost:8080${NC}"
echo -e "${CYAN}📱 Abre tu navegador y accede a la URL${NC}"
echo ""

echo -e "${YELLOW}Cuando estés listo para hacer login, presiona ENTER...${NC}"
read

echo ""
echo -e "${RED}🕵️  INICIANDO INTERCEPTACIÓN...${NC}"
echo ""

# Crear un script temporal que ejecute el monitor con timeout
cat > /tmp/demo_http.sh << 'SCRIPT'
#!/bin/bash

# Iniciar monitor en background
sudo docker compose exec -T webserver python3 /app/monitor_traffic.py &
MONITOR_PID=$!

# Esperar un poco
sleep 2

echo ""
echo "════════════════════════════════════════════════════════════"
echo "🎯 AHORA HAZ LOGIN EN TU NAVEGADOR"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "   URL: http://localhost:8080"
echo "   Usuario: admin"
echo "   Contraseña: password123"
echo ""
echo "⏱️  Esperando 30 segundos para que hagas login..."
echo "   (O presiona Ctrl+C si ya viste las credenciales)"
echo ""

# Esperar 30 segundos o hasta Ctrl+C
sleep 30 2>/dev/null || true

# Matar el monitor
kill $MONITOR_PID 2>/dev/null
wait $MONITOR_PID 2>/dev/null
SCRIPT

chmod +x /tmp/demo_http.sh
bash /tmp/demo_http.sh 2>/dev/null || true

echo ""
echo -e "${RED}═══════════════════════════════════════════════════════════${NC}"
echo -e "${RED}⚠️  RESULTADO: CREDENCIALES CAPTURADAS EN TEXTO PLANO${NC}"
echo -e "${RED}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Presiona ENTER para continuar con la demo de HTTPS...${NC}"
read

clear

echo -e "${CYAN}"
cat << "EOF"
╔════════════════════════════════════════════════════════════╗
║           PARTE 2: DEMOSTRACIÓN CON HTTPS                  ║
║                    (SEGURO)                                ║
╚════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}PARTE 2: DEMOSTRACIÓN CON HTTPS (SEGURO)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${CYAN}🔐 Generando certificado SSL...${NC}"
sudo docker compose exec -T webserver bash /app/generate_cert.sh

echo ""
echo -e "${CYAN}🔒 Iniciando servidor HTTPS...${NC}"

# Iniciar HTTPS en background
sudo docker compose exec -d webserver bash /app/start_https.sh

sleep 3

echo -e "${GREEN}✅ Servidor HTTPS listo${NC}"
echo ""

echo -e "${CYAN}🌐 Servidor HTTPS corriendo en: ${GREEN}https://localhost:8443${NC}"
echo -e "${YELLOW}⚠️  Tu navegador mostrará advertencia de certificado (es normal)${NC}"
echo -e "${CYAN}   Haz clic en 'Avanzado' → 'Continuar de todos modos'${NC}"
echo ""

echo -e "${YELLOW}Presiona ENTER cuando estés listo para hacer login por HTTPS...${NC}"
read

echo ""
echo -e "${RED}🕵️  INTENTANDO INTERCEPTAR TRÁFICO HTTPS...${NC}"
echo ""

# Intentar interceptar HTTPS
cat > /tmp/demo_https.sh << 'SCRIPT'
#!/bin/bash

sudo docker compose exec -T webserver python3 /app/monitor_traffic.py &
MONITOR_PID=$!

sleep 2

echo ""
echo "════════════════════════════════════════════════════════════"
echo "🎯 AHORA HAZ LOGIN POR HTTPS EN TU NAVEGADOR"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "   URL: https://localhost:8443"
echo "   Usuario: admin"
echo "   Contraseña: password123"
echo ""
echo "🔒 El atacante NO podrá ver las credenciales cifradas"
echo ""
echo "⏱️  Esperando 30 segundos para que hagas login..."
echo "   (O presiona Ctrl+C si ya terminaste)"
echo ""

# Esperar 30 segundos
sleep 30 2>/dev/null || true

# Matar el monitor
kill $MONITOR_PID 2>/dev/null
wait $MONITOR_PID 2>/dev/null
SCRIPT

chmod +x /tmp/demo_https.sh
bash /tmp/demo_https.sh 2>/dev/null || true

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ RESULTADO: CREDENCIALES CIFRADAS - NO INTERCEPTADAS${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}📊 COMPARACIÓN FINAL${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${RED}❌ HTTP (Puerto 8080):${NC}"
echo -e "   • Credenciales en texto plano"
echo -e "   • Fácilmente interceptables"
echo -e "   • Vulnerable a MitM"
echo ""

echo -e "${GREEN}✅ HTTPS (Puerto 8443):${NC}"
echo -e "   • Credenciales cifradas"
echo -e "   • Imposible de interceptar sin certificado"
echo -e "   • Protegido contra MitM"
echo ""

echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🎓 CONCLUSIÓN${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}SIEMPRE usa HTTPS para proteger información sensible${NC}"
echo ""

echo -e "${BLUE}Presiona ENTER para finalizar y limpiar...${NC}"
read

# Limpiar
sudo docker compose down >/dev/null 2>&1

echo ""
echo -e "${GREEN}✅ Demo completada${NC}"
echo -e "${CYAN}Gracias por usar la demostración${NC}"
echo ""
