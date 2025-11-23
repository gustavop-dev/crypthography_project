# ============================================
# Dockerfile - Attacker Container
# Contenedor para realizar ataque MitM
# ============================================

FROM python:3.11-slim

LABEL maintainer="Grupo 6 - UNAL Medellín"
LABEL description="Attacker container for MitM demonstration"

# Instalar herramientas de red y captura
RUN apt-get update && apt-get install -y \
    tcpdump \
    tshark \
    dsniff \
    ettercap-text-only \
    net-tools \
    iputils-ping \
    iproute2 \
    iptables \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Crear directorios
RUN mkdir -p /captures /logs /scripts

# Copiar scripts
COPY scripts/ /scripts/

# Hacer scripts ejecutables
RUN chmod +x /scripts/*.py /scripts/*.sh || true

# Habilitar IP forwarding (necesario para MitM)
RUN echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

WORKDIR /scripts

# Comando por defecto
CMD ["/bin/bash"]
