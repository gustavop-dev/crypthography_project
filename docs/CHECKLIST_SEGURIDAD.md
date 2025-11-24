# Checklist de Seguridad

## 🔐 SSH Hardening

### Configuración del Servidor

- [ ] Deshabilitar autenticación por contraseña
- [ ] Deshabilitar login de root
- [ ] Cambiar puerto por defecto (22)
- [ ] Usar solo protocolo SSH v2
- [ ] Configurar timeout de sesión
- [ ] Limitar intentos de login
- [ ] Usar algoritmos de cifrado modernos
- [ ] Deshabilitar X11 forwarding
- [ ] Deshabilitar port forwarding (si no se usa)
- [ ] Configurar banner de advertencia

### Autenticación

- [ ] Generar par de claves SSH (RSA 4096 o Ed25519)
- [ ] Proteger clave privada con passphrase
- [ ] Configurar autenticación de dos factores (2FA)
- [ ] Usar ssh-agent para gestión de claves
- [ ] Rotar claves regularmente
- [ ] Revocar claves comprometidas

### Control de Acceso

- [ ] Whitelist de usuarios permitidos
- [ ] Whitelist de IPs permitidas
- [ ] Configurar fail2ban
- [ ] Logs de auditoría activados
- [ ] Monitoreo de intentos fallidos

---

## 🌐 Seguridad Web (HTTPS)

### Certificados SSL/TLS

- [ ] Usar certificados válidos (Let's Encrypt)
- [ ] Renovación automática configurada
- [ ] Cadena de certificados completa
- [ ] Certificado no autofirmado en producción
- [ ] Validez del certificado verificada

### Configuración TLS

- [ ] TLS 1.3 habilitado
- [ ] TLS 1.0 y 1.1 deshabilitados
- [ ] Cipher suites modernos
- [ ] Perfect Forward Secrecy (PFS)
- [ ] OCSP Stapling habilitado

### Headers de Seguridad

- [ ] Strict-Transport-Security (HSTS)
- [ ] Content-Security-Policy (CSP)
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY
- [ ] Referrer-Policy configurado

### Cookies

- [ ] Flag Secure activado
- [ ] Flag HttpOnly activado
- [ ] SameSite=Strict o Lax
- [ ] Expiración apropiada

---

## 🛡️ Protección contra MitM

### Red

- [ ] Usar VPN en redes públicas
- [ ] Verificar HTTPS antes de login
- [ ] No aceptar certificados inválidos
- [ ] Configurar ARP inspection en switches
- [ ] Implementar 802.1X

### Aplicación

- [ ] Certificate pinning en apps móviles
- [ ] Validación de certificados
- [ ] Detección de downgrade attacks
- [ ] Logs de conexiones sospechosas

---

## 📊 Monitoreo y Auditoría

- [ ] Logs centralizados
- [ ] Alertas de seguridad configuradas
- [ ] Auditorías periódicas
- [ ] Análisis de tráfico
- [ ] Respuesta a incidentes documentada

---

## ✅ Verificación

Usa estos comandos para verificar:

```bash
# Verificar configuración SSH
ssh-audit localhost

# Verificar SSL/TLS
testssl.sh https://tu-sitio.com

# Verificar headers
curl -I https://tu-sitio.com
```
