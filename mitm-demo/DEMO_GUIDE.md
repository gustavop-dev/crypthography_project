# Guía de Ejecución - Demostración MitM

## 🚀 Inicio Rápido

### Demo Automatizada (Recomendado)

```bash
cd /home/cerrotico/unal/cryptography_project
bash scripts/start_demo.sh
# Seleccionar opción 1
```

### Demo Manual (Paso a Paso)

**Terminal 1 - ARP Spoofing:**
```bash
cd mitm-demo
docker compose up -d
docker compose exec attacker python3 /scripts/arp_spoof.py \
    --victim 172.20.0.10 --gateway 172.20.0.1
```

**Terminal 2 - Interceptación HTTP:**
```bash
docker compose exec attacker python3 /scripts/intercept_http.py
```

**Terminal 3 - Víctima:**
```bash
docker compose exec victim python3 /scripts/browse_http.py
```

**Ver Resultados:**
```bash
docker compose exec attacker cat /logs/intercepted_credentials.txt
```

## 📊 Análisis de Capturas

```bash
# Capturar tráfico
docker compose exec attacker python3 /scripts/capture_traffic.py -f "tcp port 80"

# Analizar PCAP
docker compose exec attacker python3 /scripts/analyze_pcap.py /captures/traffic.pcap
```

## 🌐 Acceso Web

- HTTP: http://localhost:8080
- Credenciales: admin / password123

## 🧹 Limpieza

```bash
docker compose down
```

---

**Universidad Nacional de Colombia - Sede Medellín**
