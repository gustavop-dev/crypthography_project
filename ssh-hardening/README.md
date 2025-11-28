# SSH Hardening - Fase 2 y 3

## Descripción

Este módulo contiene todo lo relacionado con el análisis, auditoría y endurecimiento (hardening) de OpenSSH.

---

## Objetivos

1. **Analizar** la arquitectura de SSH según RFC 4251/4253
2. **Identificar** configuraciones inseguras comunes
3. **Implementar** configuración endurecida siguiendo mejores prácticas
4. **Auditar** y comparar configuraciones (antes/después)
5. **Configurar** autenticación con claves públicas y 2FA

---

## Estructura

```
ssh-hardening/
 README.md # Este archivo
 configs/
 README.md # Explicación de cada parámetro
 sshd_config.weak # Configuración débil (baseline)
 sshd_config.hardened # Configuración endurecida
 ssh_config.client # Configuración cliente segura
 scripts/
 audit_ssh.py # Auditoría automatizada
 setup_ssh_keys.sh # Generación de claves
 setup_2fa.sh # Configuración 2FA
 test_ssh_security.py # Tests automatizados
 resultados/
 audit_before.txt # Auditoría pre-hardening
 audit_after.txt # Auditoría post-hardening
```

---

## Fase 2: Análisis de SSH

### Conceptos Clave

#### Arquitectura SSH (RFC 4251)

SSH (Secure Shell) es un protocolo de red que permite:
- Acceso remoto seguro a sistemas
- Transferencia segura de archivos
- Tunneling de otros protocolos

**Capas del protocolo:**

1. **Transport Layer (RFC 4253)**
 - Autenticación del servidor
 - Cifrado de datos
 - Integridad de datos
 - Compresión (opcional)

2. **User Authentication Layer (RFC 4252)**
 - Autenticación del cliente
 - Métodos: password, public key, keyboard-interactive

3. **Connection Layer (RFC 4254)**
 - Multiplexación de canales
 - Port forwarding
 - X11 forwarding

#### Modelo TOFU (Trust On First Use)

En la primera conexión a un servidor SSH:
1. Cliente no conoce la clave pública del servidor
2. Servidor presenta su clave pública (fingerprint)
3. Usuario debe verificar manualmente el fingerprint
4. Si acepta, la clave se guarda en `~/.ssh/known_hosts`
5. Conexiones futuras verifican contra esta clave

**Vulnerabilidad:** Si un atacante intercepta la primera conexión (MitM), puede presentar su propia clave.

#### Algoritmos de Cifrado

**Modernos (seguros):**
- `chacha20-poly1305@openssh.com` - Cifrado de flujo moderno
- `aes256-gcm@openssh.com` - AES con autenticación
- `aes128-gcm@openssh.com` - AES con autenticación

**Obsoletos (inseguros):**
- `3des-cbc` - Triple DES (lento, vulnerable)
- `arcfour` - RC4 (roto, no usar)
- `blowfish-cbc` - Blowfish (obsoleto)

#### Métodos de Autenticación

**Por orden de seguridad (más seguro primero):**

1. **Public Key + 2FA** 
 - Clave privada + código OTP
 - Protección contra robo de credenciales

2. **Public Key (ED25519/RSA 4096)** 
 - Solo clave privada
 - Muy seguro si la clave está protegida

3. **Password + 2FA** 
 - Contraseña + código OTP
 - Mejor que solo contraseña

4. **Password** 
 - Solo contraseña
 - Vulnerable a fuerza bruta

---

## Configuración Débil (Baseline)

### Parámetros Inseguros Comunes

| Parámetro | Valor Inseguro | Riesgo |
|-----------|----------------|--------|
| `PermitRootLogin` | `yes` | Permite login directo como root |
| `PasswordAuthentication` | `yes` | Vulnerable a fuerza bruta |
| `PermitEmptyPasswords` | `yes` | Permite cuentas sin contraseña |
| `ChallengeResponseAuthentication` | `no` | Deshabilita 2FA |
| `X11Forwarding` | `yes` | Puede exponer display X11 |
| `MaxAuthTries` | `6` o más | Permite múltiples intentos |
| `Ciphers` | Incluye 3des, arcfour | Algoritmos débiles |
| `MACs` | Incluye MD5 | Hash débil |
| `Protocol` | `1` o `1,2` | SSH-1 está roto |

---

## Configuración Endurecida

### Mejores Prácticas

