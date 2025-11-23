#!/usr/bin/env python3
"""
Traffic Capture Script
Captura tráfico de red y guarda en formato PCAP
"""

import sys
import argparse
import time
from datetime import datetime
from scapy.all import sniff, wrpcap, conf

try:
    from rich.console import Console
    from rich.live import Live
    from rich.table import Table
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class TrafficCapture:
    def __init__(self, interface='eth0', filter_str='', output_file=None):
        self.interface = interface
        self.filter_str = filter_str
        self.output_file = output_file or f"/captures/traffic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
        self.packets = []
        self.packet_count = 0
        self.http_count = 0
        self.https_count = 0
        
    def packet_callback(self, packet):
        """Callback para cada paquete capturado"""
        self.packets.append(packet)
        self.packet_count += 1
        
        # Contar paquetes HTTP/HTTPS
        if packet.haslayer('TCP'):
            if packet['TCP'].dport == 80 or packet['TCP'].sport == 80:
                self.http_count += 1
            elif packet['TCP'].dport == 443 or packet['TCP'].sport == 443:
                self.https_count += 1
        
        # Mostrar progreso cada 10 paquetes
        if self.packet_count % 10 == 0:
            self.print_stats()
    
    def print_stats(self):
        """Muestra estadísticas de captura"""
        if RICH_AVAILABLE:
            table = Table(title="Estadísticas de Captura")
            table.add_column("Métrica", style="cyan")
            table.add_column("Valor", style="green")
            
            table.add_row("Total Paquetes", str(self.packet_count))
            table.add_row("HTTP (puerto 80)", str(self.http_count))
            table.add_row("HTTPS (puerto 443)", str(self.https_count))
            table.add_row("Archivo", self.output_file)
            
            console.clear()
            console.print(table)
        else:
            print(f"\r📊 Paquetes: {self.packet_count} | HTTP: {self.http_count} | HTTPS: {self.https_count}", end='')
    
    def start_capture(self, count=0):
        """Inicia la captura de tráfico"""
        print(f"\n🎯 Iniciando captura de tráfico...")
        print(f"   Interfaz: {self.interface}")
        print(f"   Filtro: {self.filter_str or 'ninguno'}")
        print(f"   Archivo: {self.output_file}")
        print(f"   Paquetes: {'infinito' if count == 0 else count}")
        print(f"\n⚠️  Presiona Ctrl+C para detener\n")
        
        try:
            # Deshabilitar verbose de Scapy
            conf.verb = 0
            
            # Capturar paquetes
            sniff(
                iface=self.interface,
                filter=self.filter_str,
                prn=self.packet_callback,
                count=count,
                store=True
            )
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Captura detenida por el usuario")
        except Exception as e:
            print(f"\n❌ Error durante la captura: {e}")
        finally:
            self.save_capture()
    
    def save_capture(self):
        """Guarda los paquetes capturados"""
        if self.packets:
            print(f"\n💾 Guardando {len(self.packets)} paquetes en {self.output_file}...")
            try:
                wrpcap(self.output_file, self.packets)
                print(f"✅ Captura guardada exitosamente")
                print(f"\n📊 Resumen:")
                print(f"   Total paquetes: {self.packet_count}")
                print(f"   HTTP: {self.http_count}")
                print(f"   HTTPS: {self.https_count}")
                print(f"\n📁 Analizar con:")
                print(f"   wireshark {self.output_file}")
                print(f"   tshark -r {self.output_file}")
                print(f"   python3 /scripts/analyze_pcap.py {self.output_file}")
            except Exception as e:
                print(f"❌ Error guardando captura: {e}")
        else:
            print("\n⚠️  No se capturaron paquetes")


def main():
    parser = argparse.ArgumentParser(description='Traffic Capture Tool')
    parser.add_argument('-i', '--interface', default='eth0', help='Network interface')
    parser.add_argument('-f', '--filter', default='', help='BPF filter (e.g., "tcp port 80")')
    parser.add_argument('-o', '--output', help='Output PCAP file')
    parser.add_argument('-c', '--count', type=int, default=0, help='Number of packets to capture (0=infinite)')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("📡 TRAFFIC CAPTURE TOOL")
    print("Proyecto de Criptografía - UNAL Medellín")
    print("="*60)
    
    capture = TrafficCapture(
        interface=args.interface,
        filter_str=args.filter,
        output_file=args.output
    )
    
    capture.start_capture(count=args.count)


if __name__ == '__main__':
    main()
