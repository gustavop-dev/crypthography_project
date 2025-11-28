# Preguntas Frecuentes (FAQ)

## Instalación y Requisitos

### ¿Necesito instalar Python en mi computadora?

**NO**, si solo vas a ejecutar la demo MitM (HTTP vs HTTPS).

**SÍ**, solo si quieres usar los scripts de SSH Hardening.

**Resumen:**

| Componente | Requiere Python en host | Explicación |
|------------|------------------------|-------------|
| Demo MitM (HTTP/HTTPS) | NO | Todo corre en Docker |
| Scripts de monitoreo | NO | Corren dentro del contenedor |
| Captura de tráfico | NO | Dentro de Docker |
| SSH Hardening | SÍ | Scripts de auditoría corren en el host |
| Desarrollo/Modificación | SÍ | Para editar código |

### ¿Qué necesito instalar entonces?

**Para ejecutar la demo MitM (lo principal):**
- Docker Desktop (macOS/Windows) o Docker Engine (Linux)
- Git (para clonar el repositorio)
- Un navegador web

**Eso es todo.** No necesitas Python, pip, ni crear entornos virtuales.

### ¿Cómo funciona sin Python en mi máquina?

Todo el código Python corre dentro de contenedores Docker:

```
Tu máquina (host)
├── Docker Desktop/Engine
│   ├── Contenedor webserver (Python 3.11 + Django)
│   ├── Contenedor attacker (Python 3.11 + Scapy)
│   └── Contenedor victim (Python 3.11)
└── Tu navegador (para acceder a la web)
```

Cuando ejecutas:
```bash
bash scripts/demo_completa_cross_platform.sh
```

El script:
1. Levanta los contenedores (que ya tienen Python instalado)
2. Ejecuta comandos dentro de los contenedores
3. Tú solo accedes con tu navegador a `localhost:8080` o `localhost:8443`

### ¿Cuándo SÍ necesito Python?

Solo si quieres ejecutar los scripts de **SSH Hardening**:

```bash
# Estos scripts corren en tu máquina (no en Docker)
python3 scripts/audit_ssh.py
python3 scripts/test_ssh_security.py
```

Para esto necesitas:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Pero **esto es completamente opcional**. La demo principal funciona sin esto.

---

## Ejecución

### ¿Cómo ejecuto la demo?

**Opción 1: Demo automatizada (recomendado)**

```bash
git clone https://github.com/gustavop-dev/crypthography_project.git
cd cryptography_project
bash scripts/demo_completa_cross_platform.sh
```

Sigue las instrucciones en pantalla.

**Opción 2: Manual**

```bash
cd mitm-demo
docker compose up -d

# Abre tu navegador en:
# HTTP: http://localhost:8080
# HTTPS: https://localhost:8443

# Login: admin / password123
```

### ¿Funciona en Windows?

**Sí**, pero necesitas:
- Docker Desktop para Windows
- WSL 2 habilitado
- Git Bash o WSL 2 para ejecutar scripts `.sh`

