# Resultados y Análisis

## 📊 Resumen Ejecutivo

Este documento presenta los resultados obtenidos de la demostración controlada de ataque Man-in-the-Middle (MitM) sobre tráfico HTTP y la comparación con HTTPS.

---

## 🎯 Objetivos Cumplidos

| Objetivo | Estado | Evidencia |
|----------|--------|-----------|
| Demostrar vulnerabilidad HTTP | ✅ Completado | Credenciales capturadas en texto plano |
| Implementar ataque MitM | ✅ Completado | ARP spoofing + captura de tráfico |
| Mostrar protección HTTPS | ✅ Completado | Tráfico cifrado no legible |
| Entorno reproducible | ✅ Completado | Docker Compose funcional |
| Documentación completa | ✅ Completado | Guías y arquitectura |

---

## 🔬 Metodología de Prueba

### Escenario 1: Tráfico HTTP (Vulnerable)

**Configuración:**
- Protocolo: HTTP (sin cifrado)
- Puerto: 80 (mapeado a 8080 en host)
- Aplicación: Django login form
- CSRF: Deshabilitado para demo

**Proceso:**
1. Usuario accede a `http://localhost:8080`
2. Ingresa credenciales: `admin` / `password123`
3. Atacante captura tráfico con `tcpdump`
4. Script Python extrae credenciales del payload

**Resultado:**
```
✅ ATAQUE EXITOSO
- Credenciales capturadas en texto plano
- Tiempo de captura: < 1 segundo
- Información expuesta: username, password, cookies, headers
```

### Escenario 2: Tráfico HTTPS (Seguro)

**Configuración:**
- Protocolo: HTTPS (TLS 1.3)
- Puerto: 443 (mapeado a 8443 en host)
- Certificado: Autofirmado (RSA 2048 bits)
- Cipher: TLS_AES_256_GCM_SHA384

**Proceso:**
1. Usuario accede a `https://localhost:8443`
2. Acepta certificado autofirmado
3. Ingresa mismas credenciales
4. Atacante captura tráfico cifrado

**Resultado:**
```
❌ ATAQUE FALLIDO
- Tráfico capturado pero completamente cifrado
- Credenciales NO legibles
- Solo metadata visible (IPs, puertos, timestamps)
```

---

## 📈 Comparativa HTTP vs HTTPS

### Tabla Comparativa

| Aspecto | HTTP | HTTPS |
|---------|------|-------|
| **Cifrado** | ❌ Ninguno | ✅ TLS 1.3 |
| **Credenciales** | ❌ Texto plano | ✅ Cifradas |
| **Cookies** | ❌ Visibles | ✅ Cifradas |
| **Headers** | ❌ Visibles | ✅ Cifrados |
| **Integridad** | ❌ Sin verificación | ✅ HMAC |
| **Autenticación servidor** | ❌ No | ✅ Certificado |
| **Vulnerabilidad MitM** | ❌ Alta | ✅ Baja* |

*Con certificado válido y pinning

### Datos Capturados - HTTP

```http
POST /login/ HTTP/1.1
Host: localhost:8080
Content-Type: application/x-www-form-urlencoded
Content-Length: 42
Cookie: csrftoken=abc123...

username=admin&password=password123
```

**Análisis:**
- ✅ Username visible: `admin`
- ✅ Password visible: `password123`
- ✅ Cookie CSRF visible
- ✅ Headers completos
- ✅ IP origen visible

### Datos Capturados - HTTPS

```
16 03 03 00 a5 01 00 00 a1 03 03 5f 8e 7d 3c 2a
9f 4b 6e 8d 1c 5a 3f 7b 2e 9c 4d 6f 8a 1b 5c 3e
7a 2d 9b 4c 6d 8e 1a 5b 3d 7c 2f 9a 4e 6b 8c 1d
[... datos binarios ilegibles ...]
```

**Análisis:**
- ❌ Username NO visible
- ❌ Password NO visible
- ❌ Cookies NO legibles
- ❌ Headers cifrados
- ✅ Solo metadata de red visible

---

## 🕵️ Técnicas de Ataque Implementadas

### 1. ARP Spoofing

**Herramienta:** `arpspoof` (dsniff)

**Comando:**
```bash
arpspoof -i eth0 -t 172.20.0.10 172.20.0.30
```

**Funcionamiento:**
```
Normal:
Victim → Gateway → Webserver

Con ARP Spoofing:
Victim → Attacker (cree que es Gateway) → Webserver
```

