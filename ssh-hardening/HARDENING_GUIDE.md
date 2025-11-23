# Guía Completa de SSH Hardening

## 🎯 Objetivo

Transformar una configuración SSH débil en una configuración endurecida siguiendo las mejores prácticas de seguridad.

---

## ⚠️ ADVERTENCIAS IMPORTANTES

1. **NUNCA** apliques estos cambios en un servidor de producción sin tener un plan de respaldo
2. **SIEMPRE** mantén una sesión SSH abierta mientras pruebas cambios
3. **VERIFICA** que tienes otra forma de acceso (consola física, KVM, etc.)
4. **HAZ BACKUP** de `/etc/ssh/sshd_config` antes de modificar
5. **PRUEBA** cada cambio antes de cerrar tu sesión actual

---

## 📋 Checklist Pre-Hardening

Antes de comenzar, verifica:

- [ ] Tienes acceso root o sudo
- [ ] Tienes una sesión SSH activa
- [ ] Tienes acceso alternativo al servidor (consola, KVM, etc.)
- [ ] Has hecho backup de la configuración actual
- [ ] Tienes un par de claves SSH generado
- [ ] Has probado la autenticación con claves

---

## 🚀 Proceso de Hardening Paso a Paso

### Paso 1: Auditoría Inicial

```bash
# Ir al directorio del proyecto
cd /home/cerrotico/unal/cryptography_project/ssh-hardening

# Ejecutar auditoría
python3 scripts/audit_ssh.py > resultados/audit_before.txt

# Ver resultados
cat resultados/audit_before.txt
```

**Objetivo:** Establecer baseline de seguridad actual.

---

### Paso 2: Backup de Configuración Actual

```bash
# Backup con timestamp
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup.$(date +%Y%m%d_%H%M%S)

# Verificar backup
ls -lh /etc/ssh/sshd_config.backup.*
```

---

### Paso 3: Generar Claves SSH (Si no existen)

```bash
# Ejecutar script de generación
bash scripts/setup_ssh_keys.sh

# O manualmente:
ssh-keygen -t ed25519 -C "tu_email@example.com"

# Configurar permisos
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

**Nota:** ED25519 es más seguro y rápido que RSA.

---

### Paso 4: Copiar Clave Pública al Servidor

```bash
# Método 1: ssh-copy-id (recomendado)
ssh-copy-id -i ~/.ssh/id_ed25519.pub usuario@servidor

# Método 2: Manual
cat ~/.ssh/id_ed25519.pub | ssh usuario@servidor "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Método 3: Copiar y pegar
cat ~/.ssh/id_ed25519.pub
# Copiar el output y pegarlo en el servidor en ~/.ssh/authorized_keys
```

---

### Paso 5: Probar Autenticación con Clave

```bash
# Probar login con clave
ssh -i ~/.ssh/id_ed25519 usuario@servidor

# Si funciona, continuar. Si no, NO CONTINUAR hasta que funcione.
```

**⚠️ CRÍTICO:** Si no puedes autenticarte con clave, NO deshabilites las contraseñas.

---

### Paso 6: Aplicar Configuración Endurecida

```bash
# Copiar configuración endurecida
sudo cp configs/sshd_config.hardened /etc/ssh/sshd_config

# O editar manualmente los parámetros clave:
sudo nano /etc/ssh/sshd_config
```

**Parámetros mínimos a cambiar:**

```bash
# Deshabilitar root
PermitRootLogin no

# Solo claves públicas
PasswordAuthentication no
PubkeyAuthentication yes

# Limitar intentos
MaxAuthTries 3
LoginGraceTime 30

# Timeout de sesión
ClientAliveInterval 300
ClientAliveCountMax 2

# Algoritmos modernos
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
KexAlgorithms curve25519-sha256,diffie-hellman-group-exchange-sha256

# Deshabilitar forwarding
X11Forwarding no
AllowTcpForwarding no
AllowAgentForwarding no

# Logging verbose
LogLevel VERBOSE
```

---

### Paso 7: Verificar Sintaxis

```bash
# Verificar que no hay errores de sintaxis
sudo sshd -t

# Si hay errores, corregirlos antes de continuar
```

---

### Paso 8: Reiniciar SSH (¡MANTÉN SESIÓN ABIERTA!)

```bash
# En una terminal, mantén tu sesión actual abierta
# En otra terminal, reinicia SSH
sudo systemctl restart sshd

# Verificar que está corriendo
sudo systemctl status sshd
```

---

### Paso 9: Probar Nueva Conexión

```bash
# En una NUEVA terminal (no cierres la anterior)
ssh -i ~/.ssh/id_ed25519 usuario@servidor

# Verificar que funciona
whoami
```

**Si funciona:** ✅ Continuar  
**Si NO funciona:** ❌ Restaurar backup inmediatamente

```bash
# Restaurar backup
sudo cp /etc/ssh/sshd_config.backup.* /etc/ssh/sshd_config
sudo systemctl restart sshd
```

---

### Paso 10: Configurar 2FA (Opcional pero Recomendado)

```bash
# Ejecutar script de configuración 2FA
sudo bash scripts/setup_2fa.sh

# Cada usuario debe ejecutar (sin sudo):
google-authenticator

# Responder:
# - Time-based tokens? y
# - Update file? y
# - Disallow multiple uses? y
# - Rate limiting? y

# Escanear código QR con app Google Authenticator
# Guardar códigos de emergencia

