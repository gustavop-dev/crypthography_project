# Proyecto de Criptografía y Seguridad
## Seguridad en SSH y Demostración Controlada de Ataque Man-in-the-Middle

[![Universidad](https://img.shields.io/badge/Universidad-Nacional%20de%20Colombia-green)](https://unal.edu.co)
[![Sede](https://img.shields.io/badge/Sede-Medellín-blue)](https://medellin.unal.edu.co)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-Academic%20Use%20Only-red.svg)](#)

---

## 📚 Descripción del Proyecto

Este proyecto académico tiene como objetivo:

1. **Analizar y endurecer la seguridad del protocolo SSH (Secure Shell)**
   - Estudio de la arquitectura SSH (RFC 4251/4253)
   - Implementación de configuraciones seguras (hardening)
   - Autenticación con claves públicas y 2FA

2. **Demostrar de forma controlada un ataque Man-in-the-Middle (MitM)**
   - Simulación sobre tráfico HTTP sin cifrado
   - Captura e interceptación de credenciales
   - Evidenciar la importancia del cifrado (HTTPS/TLS)

3. **Proponer contramedidas prácticas**
   - Configuración de HTTPS con HSTS
   - Buenas prácticas de seguridad en redes
   - Checklist de defensa

---

## 👥 Integrantes - Grupo 6

- **José Daniel Moreno Ceballos**
- **David Duque Diaz**
- **Gustavo Adolfo Pérez Pérez**

**Profesor:** John Bayron Baena Giraldo  
**Curso:** Criptografía y Seguridad  
**Departamento de Matemáticas**  
**Universidad Nacional de Colombia - Sede Medellín**

---

## ⚠️ ADVERTENCIA - USO ÉTICO Y LEGAL

```
🚨 IMPORTANTE: Este proyecto es EXCLUSIVAMENTE para fines educativos 🚨

✅ PERMITIDO:
- Ejecutar en entornos de laboratorio controlados (Docker)
- Usar con fines académicos y de aprendizaje
- Compartir conocimiento de forma responsable

❌ PROHIBIDO:
- Atacar sistemas de terceros sin autorización
- Ejecutar en redes de producción
- Usar fuera del contexto educativo

El uso indebido de estas herramientas puede constituir un DELITO.
Todos los participantes han dado su consentimiento para las pruebas.
```

---

## 🛠️ Requisitos del Sistema

### Sistemas Operativos Soportados

✅ **Linux** (Ubuntu 20.04+, Debian, Fedora, Arch, etc.)  
✅ **macOS** (10.15 Catalina o superior, Intel y Apple Silicon)  
✅ **Windows** (10/11 con WSL 2 y Docker Desktop)

### Software Necesario

- **Docker:** 20.10+ ([Guía de instalación multiplataforma](docs/INSTALACION_MULTIPLATAFORMA.md))
- **Docker Compose:** 2.0+ (incluido en Docker Desktop)
- **Git:** Para clonar el repositorio
- **Python:** 3.10+ (opcional, solo para desarrollo)
- **Wireshark:** (Opcional) Para análisis manual de capturas

### Verificar Requisitos

```bash
# Verificar Docker
docker --version
docker compose version

# Verificar Python
python3 --version

# Verificar permisos de Docker (no debería requerir sudo)
docker ps
```

---

## 🚀 Instalación Rápida

### 1. Instalar Docker

**Elige tu sistema operativo:**

- 🐧 **Linux:** [Guía de instalación](docs/INSTALACION_MULTIPLATAFORMA.md#-linux-ubuntu-debian-fedora-arch-etc)
- 🍎 **macOS:** [Descargar Docker Desktop](https://docs.docker.com/desktop/install/mac-install/)
- 🪟 **Windows:** [Descargar Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) + WSL 2

📖 **[Guía completa de instalación multiplataforma](docs/INSTALACION_MULTIPLATAFORMA.md)**

### 2. Clonar el Repositorio

```bash
git clone https://github.com/gustavop-dev/crypthography_project.git
cd cryptography_project
```

### 3. Verificar Docker

```bash
# Verificar que Docker está instalado y corriendo
docker --version
docker compose version
docker ps
```

### 4. ¡Ejecutar Demo!

```bash
# Demo completa automatizada (funciona en Linux, macOS y Windows)
bash scripts/demo_completa_cross_platform.sh
```

**Notas importantes:**
- ✅ **Linux:** Puede requerir `sudo` (el script lo detecta automáticamente)
- ✅ **macOS:** NO uses `sudo`, Docker Desktop ya tiene permisos
- ✅ **Windows:** Usa Git Bash o WSL 2, NO uses `sudo`
- ✅ No necesitas instalar Python, todo corre en Docker

---

### Instalación Avanzada (Opcional)

Solo si quieres desarrollar o modificar el código:

```bash
# Crear entorno virtual Python
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Verificar
python3 -c "import scapy, django, paramiko; print('✅ OK')"
```

---

## 📂 Estructura del Proyecto

```
cryptography_project/
├── PLAN_PROYECTO.md           # Plan detallado de implementación
├── README.md                  # Este archivo
├── requirements.txt           # Dependencias Python
│
├── docs/                      # 📚 Documentación
│   ├── informe_tecnico/      # Informe en LaTeX
│   ├── guias/                # Guías paso a paso
│   └── diagramas/            # Diagramas de red
│
├── ssh-hardening/             # 🔐 Configuración y hardening de SSH
│   ├── configs/              # Archivos de configuración
│   ├── scripts/              # Scripts de auditoría y setup
│   └── resultados/           # Resultados de auditorías
│
├── mitm-demo/                 # 🎭 Demostración de ataque MitM
│   ├── docker-compose.yml    # Orquestación de contenedores
│   ├── victim/               # Contenedor cliente (víctima)
│   ├── attacker/             # Contenedor atacante
│   ├── webserver/            # Servidor web Django (HTTP/HTTPS)
│   └── network/              # Configuración de red
│
├── evidencias/                # 📸 Capturas y logs
│   ├── screenshots/          # Capturas de pantalla
│   ├── pcap_files/           # Archivos de captura de tráfico
│   └── logs/                 # Logs de las pruebas
│
└── scripts/                   # 🛠️ Scripts auxiliares
    ├── setup_environment.sh
    ├── start_demo.sh
    └── cleanup.sh
```

---

## 🎯 Inicio Rápido

### ⚡ Demo Automatizada (Recomendado)

**Un solo comando para ejecutar la demostración completa:**

```bash
# Desde la raíz del proyecto
bash scripts/demo_completa.sh
```

Este script ejecuta automáticamente:
- ✅ Limpia el entorno
- ✅ Levanta contenedores Docker
- ✅ **PARTE 1:** Demo HTTP (credenciales interceptadas)
- ✅ **PARTE 2:** Demo HTTPS (tráfico cifrado)
- ✅ Comparación lado a lado
- ✅ Limpieza al finalizar

**Duración:** ~5 minutos (interactivo)

---

### 📋 Uso Manual Paso a Paso

#### Opción 1: Solo HTTP (Vulnerable)

```bash
cd mitm-demo

# 1. Levantar entorno
sudo docker compose up -d

# 2. Abrir navegador en http://localhost:8080
# 3. Hacer login con: admin / password123

# 4. Ver credenciales interceptadas
sudo docker compose exec webserver python /app/monitor_traffic.py

# 5. Limpiar
sudo docker compose down
```

#### Opción 2: Solo HTTPS (Seguro)

```bash
cd mitm-demo

# 1. Levantar entorno
sudo docker compose up -d

# 2. Generar certificado SSL
sudo docker compose exec webserver bash /app/generate_cert.sh

# 3. Iniciar servidor HTTPS
sudo docker compose exec webserver bash /app/start_https.sh

# 4. Abrir navegador en https://localhost:8443
# 5. Aceptar certificado autofirmado
# 6. Hacer login

# 7. Ver tráfico cifrado
sudo docker compose exec webserver python /app/monitor_traffic.py

# 8. Limpiar
sudo docker compose down
```

---

### 🔐 SSH Hardening (Opcional)

```bash
cd ssh-hardening

# 1. Auditar configuración actual
python3 scripts/audit_ssh.py

# 2. Aplicar configuración endurecida
sudo cp configs/sshd_config.hardened /etc/ssh/sshd_config
sudo systemctl restart sshd

# 3. Configurar autenticación con claves
bash scripts/setup_ssh_keys.sh
```

---

## 📖 Documentación Detallada

- **[Instalación Multiplataforma](docs/INSTALACION_MULTIPLATAFORMA.md)**: Linux, macOS y Windows
- **[Arquitectura del Sistema](docs/ARQUITECTURA.md)**: Topología de red y componentes
- **[Guía de Uso Completa](docs/GUIA_USO.md)**: Paso a paso para ejecutar la demo
- **[Resultados y Análisis](docs/RESULTADOS.md)**: Evidencias y comparativas HTTP vs HTTPS
- **[Checklist de Seguridad](docs/CHECKLIST_SEGURIDAD.md)**: Lista de verificación
- **[Plan de Proyecto](PLAN_PROYECTO.md)**: Fases detalladas de implementación

---

## 🔬 Componentes Técnicos

### SSH Hardening
- Deshabilitación de autenticación por contraseña
- Restricción de login de root
- Algoritmos de cifrado modernos (ChaCha20-Poly1305, AES-GCM)
- Autenticación de dos factores (2FA)
- Listas de control de acceso

### Ataque MitM
- **ARP Spoofing**: Envenenamiento de caché ARP
- **Captura de tráfico**: tcpdump/Scapy
- **Interceptación HTTP**: Extracción de credenciales
- **Análisis**: Wireshark y scripts Python

### Contramedidas
- **HTTPS/TLS**: Cifrado de extremo a extremo
- **HSTS**: HTTP Strict Transport Security
- **Certificate Pinning**: Validación de certificados
- **SSH known_hosts**: Prevención de MitM en SSH

---

## 🧪 Tecnologías Utilizadas

| Categoría | Tecnología |
|-----------|------------|
| **Infraestructura** | Docker, Docker Compose |
| **Lenguaje** | Python 3.10+ |
| **Framework Web** | Django 4.x |
| **Redes** | Scapy, tcpdump, Wireshark |
| **SSH** | OpenSSH 8.x, Google Authenticator PAM |
| **Documentación** | LaTeX, Markdown |

---

## 📊 Resultados Esperados

Al finalizar el proyecto, se obtendrá:

✅ Configuración de SSH endurecida y auditada  
✅ Demostración funcional de ataque MitM sobre HTTP  
✅ Evidencias de protección mediante HTTPS  
✅ Informe técnico completo  
✅ Guías reproducibles para replicar el laboratorio  
✅ Checklist de seguridad aplicable en producción  

---

## 🐛 Troubleshooting

### Docker no inicia contenedores
```bash
# Verificar que Docker está corriendo
sudo systemctl status docker

# Reiniciar Docker
sudo systemctl restart docker
```

### Permisos insuficientes para captura de red
```bash
# Añadir usuario al grupo docker
sudo usermod -aG docker $USER

# Cerrar sesión y volver a entrar
```

### Python no encuentra módulos
```bash
# Asegurarse de estar en el entorno virtual
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

---

## 📚 Referencias

- [RFC 4251 - SSH Protocol Architecture](https://tools.ietf.org/html/rfc4251)
- [RFC 4253 - SSH Transport Layer Protocol](https://tools.ietf.org/html/rfc4253)
- [RFC 6797 - HTTP Strict Transport Security](https://tools.ietf.org/html/rfc6797)
- [OWASP - Man-in-the-Middle Attacks](https://owasp.org/www-community/attacks/Manipulator-in-the-middle_attack)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)

---

## 📝 Licencia

Este proyecto es de **uso académico exclusivamente**. No se permite su uso comercial ni su aplicación en entornos de producción sin las debidas autorizaciones.

---

## 📧 Contacto

Para preguntas sobre este proyecto:
- **Curso:** Criptografía y Seguridad
- **Profesor:** John Bayron Baena Giraldo
- **Universidad Nacional de Colombia - Sede Medellín**

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.0  
**Estado:** 🚧 En Desarrollo
