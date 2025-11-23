#!/usr/bin/env python3
"""
Script de Auditoría de Configuración SSH
Proyecto de Criptografía - UNAL Medellín - Grupo 6
"""

import subprocess
import sys
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    CRITICAL = "🔴 CRÍTICO"
    HIGH = "🟠 ALTO"
    MEDIUM = "🟡 MEDIO"
    LOW = "🟢 BAJO"
    INFO = "🔵 INFO"


@dataclass
class Finding:
    parameter: str
    current_value: str
    severity: Severity
    issue: str
    recommendation: str


class SSHAuditor:
    def __init__(self):
        self.findings: List[Finding] = []
        self.config: Dict[str, str] = {}
        
    def get_ssh_config(self) -> Dict[str, str]:
        try:
            result = subprocess.run(['sudo', 'sshd', '-T'], capture_output=True, text=True, check=True)
            config = {}
            for line in result.stdout.split('\n'):
                if line.strip():
                    parts = line.split(None, 1)
                    if len(parts) == 2:
                        config[parts[0].lower()] = parts[1].strip()
            return config
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    def audit_root_login(self):
        value = self.config.get('permitrootlogin', 'yes')
        if value == 'yes':
            self.findings.append(Finding('PermitRootLogin', value, Severity.CRITICAL,
                'Login de root permitido', 'Cambiar a "no"'))
    
    def audit_password_auth(self):
        if self.config.get('passwordauthentication', 'yes') == 'yes':
            self.findings.append(Finding('PasswordAuthentication', 'yes', Severity.HIGH,
                'Vulnerable a fuerza bruta', 'Cambiar a "no"'))
    
    def audit_ciphers(self):
        ciphers = self.config.get('ciphers', '').lower()
        if '3des' in ciphers or 'arcfour' in ciphers or 'cbc' in ciphers:
            self.findings.append(Finding('Ciphers', 'débiles', Severity.CRITICAL,
                'Algoritmos débiles habilitados', 'Usar solo chacha20, aes-gcm'))
    
    def run_audit(self):
        print("🔍 Auditoría de SSH\n")
        self.config = self.get_ssh_config()
        self.audit_root_login()
        self.audit_password_auth()
        self.audit_ciphers()
        
        if not self.findings:
            print("✅ Sin problemas\n")
            return
        
        print(f"📊 Hallazgos: {len(self.findings)}\n")
        for i, f in enumerate(self.findings, 1):
            print(f"{i}. {f.severity.value} - {f.parameter}")
            print(f"   Problema: {f.issue}")
            print(f"   Recomendación: {f.recommendation}\n")


if __name__ == '__main__':
    SSHAuditor().run_audit()
