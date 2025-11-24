# Guía de Uso Completa

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación](#instalación)
3. [Demo Completa HTTP vs HTTPS](#demo-completa-http-vs-https)
4. [Uso Avanzado](#uso-avanzado)
5. [Troubleshooting](#troubleshooting)

---

## Requisitos Previos

### Sistema Operativo

- **Linux** (Ubuntu 20.04+, Debian 11+, Arch, Fedora)
- **macOS** (con Docker Desktop)
- **Windows** (con WSL2 + Docker Desktop)

### Software Requerido

```bash
# Verificar Docker
docker --version
# Debe mostrar: Docker version 20.10+ o superior

# Verificar Docker Compose
docker compose version
# Debe mostrar: Docker Compose version 2.0+ o superior

# Verificar Python
python3 --version
# Debe mostrar: Python 3.10+ o superior
```

### Permisos

```bash
# Añadir usuario al grupo docker (Linux)
sudo usermod -aG docker $USER

# Cerrar sesión y volver a entrar para aplicar cambios
# O ejecutar:
newgrp docker

# Verificar que funciona sin sudo
docker ps
```

---

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/gustavop-dev/crypthography_project.git
cd cryptography_project
```

### 2. Verificar Estructura

```bash
ls -la
# Deberías ver:
# - mitm-demo/
# - ssh-hardening/
# - scripts/
# - docs/
# - README.md
```

### 3. Construir Imágenes Docker

```bash
cd mitm-demo
sudo docker compose build
```

**Tiempo estimado:** 2-3 minutos

---

## Demo Completa HTTP vs HTTPS

### Opción 1: Script Automatizado (Recomendado)

```bash
# Desde la raíz del proyecto
bash scripts/demo_completa.sh
```

Este script ejecuta automáticamente:
1. ✅ Limpia el entorno
2. ✅ Levanta contenedores
3. ✅ Configura red
4. ✅ Inicia servidor HTTP
5. ✅ Captura credenciales en texto plano
6. ✅ Cambia a HTTPS
7. ✅ Muestra tráfico cifrado
8. ✅ Limpia al finalizar

### Opción 2: Paso a Paso Manual

#### Paso 1: Levantar el Entorno

```bash
cd mitm-demo
sudo docker compose up -d
```

Verificar que los contenedores están corriendo:

```bash
sudo docker compose ps
```

Deberías ver:

```
NAME             STATUS
mitm-attacker    Up
mitm-victim      Up
mitm-webserver   Up (healthy)
```

#### Paso 2: Acceder a la Aplicación Web

Abre tu navegador y ve a:

```
http://localhost:8080
```

Deberías ver la página de inicio con:
- Título: "Vulnerable Web App"
- Warning box amarillo
- Credenciales demo
- Botón "Continue to Login"

#### Paso 3: Iniciar Monitoreo (Terminal 1)

```bash
# En una terminal separada
cd mitm-demo
sudo docker compose exec webserver python /app/monitor_traffic.py
```

Deberías ver:

```
============================================================
🕵️  HTTP TRAFFIC MONITOR
Proyecto de Criptografía - UNAL Medellín
============================================================

🎯 Monitoreando tráfico HTTP en el servidor...
   Capturando requests desde tu navegador

⚠️  Presiona Ctrl+C para detener
```

#### Paso 4: Hacer Login HTTP

En tu navegador:

1. Click en "Continue to Login"
2. Ingresa credenciales:
   - **Username:** admin
   - **Password:** password123
3. Click "Continue"

#### Paso 5: Ver Credenciales Interceptadas

En la terminal del monitor verás:

```
🚨 [21:30:45] CREDENCIALES INTERCEPTADAS

============================================================
Usuario: admin
Password: password123
IP Origen: 172.17.0.1
Timestamp: 2025-11-24 21:30:45
============================================================

⚠️  Estas credenciales fueron capturadas en TEXTO PLANO
⚠️  Cualquier atacante en la red puede verlas
```

#### Paso 6: Cambiar a HTTPS

```bash
# Detener el monitor (Ctrl+C)

# Generar certificado SSL
sudo docker compose exec webserver bash /app/generate_cert.sh

# Iniciar servidor HTTPS
sudo docker compose exec webserver bash /app/start_https.sh
```

#### Paso 7: Acceder vía HTTPS

En tu navegador:

```
https://localhost:8443
```

**Nota:** Verás una advertencia de certificado (es normal, es autofirmado)
- Click en "Avanzado" o "Advanced"
- Click en "Continuar de todos modos" o "Proceed anyway"

#### Paso 8: Monitorear Tráfico HTTPS

```bash
# Iniciar monitor de nuevo
sudo docker compose exec webserver python /app/monitor_traffic.py
```

#### Paso 9: Login por HTTPS

1. Haz login con las mismas credenciales
2. Observa el monitor

Verás:

```
🔒 [21:35:20] Tráfico HTTPS detectado
   Puerto: 443 (HTTPS)

============================================================
🔐 DATOS CIFRADOS INTERCEPTADOS
============================================================
   El atacante puede ver el tráfico, pero está CIFRADO

   Datos capturados (muestra real):
   21:35:20.123456 IP 172.17.0.1.█████ > 172.20.0.30.443: Flags [P.], seq 1:█

   Hex (primeros bytes): 16 03 03 00 a5 01 00 00 a1 03 03 5f 8e...

   ✅ Las credenciales están CIFRADAS con TLS/SSL
   ✅ Imposible leer el contenido sin la clave privada
   ✅ El atacante solo ve datos binarios sin sentido
============================================================
```

#### Paso 10: Limpieza

```bash
# Detener contenedores
sudo docker compose down

# Limpiar volúmenes (opcional)
sudo docker compose down -v
```

---

## Uso Avanzado

### Capturar Tráfico con tcpdump

```bash
# Capturar todo el tráfico HTTP
sudo docker compose exec attacker tcpdump -i eth0 -w /tmp/http.pcap port 80

# Capturar tráfico HTTPS
sudo docker compose exec attacker tcpdump -i eth0 -w /tmp/https.pcap port 443

# Copiar archivo al host
sudo docker cp mitm-attacker:/tmp/http.pcap ./evidencias/pcap_files/
```

### Analizar con Wireshark

```bash
# Abrir captura en Wireshark
wireshark evidencias/pcap_files/http.pcap
```

**Filtros útiles:**
```
http.request.method == "POST"
http contains "username"
http contains "password"
```

### ARP Spoofing Manual

```bash
# Acceder al contenedor atacante
sudo docker compose exec attacker bash

# Habilitar IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Ejecutar ARP spoofing
arpspoof -i eth0 -t 172.20.0.10 172.20.0.30

# En otra terminal, capturar tráfico
tcpdump -i eth0 -s 65535 -w capture.pcap
```

### Monitoreo con Scapy

```bash
# Acceder al contenedor
sudo docker compose exec attacker python3

# En Python:
from scapy.all import *

def packet_handler(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        print(pkt[Raw].load)

sniff(iface="eth0", prn=packet_handler, filter="port 80")
```

### Ver Logs en Tiempo Real

```bash
# Todos los contenedores
sudo docker compose logs -f

# Solo webserver
sudo docker compose logs -f webserver

# Solo attacker
sudo docker compose logs -f attacker

# Últimas 50 líneas
sudo docker compose logs --tail 50 webserver
```

### Ejecutar Comandos en Contenedores

```bash
# Bash en webserver
sudo docker compose exec webserver bash

# Bash en attacker
sudo docker compose exec attacker bash

# Bash en victim
sudo docker compose exec victim bash
```

### Reiniciar Servicios

```bash
# Reiniciar solo webserver
sudo docker compose restart webserver

# Reiniciar todos
sudo docker compose restart

# Reconstruir imagen
sudo docker compose build --no-cache webserver
sudo docker compose up -d webserver
```

---

## Troubleshooting

### Problema: Puerto 8080 ya está en uso

```bash
# Ver qué proceso usa el puerto
sudo lsof -i :8080

# Matar el proceso
sudo kill -9 <PID>

# O cambiar el puerto en docker-compose.yml
ports:
  - "8081:80"  # Cambiar 8080 por 8081
```

### Problema: Contenedores no inician

```bash
# Ver logs de error
sudo docker compose logs

# Eliminar todo y empezar de cero
sudo docker compose down -v
sudo docker compose build --no-cache
sudo docker compose up -d
```

### Problema: No se captura tráfico

```bash
# Verificar que el monitor está corriendo
sudo docker compose exec webserver ps aux | grep monitor

# Verificar permisos de red
sudo docker compose exec attacker ip a

# Verificar IP forwarding
sudo docker compose exec attacker cat /proc/sys/net/ipv4/ip_forward
# Debe mostrar: 1
```

### Problema: Certificado HTTPS no funciona

```bash
# Regenerar certificado
sudo docker compose exec webserver rm -rf /app/ssl
sudo docker compose exec webserver bash /app/generate_cert.sh

# Reiniciar servidor HTTPS
sudo docker compose exec webserver pkill gunicorn
sudo docker compose exec webserver bash /app/start_https.sh
```

### Problema: Página no carga

```bash
# Verificar que el servidor está corriendo
sudo docker compose exec webserver ps aux | grep python

# Ver logs del servidor
sudo docker compose logs webserver

# Reiniciar webserver
sudo docker compose restart webserver
```

### Problema: Cambios en código no se reflejan

```bash
# Reconstruir imagen
sudo docker compose down
sudo docker compose build --no-cache webserver
sudo docker compose up -d

# Limpiar caché del navegador
# Ctrl + Shift + R (Firefox/Chrome)
# Cmd + Shift + R (Mac)
```

### Problema: Docker requiere sudo

```bash
# Añadir usuario al grupo docker
sudo usermod -aG docker $USER

# Aplicar cambios
newgrp docker

# O cerrar sesión y volver a entrar
```

---

## Comandos Útiles de Referencia

### Docker Compose

```bash
# Levantar servicios
docker compose up -d

# Ver estado
docker compose ps

# Ver logs
docker compose logs -f

# Detener servicios
docker compose stop

# Eliminar contenedores
docker compose down

# Eliminar todo (incluye volúmenes)
docker compose down -v

# Reconstruir
docker compose build --no-cache

# Reiniciar un servicio
docker compose restart webserver
```

### Docker

```bash
# Listar contenedores
docker ps

# Listar imágenes
docker images

# Ejecutar comando en contenedor
docker exec -it mitm-webserver bash

# Ver logs de contenedor
docker logs mitm-webserver

# Copiar archivos
docker cp mitm-webserver:/app/file.txt ./

# Limpiar sistema
docker system prune -a
```

### Networking

```bash
# Ver redes Docker
docker network ls

# Inspeccionar red
docker network inspect mitm-demo_mitm-lab-network

# Ver IPs de contenedores
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mitm-webserver
```

---

## Próximos Pasos

Después de completar la demo:

1. ✅ Revisar [ARQUITECTURA.md](ARQUITECTURA.md) para entender el diseño
2. ✅ Leer [RESULTADOS.md](RESULTADOS.md) para ver análisis detallado
3. ✅ Consultar [SSH_HARDENING.md](SSH_HARDENING.md) para configuración SSH
4. ✅ Ver [CHECKLIST_SEGURIDAD.md](CHECKLIST_SEGURIDAD.md) para mejores prácticas

---

**¿Preguntas o problemas?**

Consulta el [README principal](../README.md) o revisa los logs con `docker compose logs -f`