# Reiniciar SSH
sudo systemctl restart sshd
```

---

### Paso 11: Auditoría Post-Hardening

```bash
# Ejecutar auditoría nuevamente
python3 scripts/audit_ssh.py > resultados/audit_after.txt

# Comparar resultados
diff resultados/audit_before.txt resultados/audit_after.txt
```

---

### Paso 12: Tests Automatizados

```bash
# Ejecutar suite de tests
python3 scripts/test_ssh_security.py

# Debe mostrar:
# ✅ Root Login Disabled
# ✅ Password Auth Disabled
# ✅ Public Key Auth Enabled
# ✅ Max Auth Tries
# ✅ Session Timeout
# ✅ Strong Ciphers
# ✅ Strong MACs
# etc.
```

---

## 📊 Tabla Comparativa: Antes vs Después

| Parámetro | Antes (Débil) | Después (Endurecido) |
|-----------|---------------|----------------------|
| **PermitRootLogin** | yes | no |
| **PasswordAuthentication** | yes | no |
| **MaxAuthTries** | 6 | 3 |
| **ClientAliveInterval** | 0 (sin timeout) | 300 (5 min) |
| **Ciphers** | 3DES, CBC | ChaCha20, AES-GCM |
| **MACs** | MD5, SHA1 | SHA256, SHA512 |
| **2FA** | No | Sí (opcional) |
| **Puntuación** | 2/10 ⚠️ | 9/10 ✅ |

---

## 🔧 Configuración del Cliente SSH

Para que el cliente también use algoritmos seguros:

```bash
# Copiar configuración del cliente
cp configs/ssh_config.client ~/.ssh/config
chmod 600 ~/.ssh/config

# Crear directorio para sockets
mkdir -p ~/.ssh/sockets
chmod 700 ~/.ssh/sockets
```

---

## 🛡️ Medidas Adicionales de Seguridad

### 1. Fail2ban (Protección contra Fuerza Bruta)

```bash
# Instalar
sudo apt install fail2ban  # Ubuntu/Debian
sudo pacman -S fail2ban     # Arch

# Habilitar
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Ver bans
sudo fail2ban-client status sshd
```

### 2. Firewall (UFW)

```bash
# Instalar y configurar
sudo apt install ufw
sudo ufw allow 22/tcp
sudo ufw enable

# Ver estado
sudo ufw status
```

### 3. Cambiar Puerto SSH (Seguridad por Oscuridad)

```bash
# Editar /etc/ssh/sshd_config
Port 2222  # En lugar de 22

# Actualizar firewall
sudo ufw allow 2222/tcp
sudo ufw delete allow 22/tcp

# Reiniciar SSH
sudo systemctl restart sshd
```

### 4. Restricción de Usuarios

```bash
# En /etc/ssh/sshd_config
AllowUsers usuario1 usuario2 admin
# O por grupo:
AllowGroups ssh-users sudo
```

### 5. Monitoreo de Logs

```bash
# Ver intentos de login
sudo tail -f /var/log/auth.log

# Ver intentos fallidos
sudo grep "Failed password" /var/log/auth.log

# Ver logins exitosos
sudo grep "Accepted publickey" /var/log/auth.log
```

---

## 🐛 Troubleshooting

### Problema: No puedo conectarme después del hardening

**Solución:**
```bash
# Desde la sesión que dejaste abierta:
sudo cp /etc/ssh/sshd_config.backup.* /etc/ssh/sshd_config
sudo systemctl restart sshd
```

### Problema: "Permission denied (publickey)"

**Causas comunes:**
1. Permisos incorrectos en `~/.ssh`
2. Clave pública no en `authorized_keys`
3. SELinux bloqueando acceso

**Solución:**
```bash
# Verificar permisos
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/id_ed25519

# Ver logs del servidor
sudo tail -f /var/log/auth.log
```

### Problema: 2FA no funciona

**Solución:**
```bash
# Verificar que PAM está configurado
grep "pam_google_authenticator" /etc/pam.d/sshd

# Verificar configuración SSH
grep "ChallengeResponseAuthentication" /etc/ssh/sshd_config
grep "AuthenticationMethods" /etc/ssh/sshd_config

# Regenerar configuración 2FA
google-authenticator
```

---

## ✅ Checklist Post-Hardening

Verifica que:

- [ ] Puedes conectarte con clave SSH
- [ ] No puedes conectarte con contraseña
- [ ] No puedes conectarte como root
- [ ] 2FA funciona (si está habilitado)
- [ ] Timeout de sesión funciona
- [ ] Auditoría muestra 9/10 o más
- [ ] Tests automatizados pasan
- [ ] Logs muestran actividad normal
- [ ] Fail2ban está activo
- [ ] Firewall está configurado

---

## 📚 Referencias

- [RFC 4251 - SSH Protocol Architecture](https://tools.ietf.org/html/rfc4251)
- [RFC 4253 - SSH Transport Layer Protocol](https://tools.ietf.org/html/rfc4253)
- [Mozilla SSH Guidelines](https://infosec.mozilla.org/guidelines/openssh)
- [CIS Benchmark for OpenSSH](https://www.cisecurity.org/)
- [NIST Guidelines](https://csrc.nist.gov/)

---

**Última actualización:** Noviembre 2025  
**Responsable:** José Daniel Moreno Ceballos  
**Revisado por:** Grupo 6
