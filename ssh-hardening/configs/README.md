# Configuraciones SSH - Documentación Detallada

## 📋 Archivos de Configuración

- **`sshd_config.weak`**: Configuración insegura para demostración
- **`sshd_config.hardened`**: Configuración endurecida siguiendo mejores prácticas
- **`ssh_config.client`**: Configuración del cliente SSH (pendiente)

---

## 🔍 Explicación de Parámetros Críticos

### Autenticación

#### `PermitRootLogin`
**Valores:** `yes` | `no` | `prohibit-password` | `forced-commands-only`

- **`yes`** ⚠️: Permite login directo como root con cualquier método
- **`no`** ✅: Bloquea completamente el login de root
- **`prohibit-password`**: Permite root solo con clave pública
- **`forced-commands-only`**: Solo comandos específicos

**Recomendación:** `no` - Usar usuario normal + sudo

---

#### `PasswordAuthentication`
**Valores:** `yes` | `no`

- **`yes`** ⚠️: Permite autenticación con contraseña (vulnerable a fuerza bruta)
- **`no`** ✅: Solo permite autenticación con clave pública

**Recomendación:** `no` - Forzar uso de claves públicas

---

#### `PubkeyAuthentication`
**Valores:** `yes` | `no`

- **`yes`** ✅: Permite autenticación con clave pública
- **`no`** ⚠️: Deshabilita claves públicas

**Recomendación:** `yes` - Siempre habilitar

---

#### `ChallengeResponseAuthentication`
**Valores:** `yes` | `no`

- **`yes`** ✅: Permite 2FA (requiere configuración PAM)
- **`no`** ⚠️: Sin 2FA

**Recomendación:** `yes` - Para 2FA con Google Authenticator

---

#### `AuthenticationMethods`
**Ejemplo:** `publickey,keyboard-interactive`

Define métodos de autenticación requeridos en orden.

**Opciones comunes:**
- `publickey`: Solo clave pública
- `publickey,keyboard-interactive`: Clave + 2FA
- `publickey,password`: Clave + contraseña (no recomendado)

**Recomendación:** `publickey,keyboard-interactive` para máxima seguridad

---

### Límites y Timeouts

#### `MaxAuthTries`
**Valores:** Número entero (default: 6)

Número máximo de intentos de autenticación por conexión.

- **6+** ⚠️: Facilita ataques de fuerza bruta
- **3** ✅: Balance entre seguridad y usabilidad
- **1-2**: Muy restrictivo

**Recomendación:** `3`

---

#### `LoginGraceTime`
**Valores:** Segundos (default: 120)

Tiempo máximo para completar autenticación.

- **120+** ⚠️: Permite conexiones lentas de atacantes
- **30** ✅: Suficiente para usuarios legítimos
- **0**: Sin timeout (no recomendado)

**Recomendación:** `30`

---

#### `ClientAliveInterval`
**Valores:** Segundos (default: 0)

Intervalo para enviar mensajes keepalive al cliente.

- **0** ⚠️: Sin keepalive (sesiones pueden quedar abiertas)
- **300** ✅: 5 minutos (balance)
- **60**: Muy frecuente

**Recomendación:** `300` (5 minutos)

---

#### `ClientAliveCountMax`
**Valores:** Número entero (default: 3)

Número de keepalives sin respuesta antes de desconectar.

- **3+** ⚠️: Sesiones inactivas duran mucho
- **2** ✅: 10 minutos total con ClientAliveInterval=300
- **0**: Desconecta inmediatamente

**Recomendación:** `2` (timeout total: 10 minutos)

---

### Algoritmos Criptográficos

#### `Ciphers`
**Algoritmos de cifrado simétrico**

**Modernos (seguros):**
```
chacha20-poly1305@openssh.com    # ✅ Más rápido, muy seguro
aes256-gcm@openssh.com            # ✅ AES-256 con autenticación
aes128-gcm@openssh.com            # ✅ AES-128 con autenticación
aes256-ctr                        # ✅ AES-256 modo contador
aes192-ctr                        # ✅ AES-192 modo contador
aes128-ctr                        # ✅ AES-128 modo contador
```

**Obsoletos (inseguros):**
```
3des-cbc                          # ❌ Triple DES, lento, 64-bit blocks
aes128-cbc                        # ⚠️  CBC mode vulnerable a ataques
aes256-cbc                        # ⚠️  CBC mode vulnerable a ataques
arcfour                           # ❌ RC4, completamente roto
blowfish-cbc                      # ❌ Obsoleto
```

**Recomendación:**
```
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
```

---

#### `MACs` (Message Authentication Codes)
**Algoritmos de autenticación de mensajes**

**Modernos (seguros):**
```
hmac-sha2-512-etm@openssh.com     # ✅ SHA-512, Encrypt-then-MAC
hmac-sha2-256-etm@openssh.com     # ✅ SHA-256, Encrypt-then-MAC
hmac-sha2-512                     # ✅ SHA-512
hmac-sha2-256                     # ✅ SHA-256
```

**Obsoletos (inseguros):**
```
hmac-md5                          # ❌ MD5 está roto
hmac-sha1                         # ⚠️  SHA1 débil
hmac-ripemd160                    # ❌ Obsoleto
```

**Recomendación:**
```
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256
```

---

#### `KexAlgorithms` (Key Exchange)
**Algoritmos de intercambio de claves**