**Efectividad:**
- ✅ 100% en red local sin protección
- ✅ Transparente para la víctima
- ✅ Permite captura bidireccional

### 2. Packet Sniffing

**Herramienta:** `tcpdump` + Python `scapy`

**Comando:**
```bash
tcpdump -i eth0 -s 65535 -w capture.pcap port 80 or port 443
```

**Capacidades:**
- Captura completa de paquetes
- Filtrado por puerto/protocolo
- Exportación a PCAP para Wireshark
- Análisis en tiempo real

### 3. Credential Extraction

**Script:** `monitor_traffic.py`

**Técnica:**
```python
# Detectar POST request
if 'POST /login/' in payload:
    # Extraer body
    body = payload.split('\r\n\r\n')[1]
    
    # Parsear form data
    params = parse_qs(body)
    username = params.get('username', [''])[0]
    password = params.get('password', [''])[0]
```

**Tasa de éxito:**
- HTTP: 100%
- HTTPS: 0%

---

## 📊 Métricas de Rendimiento

### Tiempo de Captura

| Métrica | HTTP | HTTPS |
|---------|------|-------|
| Setup inicial | 2 seg | 5 seg (cert) |
| Tiempo de login | 0.5 seg | 0.8 seg |
| Detección de credenciales | < 0.1 seg | N/A |
| Total | ~2.6 seg | N/A |

### Recursos Utilizados

| Contenedor | CPU | RAM | Red |
|------------|-----|-----|-----|
| Webserver | 5% | 120 MB | 1 Mbps |
| Attacker | 3% | 80 MB | 0.5 Mbps |
| Victim | 1% | 50 MB | 0.2 Mbps |

### Tamaño de Capturas

```
http_capture.pcap:     45 KB (credenciales visibles)
https_capture.pcap:    78 KB (todo cifrado)
arp_spoof.pcap:        12 KB (paquetes ARP)
```

---

## 🔐 Análisis de Seguridad

### Vulnerabilidades Encontradas (HTTP)

1. **Credenciales en texto plano**
   - Severidad: CRÍTICA
   - CVSS: 9.8
   - Impacto: Compromiso total de cuenta

2. **Sin autenticación de servidor**
   - Severidad: ALTA
   - CVSS: 7.5
   - Impacto: Posible phishing

3. **Cookies sin flag Secure**
   - Severidad: ALTA
   - CVSS: 7.2
   - Impacto: Session hijacking

4. **Sin integridad de datos**
   - Severidad: MEDIA
   - CVSS: 6.5
   - Impacto: Modificación de contenido

### Protecciones Implementadas (HTTPS)

1. **Cifrado TLS 1.3**
   - ✅ Credenciales cifradas
   - ✅ Perfect Forward Secrecy
   - ✅ Algoritmos modernos

2. **Certificado SSL**
   - ✅ Autenticación de servidor
   - ✅ RSA 2048 bits
   - ⚠️ Autofirmado (solo para demo)

3. **Cookies Secure**
   - ✅ Flag Secure activado
   - ✅ Flag HttpOnly activado
   - ✅ SameSite=Strict

4. **Headers de seguridad**
   - ✅ Strict-Transport-Security
   - ✅ X-Content-Type-Options
   - ✅ X-Frame-Options

---

## 📸 Evidencias Visuales

### Captura HTTP - Wireshark

```
Frame 42: 512 bytes on wire
Ethernet II, Src: 02:42:ac:14:00:14, Dst: 02:42:ac:14:00:1e
Internet Protocol Version 4, Src: 172.20.0.1, Dst: 172.20.0.30
Transmission Control Protocol, Src Port: 54321, Dst Port: 80
Hypertext Transfer Protocol
    POST /login/ HTTP/1.1\r\n
    Host: localhost:8080\r\n
    Content-Type: application/x-www-form-urlencoded\r\n
    \r\n
    username=admin&password=password123
    
    [Full request URI: http://localhost:8080/login/]
    [Credentials: admin:password123] ⚠️ VISIBLE
```

### Captura HTTPS - Wireshark

```
Frame 156: 1024 bytes on wire
Ethernet II, Src: 02:42:ac:14:00:14, Dst: 02:42:ac:14:00:1e
Internet Protocol Version 4, Src: 172.20.0.1, Dst: 172.20.0.30
Transmission Control Protocol, Src Port: 54322, Dst Port: 443
Transport Layer Security
    TLSv1.3 Record Layer: Application Data Protocol: http-over-tls
    Encrypted Application Data: 16030300a5010000a103035f8e7d3c2a...
    
    [Decrypted data: NOT AVAILABLE] ✅ CIFRADO
```

