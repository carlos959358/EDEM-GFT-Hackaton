# Scripts de Testing del Backend

Este conjunto de scripts te permite verificar el estado y funcionamiento de todos los endpoints del backend desplegado en Cloud Run.

## 📁 Scripts Disponibles

### 1. `test_endpoints.py` - Testing Completo
**Propósito**: Testa TODOS los endpoints de la API de forma exhaustiva

**Uso**:
```bash
python test_endpoints.py
```

**Qué hace**:
- ✅ Verifica conectividad del servidor
- ✅ Testa todos los endpoints GET (lectura)  
- ✅ Testa algunos endpoints POST/PUT (escritura)
- ✅ Proporciona detalles de errores (códigos HTTP, mensajes)
- ✅ Genera reporte completo con estadísticas

**Ideal para**: Desarrollo, debugging, testing completo

---

### 2. `backend_status_report.py` - Reporte Ejecutivo
**Propósito**: Genera un reporte de estado claro y conciso

**Uso**:
```bash
python backend_status_report.py
```

**Qué hace**:
- 📊 Estado general del backend
- 🎯 Endpoints críticos únicamente
- 💡 Recomendaciones específicas de solución
- 📋 Diagnóstico del problema principal

**Ideal para**: Reportes, gestión, troubleshooting

---

### 3. `health_check.py` - Monitoreo Simple  
**Propósito**: Health check rápido para monitoreo continuo

**Uso básico**:
```bash
python health_check.py
# Retorna: PASS/FAIL + exit code
```

**Uso con detalles**:
```bash
python health_check.py -v
# Muestra más información
```

**Exit codes**:
- `0` = Todo OK  
- `1` = Problema general
- `2` = Error de base de datos
- `3` = Timeout
- `4` = Error de conexión
- `5` = Error inesperado

**Ideal para**: Monitoreo automático, scripts de CI/CD, alertas

---

## 🚨 Estado Actual Detectado

**Backend Status**: 🚨 **CRÍTICO**

**Problema principal**: Error de conectividad con la base de datos
- Servidor FastAPI: ✅ Funcionando
- Documentación API: ✅ Accesible  
- Base de Datos: ❌ **ERROR 500 en todos los endpoints**

## 🔧 Solución Recomendada

1. **Verificar configuración de Cloud SQL**
   ```bash
   gcloud sql instances list
   gcloud sql instances describe [INSTANCE_NAME]
   ```

2. **Revisar variables de entorno**
   - DATABASE_URL
   - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

3. **Verificar logs del contenedor**
   ```bash
   gcloud logging read "resource.type=cloud_run_revision" --limit=50
   ```

4. **Comprobar que las tablas existen**
   - Conectar a Cloud SQL
   - Verificar esquema de base de datos
   - Ejecutar script de inicialización si es necesario

5. **Comprobar permisos de conectividad**
   - Service account permissions
   - Cloud SQL Auth Proxy configuration
   - Network connectivity

## 📊 Ejemplo de Uso

### Desarrollo diario:
```bash
python health_check.py -v
```

### Testing completo:
```bash
python test_endpoints.py
```

### Reporte para gestión:
```bash
python backend_status_report.py
```

### Monitoreo automático:
```bash
#!/bin/bash
python health_check.py
if [ $? -ne 0 ]; then
    echo "¡ALERTA! Backend no funciona"
    # Enviar notificación, etc.
fi
```

## 🎯 URL del Backend

```
https://gft-hackaton-backend-297014562013.europe-west1.run.app
```

- 📚 Documentación: [/docs](https://gft-hackaton-backend-297014562013.europe-west1.run.app/docs)
- 🔧 OpenAPI Schema: [/openapi.json](https://gft-hackaton-backend-297014562013.europe-west1.run.app/openapi.json)