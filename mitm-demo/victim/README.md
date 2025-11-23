# Victim Container

## Descripción

Contenedor que simula un cliente (víctima) navegando en la web y enviando credenciales por HTTP.

## Componentes

- **Python 3.11** con requests y rich
- **curl, wget** para pruebas HTTP
- **Herramientas de red** (ping, netstat, dig)

## Scripts

### `browse_http.py`
Simula navegación y envío de credenciales por HTTP.

**Uso:**
```bash
docker compose exec victim python3 /scripts/browse_http.py
```

## Comandos Útiles

```bash
# Entrar al contenedor
docker compose exec victim bash

# Probar conectividad con webserver
docker compose exec victim ping -c 3 172.20.0.30

# Hacer request HTTP
docker compose exec victim curl http://172.20.0.30/

# Ver tabla ARP
docker compose exec victim arp -a

# Ver rutas de red
docker compose exec victim ip route
```

## IP Asignada

- **IP:** 172.20.0.10
- **Hostname:** victim
- **Red:** mitm-lab-network (172.20.0.0/16)