Ver: [Guía de instalación para Windows](INSTALACION_MULTIPLATAFORMA.md#-windows)

### ¿Funciona en macOS?

**Sí**, perfectamente con Docker Desktop.

**Importante:** En macOS NO uses `sudo` con Docker.

Ver: [Guía de instalación para macOS](INSTALACION_MULTIPLATAFORMA.md#-macos)

### ¿Funciona en Linux?

**Sí**, es la plataforma nativa.

Puede requerir `sudo` si tu usuario no está en el grupo `docker`.

Ver: [Guía de instalación para Linux](INSTALACION_MULTIPLATAFORMA.md#-linux-ubuntu-debian-fedora-arch-etc)

---

## Docker

### ¿Por qué usar Docker?

**Ventajas:**
- Aislamiento completo (no afecta tu sistema)
- Reproducible en cualquier plataforma
- No necesitas instalar dependencias manualmente
- Fácil de limpiar (solo borrar contenedores)
- Seguro para pruebas de seguridad

### ¿Necesito conocimientos de Docker?

**No**. Los scripts automatizan todo.

Solo necesitas tener Docker instalado y corriendo.

### ¿Cómo verifico que Docker está funcionando?

```bash
docker --version
docker compose version
docker ps
```

Si estos comandos funcionan, estás listo.

### ¿Cuánto espacio ocupa?

Aproximadamente:
- Imágenes Docker: ~500 MB
- Contenedores corriendo: ~200 MB RAM
- Logs y capturas: ~50 MB

Total: ~750 MB

### ¿Cómo limpio todo después?

```bash
cd mitm-demo
docker compose down -v
docker system prune -a
```

Esto elimina contenedores, imágenes y volúmenes.

---

## Problemas Comunes

### "Cannot connect to Docker daemon"

**Causa:** Docker no está corriendo.

**Solución:**
- **Linux:** `sudo systemctl start docker`
- **macOS/Windows:** Abre Docker Desktop y espera a que inicie

### "Permission denied" en Linux

**Causa:** Tu usuario no está en el grupo docker.

**Solución:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### "Port 8080 already in use"

**Causa:** Otro servicio está usando el puerto.

**Solución:**
```bash
# Ver qué está usando el puerto
sudo lsof -i :8080

# Detener el servicio o cambiar el puerto en docker-compose.yml
```

### El navegador dice "Conexión rechazada"

**Causa:** El contenedor no está corriendo.

**Solución:**
```bash
cd mitm-demo
docker compose ps  # Ver estado
docker compose logs webserver  # Ver errores
docker compose restart webserver
```

### "Certificate error" en HTTPS

**Esto es normal.** El certificado es autofirmado para la demo.

**Solución:** Haz clic en "Avanzado" → "Continuar de todos modos"

### Los scripts .sh no funcionan en Windows

**Causa:** Windows no ejecuta scripts bash nativamente.

**Solución:** Usa Git Bash o WSL 2:
- **Git Bash:** Descarga de https://git-scm.com/download/win
- **WSL 2:** `wsl --install` en PowerShell como Admin

---

## Seguridad

### ¿Es seguro ejecutar esto en mi computadora?

**Sí**, porque:
- Todo corre en contenedores aislados
- No modifica tu sistema
- No instala nada permanente
- Red Docker aislada (172.20.0.0/16)
- No afecta tu red real

### ¿Puedo usar esto en producción?

**NO.** Este proyecto es **exclusivamente educativo**.

La aplicación web tiene vulnerabilidades intencionales para demostración.

### ¿Es legal usar estas técnicas?

**Sí**, en un entorno controlado y con consentimiento.

**NO** uses estas técnicas en:
- Redes que no te pertenecen
- Sin autorización explícita
- Con fines maliciosos

Ver: [Advertencia de uso ético](../README.md#advertencia---uso-ético-y-legal)

---

## Educativo

### ¿Qué aprendo con este proyecto?

- Cómo funciona un ataque Man-in-the-Middle
- Por qué HTTP es inseguro
- Cómo HTTPS protege las comunicaciones
- Importancia del cifrado
- Buenas prácticas de seguridad
- Configuración de SSH seguro

### ¿Puedo modificar el código?

**Sí**, es código abierto para fines educativos.

Para desarrollar:
```bash
# Instalar dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Editar código
# Reconstruir contenedores
cd mitm-demo
docker compose build
docker compose up -d
```

### ¿Dónde está el código de la aplicación web?

```
mitm-demo/webserver/http_vulnerable/
├── manage.py
├── login_app/
│   ├── views.py
│   ├── urls.py
│   └── templates/
└── webapp/
    └── settings.py
```

### ¿Cómo funciona la captura de tráfico?

Ver: [Arquitectura del Sistema](ARQUITECTURA.md)

---

## Contribución

### ¿Puedo contribuir al proyecto?

Este es un proyecto académico de la Universidad Nacional de Colombia.

Si encuentras errores o mejoras, puedes:
- Reportar issues en GitHub
- Sugerir mejoras
- Hacer fork para tus propios experimentos

### ¿Puedo usar esto para mi clase?

**Sí**, siempre que:
- Sea con fines educativos
- Se cite la fuente
- Se respete la licencia académica
- Se enfatice el uso ético

---

## Contacto

**Grupo 6 - Criptografía y Seguridad**
Universidad Nacional de Colombia - Sede Medellín

Ver: [README principal](../README.md) para más información.