| Parámetro | Valor Seguro | Beneficio |
|-----------|--------------|-----------|
| `PermitRootLogin` | `no` | Previene ataques directos a root |
| `PasswordAuthentication` | `no` | Solo claves públicas |
| `PubkeyAuthentication` | `yes` | Habilita autenticación por clave |
| `ChallengeResponseAuthentication` | `yes` | Habilita 2FA |
| `MaxAuthTries` | `3` | Limita intentos de login |
| `ClientAliveInterval` | `300` | Desconecta sesiones inactivas |
| `ClientAliveCountMax` | `2` | Máximo de keepalives |
| `AllowUsers` | Lista específica | Lista blanca de usuarios |
| `Ciphers` | Solo modernos | Fuerza cifrado fuerte |
| `MACs` | Solo SHA256+ | Hash seguro |
| `Protocol` | `2` | Solo SSH-2 |

---

## Uso

### 1. Auditar Configuración Actual

```bash
# Auditoría automatizada
python3 scripts/audit_ssh.py

# Ver configuración actual
sudo sshd -T

# Verificar sintaxis
sudo sshd -t
```

### 2. Aplicar Configuración Débil (Para Demo)

```bash
# SOLO EN ENTORNO DE PRUEBA
sudo cp configs/sshd_config.weak /etc/ssh/sshd_config
sudo systemctl restart sshd

# Auditar
python3 scripts/audit_ssh.py > resultados/audit_before.txt
```

### 3. Aplicar Configuración Endurecida

```bash
# Backup de configuración actual
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Aplicar configuración segura
sudo cp configs/sshd_config.hardened /etc/ssh/sshd_config

# Verificar sintaxis
sudo sshd -t

# Reiniciar servicio
sudo systemctl restart sshd

# Auditar
python3 scripts/audit_ssh.py > resultados/audit_after.txt
```

### 4. Configurar Claves SSH

```bash
# Generar par de claves ED25519
bash scripts/setup_ssh_keys.sh

# Copiar clave pública al servidor
ssh-copy-id -i ~/.ssh/id_ed25519.pub usuario@servidor
```

### 5. Configurar 2FA (Opcional)

```bash
# Instalar y configurar Google Authenticator
bash scripts/setup_2fa.sh
```

---

## Comparativa: Antes vs Después

| Aspecto | Configuración Débil | Configuración Endurecida |
|---------|---------------------|--------------------------|
| Login root | Permitido | Bloqueado |
| Contraseñas | Permitidas | Solo claves |
| Algoritmos | 3DES, RC4 | ChaCha20, AES-GCM |
| Intentos de login | 6 | 3 |
| 2FA | Deshabilitado | Habilitado |
| Timeout sesión | ∞ | 10 minutos |
| Lista de usuarios | Todos | Solo permitidos |

---

## Recomendaciones Adicionales

### A Nivel de Sistema

1. **Firewall (UFW/iptables)**
 ```bash
 sudo ufw allow 22/tcp
 sudo ufw enable
```

2. **Fail2ban** (Protección contra fuerza bruta)
 ```bash
 sudo apt install fail2ban
 sudo systemctl enable fail2ban
```

3. **Cambiar puerto SSH** (Seguridad por oscuridad)
 ```
 Port 2222 # En lugar de 22
```

4. **Monitoreo de logs**
 ```bash
 sudo tail -f /var/log/auth.log
```

### A Nivel de Usuario

1. **Proteger clave privada**
 ```bash
 chmod 600 ~/.ssh/id_ed25519
 chmod 700 ~/.ssh
```

2. **Usar passphrase en claves**
 ```bash
 ssh-keygen -t ed25519 -C "email@example.com"
 # Ingresar passphrase fuerte
```

3. **SSH Agent** (Para no escribir passphrase cada vez)
 ```bash
 eval "$(ssh-agent -s)"
 ssh-add ~/.ssh/id_ed25519
```

---

## Referencias

- [RFC 4251 - SSH Protocol Architecture](https://tools.ietf.org/html/rfc4251)
- [RFC 4252 - SSH Authentication Protocol](https://tools.ietf.org/html/rfc4252)
- [RFC 4253 - SSH Transport Layer Protocol](https://tools.ietf.org/html/rfc4253)
- [Mozilla SSH Guidelines](https://infosec.mozilla.org/guidelines/openssh)
- [CIS Benchmark for OpenSSH](https://www.cisecurity.org/)
- [ssh-audit Tool](https://github.com/jtesta/ssh-audit)

---

## Advertencias

- **NUNCA** apliques configuraciones de prueba en servidores de producción
- **SIEMPRE** haz backup de `/etc/ssh/sshd_config` antes de modificar
- **VERIFICA** que tienes otra forma de acceso antes de deshabilitar passwords
- **PRUEBA** la configuración con `sudo sshd -t` antes de reiniciar el servicio

---

**Última actualización:** Noviembre 2025 
**Responsable:** José Daniel Moreno Ceballos
