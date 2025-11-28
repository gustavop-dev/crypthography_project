#!/bin/bash

# Script de diagnóstico para la demo MitM

echo " Diagnóstico del Entorno MitM"
echo "================================"
echo ""

cd mitm-demo

echo " Estado de los contenedores:"
sudo docker compose ps
echo ""

echo " Logs del webserver:"
echo "----------------------"
sudo docker compose logs --tail=50 webserver
echo ""

echo " Logs del victim:"
echo "-------------------"
sudo docker compose logs --tail=20 victim
echo ""

echo " Logs del attacker:"
echo "---------------------"
sudo docker compose logs --tail=20 attacker
echo ""

echo " Verificar conectividad:"
echo "--------------------------"
echo "Ping desde victim a webserver:"
sudo docker compose exec -T victim ping -c 2 172.20.0.30 2>&1 || echo " No se pudo hacer ping"
echo ""

echo " Verificar puerto 80 en webserver:"
sudo docker compose exec -T webserver netstat -tuln | grep :80 || echo " Puerto 80 no está escuchando"
echo ""
