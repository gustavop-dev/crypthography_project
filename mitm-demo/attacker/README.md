# Attacker Container

## Descripción

Contenedor que realiza el ataque Man-in-the-Middle mediante ARP spoofing y captura de tráfico.

## Componentes

- **Python 3.11** con Scapy, PyShark
- **tcpdump, tshark** para captura de paquetes
- **dsniff, arpspoof, ettercap** para ARP spoofing
- **Capacidades NET_ADMIN y NET_RAW** para manipulación de red

## Scripts

### `arp_spoof.py`
Realiza ARP spoofing para posicionarse como MitM.

**Uso:**
```bash
docker compose exec attacker python3 /scripts/arp_spoof.py \
    --victim 172.20.0.10 \
    --gateway 172.20.0.1 \
    --interface eth0
```

### `capture_traffic.py`
Captura tráfico de red y guarda en formato PCAP.

**Uso:**
```bash
# Capturar todo el tráfico
docker compose exec attacker python3 /scripts/capture_traffic.py

# Capturar solo HTTP
docker compose exec attacker python3 /scripts/capture_traffic.py -f "tcp port 80"

# Capturar N paquetes
docker compose exec attacker python3 /scripts/capture_traffic.py -c 100
```

### `intercept_http.py`
Intercepta y muestra tráfico HTTP en tiempo real, extrayendo credenciales.

**Uso:**
```bash
docker compose exec attacker python3 /scripts/intercept_http.py
```

## Comandos Útiles

```bash
# Entrar al contenedor
docker compose exec attacker bash

# Ver tabla ARP
docker compose exec attacker arp -a

# Capturar con tcpdump
docker compose exec attacker tcpdump -i eth0 -w /captures/traffic.pcap

# Ver capturas guardadas
docker compose exec attacker ls -lh /captures/

# Ver credenciales interceptadas
docker compose exec attacker cat /logs/intercepted_credentials.txt
```

## IP Asignada

- **IP:** 172.20.0.20
- **Hostname:** attacker
- **Red:** mitm-lab-network (172.20.0.0/16)

## Capacidades Especiales

- `NET_ADMIN`: Permite manipular tablas ARP
- `NET_RAW`: Permite captura de paquetes raw
