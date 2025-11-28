# Guía de Instalación Multiplataforma

Esta guía te ayudará a instalar y ejecutar el proyecto en **Linux**, **macOS** y **Windows**.

---

## Linux (Ubuntu, Debian, Fedora, Arch, etc.)

### Requisitos

- Sistema operativo Linux (cualquier distribución)
- Acceso a terminal
- Conexión a Internet

### Instalación de Docker

#### Ubuntu/Debian

```bash
# Actualizar paquetes
sudo apt update

# Instalar dependencias
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Añadir clave GPG de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Añadir repositorio
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verificar instalación
docker --version
docker compose version
```

#### Fedora

```bash
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
```

#### Arch Linux

```bash
sudo pacman -S docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### Configurar Permisos (Opcional pero recomendado)

Para no usar `sudo` cada vez:

```bash
# Añadir tu usuario al grupo docker
sudo usermod -aG docker $USER

# Aplicar cambios (elige una opción)
# Opción 1: Cerrar sesión y volver a entrar
# Opción 2: Ejecutar
newgrp docker

# Verificar que funciona sin sudo
docker ps
```

### Ejecutar Demo

```bash
# Clonar repositorio
git clone https://github.com/gustavop-dev/crypthography_project.git
cd cryptography_project

# Ejecutar demo
bash scripts/demo_completa_cross_platform.sh
```

---

## macOS

### Requisitos

- macOS 10.15 (Catalina) o superior
- Procesador Intel o Apple Silicon (M1/M2/M3)
- 4 GB de RAM mínimo

### Instalación de Docker Desktop

#### Opción 1: Descarga directa

1. Ve a [Docker Desktop para Mac](https://docs.docker.com/desktop/install/mac-install/)
2. Descarga la versión para tu chip:
 - **Apple Silicon (M1/M2/M3):** Docker Desktop for Mac (Apple Silicon)
 - **Intel:** Docker Desktop for Mac (Intel)
3. Abre el archivo `.dmg` descargado
4. Arrastra Docker a la carpeta Applications
5. Abre Docker desde Applications
6. Acepta los permisos cuando se soliciten

#### Opción 2: Con Homebrew

```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Docker Desktop
brew install --cask docker

# Abrir Docker Desktop
open /Applications/Docker.app
```

### Verificar Instalación

```bash
# Espera a que Docker Desktop inicie (icono en la barra superior)
# Luego verifica:
docker --version
docker compose version
docker ps
```

### Ejecutar Demo

```bash
# Clonar repositorio
git clone https://github.com/gustavop-dev/crypthography_project.git
cd cryptography_project

# Ejecutar demo (NO necesitas sudo en macOS)
bash scripts/demo_completa_cross_platform.sh
```

**Nota:** En macOS **NO** uses `sudo` con Docker. Docker Desktop ya tiene los permisos necesarios.

---

## Windows

### Requisitos

- Windows 10 64-bit: Pro, Enterprise, o Education (Build 19041 o superior)
- O Windows 11
- WSL 2 habilitado
- Virtualización habilitada en BIOS

### Opción 1: Docker Desktop con WSL 2 (Recomendado)

#### Paso 1: Habilitar WSL 2

```powershell
# Abrir PowerShell como Administrador y ejecutar:

# Habilitar WSL
wsl --install

# Reiniciar el computador
```

Después de reiniciar:

```powershell
# Verificar versión de WSL
wsl --list --verbose

# Asegurarse de que sea WSL 2
wsl --set-default-version 2
```

#### Paso 2: Instalar Docker Desktop

1. Descarga [Docker Desktop para Windows](https://docs.docker.com/desktop/install/windows-install/)
2. Ejecuta el instalador
3. Asegúrate de marcar "Use WSL 2 instead of Hyper-V"
4. Reinicia cuando se solicite
5. Abre Docker Desktop
6. Acepta los términos de servicio

#### Paso 3: Configurar WSL 2

1. Abre Docker Desktop
2. Ve a Settings → General
3. Asegúrate de que "Use the WSL 2 based engine" esté marcado
4. Ve a Settings → Resources → WSL Integration
5. Habilita integración con tu distribución de Linux (Ubuntu recomendado)

#### Paso 4: Instalar Git Bash (para ejecutar scripts .sh)

1. Descarga [Git para Windows](https://git-scm.com/download/win)
2. Instala con opciones por defecto
3. Abre "Git Bash" desde el menú de inicio

### Opción 2: Usar WSL 2 directamente

Si prefieres trabajar completamente en Linux:

```bash
# En PowerShell como Administrador
wsl --install -d Ubuntu

# Reiniciar computador

# Abrir Ubuntu desde el menú de inicio
# Configurar usuario y contraseña

# Dentro de Ubuntu WSL, seguir instrucciones de Linux
```

### Ejecutar Demo en Windows

#### Con Git Bash:

```bash
# Abrir Git Bash
# Clonar repositorio
git clone https://github.com/gustavop-dev/crypthography_project.git
cd cryptography_project

