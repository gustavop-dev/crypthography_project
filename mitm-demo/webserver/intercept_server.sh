#!/bin/bash

echo "============================================================"
echo "🕵️  HTTP TRAFFIC MONITOR - Webserver Side"
echo "Proyecto de Criptografía - UNAL Medellín"
echo "============================================================"
echo ""
echo "🎯 Monitoreando TODO el tráfico HTTP que llega al servidor..."
echo "   Incluyendo desde tu navegador (localhost:8080)"
echo ""
echo "⚠️  Presiona Ctrl+C para detener"
echo ""

# Instalar tcpdump si no está
apt-get update -qq && apt-get install -y tcpdump -qq 2>/dev/null

# Capturar y mostrar tráfico HTTP
tcpdump -i any -A -s 0 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)' 2>/dev/null | \
grep -E "POST|username|password|GET" --line-buffered --color=always
