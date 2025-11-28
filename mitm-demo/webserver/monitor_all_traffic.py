#!/usr/bin/env python3
"""
HTTP/HTTPS Traffic Monitor - Webserver Side
Muestra tráfico HTTP (texto plano) y HTTPS (cifrado)
"""

import subprocess
import re
import sys
from datetime import datetime

def print_header():
    print("\n" + "="*60)
    print("  HTTP/HTTPS TRAFFIC MONITOR")
    print("Proyecto de Criptografía - UNAL Medellín")
    print("="*60)
    print("\n Monitoreando TODO el tráfico web...")
    print("   • HTTP (puerto 80): Texto plano visible")
    print("   • HTTPS (puerto 443): Datos cifrados")
    print("\n  Presiona Ctrl+C para detener\n")

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

def is_tls_handshake(line):
    """Detecta si es un handshake TLS/SSL"""
    # TLS handshake contiene bytes específicos
    tls_indicators = [
        '0x0000:',  # Inicio de paquete hex
        '16 03',    # TLS handshake
        'Client Hello',
        'Server Hello',
        'Certificate',
    ]
    return any(indicator in line for indicator in tls_indicators)

def is_encrypted_data(line):
    """Detecta datos cifrados (muchos caracteres no imprimibles)"""
    # Contar caracteres no ASCII o de control
    if len(line) < 10:
        return False
    
    non_printable = sum(1 for c in line if ord(c) < 32 or ord(c) > 126)
    ratio = non_printable / len(line)
    
    return ratio > 0.3  # Más del 30% no imprimible = probablemente cifrado

def monitor_traffic():
    """Monitorea el tráfico HTTP y HTTPS"""
    print_header()
    
    try:
        # Instalar tcpdump si no está
        subprocess.run(['apt-get', 'update', '-qq'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['apt-get', 'install', '-y', 'tcpdump', '-qq'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Iniciar captura de HTTP y HTTPS
        # Usar filtro más específico para evitar falsos positivos
        process = subprocess.Popen(
            ['tcpdump', '-i', 'any', '-A', '-s', '65535', '-l', 
             'tcp port 80 or tcp port 443'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
            bufsize=1
        )
        
        buffer = []
        in_http_post = False
        in_https_traffic = False
        post_lines = []
        https_packet_count = 0
        
        for line in process.stdout:
            buffer.append(line)
            
            # Detectar tráfico HTTPS (solo si hay handshake TLS o datos cifrados reales)
            if '.443' in line or ':443' in line:
                # Verificar que realmente hay datos TLS/SSL
                if (is_tls_handshake(line) or 
                    (is_encrypted_data(line) and len(line) > 30)):
                    if not in_https_traffic:
                        in_https_traffic = True
                        https_packet_count = 0
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        print(f"\n [{timestamp}] Tráfico HTTPS detectado")
                        print(f"   Puerto: 443 (HTTPS)")
            
            # Mostrar datos cifrados de HTTPS
            if in_https_traffic:
                https_packet_count += 1
                
                # Buscar líneas con datos binarios/cifrados
                if is_encrypted_data(line) or is_tls_handshake(line):
                    if https_packet_count == 1:
                        print("\n" + "="*60)
                        print(" DATOS CIFRADOS DETECTADOS")
                        print("="*60)
                        print("   Ejemplo de datos cifrados (ilegibles):")
                        print("   " + "" * 50)
                        
                        # Mostrar algunos bytes en hexadecimal
                        hex_sample = ' '.join([f'{ord(c):02x}' if ord(c) < 128 else 'xx' 
                                              for c in line[:20] if c.isprintable() == False])
                        if hex_sample:
                            print(f"   Hex: {hex_sample}...")
                        
                        print("\n    Las credenciales están CIFRADAS")
                        print("    Imposible leer el contenido sin la clave")
                        print("="*60 + "\n")
                
                # Resetear después de algunos paquetes
                if https_packet_count > 20:
                    in_https_traffic = False
                    https_packet_count = 0
            
            # Detectar POST HTTP (texto plano) - solo puerto 80
            if 'POST' in line and '/login/' in line:
                # Verificar que NO es puerto 443
                if '.443' not in line and ':443' not in line:
                    in_http_post = True
                    post_lines = []
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"\n [{timestamp}] HTTP POST Request detectado")
                    print(f"   Ruta: /login/ (Puerto 80 - SIN CIFRAR)")
            
            # Acumular líneas del POST HTTP
            if in_http_post:
                post_lines.append(line)
                
                # Buscar credenciales en texto plano
                full_text = ''.join(post_lines)
                credentials = extract_credentials(full_text)
                
                if credentials and len(credentials) >= 2:
                    print("\n" + "="*60)
                    print(" CREDENCIALES INTERCEPTADAS (TEXTO PLANO)")
                    print("="*60)
                    
                    if 'username' in credentials:
                        print(f"   Usuario: {credentials['username']}")
                    if 'password' in credentials:
                        print(f"   Contraseña: {credentials['password']}")
                    
                    print("\n    Completamente visible para el atacante")
                    print("    Sin protección alguna")
                    print("="*60 + "\n")
                    
                    in_http_post = False
                    post_lines = []
                    buffer = []
                
                # Timeout
                if len(post_lines) > 30:
                    in_http_post = False
                    post_lines = []
            
            # Limpiar buffer
            if len(buffer) > 100:
                buffer = buffer[-50:]
        
    except KeyboardInterrupt:
        print("\n\n  Monitoreo detenido")
        sys.exit(0)
    except Exception as e:
        print(f"\n Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    monitor_traffic()
