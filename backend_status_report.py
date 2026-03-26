#!/usr/bin/env python3
"""
Reporte de Estado del Backend - Resumen ejecutivo
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://gft-hackaton-backend-297014562013.europe-west1.run.app"

def generate_status_report():
    """Genera un reporte del estado del backend"""
    
    print("=" * 70)
    print("📊 REPORTE DE ESTADO DEL BACKEND")
    print("=" * 70)
    print(f"🎯 URL: {BASE_URL}")
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Test de conectividad básica
    print("🔍 1. CONECTIVIDAD DEL SERVIDOR")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor FastAPI: FUNCIONANDO")
            print("✅ Documentación API: ACCESIBLE")
        else:
            print(f"❌ Problema con servidor: Status {response.status_code}")
            return
    except Exception as e:
        print(f"❌ No se puede conectar al servidor: {e}")
        return
    
    # 2. Test de base de datos
    print("\n🗄️ 2. CONECTIVIDAD BASE DE DATOS")
    print("-" * 40)
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/users/me", timeout=10)
        if response.status_code == 500:
            print("❌ Base de datos: NO FUNCIONA (Error 500)")
            print("   Todos los endpoints de la API fallan")
        else:
            print(f"✅ Base de datos: FUNCIONANDO (Status {response.status_code})")
    except Exception as e:
        print(f"❌ Error al testear BBDD: {e}")
    
    # 3. Test de endpoints críticos
    print("\n⚡ 3. ENDPOINTS CRÍTICOS")
    print("-" * 40)
    
    critical_endpoints = [
        ("/api/v1/users/me", "Perfil de usuario"),
        ("/api/v1/calendar/events", "Calendario"),
        ("/api/v1/subjects", "Asignaturas"), 
        ("/api/v1/grades/me", "Notas"),
        ("/api/v1/attendance/me", "Asistencia")
    ]
    
    working_endpoints = 0
    total_endpoints = len(critical_endpoints)
    
    for endpoint, name in critical_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: FUNCIONANDO")
                working_endpoints += 1
            else:
                print(f"❌ {name}: ERROR {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: ERROR DE CONEXIÓN")
    
    # 4. Resumen y diagnóstico
    print("\n📋 4. RESUMEN Y DIAGNÓSTICO")
    print("-" * 40)
    
    if working_endpoints == 0:
        status = "🚨 CRÍTICO"
        color = "ROJO"
    elif working_endpoints < total_endpoints / 2:
        status = "⚠️ PROBLEMÁTICO"
        color = "AMARILLO"
    else:
        status = "✅ OPERACIONAL"
        color = "VERDE"
    
    print(f"Estado general: {status}")
    print(f"Endpoints funcionando: {working_endpoints}/{total_endpoints}")
    print(f"Disponibilidad: {(working_endpoints/total_endpoints*100):.0f}%")
    
    # 5. Recomendaciones
    print("\n💡 5. RECOMENDACIONES")
    print("-" * 40)
    
    if working_endpoints == 0:
        print("🔧 ACCIONES INMEDIATAS REQUERIDAS:")
        print("   1. Verificar configuración de Cloud SQL")
        print("   2. Revisar variables de entorno de la BBDD")
        print("   3. Comprobar que las tablas existen en la BBDD")
        print("   4. Verificar logs del contenedor en Cloud Run")
        print("   5. Comprobar permisos de conectividad")
        print()
        print("📚 COMANDOS PARA DIAGNÓSTICO:")
        print("   - Revisar logs: gcloud logging read")
        print("   - Conectar a Cloud SQL: gcloud sql connect")
        print("   - Ver variables de entorno del servicio")
    
    elif working_endpoints < total_endpoints:
        print("🔧 ACCIONES RECOMENDADAS:")
        print("   1. Investigar endpoints específicos que fallan")
        print("   2. Revisar logs para errores específicos")
        print("   3. Verificar datos de prueba en la BBDD")
    
    else:
        print("🎉 ¡Todo funciona correctamente!")
        print("   - Backend completamente operacional")
        print("   - Todos los endpoints responden correctamente")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    generate_status_report()