# Ejecutar demo
bash scripts/demo_completa_cross_platform.sh
```

#### Con WSL 2 (Ubuntu):

```bash
# Abrir Ubuntu desde el menú de inicio
# Clonar repositorio
git clone https://github.com/gustavop-dev/crypthography_project.git
cd cryptography_project

# Ejecutar demo
bash scripts/demo_completa_cross_platform.sh
```

**Nota:** En Windows con Docker Desktop **NO** uses `sudo`. No existe en Git Bash y no es necesario.

---

## Troubleshooting Multiplataforma

### Linux

**Problema:** "permission denied" al ejecutar docker

```bash
# Solución: Añadir usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

**Problema:** Docker no inicia

```bash
# Solución: Iniciar servicio
sudo systemctl start docker
sudo systemctl enable docker
```

### macOS

**Problema:** "Cannot connect to Docker daemon"

```
Solución:
1. Abre Docker Desktop desde Applications
2. Espera a que el icono de Docker en la barra superior deje de animarse
3. Intenta de nuevo
```

**Problema:** "Docker Desktop requires a newer macOS version"

```
Solución:
- Actualiza macOS a 10.15 (Catalina) o superior
- O usa Docker Toolbox (versión legacy)
```

### Windows

**Problema:** "WSL 2 installation is incomplete"

```powershell
# Solución: En PowerShell como Administrador
wsl --update
wsl --set-default-version 2
```

**Problema:** "Hardware assisted virtualization is not enabled"

```
Solución:
1. Reiniciar computador
2. Entrar a BIOS (F2, F10, o DEL al iniciar)
3. Buscar "Virtualization Technology" o "Intel VT-x" o "AMD-V"
4. Habilitarlo
5. Guardar y salir
```

**Problema:** "Docker Desktop starting..." se queda cargando

```
Solución:
1. Cerrar Docker Desktop completamente
2. Abrir PowerShell como Administrador
3. Ejecutar: wsl --shutdown
4. Abrir Docker Desktop de nuevo
```

---

## Verificación de Instalación

En **cualquier sistema operativo**, ejecuta:

```bash
# Verificar Docker
docker --version
# Debe mostrar: Docker version 20.10+ o superior

# Verificar Docker Compose
docker compose version
# Debe mostrar: Docker Compose version 2.0+ o superior

# Verificar que Docker está corriendo
docker ps
# Debe mostrar una tabla (puede estar vacía)

# Probar un contenedor simple
docker run hello-world
# Debe mostrar: "Hello from Docker!"
```

Si todos estos comandos funcionan, **estás listo para ejecutar la demo**.

---

## Instalación de Dependencias Python (Solo para SSH Hardening)

**IMPORTANTE:** La demo MitM NO requiere Python en tu máquina (todo corre en Docker).

Solo necesitas instalar Python si quieres usar los scripts de **SSH Hardening**:

### Linux/macOS

```bash
# Verificar Python
python3 --version
# Debe ser 3.10 o superior

# Crear entorno virtual (opcional pero recomendado)
cd cryptography_project
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Windows

```bash
# En PowerShell o Git Bash
python --version
# Debe ser 3.10 o superior

# Crear entorno virtual
cd cryptography_project
python -m venv venv
venv\Scripts\activate  # PowerShell
# O
source venv/Scripts/activate  # Git Bash

# Instalar dependencias
pip install -r requirements.txt
```

**Nota:** Si solo vas a ejecutar la demo MitM, puedes omitir completamente esta sección.

---

## Ejecutar la Demo

Una vez Docker esté instalado y funcionando:

```bash
# 1. Clonar el repositorio
git clone https://github.com/gustavop-dev/crypthography_project.git
cd cryptography_project

# 2. Ejecutar demo multiplataforma
bash scripts/demo_completa_cross_platform.sh
```

El script detectará automáticamente tu sistema operativo y usará los comandos apropiados.

---

## Notas Importantes

### Linux
- Puede requerir `sudo` si no estás en el grupo docker
- El script lo detecta automáticamente

### macOS
- **NO** uses `sudo` con Docker Desktop
- Asegúrate de que Docker Desktop esté corriendo antes de ejecutar

### Windows
- **NO** uses `sudo` (no existe en Windows)
- Usa Git Bash o WSL 2 para ejecutar scripts `.sh`
- Asegúrate de que Docker Desktop esté corriendo

---

## Soporte

Si tienes problemas:

1. Revisa la sección de Troubleshooting arriba
2. Verifica que Docker esté corriendo: `docker ps`
3. Consulta los logs: `docker compose logs`
4. Revisa la [documentación oficial de Docker](https://docs.docker.com/)

---

## Recursos Adicionales

- [Docker Desktop para Mac](https://docs.docker.com/desktop/install/mac-install/)
- [Docker Desktop para Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Docker Engine para Linux](https://docs.docker.com/engine/install/)
- [WSL 2 Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
