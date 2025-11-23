# Demo Interactiva - MitM Attack

## 🎬 Workflow Recomendado para Presentación

### Preparación (Antes de la Demo)

```bash
cd ~/unal/cryptography_project/mitm-demo
sudo docker compose up -d
```

---

## 📺 Presentación en Vivo

### Paso 1: Mostrar la Aplicación Web Vulnerable

**Abrir en navegador:** http://localhost:8080

**Explicar:**
- ⚠️ Banner rojo: "HTTP (Unencrypted)"
- Esta es una aplicación web vulnerable
- Usa HTTP sin cifrado
- Vamos a demostrar cómo un atacante puede interceptar credenciales

**Navegar por la interfaz:**
- Página principal
- Formulario de login
- Mostrar las advertencias de seguridad

---

### Paso 2: Configurar el Atacante

**Terminal 1 - Mostrar en pantalla:**

```bash
# Iniciar interceptación HTTP
sudo docker compose exec attacker python3 /scripts/intercept_http.py
```

**Explicar:**
- El atacante está escuchando todo el tráfico HTTP en la red
- Esperando capturar credenciales en texto plano

---

### Paso 3: Simular la Víctima

**Terminal 2 - Ejecutar:**

```bash
# La víctima navega y envía credenciales
sudo docker compose exec victim python3 /scripts/browse_http.py
```

**Explicar:**
- Esta víctima está en la misma red
- No sabe que está siendo interceptada
- Envía sus credenciales por HTTP

---

### Paso 4: ¡Credenciales Interceptadas!

**En Terminal 1 aparecerá:**

```
📡 HTTP Request #2
172.20.0.10 → 172.20.0.30
POST /login/ HTTP/1.1

╔════════════════════════════════════════╗
║ 🔓 CREDENCIALES INTERCEPTADAS!         ║
║                                        ║
║ username: admin                        ║
║ password: password123                  ║
╚════════════════════════════════════════╝

💾 Guardado en: /logs/intercepted_credentials.txt
```

**Explicar:**
- ✅ El atacante capturó las credenciales en texto plano
- ✅ Usuario y contraseña completamente visibles
- ⚠️ Esto es posible porque se usó HTTP sin cifrado

---

### Paso 5: Mostrar el Archivo de Log

```bash
sudo docker compose exec attacker cat /logs/intercepted_credentials.txt
```

**Explicar:**
- Todas las credenciales quedan guardadas
- El atacante tiene acceso completo

---

### Paso 6: Demostrar ARP Spoofing (Opcional)

**Terminal 3:**

```bash
# Ver tabla ARP antes del ataque
sudo docker compose exec victim arp -a
```

**Terminal 4:**

```bash
# Iniciar ARP spoofing
sudo docker compose exec attacker python3 /scripts/arp_spoof.py \
    --victim 172.20.0.10 --gateway 172.20.0.1
```

**Terminal 3 de nuevo:**

```bash
# Ver tabla ARP después del ataque
sudo docker compose exec victim arp -a
```

**Explicar:**
- El atacante se posicionó como "man in the middle"
- Modificó la tabla ARP de la víctima
- Todo el tráfico pasa por el atacante

---

## 🎯 Variante: Login Interactivo en Vivo

Si quieres hacer el login tú mismo en el navegador mientras muestras la interceptación:

### Opción A: Dos Pantallas

**Pantalla 1:** Navegador con http://localhost:8080

**Pantalla 2:** Terminal con interceptación corriendo

**Problema:** Tu tráfico NO será interceptado porque no pasa por el contenedor attacker.

**Solución:** Explica que estás mostrando la interfaz, pero la interceptación real se hace con el script de la víctima.

### Opción B: Captura de Tráfico

```bash
# Capturar TODO el tráfico mientras haces login
sudo docker compose exec attacker tcpdump -i eth0 -A 'tcp port 80' &

# Luego hacer login desde el navegador o script
# Detener con Ctrl+C

# Analizar la captura
sudo docker compose exec attacker cat /captures/traffic.pcap
```

---

## 📊 Flujo Completo para Presentación

```
1. [Navegador] Mostrar web vulnerable
   ↓
2. [Terminal 1] Iniciar interceptación
   ↓
3. [Terminal 2] Víctima envía credenciales
   ↓
4. [Terminal 1] ¡Credenciales capturadas!
   ↓
5. [Terminal] Mostrar logs guardados
   ↓
6. [Explicar] Contramedidas (HTTPS, HSTS, etc.)
```

---

## 🎬 Script de Presentación

**Inicio:**
> "Vamos a demostrar cómo un atacante puede interceptar credenciales en una red cuando se usa HTTP sin cifrado."

**Mostrar Web:**
> "Esta es una aplicación web típica con un formulario de login. Noten el banner rojo que advierte que es HTTP sin cifrar."

**Iniciar Atacante:**
> "El atacante está en la misma red y comienza a escuchar todo el tráfico HTTP."

**Víctima Navega:**
> "La víctima, sin saber que está siendo interceptada, ingresa sus credenciales y hace login."

**Mostrar Captura:**
> "Como pueden ver, el atacante capturó las credenciales en texto plano. Usuario: admin, Contraseña: password123."

**Conclusión:**
> "Esto demuestra por qué es crítico usar HTTPS. Con HTTPS, todo este tráfico estaría cifrado y el atacante solo vería datos ilegibles."

---

## 🛡️ Contramedidas a Mencionar

1. **HTTPS/TLS** - Cifrado de extremo a extremo
2. **HSTS** - Forzar HTTPS siempre
3. **Certificate Pinning** - Prevenir MitM con certificados falsos
4. **VPN** - Túnel cifrado
5. **Autenticación Multifactor** - Protección adicional
6. **Detección de ARP Spoofing** - Herramientas de monitoreo

---

**Universidad Nacional de Colombia - Sede Medellín**  
**Criptografía y Seguridad - Grupo 6**
