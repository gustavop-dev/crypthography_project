# Plan de Implementación - Proyecto de Criptografía
## Seguridad en SSH y Ataque Man-in-the-Middle sobre HTTP

**Universidad Nacional de Colombia - Sede Medellín** 
**Grupo 6** 
**Fecha:** Noviembre 2025

---

## Índice
1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Fases de Implementación](#fases-de-implementación)
3. [Tecnologías Seleccionadas](#tecnologías-seleccionadas)
4. [Cronograma Estimado](#cronograma-estimado)

---

## Estructura del Proyecto

```
cryptography_project/

 README.md # Documentación principal del proyecto
 PLAN_PROYECTO.md # Este archivo - Plan de trabajo

 docs/ # Documentación técnica
 informe_tecnico/ # Informe final en LaTeX
 main.tex
 sections/
 01_introduccion.tex
 02_marco_teorico.tex
 03_ssh_analisis.tex
 04_ssh_hardening.tex
 05_mitm_simulacion.tex
 06_contramedidas.tex
 07_conclusiones.tex
 images/ # Diagramas y capturas
 referencias.bib

 guias/ # Guías paso a paso
 01_guia_ssh_hardening.md
 02_guia_mitm_demo.md
 03_checklist_seguridad.md

 diagramas/ # Diagramas de red y arquitectura
 topologia_red.png
 flujo_ataque_mitm.png

 ssh-hardening/ # Fase SSH
 README.md # Documentación de esta fase

 configs/ # Configuraciones OpenSSH
 sshd_config.weak # Configuración débil (baseline)
 sshd_config.hardened # Configuración endurecida
 ssh_config.client # Configuración cliente segura
 README.md # Explicación de cada parámetro

 scripts/ # Scripts de auditoría y setup
 audit_ssh.py # Auditoría de configuración SSH
 setup_ssh_keys.sh # Generación y distribución de claves
 setup_2fa.sh # Configuración 2FA con Google Authenticator
 test_ssh_security.py # Tests de seguridad automatizados
 README.md

 resultados/ # Resultados de auditorías
 audit_before.txt
 audit_after.txt

 mitm-demo/ # Fase MitM
 README.md # Documentación de la demo
 docker-compose.yml # Orquestación de contenedores

 victim/ # Contenedor Cliente (Víctima)
 Dockerfile
 scripts/
 browse_http.py # Simula navegación HTTP
 send_credentials.py # Envía credenciales al servidor
 README.md

 attacker/ # Contenedor Atacante (MitM)
 Dockerfile
 scripts/
 arp_spoof.py # ARP Spoofing
 capture_traffic.py # Captura de tráfico
 intercept_http.py # Intercepta y muestra HTTP
 analyze_pcap.py # Analiza archivos .pcap
 requirements.txt
 README.md

 webserver/ # Servidor Web Demo
 Dockerfile

 http_vulnerable/ # Versión HTTP (vulnerable)
 manage.py
 requirements.txt
 webapp/
 __init__.py
 settings.py
 urls.py
 wsgi.py
 login_app/ # App Django con login
 models.py
 views.py
 forms.py
 urls.py
 templates/
 login.html
 dashboard.html
 base.html

 https_secure/ # Versión HTTPS (segura)
 [misma estructura]
 ssl/ # Certificados SSL/TLS
 generate_certs.sh
 server.crt
 server.key
 settings.py # Con HSTS habilitado

 README.md

 network/ # Configuración de red
 network_setup.sh # Script de configuración de red

 evidencias/ # Evidencias y resultados
 screenshots/ # Capturas de pantalla
 01_ssh_weak_config.png
 02_ssh_hardened_config.png
 03_mitm_arp_spoofing.png
 04_wireshark_http_capture.png
 05_credentials_intercepted.png
 06_https_protection.png

 pcap_files/ # Archivos de captura de tráfico
 http_vulnerable.pcap
 https_secure.pcap
 README.md # Cómo analizar los .pcap

 logs/ # Logs de las pruebas
 ssh_audit_logs.txt
 mitm_attack_log.txt
 server_access_logs.txt

 scripts/ # Scripts auxiliares globales
 setup_environment.sh # Configuración inicial del entorno
 start_demo.sh # Inicia toda la demo MitM
 stop_demo.sh # Detiene y limpia contenedores
 cleanup.sh # Limpieza completa
 generate_report.py # Genera reporte automático

 requirements.txt # Dependencias Python globales
```

---

## Fases de Implementación

### **FASE 1: Configuración del Entorno Base**
**Objetivo:** Preparar el entorno de desarrollo y documentación inicial

#### Paso 1.1: Estructura de Directorios
- [ ] Crear toda la estructura de carpetas del proyecto
- [ ] Inicializar repositorio Git
- [ ] Crear `.gitignore` apropiado (excluir .pcap, logs sensibles, etc.)
- [ ] Crear README.md principal con descripción del proyecto

#### Paso 1.2: Configuración de Docker
- [ ] Instalar Docker y Docker Compose (si no están instalados)
- [ ] Verificar que Docker funciona correctamente
- [ ] Crear red virtual aislada para el laboratorio
- [ ] Documentar arquitectura de contenedores

#### Paso 1.3: Dependencias Python
- [ ] Crear `requirements.txt` global con dependencias:
 - scapy (para ARP spoofing)
 - django (servidor web)
 - cryptography (análisis SSL/TLS)
 - paramiko (cliente SSH en Python)
 - pyshark o scapy (análisis de .pcap)
- [ ] Crear entorno virtual Python (opcional pero recomendado)

**Entregables Fase 1:**
- Estructura de directorios completa
- Repositorio Git inicializado
- Docker configurado y funcionando
- Documentación base (README.md)

---

### **FASE 2: Estudio y Análisis de SSH**
**Objetivo:** Comprender la arquitectura de SSH y sus mecanismos de seguridad

#### Paso 2.1: Investigación Teórica
- [ ] Estudiar RFC 4251 (Arquitectura SSH)
- [ ] Estudiar RFC 4253 (Protocolo de Transporte SSH)
- [ ] Documentar modelo TOFU (Trust On First Use)
- [ ] Documentar mecanismos de autenticación (password, public key, 2FA)
- [ ] Crear sección en informe LaTeX: Marco Teórico SSH

#### Paso 2.2: Análisis de Configuración Débil
- [ ] Crear `sshd_config.weak` con configuración insegura:
 - PermitRootLogin yes
 - PasswordAuthentication yes
 - Algoritmos de cifrado débiles (3des, arcfour)
 - Sin restricciones de usuarios/IPs
- [ ] Documentar cada parámetro inseguro y sus riesgos
- [ ] Crear script `audit_ssh.py` para analizar configuración

#### Paso 2.3: Pruebas con Configuración Débil
- [ ] Levantar servidor SSH con configuración débil
- [ ] Ejecutar auditoría con `ssh-audit` (herramienta externa)
- [ ] Ejecutar script propio `audit_ssh.py`
- [ ] Capturar evidencias (screenshots, logs)
- [ ] Guardar resultados en `resultados/audit_before.txt`

**Entregables Fase 2:**
- Sección de Marco Teórico en LaTeX
- Configuración SSH débil documentada
- Script de auditoría funcional
- Evidencias de vulnerabilidades

---

### **FASE 3: Hardening de OpenSSH**
**Objetivo:** Implementar y documentar configuración segura de SSH

#### Paso 3.1: Configuración Endurecida
- [ ] Crear `sshd_config.hardened` con mejores prácticas:
 - PermitRootLogin no
 - PasswordAuthentication no (solo claves públicas)
 - Algoritmos modernos (chacha20-poly1305, aes256-gcm)
 - AllowUsers/AllowGroups (lista blanca)
 - ClientAliveInterval y ClientAliveCountMax
 - MaxAuthTries reducido
 - Protocol 2 (explícito)
- [ ] Documentar cada parámetro y su justificación

#### Paso 3.2: Autenticación con Claves Públicas
- [ ] Crear script `setup_ssh_keys.sh`:
 - Genera par de claves ED25519 (más seguro que RSA)
 - Configura `authorized_keys`
 - Establece permisos correctos (600, 700)
- [ ] Documentar proceso paso a paso
- [ ] Probar autenticación sin contraseña

#### Paso 3.3: Implementación de 2FA
- [ ] Crear script `setup_2fa.sh`:
 - Instala Google Authenticator PAM
 - Configura `/etc/pam.d/sshd`
 - Configura `sshd_config` para usar PAM
- [ ] Documentar configuración de 2FA
- [ ] Probar autenticación con 2FA (clave + OTP)

#### Paso 3.4: Tests de Seguridad
- [ ] Crear `test_ssh_security.py`:
 - Intenta login con root (debe fallar)
 - Intenta login con contraseña (debe fallar)
 - Intenta algoritmos débiles (debe rechazar)
 - Verifica timeout de sesión
- [ ] Ejecutar auditoría post-hardening
- [ ] Guardar resultados en `resultados/audit_after.txt`

#### Paso 3.5: Documentación
- [ ] Crear `guias/01_guia_ssh_hardening.md` con pasos reproducibles
- [ ] Crear tabla comparativa: antes vs después
- [ ] Documentar en informe LaTeX (sección SSH Hardening)
- [ ] Capturar evidencias (screenshots, logs)

**Entregables Fase 3:**
- Configuración SSH endurecida
- Scripts de setup automatizados
- Guía de hardening reproducible
- Tests de seguridad automatizados
- Sección completa en informe LaTeX
- Evidencias comparativas

---

### **FASE 4: Diseño del Entorno MitM**
**Objetivo:** Crear infraestructura Docker para simulación de ataque

#### Paso 4.1: Arquitectura de Red
- [ ] Diseñar topología de red:
 ```
 [Víctima] <---> [Atacante MitM] <---> [Servidor Web]
 | |
 +---------- Red Local (172.20.0.0/16) +
```
- [ ] Crear diagrama de red (para documentación)
- [ ] Documentar flujo de ataque paso a paso

#### Paso 4.2: Contenedor Servidor Web (Django)
- [ ] Crear Dockerfile para servidor Django
- [ ] Crear proyecto Django con app de login:
 - Formulario de login (usuario/contraseña)
 - Dashboard simple post-login
 - Templates con Bootstrap (UI moderna)
- [ ] Configurar para HTTP (puerto 80) - versión vulnerable
- [ ] Configurar para HTTPS (puerto 443) - versión segura
- [ ] Crear script `generate_certs.sh` para certificados autofirmados
- [ ] Configurar HSTS en versión HTTPS

#### Paso 4.3: Contenedor Víctima
- [ ] Crear Dockerfile para cliente
- [ ] Crear `browse_http.py`:
 - Simula navegación al servidor HTTP
 - Envía credenciales de prueba
 - Muestra respuesta del servidor
- [ ] Instalar herramientas de red (curl, wget, navegador headless)

#### Paso 4.4: Contenedor Atacante
- [ ] Crear Dockerfile con herramientas de ataque:
 - Python 3 con scapy
 - tcpdump / tshark
 - arpspoof (dsniff) o ettercap
 - Wireshark (tshark para CLI)
- [ ] Configurar contenedor con privilegios de red (NET_ADMIN)

#### Paso 4.5: Docker Compose
- [ ] Crear `docker-compose.yml`:
 - Definir 3 servicios (victim, attacker, webserver)
 - Configurar red bridge personalizada
 - Configurar volúmenes para compartir capturas
 - Variables de entorno necesarias
- [ ] Documentar cómo levantar/detener el entorno

**Entregables Fase 4:**
- Dockerfiles para cada contenedor
- Aplicación Django funcional (HTTP y HTTPS)
- docker-compose.yml completo
- Diagramas de arquitectura
- Documentación de la topología

---

### **FASE 5: Implementación del Ataque MitM**
**Objetivo:** Simular ataque Man-in-the-Middle sobre HTTP

#### Paso 5.1: Script de ARP Spoofing
- [ ] Crear `arp_spoof.py`:
 - Envía paquetes ARP falsos a la víctima
 - Envía paquetes ARP falsos al servidor
 - Se posiciona como "gateway" entre ambos
 - Habilita IP forwarding para no romper conexión
- [ ] Documentar funcionamiento del ARP spoofing
- [ ] Añadir logs detallados del proceso

#### Paso 5.2: Script de Captura de Tráfico
- [ ] Crear `capture_traffic.py`:
 - Captura tráfico en interfaz del atacante
 - Filtra tráfico HTTP (puerto 80)
 - Guarda en formato .pcap
 - Muestra estadísticas en tiempo real
- [ ] Documentar uso de tcpdump/scapy

#### Paso 5.3: Script de Interceptación HTTP
- [ ] Crear `intercept_http.py`:
 - Parsea paquetes HTTP en tiempo real
 - Extrae credenciales de POST requests
 - Muestra headers y body de requests
 - Guarda credenciales interceptadas en log
- [ ] Añadir colores para mejor visualización (rich library)

#### Paso 5.4: Análisis de Capturas
- [ ] Crear `analyze_pcap.py`:
 - Lee archivos .pcap guardados
 - Extrae información relevante:
 - Credenciales en claro
 - Cookies de sesión
 - Headers HTTP
 - Genera reporte en texto/HTML
- [ ] Documentar cómo usar Wireshark para análisis manual

#### Paso 5.5: Ejecución de la Demo
- [ ] Crear script maestro `start_demo.sh`:
 - Levanta contenedores Docker
 - Configura red
 - Inicia ARP spoofing en atacante
 - Inicia captura de tráfico
 - Ejecuta navegación desde víctima
 - Muestra resultados en tiempo real
- [ ] Documentar paso a paso la ejecución
- [ ] Capturar evidencias (screenshots, videos opcionales)

**Entregables Fase 5:**
- Scripts de ataque funcionales
- Archivos .pcap con tráfico capturado
- Logs con credenciales interceptadas
- Script de demo automatizado
- Evidencias visuales (screenshots)
- Sección en informe LaTeX

---

### **FASE 6: Contramedidas y Protección**
**Objetivo:** Demostrar cómo HTTPS protege contra MitM

#### Paso 6.1: Configuración HTTPS
- [ ] Generar certificados SSL/TLS autofirmados
- [ ] Configurar Django para HTTPS:
 - SECURE_SSL_REDIRECT = True
 - SECURE_HSTS_SECONDS = 31536000
 - SECURE_HSTS_INCLUDE_SUBDOMAINS = True
 - SECURE_HSTS_PRELOAD = True
 - SESSION_COOKIE_SECURE = True
 - CSRF_COOKIE_SECURE = True
- [ ] Documentar cada parámetro de seguridad

#### Paso 6.2: Prueba de Ataque contra HTTPS
- [ ] Ejecutar mismo ataque MitM pero contra HTTPS
- [ ] Demostrar que:
 - Tráfico está cifrado en .pcap
 - Credenciales no son visibles
 - Certificado autofirmado genera advertencia
- [ ] Capturar evidencias comparativas

#### Paso 6.3: Gestión de known_hosts (SSH)
- [ ] Documentar cómo SSH previene MitM:
 - Primera conexión: TOFU (Trust On First Use)
 - Verificación de fingerprint
 - Archivo known_hosts
 - Advertencia si cambia la clave del servidor
- [ ] Crear demo de cambio de clave (simula MitM en SSH)
- [ ] Mostrar advertencia de SSH

#### Paso 6.4: Otras Contramedidas
- [ ] Documentar:
 - Certificate Pinning
 - DANE (DNS-based Authentication)
 - VPN como protección en redes no confiables
 - Detección de ARP spoofing (arpwatch)
 - Static ARP entries
- [ ] Crear checklist de seguridad

**Entregables Fase 6:**
- Configuración HTTPS completa
- Evidencias de protección contra MitM
- Documentación de contramedidas
- Checklist de seguridad
- Sección en informe LaTeX

---

### **FASE 7: Documentación Final y Entregables**
**Objetivo:** Completar toda la documentación del proyecto

#### Paso 7.1: Informe Técnico LaTeX
- [ ] Completar todas las secciones:
 - Introducción y planteamiento del problema
 - Marco teórico (SSH, MitM, TLS/HTTPS)
 - Análisis de SSH (arquitectura, RFC)
 - SSH Hardening (configuración, resultados)
 - Simulación MitM (metodología, resultados)
 - Contramedidas (HTTPS, HSTS, buenas prácticas)
 - Conclusiones y recomendaciones
- [ ] Añadir todas las imágenes y diagramas
- [ ] Añadir referencias bibliográficas
- [ ] Compilar PDF final

#### Paso 7.2: Guías Reproducibles
- [ ] Completar `01_guia_ssh_hardening.md`:
 - Paso a paso con comandos exactos
 - Explicación de cada parámetro
 - Troubleshooting común
- [ ] Completar `02_guia_mitm_demo.md`:
 - Requisitos previos
 - Instalación y configuración
 - Ejecución de la demo
 - Interpretación de resultados
- [ ] Completar `03_checklist_seguridad.md`:
 - Checklist para SSH
 - Checklist para servidores web
 - Checklist para redes

#### Paso 7.3: README Principal
- [ ] Crear README.md completo con:
 - Descripción del proyecto
 - Integrantes y profesor
 - Requisitos del sistema
 - Instalación rápida
 - Uso básico
 - Estructura del proyecto
 - Enlaces a documentación detallada
 - Advertencias éticas y legales
 - Licencia

#### Paso 7.4: Limpieza y Organización
- [ ] Revisar que todos los archivos estén en su lugar
- [ ] Eliminar archivos temporales
- [ ] Anonimizar logs si contienen información sensible
- [ ] Verificar que .gitignore excluye archivos sensibles
- [ ] Crear release/tag en Git

#### Paso 7.5: Presentación (Opcional)
- [ ] Crear slides para presentación:
 - Introducción y objetivos
 - Demo en vivo o video
 - Resultados y hallazgos
 - Conclusiones
- [ ] Preparar demo en vivo para la clase

**Entregables Fase 7:**
- Informe técnico completo (PDF)
- Guía reproducible de SSH hardening
- PoC documentada de MitM sobre HTTP
- Checklist de defensa
- README completo
- Repositorio limpio y organizado
- (Opcional) Presentación

---

## Tecnologías Seleccionadas

### Infraestructura
- **Docker** + **Docker Compose**: Aislamiento y reproducibilidad
- **Alpine Linux** o **Ubuntu**: Imágenes base para contenedores
- **Red bridge personalizada**: Simulación de LAN

### SSH
- **OpenSSH 8.x+**: Servidor y cliente SSH
- **ssh-audit**: Auditoría de configuración (herramienta externa)
- **Google Authenticator PAM**: 2FA
- **ED25519**: Algoritmo de clave pública moderno

### Ataque MitM
- **Python 3.10+**: Lenguaje principal para scripts
- **Scapy**: Manipulación de paquetes (ARP spoofing)
- **tcpdump/tshark**: Captura de tráfico
- **Wireshark**: Análisis de .pcap (GUI)
- **dsniff (arpspoof)**: Alternativa para ARP spoofing

### Servidor Web
- **Django 4.x**: Framework web Python
- **Bootstrap 5**: UI moderna y responsive
- **Gunicorn**: WSGI server para producción
- **Nginx** (opcional): Reverse proxy para HTTPS

### Documentación
- **LaTeX**: Informe técnico profesional
- **Markdown**: Guías y documentación técnica
- **Mermaid**: Diagramas de red y flujo
- **asciinema** (opcional): Grabación de sesiones de terminal

### Librerías Python
```
django>=4.2
scapy>=2.5
pyshark>=0.6
paramiko>=3.0
cryptography>=41.0
rich>=13.0 # Output colorido en terminal
requests>=2.31
```

---

## Cronograma Estimado

| Fase | Descripción | Duración Estimada | Prioridad |
|------|-------------|-------------------|-----------|
| **Fase 1** | Configuración del Entorno Base | 2-3 horas | Alta |
| **Fase 2** | Estudio y Análisis de SSH | 4-6 horas | Alta |
| **Fase 3** | Hardening de OpenSSH | 6-8 horas | Alta |
| **Fase 4** | Diseño del Entorno MitM | 4-6 horas | 🟡 Media |
| **Fase 5** | Implementación del Ataque MitM | 8-10 horas | Alta |
| **Fase 6** | Contramedidas y Protección | 4-6 horas | 🟡 Media |
| **Fase 7** | Documentación Final | 6-8 horas | Alta |
| **TOTAL** | | **34-47 horas** | |

### Distribución Sugerida entre Integrantes

**José Daniel Moreno Ceballos:**
- Fases 2 y 3 (SSH: análisis y hardening)
- Secciones del informe LaTeX relacionadas con SSH

**David Duque Diaz:**
- Fases 4 y 5 (Diseño e implementación MitM)
- Scripts de ataque y captura

**Gustavo Adolfo Pérez Pérez:**
- Fase 6 (Contramedidas)
- Fase 7 (Documentación final y compilación)
- Servidor Django

**Trabajo Colaborativo:**
- Fase 1 (Setup inicial): Todos
- Revisión cruzada de código y documentación
- Pruebas finales y demo

---

## Consideraciones Éticas y Legales

### Recordatorios Importantes

1. **Entorno Controlado**: Todas las pruebas se realizan ÚNICAMENTE en contenedores Docker aislados
2. **No Atacar Terceros**: NUNCA ejecutar estos scripts fuera del entorno de laboratorio
3. **Consentimiento**: Todos los participantes conocen y aprueban las pruebas
4. **Datos Sensibles**: No usar credenciales reales, solo datos de prueba
5. **Limpieza**: Eliminar capturas de tráfico al finalizar el proyecto
6. **Uso Académico**: Este proyecto es exclusivamente con fines educativos

### Advertencia en Scripts

Todos los scripts deben incluir un banner de advertencia:

```python
"""
 ADVERTENCIA - USO EDUCATIVO ÚNICAMENTE 

Este script es parte de un proyecto académico de la Universidad Nacional de Colombia.
Su uso está destinado EXCLUSIVAMENTE a entornos de laboratorio controlados.

ESTÁ PROHIBIDO:
- Ejecutar en redes de producción
- Atacar sistemas de terceros sin autorización
- Usar fuera del contexto educativo

El uso indebido de estas herramientas puede constituir un delito.
"""
```

---

## Referencias Iniciales

- RFC 4251: The Secure Shell (SSH) Protocol Architecture
- RFC 4253: The Secure Shell (SSH) Transport Layer Protocol
- RFC 6797: HTTP Strict Transport Security (HSTS)
- OWASP: Man-in-the-Middle Attacks
- Mozilla SSL Configuration Generator
- CIS Benchmark for OpenSSH

---

## Checklist de Inicio

Antes de comenzar la implementación, verificar:

- [ ] Docker y Docker Compose instalados
- [ ] Python 3.10+ instalado
- [ ] Git configurado
- [ ] Editor de LaTeX (TeXLive, Overleaf, etc.)
- [ ] Wireshark instalado (para análisis manual)
- [ ] Permisos de administrador (para configurar SSH)
- [ ] Espacio en disco suficiente (~5GB para imágenes Docker)

---

## Próximos Pasos

1. **Revisar este plan** con todos los integrantes del grupo
2. **Asignar responsabilidades** según las fortalezas de cada uno
3. **Comenzar con Fase 1**: Setup del entorno
4. **Crear repositorio Git** y hacer commit inicial de este plan
5. **Establecer reuniones de seguimiento** semanales

---

**Última actualización:** Noviembre 23, 2025 
**Versión:** 1.0 
**Estado:** Planificación Inicial
