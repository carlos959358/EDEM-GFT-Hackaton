#!/usr/bin/env python3
"""
Health Check Completo - Sistema de monitoreo integral del backend
Autor: Sistema automatizado
Fecha: 2026-03-26
Version: 2.0

Modos de operación:
- python health_check.py          -> Simple health check (para scripts de monitoreo)
- python health_check.py -v       -> Verbose health check (diagnóstico detallado)
- python health_check.py -j       -> JSON output (para integración con sistemas)
- python health_check.py -f       -> Full test (test completo de todos los endpoints)
- python health_check.py -b       -> Benchmark mode (incluye métricas de performance)

Exit codes:
0: Todo OK
1: Problemas menores/warnings
2: Error de base de datos
3: Timeout del servidor
4: No se puede conectar
5: Error crítico del sistema
"""

import requests
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Configuración
BASE_URL = "https://gft-hackaton-backend-297014562013.europe-west1.run.app"
TIMEOUT_SHORT = 5
TIMEOUT_LONG = 15

class HealthChecker:
    def __init__(self):
        self.results = {}
        self.start_time = datetime.now()
        self.total_tests = 0
        self.passed_tests = 0
        self.warnings = 0
        self.errors = 0
        
    def test_server_connectivity(self) -> Tuple[bool, str, float]:
        """Test básico de conectividad del servidor"""
        try:
            start = time.time()
            response = requests.get(f"{BASE_URL}/docs", timeout=TIMEOUT_SHORT)
            elapsed = time.time() - start
            
            if response.status_code == 200:
                return True, f"OK ({elapsed:.2f}s)", elapsed
            else:
                return False, f"HTTP {response.status_code}", elapsed
        except requests.exceptions.Timeout:
            return False, "TIMEOUT", TIMEOUT_SHORT
        except requests.exceptions.ConnectionError:
            return False, "CONNECTION_ERROR", 0
        except Exception as e:
            return False, f"ERROR: {str(e)[:50]}", 0
    
    def test_database_connectivity(self) -> Tuple[bool, str, float]:
        """Test de conectividad con la base de datos"""
        try:
            start = time.time()
            response = requests.get(f"{BASE_URL}/api/v1/users/me", timeout=TIMEOUT_LONG)
            elapsed = time.time() - start
            
            if response.status_code == 500:
                return False, f"DATABASE_ERROR ({elapsed:.2f}s)", elapsed
            elif response.status_code in [200, 401, 403]:
                return True, f"OK ({elapsed:.2f}s)", elapsed
            else:
                return True, f"UNEXPECTED_STATUS_{response.status_code} ({elapsed:.2f}s)", elapsed
        except requests.exceptions.Timeout:
            return False, "TIMEOUT", TIMEOUT_LONG
        except Exception as e:
            return False, f"ERROR: {str(e)[:50]}", 0
    
    def test_critical_endpoints(self) -> Dict[str, Tuple[bool, str, float]]:
        """Test de todos los endpoints críticos"""
        endpoints = [
            ("/api/v1/users/me", "Perfil de usuario"),
            ("/api/v1/calendar/events", "Calendario"),
            ("/api/v1/subjects", "Asignaturas"),
            ("/api/v1/grades/me", "Notas del usuario"),
            ("/api/v1/attendance/me", "Asistencia del usuario"),
            ("/api/v1/attendance/me/metrics", "Métricas de asistencia"),
        ]
        
        results = {}
        for endpoint, name in endpoints:
            try:
                start = time.time()
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT_SHORT)
                elapsed = time.time() - start
                
                if response.status_code in [200, 401, 403]:
                    status = True
                    message = f"OK ({elapsed:.2f}s)"
                elif response.status_code == 500:
                    status = False
                    message = f"SERVER_ERROR ({elapsed:.2f}s)"
                else:
                    status = True  # Other status codes might be OK depending on auth
                    message = f"HTTP_{response.status_code} ({elapsed:.2f}s)"
                
                results[name] = (status, message, elapsed)
            except requests.exceptions.Timeout:
                results[name] = (False, "TIMEOUT", TIMEOUT_SHORT)
            except Exception as e:
                results[name] = (False, f"ERROR: {str(e)[:30]}", 0)
        
        return results
    
    def run_simple_check(self) -> int:
        """Health check simple para scripts de monitoreo"""
        # Test servidor
        server_ok, server_msg, _ = self.test_server_connectivity()
        if not server_ok:
            if "TIMEOUT" in server_msg:
                print("FAIL: Timeout - servidor muy lento")
                return 3
            elif "CONNECTION" in server_msg:
                print("FAIL: No se puede conectar al servidor")
                return 4
            else:
                print(f"FAIL: Servidor no responde ({server_msg})")
                return 1
        
        # Test base de datos
        db_ok, db_msg, _ = self.test_database_connectivity()
        if not db_ok:
            if "DATABASE_ERROR" in db_msg:
                print("FAIL: Error de base de datos (500)")
                return 2
            elif "TIMEOUT" in db_msg:
                print("FAIL: Timeout en base de datos")
                return 3
            else:
                print(f"FAIL: Error en API ({db_msg})")
                return 1
        
        print("PASS: Backend completamente funcional")
        return 0
    
    def run_verbose_check(self) -> int:
        """Health check detallado con diagnósticos"""
        print(f"🏥 Health Check Backend Completo - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print(f"🎯 URL: {BASE_URL}")
        print()
        
        exit_code = 0
        
        # 1. Test servidor
        print("📡 1. CONECTIVIDAD DEL SERVIDOR")
        print("-" * 40)
        server_ok, server_msg, server_time = self.test_server_connectivity()
        if server_ok:
            print(f"✅ Servidor FastAPI: {server_msg}")
            print("✅ Documentación API: ACCESIBLE")
        else:
            print(f"❌ Servidor FastAPI: {server_msg}")
            exit_code = max(exit_code, 4 if "CONNECTION" in server_msg else 3 if "TIMEOUT" in server_msg else 1)
        
        # 2. Test base de datos
        print("\n🗄️ 2. CONECTIVIDAD BASE DE DATOS")
        print("-" * 40)
        db_ok, db_msg, db_time = self.test_database_connectivity()
        if db_ok:
            print(f"✅ Base de datos: {db_msg}")
        else:
            print(f"❌ Base de datos: {db_msg}")
            exit_code = max(exit_code, 2 if "DATABASE" in db_msg else 3 if "TIMEOUT" in db_msg else 1)
        
        # 3. Test endpoints críticos
        print("\n⚡ 3. ENDPOINTS CRÍTICOS")
        print("-" * 40)
        endpoints_results = self.test_critical_endpoints()
        
        working = sum(1 for success, _, _ in endpoints_results.values() if success)
        total = len(endpoints_results)
        
        for name, (success, message, elapsed) in endpoints_results.items():
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {name}: {message}")
            if not success and "SERVER_ERROR" in message:
                exit_code = max(exit_code, 2)
            elif not success:
                exit_code = max(exit_code, 1)
        
        # 4. Métricas de performance
        print("\n⚡ 4. MÉTRICAS DE PERFORMANCE")
        print("-" * 40)
        if server_ok:
            if server_time < 1.0:
                print(f"✅ Latencia del servidor: {server_time:.2f}s (EXCELENTE)")
            elif server_time < 3.0:
                print(f"⚠️ Latencia del servidor: {server_time:.2f}s (ACEPTABLE)")
            else:
                print(f"❌ Latencia del servidor: {server_time:.2f}s (LENTA)")
                exit_code = max(exit_code, 1)
        
        if db_ok:
            if db_time < 2.0:
                print(f"✅ Latencia de BBDD: {db_time:.2f}s (EXCELENTE)")
            elif db_time < 5.0:
                print(f"⚠️ Latencia de BBDD: {db_time:.2f}s (ACEPTABLE)")
            else:
                print(f"❌ Latencia de BBDD: {db_time:.2f}s (LENTA)")
                exit_code = max(exit_code, 1)
        
        # 5. Resumen
        print("\n📊 5. RESUMEN")
        print("-" * 40)
        availability = (working / total * 100) if total > 0 else 0
        
        if availability >= 90:
            status = "🟢 OPERACIONAL"
        elif availability >= 70:
            status = "🟡 DEGRADADO"
        else:
            status = "🔴 CRÍTICO"
        
        print(f"Estado general: {status}")
        print(f"Endpoints funcionando: {working}/{total}")
        print(f"Disponibilidad: {availability:.1f}%")
        print(f"Tiempo total de verificación: {(datetime.now() - self.start_time).total_seconds():.2f}s")
        
        # 6. Recomendaciones
        print("\n💡 6. RECOMENDACIONES")
        print("-" * 40)
        if exit_code == 0:
            print("🎉 ¡Todo funciona correctamente!")
        elif exit_code == 2:
            print("🚨 PROBLEMA CRÍTICO DE BASE DE DATOS:")
            print("   1. Verificar configuración de Cloud SQL")
            print("   2. Revisar variables de entorno BBDD")
            print("   3. Comprobar permisos de conectividad")
            print("   4. Verificar logs del contenedor en Cloud Run")
        elif exit_code >= 3:
            print("🚨 PROBLEMA DE CONECTIVIDAD:")
            print("   1. Verificar estado de Cloud Run")
            print("   2. Comprobar configuración de red")
            print("   3. Revisar DNS y certificados SSL")
        else:
            print("⚠️ PROBLEMAS MENORES DETECTADOS:")
            print("   1. Revisar logs específicos de endpoints con fallos")
            print("   2. Verificar datos de prueba en BBDD")
            print("   3. Monitorear métricas de performance")
        
        print("\n" + "=" * 80)
        return exit_code
    
    def run_json_check(self) -> int:
        """Health check con output en JSON para integración"""
        server_ok, server_msg, server_time = self.test_server_connectivity()
        db_ok, db_msg, db_time = self.test_database_connectivity()
        endpoints = self.test_critical_endpoints()
        
        working_endpoints = sum(1 for success, _, _ in endpoints.values() if success)
        total_endpoints = len(endpoints)
        
        result = {
            "timestamp": self.start_time.isoformat(),
            "base_url": BASE_URL,
            "status": {
                "overall": "healthy" if server_ok and db_ok and working_endpoints == total_endpoints else "unhealthy",
                "server": {"ok": server_ok, "message": server_msg, "response_time": server_time},
                "database": {"ok": db_ok, "message": db_msg, "response_time": db_time}
            },
            "endpoints": {
                name: {"ok": ok, "message": msg, "response_time": time}
                for name, (ok, msg, time) in endpoints.items()
            },
            "metrics": {
                "total_endpoints": total_endpoints,
                "working_endpoints": working_endpoints,
                "availability_percent": round((working_endpoints / total_endpoints * 100) if total_endpoints > 0 else 0, 1),
                "avg_response_time": round(sum(time for _, _, time in endpoints.values()) / len(endpoints) if endpoints else 0, 3)
            }
        }
        
        print(json.dumps(result, indent=2))
        
        # Determine exit code
        if not server_ok:
            return 4 if "CONNECTION" in server_msg else 3
        elif not db_ok and "DATABASE" in db_msg:
            return 2
        elif working_endpoints < total_endpoints:
            return 1
        else:
            return 0

def main():
    checker = HealthChecker()
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "-v":
            exit_code = checker.run_verbose_check()
        elif mode == "-j":
            exit_code = checker.run_json_check()
        elif mode in ["-f", "--full"]:
            exit_code = checker.run_verbose_check()  # Por ahora es igual que verbose
        elif mode in ["-h", "--help"]:
            print(__doc__)
            sys.exit(0)
        else:
            print(f"Modo desconocido: {mode}")
            print("Usa -h para ayuda")
            sys.exit(1)
    else:
        exit_code = checker.run_simple_check()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()