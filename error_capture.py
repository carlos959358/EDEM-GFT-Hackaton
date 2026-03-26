#!/usr/bin/env python3
"""
Error Detail Capture - Capturar detalles específicos de errores 500
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://gft-hackaton-backend-297014562013.europe-west1.run.app"

def capture_error_details(endpoint: str, name: str) -> None:
    """Captura detalles específicos de errores"""
    try:
        print(f"🔍 {name} ({endpoint}):", flush=True)
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 500:
            print(f"   Response Text: {response.text}")
            try:
                error_json = response.json()
                print(f"   JSON Error: {json.dumps(error_json, indent=2)}")
            except:
                print(f"   Raw Text: {response.text}")
        elif response.status_code in [200, 401, 403]:
            print(f"   ✅ Working (expected auth response)")
        else:
            print(f"   Response: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ TIMEOUT after 5s")
    except Exception as e:
        print(f"   💥 ERROR: {e}")
    
    print("-" * 60)

def main():
    print(f"🔍 Error Detail Capture - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Test solo los endpoints con errores 500
    error_endpoints = [
        ("/api/v1/subjects", "Asignaturas"),
        ("/api/v1/grades/me", "Notas"),
        ("/api/v1/attendance/me", "Asistencia"),
    ]
    
    for endpoint, name in error_endpoints:
        capture_error_details(endpoint, name)
    
    print("=" * 80)

if __name__ == "__main__":
    main()