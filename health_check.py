#!/usr/bin/env python3
"""
Health Check Simple - Para monitoreo continuo del backend
"""

import requests
import sys
from datetime import datetime

BASE_URL = "https://gft-hackaton-backend-297014562013.europe-west1.run.app"

def simple_health_check():
    """Health check simple que retorna exit code para scripts de monitoreo"""
    
    try:
        # Test 1: Servidor funcionando
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code != 200:
            print(f"FAIL: Servidor no responde (Status: {response.status_code})")
            return 1
        
        # Test 2: API funcionando (test básico de BBDD)
        response = requests.get(f"{BASE_URL}/api/v1/users/me", timeout=10)
        if response.status_code == 500:
            print("FAIL: Error de base de datos (500)")
            return 2
        elif response.status_code in [200, 401, 403]:  # Cualquiera de estos es OK
            print("PASS: Backend completamente funcional")
            return 0
        else:
            print(f"WARN: API responde pero con status inesperado ({response.status_code})")
            return 1
            
    except requests.exceptions.Timeout:
        print("FAIL: Timeout - servidor muy lento")
        return 3
    except requests.exceptions.ConnectionError:
        print("FAIL: No se puede conectar al servidor")
        return 4
    except Exception as e:
        print(f"FAIL: Error inesperado - {e}")
        return 5

def verbose_health_check():
    """Health check con más detalles"""
    
    print(f"🏥 Health Check Backend - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test servidor
    print("📡 Testing servidor...", end=" ")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ OK")
        else:
            print(f"❌ FAIL ({response.status_code})")
            return 1
    except Exception as e:
        print(f"❌ ERROR ({e})")
        return 1
    
    # Test API/BBDD
    print("🗄️ Testing API/Database...", end=" ")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/users/me", timeout=10)
        if response.status_code == 500:
            print("❌ BBDD ERROR")
            return 2
        elif response.status_code in [200, 401, 403]:
            print("✅ OK")
        else:
            print(f"⚠️ UNEXPECTED ({response.status_code})")
            return 1
    except Exception as e:
        print(f"❌ ERROR ({e})")
        return 1
    
    print("🎉 Backend completamente funcional!")
    return 0

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        exit_code = verbose_health_check()
    else:
        exit_code = simple_health_check()
    
    sys.exit(exit_code)