#!/usr/bin/env python3
"""
HTTP Browser Simulation Script
Simula un usuario navegando y enviando credenciales por HTTP
"""

import requests
import time
import sys
from urllib.parse import urljoin

try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
except ImportError:
    console = None


def print_info(message):
    if console:
        console.print(f"[blue]ℹ️  {message}[/blue]")
    else:
        print(f"ℹ️  {message}")


def print_success(message):
    if console:
        console.print(f"[green]✅ {message}[/green]")
    else:
        print(f"✅ {message}")


def print_error(message):
    if console:
        console.print(f"[red]❌ {message}[/red]")
    else:
        print(f"❌ {message}")


def print_warning(message):
    if console:
        console.print(f"[yellow]⚠️  {message}[/yellow]")
    else:
        print(f"⚠️  {message}")


def browse_website(base_url, username, password):
    """Simula navegación y login en el sitio web"""
    
    print_info(f"Conectando a {base_url}...")
    
    # Crear sesión
    session = requests.Session()
    
    try:
        # 1. Obtener página principal
        print_info("Obteniendo página principal...")
        response = session.get(base_url, timeout=5)
        
        if response.status_code == 200:
            print_success(f"Página principal obtenida (Status: {response.status_code})")
        else:
            print_warning(f"Status inesperado: {response.status_code}")
        
        time.sleep(1)
        
        # 2. Obtener página de login
        login_url = urljoin(base_url, '/login/')
        print_info(f"Accediendo a página de login: {login_url}")
        
        response = session.get(login_url, timeout=5)
        
        if response.status_code == 200:
            print_success("Página de login obtenida")
        
        time.sleep(1)
        
        # 3. Enviar credenciales (¡EN TEXTO PLANO POR HTTP!)
        print_warning("⚠️  ENVIANDO CREDENCIALES POR HTTP (SIN CIFRAR)")
        print_info(f"Usuario: {username}")
        print_info(f"Contraseña: {'*' * len(password)}")
        
        # Datos del formulario
        login_data = {
            'username': username,
            'password': password,
        }
        
        # Enviar POST
        response = session.post(login_url, data=login_data, timeout=5, allow_redirects=True)
        
        if response.status_code == 200:
            if 'dashboard' in response.url or 'welcome' in response.text.lower():
                print_success("✅ Login exitoso!")
                print_info(f"Redirigido a: {response.url}")
            else:
                print_warning("Login completado pero sin redirección esperada")
        else:
            print_error(f"Error en login: Status {response.status_code}")
        
        time.sleep(1)
        
        # 4. Navegar por el sitio
        print_info("Navegando por el sitio...")
        dashboard_url = urljoin(base_url, '/dashboard/')
        
        try:
            response = session.get(dashboard_url, timeout=5)
            if response.status_code == 200:
                print_success("Dashboard accedido correctamente")
        except:
            pass
        
        print_success("\n🎯 Simulación completada")
        print_warning("\n⚠️  ADVERTENCIA: Todas las credenciales fueron enviadas en TEXTO PLANO")
        print_warning("    Un atacante en la red puede interceptar fácilmente esta información")
        
    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar al servidor")
        print_info("Verifica que el contenedor webserver esté corriendo")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print_error("Timeout al conectar con el servidor")
        sys.exit(1)
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        sys.exit(1)


def main():
    """Función principal"""
    
    if console:
        console.print(Panel.fit(
            "[bold cyan]HTTP Browser Simulation[/bold cyan]\n"
            "[yellow]⚠️  Demostración de tráfico HTTP sin cifrar[/yellow]",
            border_style="cyan"
        ))
    else:
        print("\n" + "="*60)
        print("HTTP Browser Simulation")
        print("⚠️  Demostración de tráfico HTTP sin cifrar")
        print("="*60 + "\n")
    
    # Configuración
    BASE_URL = "http://172.20.0.30"  # IP del webserver
    USERNAME = "admin"
    PASSWORD = "password123"
    
    print_info("Configuración:")
    print(f"  Servidor: {BASE_URL}")
    print(f"  Usuario: {USERNAME}")
    print(f"  Contraseña: {PASSWORD}")
    print()
    
    # Ejecutar simulación
    browse_website(BASE_URL, USERNAME, PASSWORD)
    
    print()
    print_info("Para ver el tráfico capturado:")
    print("  docker compose exec attacker cat /logs/intercepted_credentials.txt")
    print()


if __name__ == '__main__':
    main()
