# Arquitectura Docker - Laboratorio MitM

## 🏗️ Diseño de la Infraestructura

Este documento describe la arquitectura de contenedores Docker para la simulación del ataque Man-in-the-Middle.

---

## 📊 Topología de Red

```
┌─────────────────────────────────────────────────────────────┐
│                    Red Docker Bridge                         │
│                   (mitm-lab-network)                         │
│                    172.20.0.0/16                             │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   VICTIM     │    │   ATTACKER   │    │  WEBSERVER   │  │
│  │  (Cliente)   │    │    (MitM)    │    │   (Django)   │  │
│  │              │    │              │    │              │  │
│  │ 172.20.0.10  │◄──►│ 172.20.0.20  │◄──►│ 172.20.0.30  │  │
│  │              │    │              │    │              │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                    │          │
│         │                   │                    │          │
│         └───────────────────┴────────────────────┘          │
│                    Tráfico HTTP/HTTPS                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🐳 Contenedores

### 1. **Contenedor VICTIM (Cliente/Víctima)**

**Propósito:** Simula un usuario navegando en la web y enviando credenciales.

**Características:**
- Sistema base: Ubuntu/Alpine Linux
- Python 3.10+
- Cliente HTTP (requests, curl)
- Scripts de navegación automatizada

**IP Estática:** `172.20.0.10`

**Servicios:**
- Cliente HTTP que envía credenciales al servidor web
- Simula comportamiento de usuario real

**Archivos principales:**
```
victim/
├── Dockerfile
├── scripts/
│   ├── browse_http.py      # Navega al servidor HTTP
│   └── send_credentials.py # Envía credenciales de prueba
└── README.md
```

---

### 2. **Contenedor ATTACKER (Atacante MitM)**

**Propósito:** Intercepta y captura el tráfico entre víctima y servidor.

**Características:**
- Sistema base: Ubuntu (requiere herramientas de red)
- Python 3.10+ con Scapy
- tcpdump / tshark
- Herramientas de ARP spoofing
- **Privilegios especiales:** `NET_ADMIN`, `NET_RAW`

**IP Estática:** `172.20.0.20`

**Servicios:**
- ARP Spoofing (envenenamiento de caché ARP)
- Captura de tráfico de red
- Análisis en tiempo real de paquetes HTTP
- Extracción de credenciales

**Archivos principales:**
```
attacker/
├── Dockerfile
├── requirements.txt
├── scripts/
│   ├── arp_spoof.py        # ARP Spoofing
│   ├── capture_traffic.py  # Captura con tcpdump/scapy
│   ├── intercept_http.py   # Intercepta y muestra HTTP
│   └── analyze_pcap.py     # Analiza archivos .pcap
└── README.md
```

**Capacidades de red necesarias:**
```yaml
cap_add:
  - NET_ADMIN  # Para manipular tablas ARP
  - NET_RAW    # Para captura de paquetes
```

---

### 3. **Contenedor WEBSERVER (Servidor Web Django)**

**Propósito:** Servidor web con formulario de login (HTTP y HTTPS).

**Características:**
- Django 4.x
- Gunicorn como WSGI server
- Dos configuraciones:
  - **HTTP** (puerto 80): Vulnerable a MitM
  - **HTTPS** (puerto 443): Protegido con TLS

**IP Estática:** `172.20.0.30`

**Puertos expuestos:**
- `80`: HTTP (vulnerable)
- `443`: HTTPS (seguro)

**Servicios:**
- Aplicación Django con formulario de login
- Base de datos SQLite (demo)
- Certificados SSL/TLS autofirmados

**Archivos principales:**
```
webserver/
├── Dockerfile
├── http_vulnerable/          # Versión HTTP
│   ├── manage.py
│   ├── requirements.txt
│   └── webapp/
│       ├── settings.py       # Sin HTTPS
│       └── login_app/
│           ├── views.py
│           ├── forms.py
│           └── templates/
│               └── login.html
└── https_secure/             # Versión HTTPS
    ├── manage.py
    ├── requirements.txt
    ├── ssl/
    │   ├── generate_certs.sh
    │   ├── server.crt
    │   └── server.key
    └── webapp/
        └── settings.py       # Con HSTS habilitado
```

---

## 🌐 Configuración de Red

### Red Bridge Personalizada

```yaml
networks:
  mitm-lab-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
```

**Ventajas de red personalizada:**
- IPs estáticas predecibles
- Aislamiento del host
- Control sobre el tráfico
- Facilita el ARP spoofing

### Tabla de IPs

| Contenedor | IP Estática | Hostname | Puertos |
|------------|-------------|----------|---------|
| Victim     | 172.20.0.10 | victim   | -       |
| Attacker   | 172.20.0.20 | attacker | -       |
| Webserver  | 172.20.0.30 | webserver| 80, 443 |

---

## 🔄 Flujo del Ataque MitM

### Fase 1: Configuración Normal (Sin Ataque)

```
Victim (172.20.0.10)
    │
    │ HTTP Request
    │ GET /login
    │
    ▼
Webserver (172.20.0.30)
    │
    │ HTTP Response
    │ 200 OK
    │
    ▼
Victim recibe página de login
```

### Fase 2: ARP Spoofing (Inicio del Ataque)

El atacante envía paquetes ARP falsos:

```
Attacker → Victim:
  "Soy el webserver (172.20.0.30), mi MAC es XX:XX:XX:XX:XX:XX"
  
Attacker → Webserver:
  "Soy la victim (172.20.0.10), mi MAC es YY:YY:YY:YY:YY:YY"
```

**Resultado:** Ambos actualizan sus tablas ARP con información falsa.

### Fase 3: Interceptación (Ataque Activo)

```
Victim (172.20.0.10)
    │
    │ HTTP POST /login
    │ username=admin&password=secret123
    │
    ▼
