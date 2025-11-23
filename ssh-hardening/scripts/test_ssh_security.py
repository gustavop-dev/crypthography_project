#!/usr/bin/env python3
"""
SSH Security Testing Script
Proyecto de Criptografía - UNAL Medellín - Grupo 6

Tests automatizados para verificar la configuración de seguridad SSH
"""

import subprocess
import sys
import socket
import time
from typing import List, Tuple
from dataclasses import dataclass
from enum import Enum


class TestResult(Enum):
    PASS = "✅ PASS"
    FAIL = "❌ FAIL"
    SKIP = "⏭️  SKIP"
    WARN = "⚠️  WARN"


@dataclass
class Test:
    name: str
    description: str
    result: TestResult
    message: str


class SSHSecurityTester:
    def __init__(self, host: str = "localhost", port: int = 22):
        self.host = host
        self.port = port
        self.tests: List[Test] = []
        self.config = {}
        
    def get_ssh_config(self) -> dict:
        """Obtiene configuración SSH"""
        try:
            result = subprocess.run(
                ['sudo', 'sshd', '-T'],
                capture_output=True,
                text=True,
                check=True
            )
            config = {}
            for line in result.stdout.split('\n'):
                if line.strip():
                    parts = line.split(None, 1)
                    if len(parts) == 2:
                        config[parts[0].lower()] = parts[1].strip()
            return config
        except Exception as e:
            print(f"❌ Error obteniendo configuración: {e}")
            return {}
    
    def test_root_login_disabled(self):
        """Test: Root login debe estar deshabilitado"""
        value = self.config.get('permitrootlogin', 'yes')
        
        if value == 'no':
            self.tests.append(Test(
                "Root Login Disabled",
                "PermitRootLogin debe ser 'no'",
                TestResult.PASS,
                f"PermitRootLogin = {value}"
            ))
        else:
            self.tests.append(Test(
                "Root Login Disabled",
                "PermitRootLogin debe ser 'no'",
                TestResult.FAIL,
                f"PermitRootLogin = {value} (debería ser 'no')"
            ))
    
    def test_password_auth_disabled(self):
        """Test: Autenticación por contraseña debe estar deshabilitada"""
        value = self.config.get('passwordauthentication', 'yes')
        
        if value == 'no':
            self.tests.append(Test(
                "Password Auth Disabled",
                "PasswordAuthentication debe ser 'no'",
                TestResult.PASS,
                f"PasswordAuthentication = {value}"
            ))
        else:
            self.tests.append(Test(
                "Password Auth Disabled",
                "PasswordAuthentication debe ser 'no'",
                TestResult.FAIL,
                f"PasswordAuthentication = {value} (debería ser 'no')"
            ))
    
    def test_pubkey_auth_enabled(self):
        """Test: Autenticación por clave pública debe estar habilitada"""
        value = self.config.get('pubkeyauthentication', 'yes')
        
        if value == 'yes':
            self.tests.append(Test(
                "Public Key Auth Enabled",
                "PubkeyAuthentication debe ser 'yes'",
                TestResult.PASS,
                f"PubkeyAuthentication = {value}"
            ))
        else:
            self.tests.append(Test(
                "Public Key Auth Enabled",
                "PubkeyAuthentication debe ser 'yes'",
                TestResult.FAIL,
                f"PubkeyAuthentication = {value} (debería ser 'yes')"
            ))
    
    def test_max_auth_tries(self):
        """Test: Máximo de intentos de autenticación"""
        value = int(self.config.get('maxauthtries', '6'))
        
        if value <= 3:
            self.tests.append(Test(
                "Max Auth Tries",
                "MaxAuthTries debe ser <= 3",
                TestResult.PASS,
                f"MaxAuthTries = {value}"
            ))
        else:
            self.tests.append(Test(
                "Max Auth Tries",
                "MaxAuthTries debe ser <= 3",
                TestResult.FAIL,
                f"MaxAuthTries = {value} (debería ser <= 3)"
            ))
    
    def test_client_alive_interval(self):
        """Test: Timeout de sesión configurado"""
        interval = int(self.config.get('clientaliveinterval', '0'))
        count_max = int(self.config.get('clientalivecountmax', '3'))
        
        if interval > 0:
            timeout_minutes = (interval * count_max) / 60
            self.tests.append(Test(
                "Session Timeout",
                "ClientAliveInterval debe estar configurado",
                TestResult.PASS,
                f"Timeout: {timeout_minutes:.1f} minutos"
            ))
        else:
            self.tests.append(Test(
                "Session Timeout",
                "ClientAliveInterval debe estar configurado",
                TestResult.FAIL,
                "Sin timeout de sesión configurado"
            ))
    
    def test_strong_ciphers(self):
        """Test: Solo algoritmos de cifrado fuertes"""
        ciphers = self.config.get('ciphers', '').lower()
        
        weak_ciphers = ['3des', 'arcfour', 'blowfish', 'cast128']
        found_weak = [w for w in weak_ciphers if w in ciphers]
        
        if not found_weak and 'chacha20' in ciphers:
            self.tests.append(Test(
                "Strong Ciphers",
                "Solo algoritmos de cifrado modernos",
                TestResult.PASS,
                "Usando ChaCha20, AES-GCM, AES-CTR"
            ))
        elif found_weak:
            self.tests.append(Test(
                "Strong Ciphers",
                "Solo algoritmos de cifrado modernos",
                TestResult.FAIL,
                f"Algoritmos débiles encontrados: {', '.join(found_weak)}"
            ))
        else:
            self.tests.append(Test(
                "Strong Ciphers",
                "Solo algoritmos de cifrado modernos",
                TestResult.WARN,
                "No se encontró ChaCha20 en la configuración"
            ))
    
    def test_strong_macs(self):
        """Test: Solo MACs fuertes"""
        macs = self.config.get('macs', '').lower()
        
        weak_macs = ['md5', 'sha1', 'ripemd160']
        found_weak = [w for w in weak_macs if w in macs and 'sha2' not in macs]
        
        if not found_weak and 'sha2' in macs:
            self.tests.append(Test(
                "Strong MACs",
                "Solo MACs seguros (SHA2+)",
                TestResult.PASS,
                "Usando HMAC-SHA2-256/512"
            ))
        elif found_weak:
            self.tests.append(Test(
                "Strong MACs",
                "Solo MACs seguros (SHA2+)",
                TestResult.FAIL,
                f"MACs débiles encontrados: {', '.join(found_weak)}"
            ))
        else:
            self.tests.append(Test(
                "Strong MACs",
                "Solo MACs seguros (SHA2+)",
                TestResult.WARN,
                "Configuración de MACs no óptima"
            ))
    
    def test_x11_forwarding_disabled(self):
        """Test: X11 forwarding deshabilitado"""
        value = self.config.get('x11forwarding', 'no')
        
        if value == 'no':
            self.tests.append(Test(
                "X11 Forwarding Disabled",
                "X11Forwarding debe ser 'no'",
                TestResult.PASS,
                f"X11Forwarding = {value}"
            ))
        else:
            self.tests.append(Test(
                "X11 Forwarding Disabled",
                "X11Forwarding debe ser 'no'",
                TestResult.WARN,
                f"X11Forwarding = {value} (recomendado: 'no')"
            ))
    
    def test_tcp_forwarding_disabled(self):
        """Test: TCP forwarding deshabilitado"""
        value = self.config.get('allowtcpforwarding', 'yes')
        
        if value == 'no':
            self.tests.append(Test(
                "TCP Forwarding Disabled",
                "AllowTcpForwarding debe ser 'no'",
                TestResult.PASS,
                f"AllowTcpForwarding = {value}"
            ))
        else:
            self.tests.append(Test(
                "TCP Forwarding Disabled",
                "AllowTcpForwarding debe ser 'no'",
                TestResult.WARN,
                f"AllowTcpForwarding = {value} (recomendado: 'no')"
            ))
    
    def test_ssh_port_open(self):
        """Test: Puerto SSH está abierto"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.host, self.port))
            sock.close()
            
            if result == 0:
                self.tests.append(Test(
                    "SSH Port Open",
                    f"Puerto {self.port} debe estar abierto",
                    TestResult.PASS,
                    f"Puerto {self.port} accesible en {self.host}"
                ))
            else:
                self.tests.append(Test(
                    "SSH Port Open",
                    f"Puerto {self.port} debe estar abierto",
                    TestResult.FAIL,
                    f"Puerto {self.port} no accesible"
                ))
        except Exception as e:
            self.tests.append(Test(
                "SSH Port Open",
                f"Puerto {self.port} debe estar abierto",
                TestResult.FAIL,
                f"Error: {e}"
            ))
    
    def run_all_tests(self):
        """Ejecuta todos los tests"""
        print("🧪 SSH Security Testing Suite")
        print("=" * 60)
        print(f"Host: {self.host}:{self.port}")
        print("=" * 60)
        print()
        
        print("📋 Obteniendo configuración SSH...")
        self.config = self.get_ssh_config()
        
        if not self.config:
            print("❌ No se pudo obtener la configuración SSH")
            sys.exit(1)
        
        print("✅ Configuración obtenida")
        print()
        
        print("🔍 Ejecutando tests de seguridad...")
        print()
        
        # Ejecutar todos los tests
        self.test_root_login_disabled()
        self.test_password_auth_disabled()
        self.test_pubkey_auth_enabled()
        self.test_max_auth_tries()
        self.test_client_alive_interval()
        self.test_strong_ciphers()
        self.test_strong_macs()
        self.test_x11_forwarding_disabled()
        self.test_tcp_forwarding_disabled()
        self.test_ssh_port_open()
        
        # Mostrar resultados
        self.display_results()
    
    def display_results(self):
        """Muestra resultados de los tests"""
        print("=" * 60)
        print("📊 Resultados de Tests")
        print("=" * 60)
        print()
        
        passed = sum(1 for t in self.tests if t.result == TestResult.PASS)
        failed = sum(1 for t in self.tests if t.result == TestResult.FAIL)
        warned = sum(1 for t in self.tests if t.result == TestResult.WARN)
        total = len(self.tests)
        
        for test in self.tests:
            print(f"{test.result.value} {test.name}")
            print(f"   {test.message}")
            print()
        
        print("=" * 60)
        print(f"Total: {total} tests")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Warnings: {warned}")
        print("=" * 60)
        print()
        
        # Calcular puntuación
        score = (passed / total) * 10
        
        print(f"Puntuación de Seguridad: {score:.1f}/10")
        
        if score >= 9:
            print("Estado: ✅ Excelente")
        elif score >= 7:
            print("Estado: 🟢 Bueno")
        elif score >= 5:
            print("Estado: 🟡 Aceptable")
        else:
            print("Estado: 🔴 Necesita mejoras")
        
        print()
        
        # Exit code basado en resultados
        if failed > 0:
            sys.exit(1)
        else:
            sys.exit(0)


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SSH Security Testing Suite')
    parser.add_argument('--host', default='localhost', help='SSH host to test')
    parser.add_argument('--port', type=int, default=22, help='SSH port')
    
    args = parser.parse_args()
    
    tester = SSHSecurityTester(host=args.host, port=args.port)
    tester.run_all_tests()


if __name__ == '__main__':
    main()
