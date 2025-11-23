# ============================================
# Dockerfile - Webserver Container
# Servidor Django con formulario de login
# ============================================

FROM python:3.11-slim

LABEL maintainer="Grupo 6 - UNAL Medellín"
LABEL description="Django webserver for MitM demonstration"

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de aplicación
WORKDIR /app

# Copiar requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY http_vulnerable/ /app/

# Crear directorios necesarios
RUN mkdir -p /app/logs /app/staticfiles

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput || true

# Crear base de datos y migraciones
RUN python manage.py migrate --noinput || true

# Crear superusuario (para demo)
RUN python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'password123')" || true

# Exponer puertos
EXPOSE 80 443

# Comando de inicio
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