Attacker (172.20.0.20) ◄── INTERCEPTA Y CAPTURA
    │
    │ Reenvía el paquete (IP forwarding)
    │
    ▼
Webserver (172.20.0.30)
    │
    │ HTTP Response
    │ 302 Redirect
    │
    ▼
Attacker ◄── INTERCEPTA RESPUESTA
    │
    │ Reenvía al cliente
    │
    ▼
Victim (cree que todo es normal)
```

**El atacante puede:**
- ✅ Ver credenciales en texto plano
- ✅ Capturar cookies de sesión
- ✅ Modificar requests/responses (opcional)
- ✅ Guardar todo en archivos .pcap

### Fase 4: Protección con HTTPS

```
Victim (172.20.0.10)
    │
    │ HTTPS Request (TLS Handshake)
    │ Cifrado con clave pública del servidor
    │
    ▼
Attacker (172.20.0.20) ◄── SOLO VE TRÁFICO CIFRADO
    │                       ❌ No puede leer contenido
    │                       ❌ No puede modificar sin romper TLS
    │
    ▼
Webserver (172.20.0.30)
    │
    │ HTTPS Response (Cifrado)
    │
    ▼
Victim (conexión segura ✅)
```

---

## 🛠️ Docker Compose

### Estructura del archivo `docker-compose.yml`

```yaml
version: '3.8'

services:
  # Cliente (Víctima)
  victim:
    build: ./victim
    container_name: mitm-victim
    hostname: victim
    networks:
      mitm-lab-network:
        ipv4_address: 172.20.0.10
    depends_on:
      - webserver
    stdin_open: true
    tty: true

  # Atacante (MitM)
  attacker:
    build: ./attacker
    container_name: mitm-attacker
    hostname: attacker
    networks:
      mitm-lab-network:
        ipv4_address: 172.20.0.20
    cap_add:
      - NET_ADMIN
      - NET_RAW
    volumes:
      - ./evidencias/pcap_files:/captures
    stdin_open: true
    tty: true

  # Servidor Web
  webserver:
    build: ./webserver
    container_name: mitm-webserver
    hostname: webserver
    networks:
      mitm-lab-network:
        ipv4_address: 172.20.0.30
    ports:
      - "8080:80"    # HTTP
      - "8443:443"   # HTTPS
    environment:
      - DJANGO_SETTINGS_MODULE=webapp.settings

networks:
  mitm-lab-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
```

---

## 📦 Volúmenes Compartidos

### Capturas de Tráfico

```yaml
volumes:
  - ./evidencias/pcap_files:/captures
```

**Propósito:** Los archivos .pcap capturados por el atacante se guardan en el host para análisis posterior con Wireshark.

### Logs

```yaml
volumes:
  - ./evidencias/logs:/logs
```

**Propósito:** Logs de todos los contenedores accesibles desde el host.

---

## 🚀 Comandos de Gestión

### Levantar el Entorno

```bash
cd mitm-demo
docker compose up -d
```

### Ver Logs en Tiempo Real

```bash
# Todos los contenedores
docker compose logs -f

# Solo el atacante
docker compose logs -f attacker

# Solo el servidor web
docker compose logs -f webserver
```

### Ejecutar Comandos en Contenedores

```bash
# Entrar al contenedor atacante
docker compose exec attacker bash

# Ejecutar script de ARP spoofing
docker compose exec attacker python3 /scripts/arp_spoof.py

# Ver tabla ARP en la víctima
docker compose exec victim arp -a
```

### Detener y Limpiar

```bash
# Detener contenedores
docker compose down

# Detener y eliminar volúmenes
docker compose down -v

# Limpiar todo (imágenes, contenedores, redes)
docker system prune -a
```

---

## 🔒 Consideraciones de Seguridad

### Aislamiento

- ✅ Red Docker aislada del host
- ✅ Sin acceso a internet desde contenedores (opcional)
- ✅ Volúmenes limitados solo a directorios necesarios

### Privilegios

- ⚠️ El contenedor `attacker` requiere `NET_ADMIN` y `NET_RAW`
- ⚠️ Estos privilegios son necesarios para ARP spoofing
- ⚠️ **NUNCA** ejecutar en producción

### Limpieza

- 🗑️ Eliminar archivos .pcap después de las pruebas
- 🗑️ No commitear credenciales (aunque sean de prueba)
- 🗑️ Limpiar logs con información sensible

---

## 📊 Monitoreo y Debugging

### Ver Tráfico de Red

```bash
# Desde el atacante
docker compose exec attacker tcpdump -i eth0 -n

# Filtrar solo HTTP
docker compose exec attacker tcpdump -i eth0 -n 'tcp port 80'

# Guardar en .pcap
docker compose exec attacker tcpdump -i eth0 -w /captures/traffic.pcap
```

### Verificar Tablas ARP

```bash
# En la víctima (antes del ataque)
docker compose exec victim arp -a

# En la víctima (durante el ataque - MAC del atacante)
docker compose exec victim arp -a

# En el webserver
docker compose exec webserver arp -a
```

### Verificar Conectividad

```bash
# Ping desde víctima a servidor
docker compose exec victim ping -c 3 172.20.0.30

# Curl al servidor HTTP
docker compose exec victim curl http://172.20.0.30/

# Curl al servidor HTTPS (ignorar certificado)
docker compose exec victim curl -k https://172.20.0.30/
```

---

## 🎓 Recursos Adicionales

- [Docker Networking](https://docs.docker.com/network/)
- [Docker Compose Networking](https://docs.docker.com/compose/networking/)
- [Linux Capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- [ARP Protocol (RFC 826)](https://tools.ietf.org/html/rfc826)

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.0
