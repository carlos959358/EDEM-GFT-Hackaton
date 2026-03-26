#!/usr/bin/env python3
"""
Health Check Detallado con Diagnóstico de Errores Específicos
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any

BASE_URL = "https://gft-hackaton-backend-297014562013.europe-west1.run.app"

def test_endpoint_detailed(endpoint: str, name: str) -> Dict[str, Any]:
    """Test detallado de un endpoint específico"""
    try:
        print(f"🔍 Testing {name}...", end=" ", flush=True)
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        
        result = {
            "name": name,
            "endpoint": endpoint,
            "status_code": response.status_code,
            "success": response.status_code in [200, 401, 403],
            "response_time": response.elapsed.total_seconds(),
            "error_details": None,
            "response_size": len(response.content) if response.content else 0
        }
        
        # Analizar respuesta específica
        if response.status_code == 200:
            print("✅ OK")
        elif response.status_code == 401:
            print("⚠️ UNAUTHORIZED (Normal sin auth)")  
        elif response.status_code == 403:
            print("⚠️ FORBIDDEN (Normal sin permisos)")
        elif response.status_code == 404:
            print("❌ NOT FOUND")
        elif response.status_code == 500:
            print("❌ SERVER ERROR")
            try:
                error_data = response.json()
                result["error_details"] = error_data
            except:
                result["error_details"] = {"message": response.text[:200]}
        else:
            print(f"❓ HTTP {response.status_code}")
            
        return result
        
    except requests.exceptions.Timeout:
        print("⏰ TIMEOUT")
        return {
            "name": name,
            "endpoint": endpoint,
            "status_code": None,
            "success": False,
            "response_time": 10.0,
            "error_details": {"error": "Request timeout"}
        }
    except requests.exceptions.ConnectionError:
        print("🔌 CONNECTION ERROR")
        return {
            "name": name,
            "endpoint": endpoint,
            "status_code": None,
            "success": False,
            "response_time": 0,
            "error_details": {"error": "Connection failed"}
        }
    except Exception as e:
        print(f"💥 ERROR: {str(e)[:50]}")
        return {
            "name": name,
            "endpoint": endpoint,
            "status_code": None,
            "success": False,
            "response_time": 0,
            "error_details": {"error": str(e)}
        }

def detailed_health_check():
    """Health check con diagnóstico detallado de errores"""
    
    print(f"🏥 Health Check Detallado - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print(f"🎯 URL: {BASE_URL}")
    print()
    
    # Primero test básico del servidor
    print("📡 SERVIDOR BÁSICO")
    print("-" * 40)
    server_result = test_endpoint_detailed("/docs", "Documentación FastAPI")
    print()
    
    # Test de endpoints específicos
    print("⚡ ENDPOINTS DE LA API")
    print("-" * 40)
    
    endpoints = [
        ("/api/v1/users/me", "Perfil de usuario"),
        ("/api/v1/calendar/events", "Eventos de calendario"),
        ("/api/v1/subjects", "Lista de asignaturas"),
        ("/api/v1/grades/me", "Mis notas"),
        ("/api/v1/attendance/me", "Mi asistencia"),
        ("/api/v1/attendance/me/metrics", "Métricas de asistencia"),
    ]
    
    results = []
    working = 0
    
    for endpoint, name in endpoints:
        result = test_endpoint_detailed(endpoint, name)
        results.append(result)
        if result["success"]:
            working += 1
        
        # Mostrar detalles de error si existe
        if result.get("error_details") and result["status_code"] == 500:
            print(f"   🔍 Error details: {result['error_details']}")
        
        print()
    
    # Resumen con estadísticas
    print("📊 RESUMEN DETALLADO")
    print("-" * 40)
    total = len(endpoints)
    availability = (working / total * 100) if total > 0 else 0
    
    print(f"✅ Endpoints funcionando: {working}/{total} ({availability:.1f}%)")
    print(f"⚡ Tiempo promedio de respuesta: {sum(r['response_time'] for r in results) / len(results):.2f}s")
    
    # Análisis de errores específicos
    errors_500 = [r for r in results if r["status_code"] == 500]
    errors_404 = [r for r in results if r["status_code"] == 404]
    errors_timeout = [r for r in results if r.get("error_details", {}).get("error") == "Request timeout"]
    
    if errors_500:
        print(f"🚨 Errores 500 (Server Error): {len(errors_500)}")
        for err in errors_500:
            print(f"   - {err['name']}: {err['endpoint']}")
            if err.get("error_details"):
                error_msg = err["error_details"].get("detail", err["error_details"].get("message", "Unknown error"))
                print(f"     Error: {error_msg}")
    
    if errors_404:
        print(f"❓ Errores 404 (Not Found): {len(errors_404)}")
        for err in errors_404:
            print(f"   - {err['name']}: {err['endpoint']}")
    
    if errors_timeout:
        print(f"⏰ Errores de Timeout: {len(errors_timeout)}")
    
    # Diagnóstico y recomendaciones
    print("\n💡 DIAGNÓSTICO")
    print("-" * 40)
    
    if len(errors_500) > 0:
        print("🚨 PROBLEMA PRINCIPAL: Errores de servidor (500)")
        print("   Causa probable: Problemas con la base de datos")
        print("   Acciones:")
        print("   1. Verificar conexión a Cloud SQL")
        print("   2. Revisar logs del contenedor en Cloud Run")
        print("   3. Verificar que las tablas existen en la BBDD")
        print("   4. Comprobar variables de entorno de conexión")
        
    elif len(errors_404) > 0:
        print("❓ PROBLEMA: Endpoints no encontrados")
        print("   Causa probable: Rutas no implementadas o mal configuradas")
        
    elif availability < 50:
        print("⚠️ PROBLEMA: Baja disponibilidad del sistema")
        
    else:
        print("🎉 Sistema funcionando correctamente")
    
    print("\n" + "=" * 80)
    
    return results

if __name__ == "__main__":
    detailed_health_check()