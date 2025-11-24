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

### Software Necesario

- **Sistema Operativo:** Linux (Ubuntu 20.04+, Debian, Arch, etc.)
- **Docker:** 20.10+
- **Docker Compose:** 2.0+
- **Python:** 3.10 o superior
- **Git:** Para clonar el repositorio
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

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd cryptography_project
```

### 2. Crear Entorno Virtual Python (Recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Verificar Instalación

```bash
python3 -c "import scapy, django, paramiko; print('✅ Dependencias instaladas correctamente')"
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

## 🎯 Uso Básico

### Fase 1: SSH Hardening

```bash
cd ssh-hardening

# 1. Auditar configuración actual
python3 scripts/audit_ssh.py

# 2. Aplicar configuración endurecida
sudo cp configs/sshd_config.hardened /etc/ssh/sshd_config
sudo systemctl restart sshd

# 3. Configurar autenticación con claves
bash scripts/setup_ssh_keys.sh

# 4. (Opcional) Configurar 2FA
bash scripts/setup_2fa.sh
```

### Fase 2: Demostración MitM

```bash
cd mitm-demo

# 1. Levantar entorno Docker
docker compose up -d

# 2. Ejecutar demo completa
bash ../scripts/start_demo.sh

# 3. Ver resultados en tiempo real
docker compose logs -f attacker

# 4. Detener y limpiar
docker compose down
bash ../scripts/cleanup.sh
```

---

## 📖 Documentación Detallada

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
