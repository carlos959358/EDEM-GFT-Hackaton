#!/usr/bin/env python3
"""
Script para testear todos los endpoints del backend desplegado en Cloud Run.
Verifica que los endpoints respondan correctamente y devuelvan datos en el formato esperado.
"""

import requests
import json
from typing import Dict, List, Tuple
from datetime import datetime

# Base URL del backend desplegado
BASE_URL = "https://gft-hackaton-backend-297014562013.europe-west1.run.app"

class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        
    def log_result(self, method: str, endpoint: str, status: str, details: str = ""):
        """Registra el resultado de un test"""
        result = {
            'method': method,
            'endpoint': endpoint,
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.results.append(result)
        
        # Color coding para la console
        color = "\033[92m" if status == "✅ PASS" else "\033[91m" if status == "❌ FAIL" else "\033[93m"
        reset = "\033[0m"
        print(f"{color}{method:<6} {endpoint:<50} {status}{reset}")
        if details:
            print(f"       └─ {details}")

    def test_endpoint(self, method: str, endpoint: str, expected_status: int = 200, 
                     data: dict = None, expected_fields: List[str] = None) -> bool:
        """Testa un endpoint específico"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = self.session.get(url, timeout=10)
            elif method == "POST":
                response = self.session.post(url, json=data, timeout=10)
            elif method == "PUT":
                response = self.session.put(url, json=data, timeout=10)
            elif method == "DELETE":
                response = self.session.delete(url, timeout=10)
            else:
                self.log_result(method, endpoint, "❌ FAIL", "Método HTTP no soportado")
                return False
            
            # Verificar código de estado
            if response.status_code != expected_status:
                error_detail = f"Status {response.status_code}, esperado {expected_status}"
                
                # Si es un error 500, intentar obtener más detalles
                if response.status_code == 500:
                    try:
                        error_response = response.json()
                        if 'detail' in error_response:
                            error_detail += f" - {error_response['detail']}"
                    except:
                        # Si no es JSON, usar el texto de la respuesta
                        if response.text:
                            error_detail += f" - {response.text[:100]}..."
   
                self.log_result(method, endpoint, "❌ FAIL", error_detail)
                return False
            
            # Para códigos 204 (No Content), no esperamos JSON
            if response.status_code == 204:
                self.log_result(method, endpoint, "✅ PASS", "No content response")
                return True
                
            # Verificar que la respuesta sea JSON válido
            try:
                json_data = response.json()
            except json.JSONDecodeError:
                self.log_result(method, endpoint, "❌ FAIL", "Respuesta no es JSON válido")
                return False
            
            # Verificar campos esperados si los hay
            if expected_fields and isinstance(json_data, dict):
                missing_fields = [field for field in expected_fields if field not in json_data]
                if missing_fields:
                    self.log_result(method, endpoint, "❌ FAIL", 
                                   f"Faltan campos: {missing_fields}")
                    return False
            
            # Si llegamos aquí, el test pasó
            response_info = ""
            if isinstance(json_data, list):
                response_info = f"Lista con {len(json_data)} elementos"
            elif isinstance(json_data, dict):
                response_info = f"Objeto con {len(json_data)} campos"
            
            self.log_result(method, endpoint, "✅ PASS", response_info)
            return True
            
        except requests.exceptions.Timeout:
            self.log_result(method, endpoint, "❌ FAIL", "Timeout")
            return False
        except requests.exceptions.ConnectionError:
            self.log_result(method, endpoint, "❌ FAIL", "Error de conexión")
            return False
        except Exception as e:
            self.log_result(method, endpoint, "❌ FAIL", f"Error: {str(e)}")
            return False

    def test_health_check(self):
        """Test básico de salud del servidor"""
        print("\n🔍 Testing server health...")
        try:
            # Test de documentación
            response = self.session.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor activo y documentación accesible")
            else:
                print(f"❌ Problema con la documentación (Status: {response.status_code})")
                return False
            
            # Test de OpenAPI JSON
            response = self.session.get(f"{self.base_url}/openapi.json", timeout=5)
            if response.status_code == 200:
                print("✅ OpenAPI schema accesible")
            else:
                print(f"⚠️ OpenAPI schema no accesible (Status: {response.status_code})")
            
            return True
        except Exception as e:
            print(f"❌ No se puede conectar al servidor: {e}")
            return False

    def test_simple_endpoints(self):
        """Test de endpoints simples para diagnosticar problemas"""
        print("\n🔧 Testing endpoints básicos para diagnóstico...")
        
        # Primero testear un endpoint simple que podría existir
        endpoints_to_test = [
            ("/", "Root endpoint"),
            ("/health", "Health check"),
            ("/ping", "Ping endpoint"),
        ]
        
        for endpoint, description in endpoints_to_test:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=5)
                if response.status_code in [200, 404]:  # 404 es OK para endpoints que no existen
                    print(f"✅ {description}: Status {response.status_code}")
                else:
                    print(f"⚠️ {description}: Status {response.status_code}")
            except Exception as e:
                print(f"❌ {description}: Error {e}")
                
        # Test específico para ver si hay un problema con la BBDD
        print("\n🗄️ Testing database connectivity...")
        try:
            # Intentar un endpoint simple como /docs que sabemos que funciona
            # luego uno que requiere BBDD
            response = self.session.get(f"{self.base_url}/api/v1/users/me", timeout=10)
            
            if response.status_code == 500:
                try:
                    error_data = response.json()
                    print(f"❌ Error 500 en endpoint de BBDD:")
                    print(f"   {json.dumps(error_data, indent=2)}")
                except:
                    print(f"❌ Error 500 en endpoint de BBDD (no JSON):")
                    print(f"   {response.text[:200]}...")
            else:
                print(f"✅ Endpoint de BBDD responde: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error al testear connectivity BBDD: {e}")

    def run_all_tests(self):
        """Ejecuta todos los tests de endpoints"""
        print("🚀 Iniciando tests de endpoints del backend...")
        print("=" * 80)
        
        # Test de salud del servidor
        if not self.test_health_check():
            print("❌ No se puede conectar al servidor. Abortando tests.")
            return
        
        # Test de diagnóstico
        self.test_simple_endpoints()
        
        print("\n📋 Testing endpoints GET (solo lectura)...")
        print("-" * 80)
        
        # ===============================
        # ENDPOINTS GET - PERFIL Y ROLES
        # ===============================
        self.test_endpoint("GET", "/api/v1/users/me", 
                          expected_fields=["id", "nombre", "correo"])
        
        # Test con un user_id de ejemplo (podría no existir, esperamos 404)
        self.test_endpoint("GET", "/api/v1/users/EJEMPLO123", expected_status=404)
        
        # ===============================
        # ENDPOINTS GET - CALENDARIO
        # ===============================
        self.test_endpoint("GET", "/api/v1/calendar/events")
        self.test_endpoint("GET", "/api/v1/calendar/events/evento123", expected_status=404)
        
        # ===============================
        # ENDPOINTS GET - ASIGNATURAS
        # ===============================
        self.test_endpoint("GET", "/api/v1/subjects")
        self.test_endpoint("GET", "/api/v1/subjects/asignatura123", expected_status=404)
        self.test_endpoint("GET", "/api/v1/subjects/asignatura123/students", expected_status=404)
        
        # ===============================
        # ENDPOINTS GET - NOTAS
        # ===============================
        self.test_endpoint("GET", "/api/v1/grades/me")
        self.test_endpoint("GET", "/api/v1/grades/me/subjects/asignatura123")
        
        # ===============================
        # ENDPOINTS GET - ASISTENCIA
        # ===============================
        self.test_endpoint("GET", "/api/v1/attendance/me")
        self.test_endpoint("GET", "/api/v1/attendance/me/metrics")
        self.test_endpoint("GET", "/api/v1/attendance/subjects/asignatura123")
        
        # ===============================
        # ENDPOINTS GET - RESERVAS Y TUTORÍAS
        # ===============================
        self.test_endpoint("GET", "/api/v1/reservations")
        self.test_endpoint("GET", "/api/v1/tutorings/slots")
        
        # ===============================
        # ENDPOINTS GET - NOTIFICACIONES
        # ===============================
        self.test_endpoint("GET", "/api/v1/notifications")
        self.test_endpoint("GET", "/api/v1/notifications/settings")
        
        # ===============================
        # ENDPOINTS GET - CORREOS
        # ===============================
        self.test_endpoint("GET", "/api/v1/emails")
        self.test_endpoint("GET", "/api/v1/emails/correo123", expected_status=404)
        
        # ===============================
        # TESTS DE ENDPOINTS POST/PUT (sin modificar datos reales)
        # ===============================
        print("\n📝 Testing endpoints POST/PUT (con datos de prueba)...")
        print("-" * 80)
        
        # Test PUT perfil (datos válidos)
        profile_data = {
            "nombre": "Test",
            "apellido": "User",
            "correo": "test@test.com"
        }
        self.test_endpoint("PUT", "/api/v1/users/me", data=profile_data)
        
        # Test POST crear evento (debería funcionar)
        event_data = {
            "titulo": "Evento Test",
            "descripcion": "Descripción de prueba",
            "fecha_inicio": "2024-04-01T10:00:00",
            "fecha_fin": "2024-04-01T11:00:00",
            "tipo": "clase"
        }
        self.test_endpoint("POST", "/api/v1/calendar/events", data=event_data, expected_status=201)
        
        # Test POST crear asignatura (podría requerir permisos)
        subject_data = {
            "nombre": "Asignatura Test",
            "creditos": 6,
            "descripcion": "Test description"
        }
        # Esperamos 422 si faltan campos requeridos, o 403 si no hay permisos
        self.test_endpoint("POST", "/api/v1/subjects", data=subject_data, 
                          expected_status=201)
        
        print("\n📊 Resumen de resultados...")
        self.print_summary()

    def print_summary(self):
        """Imprime un resumen de los resultados"""
        total = len(self.results)
        passed = len([r for r in self.results if r['status'] == '✅ PASS'])
        failed = len([r for r in self.results if r['status'] == '❌ FAIL'])
        
        print("=" * 80)
        print(f"📈 RESUMEN FINAL:")
        print(f"   Total de tests: {total}")
        print(f"   ✅ Exitosos: {passed}")
        print(f"   ❌ Fallidos: {failed}")
        print(f"   📊 Tasa de éxito: {(passed/total*100):.1f}%" if total > 0 else "   📊 No tests ejecutados")
        
        if failed > 0:
            print(f"\n❌ Endpoints con problemas:")
            for result in self.results:
                if result['status'] == '❌ FAIL':
                    print(f"   {result['method']} {result['endpoint']}: {result['details']}")
        
        print("\n💡 Notas:")
        print("   - Algunos endpoints pueden fallar por falta de datos de prueba en la BBDD")
        print("   - Los errores 404 en endpoints con IDs específicos son esperados")
        print("   - Los endpoints POST/PUT pueden requerir permisos especiales")

def main():
    """Función principal"""
    tester = APITester(BASE_URL)
    
    print("🧪 SCRIPT DE TESTING DE ENDPOINTS")
    print(f"🎯 Target: {BASE_URL}")
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrumpidos por el usuario")
    except Exception as e:
        print(f"\n\n💥 Error inesperado: {e}")
    
    print("\n🏁 Tests completados!")

if __name__ == "__main__":
    main()