**Modernos (seguros):**
```
curve25519-sha256                 # ✅ Curva elíptica moderna
curve25519-sha256@libssh.org      # ✅ Variante libssh
diffie-hellman-group-exchange-sha256  # ✅ DH con SHA-256
diffie-hellman-group16-sha512     # ✅ DH grupo 16 (4096-bit)
diffie-hellman-group18-sha512     # ✅ DH grupo 18 (8192-bit)
```

**Obsoletos (inseguros):**
```
diffie-hellman-group1-sha1        # ❌ Grupo 1 (768-bit), SHA1
diffie-hellman-group14-sha1       # ⚠️  SHA1 débil
diffie-hellman-group-exchange-sha1 # ❌ SHA1
```

**Recomendación:**
```
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512
```

---

### Control de Acceso

#### `AllowUsers`
**Valores:** Lista de usuarios separados por espacios

Solo los usuarios listados pueden conectarse (lista blanca).

**Ejemplo:**
```
AllowUsers admin usuario1 usuario2@192.168.1.*
```

**Recomendación:** Usar en producción para limitar acceso

---

#### `AllowGroups`
**Valores:** Lista de grupos separados por espacios

Solo usuarios en estos grupos pueden conectarse.

**Ejemplo:**
```
AllowGroups ssh-users sudo
```

**Recomendación:** Más mantenible que AllowUsers

---

#### `DenyUsers` / `DenyGroups`
**Valores:** Lista de usuarios/grupos (lista negra)

Bloquea usuarios o grupos específicos.

**Ejemplo:**
```
DenyUsers root guest
DenyGroups noremote
```

**Recomendación:** Usar AllowUsers/AllowGroups en su lugar (lista blanca)

---

### Forwarding y Tunneling

#### `X11Forwarding`
**Valores:** `yes` | `no`

Permite reenvío de aplicaciones gráficas X11.

- **`yes`** ⚠️: Puede exponer display X11
- **`no`** ✅: Más seguro

**Recomendación:** `no` - A menos que sea necesario

---

#### `AllowTcpForwarding`
**Valores:** `yes` | `no` | `local` | `remote`

Permite port forwarding (tunneling).

- **`yes`** ⚠️: Permite pivoting en la red
- **`no`** ✅: Bloquea tunneling
- **`local`**: Solo forwarding local
- **`remote`**: Solo forwarding remoto

**Recomendación:** `no` - A menos que sea necesario para SFTP/SCP

---

#### `AllowAgentForwarding`
**Valores:** `yes` | `no`

Permite reenvío del agente SSH.

- **`yes`** ⚠️: Puede exponer claves privadas
- **`no`** ✅: Más seguro

**Recomendación:** `no`

---

### Logging y Auditoría

#### `LogLevel`
**Valores:** `QUIET` | `FATAL` | `ERROR` | `INFO` | `VERBOSE` | `DEBUG`

Nivel de detalle en logs.

- **`INFO`** ⚠️: Información básica
- **`VERBOSE`** ✅: Más detalles para auditoría
- **`DEBUG`**: Solo para troubleshooting

**Recomendación:** `VERBOSE` - Para auditoría completa

---

#### `SyslogFacility`
**Valores:** `DAEMON` | `USER` | `AUTH` | `LOCAL0-7`

Facility de syslog para logs.

**Recomendación:** `AUTH` - Logs de autenticación

---

### Claves del Host

#### `HostKey`
**Valores:** Ruta a archivo de clave privada

Define las claves privadas del servidor.

**Tipos de claves (por seguridad):**
1. **ED25519** ✅ - Más moderno, rápido, seguro (256-bit)
2. **RSA 4096+** ✅ - Ampliamente compatible (4096-bit mínimo)
3. **ECDSA** ⚠️ - Curvas NIST (posibles backdoors)
4. **DSA** ❌ - Obsoleto, inseguro

**Recomendación:**
```
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key
```

**Generar claves:**
```bash
sudo ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ""
sudo ssh-keygen -t rsa -b 4096 -f /etc/ssh/ssh_host_rsa_key -N ""
```

---

## 📊 Tabla Comparativa Rápida

| Parámetro | Débil ⚠️ | Endurecido ✅ |
|-----------|---------|---------------|
| PermitRootLogin | yes | no |
| PasswordAuthentication | yes | no |
| PubkeyAuthentication | yes | yes |
| ChallengeResponseAuthentication | no | yes (con 2FA) |
| MaxAuthTries | 6 | 3 |
| LoginGraceTime | 120 | 30 |
| ClientAliveInterval | 0 | 300 |
| ClientAliveCountMax | 3 | 2 |
| Ciphers | Incluye 3DES, CBC | Solo GCM, CTR, ChaCha20 |
| MACs | Incluye MD5, SHA1 | Solo SHA256+ |
| KexAlgorithms | Incluye DH-group1 | Solo Curve25519, DH-GEX |
| X11Forwarding | yes | no |
| AllowTcpForwarding | yes | no |
| LogLevel | INFO | VERBOSE |

---

## 🔗 Referencias

- [OpenSSH Manual](https://man.openbsd.org/sshd_config)
- [Mozilla SSH Guidelines](https://infosec.mozilla.org/guidelines/openssh)
- [CIS Benchmark](https://www.cisecurity.org/)
- [NIST Guidelines](https://csrc.nist.gov/)

---

**Última actualización:** Noviembre 2025
