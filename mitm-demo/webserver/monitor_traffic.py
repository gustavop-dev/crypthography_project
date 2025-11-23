#!/usr/bin/env python3
"""
HTTP Traffic Monitor - Webserver Side
Monitorea y muestra tráfico HTTP en tiempo real
"""

import subprocess
import re
import sys
from datetime import datetime

def print_header():
    print("\n" + "="*60)
    print("🕵️  HTTP TRAFFIC MONITOR")
    print("Proyecto de Criptografía - UNAL Medellín")
    print("="*60)
    print("\n🎯 Monitoreando tráfico HTTP en el servidor...")
    print("   Capturando requests desde tu navegador")
    print("\n⚠️  Presiona Ctrl+C para detener\n")

def extract_credentials(data):
    """Extrae credenciales del POST data"""
    credentials = {}
    
    # Buscar username
    username_match = re.search(r'username=([^&\s]+)', data)
    if username_match:
        credentials['username'] = username_match.group(1)
    
    # Buscar password
    password_match = re.search(r'password=([^&\s]+)', data)
    if password_match:
        credentials['password'] = password_match.group(1)
    
    return credentials

def monitor_traffic():
    """Monitorea el tráfico HTTP"""
    print_header()
    
    try:
        # Instalar tcpdump si no está
        subprocess.run(['apt-get', 'update', '-qq'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['apt-get', 'install', '-y', 'tcpdump', '-qq'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Iniciar captura con más bytes
        process = subprocess.Popen(
            ['tcpdump', '-i', 'any', '-A', '-s', '65535', 'tcp port 80'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
            bufsize=1
        )
        
        buffer = []
        in_post = False
        post_lines = []
        
        for line in process.stdout:
            buffer.append(line)
            
            # Detectar POST request
            if 'POST' in line and '/login/' in line:
                in_post = True
                post_lines = []
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"\n📡 [{timestamp}] HTTP POST Request detectado")
                print(f"   Ruta: /login/")
            
            # Acumular líneas del POST
            if in_post:
                post_lines.append(line)
                
                # Buscar credenciales en cualquier línea acumulada
                full_text = ''.join(post_lines)
                credentials = extract_credentials(full_text)
                
                if credentials and len(credentials) >= 2:
                    print("\n" + "="*60)
                    print("🔓 CREDENCIALES INTERCEPTADAS!")
                    print("="*60)
                    
                    if 'username' in credentials:
                        print(f"   Usuario: {credentials['username']}")
                    if 'password' in credentials:
                        print(f"   Contraseña: {credentials['password']}")
                    
                    print("="*60 + "\n")
                    
                    in_post = False
                    post_lines = []
                    buffer = []
                
                # Timeout si acumulamos muchas líneas sin encontrar nada
                if len(post_lines) > 30:
                    in_post = False
                    post_lines = []
            
            # Limpiar buffer si es muy grande
            if len(buffer) > 100:
                buffer = buffer[-50:]
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitoreo detenido")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    monitor_traffic()
