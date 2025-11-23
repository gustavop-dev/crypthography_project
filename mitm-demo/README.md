# MitM Demo Environment

## 📋 Descripción

Entorno Docker completo para demostración de ataque Man-in-the-Middle sobre tráfico HTTP.

## 🏗️ Arquitectura

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   VICTIM     │    │   ATTACKER   │    │  WEBSERVER   │
│ 172.20.0.10  │◄──►│ 172.20.0.20  │◄──►│ 172.20.0.30  │
│              │    │              │    │              │
│  Cliente     │    │  MitM        │    │  Django      │
│  HTTP        │    │  ARP Spoof   │    │  HTTP:80     │
└──────────────┘    └──────────────┘    └──────────────┘
```

## 🚀 Inicio Rápido

### 1. Levantar el Entorno

```bash
cd mitm-demo
docker compose up -d
```

### 2. Verificar que los Contenedores Están Corriendo

```bash
docker compose ps
```

### 3. Acceder al Servidor Web

Desde tu navegador: http://localhost:8080

O desde el contenedor victim:
```bash
docker compose exec victim python3 /scripts/browse_http.py
```

## 🎯 Demostración del Ataque

### Paso 1: Iniciar ARP Spoofing

```bash
docker compose exec attacker python3 /scripts/arp_spoof.py \
    --victim 172.20.0.10 \
    --gateway 172.20.0.1 \
    --interface eth0
```

### Paso 2: Iniciar Interceptación HTTP

En otra terminal:
```bash
docker compose exec attacker python3 /scripts/intercept_http.py
```

### Paso 3: Víctima Navega y Envía Credenciales

En otra terminal:
```bash
docker compose exec victim python3 /scripts/browse_http.py
```

### Paso 4: Ver Credenciales Interceptadas

```bash
docker compose exec attacker cat /logs/intercepted_credentials.txt
```

## 📊 Componentes

### Victim (172.20.0.10)
- Cliente que navega por HTTP
- Envía credenciales sin cifrar
- Script: `browse_http.py`

### Attacker (172.20.0.20)
- Realiza ARP spoofing
- Captura tráfico de red
- Intercepta credenciales HTTP
- Scripts:
  - `arp_spoof.py` - ARP spoofing
  - `capture_traffic.py` - Captura de tráfico
  - `intercept_http.py` - Interceptación HTTP

### Webserver (172.20.0.30)
- Aplicación Django con login
- Corre sobre HTTP (puerto 80)
- Credenciales demo:
  - Usuario: `admin`
  - Contraseña: `password123`

## 🛠️ Comandos Útiles

### Ver Logs

```bash
# Todos los contenedores
docker compose logs -f

# Solo attacker
docker compose logs -f attacker

# Solo webserver
docker compose logs -f webserver
```

### Ejecutar Comandos en Contenedores

```bash
# Entrar a un contenedor
docker compose exec victim bash
docker compose exec attacker bash
docker compose exec webserver bash

# Ver tabla ARP
docker compose exec victim arp -a

# Ping entre contenedores
docker compose exec victim ping -c 3 172.20.0.30
```

### Capturar Tráfico

```bash
# Capturar todo el tráfico
docker compose exec attacker python3 /scripts/capture_traffic.py

# Capturar solo HTTP
docker compose exec attacker python3 /scripts/capture_traffic.py -f "tcp port 80"

# Capturar N paquetes
docker compose exec attacker python3 /scripts/capture_traffic.py -c 100
```

### Ver Capturas

```bash
# Listar capturas
docker compose exec attacker ls -lh /captures/

# Analizar con tshark
docker compose exec attacker tshark -r /captures/traffic_*.pcap

# Copiar al host
docker cp mitm-attacker:/captures/traffic.pcap ./evidencias/pcap_files/
```

## 🧹 Limpieza

```bash
# Detener contenedores
docker compose down

# Detener y eliminar volúmenes
docker compose down -v

# Limpiar todo (imágenes, contenedores, redes)
docker system prune -a
```

## ⚠️ Advertencias

1. **Uso Educativo Únicamente**: Este entorno es solo para aprendizaje
2. **Red Aislada**: Todo ocurre en una red Docker aislada
3. **No Usar en Producción**: Configuraciones intencionalmente inseguras
4. **Credenciales de Demo**: No usar credenciales reales

## 📚 Documentación Adicional

- [Arquitectura Docker](../docs/ARQUITECTURA_DOCKER.md)
- [Victim Container](victim/README.md)
- [Attacker Container](attacker/README.md)

## 🎓 Objetivos de Aprendizaje

1. Entender cómo funciona ARP spoofing
2. Ver el peligro de HTTP sin cifrado
3. Aprender a capturar y analizar tráfico de red
4. Comprender la importancia de HTTPS
5. Conocer contramedidas contra MitM

---

**Universidad Nacional de Colombia - Sede Medellín**  
**Criptografía y Seguridad - Grupo 6**