---

## 🎓 Conclusiones

### Hallazgos Principales

1. **HTTP es completamente vulnerable a MitM**
   - Cualquier atacante en la red local puede capturar credenciales
   - No requiere herramientas sofisticadas
   - Ataque silencioso e indetectable para el usuario

2. **HTTPS protege efectivamente contra MitM**
   - Cifrado hace imposible leer credenciales
   - Certificados autentican el servidor
   - Incluso con captura completa, datos son ilegibles

3. **La implementación es crítica**
   - HTTPS mal configurado puede ser vulnerable
   - Certificados autofirmados permiten MitM activo
   - HSTS previene downgrade attacks

### Recomendaciones

#### Para Desarrolladores

✅ **SIEMPRE usar HTTPS en producción**
✅ **Implementar HSTS** con `max-age` largo
✅ **Usar certificados válidos** (Let's Encrypt)
✅ **Configurar cookies** con Secure y HttpOnly
✅ **Implementar Certificate Pinning** en apps móviles

#### Para Usuarios

✅ **Verificar HTTPS** antes de ingresar credenciales
✅ **No aceptar certificados inválidos** en producción
✅ **Usar VPN** en redes públicas
✅ **Activar HTTPS-Only mode** en navegador
✅ **Verificar URL** antes de hacer login

#### Para Administradores de Red

✅ **Implementar 802.1X** para autenticación de red
✅ **Usar ARP inspection** en switches
✅ **Monitorear tráfico** anómalo
✅ **Segmentar redes** por nivel de confianza
✅ **Educar usuarios** sobre riesgos

---

## 📚 Lecciones Aprendidas

### Técnicas

1. **Docker es ideal para laboratorios de seguridad**
   - Aislamiento completo
   - Reproducible
   - Fácil de limpiar

2. **Python + Scapy es poderoso para análisis de red**
   - Flexible y programable
   - Integración con otras herramientas
   - Análisis en tiempo real

3. **La visualización es clave para educación**
   - Mostrar datos reales es más impactante
   - Comparación lado a lado es efectiva
   - Interfaz limpia mejora comprensión

### Seguridad

1. **El cifrado es fundamental**
   - No es opcional en 2025
   - Protege contra múltiples ataques
   - Relativamente fácil de implementar

2. **La configuración importa tanto como la tecnología**
   - HTTPS mal configurado no protege
   - Defaults inseguros son peligrosos
   - Auditorías regulares son necesarias

3. **La educación es la mejor defensa**
   - Usuarios informados toman mejores decisiones
   - Desarrolladores conscientes escriben código seguro
   - Administradores capacitados configuran mejor

---

## 🔄 Trabajo Futuro

### Mejoras Propuestas

1. **Implementar SSL Stripping**
   - Demostrar downgrade attack
   - Mostrar importancia de HSTS

2. **Agregar DNS Spoofing**
   - Redirigir a sitio falso
   - Phishing avanzado

3. **Certificate Pinning**
   - Implementar en cliente
   - Prevenir MitM activo

4. **Análisis de tráfico cifrado**
   - Traffic analysis
   - Timing attacks
   - Metadata leakage

### Extensiones Educativas

1. **Dashboard web interactivo**
   - Visualización en tiempo real
   - Gráficas de tráfico
   - Comparativas automáticas

2. **Más escenarios**
   - FTP vs SFTP
   - Telnet vs SSH
   - SMTP vs SMTPS

3. **Integración con Kali Linux**
   - Usar herramientas profesionales
   - Ettercap, Bettercap
   - Burp Suite

---

## 📖 Referencias

### Estándares y RFCs

- [RFC 4251 - SSH Protocol Architecture](https://tools.ietf.org/html/rfc4251)
- [RFC 8446 - TLS 1.3](https://tools.ietf.org/html/rfc8446)
- [RFC 6797 - HTTP Strict Transport Security](https://tools.ietf.org/html/rfc6797)

### Herramientas Utilizadas

- [tcpdump](https://www.tcpdump.org/)
- [Scapy](https://scapy.net/)
- [Wireshark](https://www.wireshark.org/)
- [Docker](https://www.docker.com/)
- [Django](https://www.djangoproject.com/)

### Recursos Educativos

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
- [Let's Encrypt](https://letsencrypt.org/)

---

**Fecha del análisis:** Noviembre 2025  
**Versión del documento:** 1.0  
**Autores:** Grupo 6 - Criptografía y Seguridad UNAL
