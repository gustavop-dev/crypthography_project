# ============================================
# Dockerfile - Victim Container
# Cliente que navega y envía credenciales
# ============================================

FROM python:3.11-slim

LABEL maintainer="Grupo 6 - UNAL Medellín"
LABEL description="Victim container for MitM demonstration"

# Instalar herramientas necesarias
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    iputils-ping \
    net-tools \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
RUN pip install --no-cache-dir \
    requests \
    rich

# Crear directorio de trabajo
WORKDIR /scripts

# Copiar scripts
COPY scripts/ /scripts/

# Hacer scripts ejecutables
RUN chmod +x /scripts/*.py || true

# Comando por defecto: shell interactivo
CMD ["/bin/bash"]
