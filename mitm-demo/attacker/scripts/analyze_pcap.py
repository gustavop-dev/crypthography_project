#!/usr/bin/env python3
"""
PCAP Analysis Script
Analiza archivos PCAP y extrae información relevante
"""

import sys
import argparse
from collections import defaultdict

try:
    from scapy.all import rdpcap, TCP, Raw, IP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("❌ Scapy no está instalado")
    sys.exit(1)

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class PCAPAnalyzer:
    def __init__(self, pcap_file):
        self.pcap_file = pcap_file
        self.packets = []
        self.stats = {
            'total': 0,
            'tcp': 0,
            'udp': 0,
            'http': 0,
            'https': 0,
            'other': 0
        }
        self.http_requests = []
        self.credentials = []
        
    def load_pcap(self):
        """Carga el archivo PCAP"""
        try:
            print(f"📂 Cargando {self.pcap_file}...")
            self.packets = rdpcap(self.pcap_file)
            self.stats['total'] = len(self.packets)
            print(f"✅ {self.stats['total']} paquetes cargados")
            return True
        except Exception as e:
            print(f"❌ Error cargando PCAP: {e}")
            return False
    
    def analyze_packets(self):
        """Analiza los paquetes"""
        print("\n🔍 Analizando paquetes...")
        
        for packet in self.packets:
            # Contar por protocolo
            if packet.haslayer(TCP):
                self.stats['tcp'] += 1
                
                # Detectar HTTP/HTTPS por puerto
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    self.stats['http'] += 1
                    self.analyze_http_packet(packet)
                elif packet[TCP].dport == 443 or packet[TCP].sport == 443:
                    self.stats['https'] += 1
            elif packet.haslayer('UDP'):
                self.stats['udp'] += 1
            else:
                self.stats['other'] += 1
        
        print("✅ Análisis completado")
    
    def analyze_http_packet(self, packet):
        """Analiza un paquete HTTP"""
        if packet.haslayer(Raw):
            try:
                payload = packet[Raw].load.decode('utf-8', errors='ignore')
                
                # Detectar HTTP request
                if payload.startswith(('GET', 'POST', 'PUT', 'DELETE', 'HEAD')):
                    lines = payload.split('\r\n')
                    method_line = lines[0]
                    
                    self.http_requests.append({
                        'src': packet[IP].src,
                        'dst': packet[IP].dst,
                        'method': method_line,
                        'payload': payload
                    })
                    
                    # Buscar credenciales en POST
                    if method_line.startswith('POST'):
                        self.extract_credentials(payload, packet[IP].src, packet[IP].dst)
            except:
                pass
    
    def extract_credentials(self, payload, src_ip, dst_ip):
        """Extrae credenciales del payload"""
        import re
        
        patterns = {
            'username': r'username=([^&\s]+)',
            'user': r'user=([^&\s]+)',
            'email': r'email=([^&\s]+)',
            'password': r'password=([^&\s]+)',
            'passwd': r'passwd=([^&\s]+)',
            'pwd': r'pwd=([^&\s]+)',
        }
        
        found = {}
        for key, pattern in patterns.items():
            matches = re.findall(pattern, payload, re.IGNORECASE)
            if matches:
                from urllib.parse import unquote
                found[key] = unquote(matches[0])
        
        if found:
            self.credentials.append({
                'src': src_ip,
                'dst': dst_ip,
                'data': found
            })
    
    def display_results(self):
        """Muestra los resultados del análisis"""
        print("\n" + "="*60)
        print("📊 RESULTADOS DEL ANÁLISIS")
        print("="*60)
        
        # Estadísticas generales
        print(f"\n📈 Estadísticas Generales:")
        print(f"  Total de paquetes: {self.stats['total']}")
        print(f"  TCP: {self.stats['tcp']}")
        print(f"  UDP: {self.stats['udp']}")
        print(f"  HTTP (puerto 80): {self.stats['http']}")
        print(f"  HTTPS (puerto 443): {self.stats['https']}")
        print(f"  Otros: {self.stats['other']}")
        
        # HTTP Requests
        if self.http_requests:
            print(f"\n🌐 HTTP Requests encontrados: {len(self.http_requests)}")
            for i, req in enumerate(self.http_requests[:10], 1):  # Mostrar primeros 10
                print(f"\n  Request #{i}:")
                print(f"    {req['src']} → {req['dst']}")
                print(f"    {req['method']}")
        
        # Credenciales
        if self.credentials:
            print(f"\n🔓 CREDENCIALES ENCONTRADAS: {len(self.credentials)}")
            print("="*60)
            
            for i, cred in enumerate(self.credentials, 1):
                print(f"\nCredencial #{i}:")
                print(f"  Origen: {cred['src']}")
                print(f"  Destino: {cred['dst']}")
                print(f"  Datos:")
                for key, value in cred['data'].items():
                    print(f"    {key}: {value}")
            
            print("="*60)
        else:
            print(f"\n✅ No se encontraron credenciales en texto plano")
        
        # Recomendaciones
        print(f"\n💡 Recomendaciones:")
        if self.stats['http'] > 0:
            print(f"  ⚠️  Se detectaron {self.stats['http']} paquetes HTTP (sin cifrar)")
            print(f"     Recomendación: Usar HTTPS para proteger el tráfico")
        
        if self.credentials:
            print(f"  🔴 Se encontraron credenciales en texto plano")
            print(f"     Recomendación: NUNCA enviar credenciales por HTTP")
        
        if self.stats['https'] > 0:
            print(f"  ✅ Se detectaron {self.stats['https']} paquetes HTTPS (cifrados)")
            print(f"     El contenido está protegido")
    
    def generate_report(self, output_file):
        """Genera un reporte en archivo"""
        try:
            with open(output_file, 'w') as f:
                f.write("="*60 + "\n")
                f.write("PCAP ANALYSIS REPORT\n")
                f.write(f"File: {self.pcap_file}\n")
                f.write("="*60 + "\n\n")
                
                f.write("STATISTICS\n")
                f.write("-"*60 + "\n")
                for key, value in self.stats.items():
                    f.write(f"{key}: {value}\n")
                
                f.write("\n\nHTTP REQUESTS\n")
                f.write("-"*60 + "\n")
                for req in self.http_requests:
                    f.write(f"\n{req['src']} → {req['dst']}\n")
                    f.write(f"{req['method']}\n")
                
                f.write("\n\nCREDENTIALS FOUND\n")
                f.write("-"*60 + "\n")
                for cred in self.credentials:
                    f.write(f"\nSource: {cred['src']}\n")
                    f.write(f"Destination: {cred['dst']}\n")
                    f.write("Data:\n")
                    for key, value in cred['data'].items():
                        f.write(f"  {key}: {value}\n")
                
                f.write("\n" + "="*60 + "\n")
            
            print(f"\n💾 Reporte guardado en: {output_file}")
        except Exception as e:
            print(f"❌ Error guardando reporte: {e}")


def main():
    parser = argparse.ArgumentParser(description='PCAP Analysis Tool')
    parser.add_argument('pcap_file', help='PCAP file to analyze')
    parser.add_argument('-o', '--output', help='Output report file')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🔍 PCAP ANALYZER")
    print("Proyecto de Criptografía - UNAL Medellín")
    print("="*60 + "\n")
    
    analyzer = PCAPAnalyzer(args.pcap_file)
    
    if not analyzer.load_pcap():
        sys.exit(1)
    
    analyzer.analyze_packets()
    analyzer.display_results()
    
    if args.output:
        analyzer.generate_report(args.output)
    
    print("\n✅ Análisis completado\n")


if __name__ == '__main__':
    main()
