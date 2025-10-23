# 🧪 SUITE DE TESTS - RELOJ FICHADOR

**Versión:** 1.0
**Fecha de creación:** 23 de Octubre de 2025
**Estado:** ✅ COMPLETADA Y DOCUMENTADA

---

## 📋 DESCRIPCIÓN GENERAL

Esta es una suite completa de **20 test cases** que validan las nuevas funcionalidades implementadas en el Reloj Fichador:

1. **Sincronización automática de feriados** (10 tests)
2. **Gestión de licencias médicas** (10 tests)

---

## 🗂️ ESTRUCTURA DEL DIRECTORIO TEST

```
TEST/
├── README_TESTS.md                          # Este archivo - Guía rápida
├── REPORTE_TESTS.md                         # Reporte detallado de tests
├── __init__.py                              # Módulo inicialización
│
├── test_sincronizacion_feriados.py          # 10 tests para feriados
│   ├── SincronizacionFeriadosAPITestCase
│   │   ├── test_01_obtener_feriados_api_exitoso
│   │   ├── test_02_crear_sugerencia_feriado
│   │   ├── test_03_prevenir_duplicados
│   │   ├── test_04_aceptar_sugerencia
│   │   ├── test_05_rechazar_sugerencia
│   │   ├── test_06_tarea_celery_sincronizar
│   │   ├── test_07_comando_management_sincronizar
│   │   ├── test_08_es_dia_laboral_feriado
│   │   ├── test_09_obtener_feriados_mes
│   │   └── test_10_no_crear_registro_en_feriado
│   │
│   └── SincronizacionConRegistroAsistenciaTestCase
│       └── test_10_no_crear_registro_en_feriado
│
├── test_licencias_medicas.py                # 10 tests para licencias
│   ├── LicenciasMedicasTestCase
│   │   ├── test_01_crear_licencia_medica
│   │   ├── test_02_campos_licencia_medica
│   │   ├── test_03_procesar_licencia_aprobada
│   │   ├── test_04_verificar_licencias_activas
│   │   ├── test_05_licencia_rechazada
│   │   ├── test_06_licencia_sin_aplicar_asistencia
│   │   ├── test_07_multiples_licencias_mismo_periodo
│   │   ├── test_08_duracion_licencia_medica
│   │   ├── test_09_justificacion_de_ausencia
│   │   └── test_10_tipos_licencia
│   │
│   └── SincronizacionConRegistroAsistenciaTestCase (hereda de anterior)
│
└── run_tests.py                             # Script para ejecutar tests
```

---

## 🚀 INICIO RÁPIDO

### Ejecutar TODOS los tests

```bash
docker compose exec web python manage.py test TEST -v 2
```

### Ejecutar solo tests de SINCRONIZACIÓN

```bash
docker compose exec web python manage.py test TEST.test_sincronizacion_feriados -v 2
```

### Ejecutar solo tests de LICENCIAS

```bash
docker compose exec web python manage.py test TEST.test_licencias_medicas -v 2
```

### Ejecutar UN test específico

```bash
docker compose exec web python manage.py test TEST.test_sincronizacion_feriados.SincronizacionFeriadosAPITestCase.test_01_obtener_feriados_api_exitoso -v 2
```

### Ejecutar con script

```bash
docker compose exec web python TEST/run_tests.py
```

---

## 📚 DESCRIPCIÓN DE TEST CASES

### SINCRONIZACIÓN DE FERIADOS (test_sincronizacion_feriados.py)

#### Test 1: Obtener feriados de API
```
✅ Verifica que obtener_feriados_api() se conecta a ArgentinaDatos
   - Conexión exitosa
   - Retorna lista de feriados
   - Mínimo 1 feriado por año
```

#### Test 2: Crear sugerencia de feriado
```
✅ Verifica creación de SugerenciaFeriado
   - Se crea con ID
   - Estados válidos (pendiente, aceptado, rechazado)
   - Campos requeridos presentes
```

#### Test 3: Prevenir duplicados
```
✅ Verifica que no se crean sugerencias duplicadas
   - get_or_create() funciona correctamente
   - Una fecha = una sugerencia por fuente
```

#### Test 4: Aceptar sugerencia
```
✅ Verifica aceptación de sugerencia
   - Se crea en CalendarioLaboral
   - Estado cambia a "aceptado"
   - Fecha se excluye de registros de asistencia
```

#### Test 5: Rechazar sugerencia
```
✅ Verifica rechazo de sugerencia
   - Estado cambia a "rechazado"
   - NO se crea en CalendarioLaboral
   - Permite guardar observaciones
```

#### Test 6: Tarea Celery
```
✅ Verifica sincronizar_feriados_api() de Celery
   - Se ejecuta sin errores
   - Crea sugerencias para feriados nuevos
   - Evita duplicados
   - Retorna resumen
```

#### Test 7: Comando management
```
✅ Verifica comando Django sincronizar_feriados
   - Se ejecuta sin errores
   - Retorna salida informativa
   - Procesa año actual por defecto
```

#### Test 8: es_dia_laboral()
```
✅ Verifica validación de días laborales
   - Feriado aceptado = no laboral
   - Lunes-viernes = laboral
   - Domingos = no laboral
```

#### Test 9: Obtener feriados del mes
```
✅ Verifica obtener_feriados_mes()
   - Retorna solo feriados del mes
   - Excluye otros meses
   - Estructura correcta
```

#### Test 10: No crear registro en feriado
```
✅ Verifica generar_registros_asistencia()
   - No crea en feriados
   - Sí crea en días normales
```

---

### LICENCIAS MÉDICAS (test_licencias_medicas.py)

#### Test 1: Crear licencia
```
✅ Verifica creación de Licencia
   - Se crea con ID
   - Campos requeridos
   - Estados válidos
```

#### Test 2: Campos de licencia
```
✅ Verifica campos específicos
   - estado (pendiente/aprobada/rechazada)
   - aplicar_a_asistencia (booleano)
   - aprobada_por (User FK)
   - fecha_aprobacion (DateTime)
   - observaciones (Text)
```

#### Test 3: Procesar licencia aprobada
```
✅ Verifica procesar_licencia_aprobada()
   - Crea RegistroAsistencia por día
   - Marca como ausente justificado
   - Vincula a licencia
```

#### Test 4: Verificar licencias activas
```
✅ Verifica verificar_licencias_activas()
   - Identifica licencias de hoy
   - Crea registros justificados
   - Se ejecuta sin errores
```

#### Test 5: Licencia rechazada
```
✅ Verifica rechazo de licencia
   - No procesa asistencia
   - Permite guardar razón
   - Estado = rechazada
```

#### Test 6: Sin aplicar a asistencia
```
✅ Verifica licencias que no afectan asistencia
   - aplicar_a_asistencia = False
   - No crea registros
```

#### Test 7: Múltiples licencias
```
✅ Verifica múltiples licencias simultáneas
   - Operario puede tener varias
   - Se procesan sin conflictos
```

#### Test 8: Duración de licencia
```
✅ Verifica cálculo de días
   - Inclusividad (inicio Y fin)
   - Cálculo correcto
```

#### Test 9: Justificación de ausencia
```
✅ Verifica justificación automática
   - estado_justificacion = True
   - licencia_relacionada = Licencia
```

#### Test 10: Tipos de licencia
```
✅ Verifica diferentes tipos
   - medica, vacaciones, especial, otra
   - Todos se guardan correctamente
```

---

## 🔧 CONFIGURACIÓN

### Dependencias

Los tests requieren:
- Django 5.1+
- Python 3.11+
- MySQL 8.4+ (para tests con DB real)
- requests (para API calls)

### Instalar dependencias

```bash
# En el contenedor web
docker compose exec web pip install requests
```

### Configuración de tests

Tests usan SQLite en memoria por defecto (rápido):
```python
# settings.py test configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
```

Para usar MySQL en tests:
```bash
docker compose exec web python manage.py test TEST --settings=tests_utils.mysql_settings
```

---

## 📊 RESULTADOS ESPERADOS

### Ejecución exitosa
```
Ran 20 tests in X.XXXs

OK
```

### Ejecución con fallos
```
FAILED (failures=X, errors=Y)
```

**Troubleshooting:**
- ❌ `ModuleNotFoundError: requests` → `pip install requests`
- ❌ Migration errors → `python manage.py migrate`
- ❌ Schema mismatch → Sincronizar migraciones
- ❌ Database locked → Reiniciar servicios

---

## 📈 COBERTURA

**Total funcionalidades cubiertas:** 20 cases
- Sincronización: 10 tests ✅
- Licencias: 10 tests ✅

**Cobertura por módulo:**
- `apps/reloj_fichador/tasks.py` → 4 tests
- `apps/reloj_fichador/utils.py` → 4 tests
- `apps/reloj_fichador/models.py` → 8 tests
- `apps/reloj_fichador/management/commands/` → 2 tests
- `apps/reloj_fichador/admin.py` → 2 tests (implícito)

---

## 🎯 VALIDACIÓN INCLUIDA

Cada test incluye:
- ✅ Setup: Configuración inicial
- ✅ Assertions: Verificaciones múltiples
- ✅ Cleanup: Limpieza de datos
- ✅ Mensajes descriptivos
- ✅ Documentación inline

---

## 📝 EXTENSIÓN DE TESTS

Para agregar nuevos tests:

1. **Crear nueva clase TestCase:**
```python
class NuevoTestCase(TestCase):
    def setUp(self):
        # Crear datos de prueba
        pass

    def test_nueva_funcionalidad(self):
        # Implementar test
        self.assertEqual(resultado, esperado)
```

2. **Agregar a archivo correspondiente:**
   - `test_sincronizacion_feriados.py` - para feriados
   - `test_licencias_medicas.py` - para licencias

3. **Documentar en REPORTE_TESTS.md**

---

## 🔄 INTEGRACIÓN CONTINUA

Para agregar a CI/CD:

```yaml
# .github/workflows/tests.yml
- name: Run tests
  run: docker compose exec web python manage.py test TEST -v 2
```

---

## 📞 SOPORTE

**Documentación adicional:**
- [REPORTE_TESTS.md](REPORTE_TESTS.md) - Documentación detallada
- [Django Testing Docs](https://docs.djangoproject.com/en/5.1/topics/testing/)
- [Celery Testing](https://docs.celeryproject.org/en/latest/userguide/testing.html)

**Contacto:** Claude Code (AI Assistant)

---

## ✅ CHECKLIST

- [x] 10 tests para sincronización de feriados
- [x] 10 tests para licencias médicas
- [x] Documentación completa
- [x] Script de ejecución
- [x] Reporte de resultados
- [x] Guía rápida (este archivo)
- [ ] Tests pasando 100% (en progreso)
- [ ] Integración CI/CD (próximo)

---

**Estado:** 🟡 LISTO PARA REVISIÓN (requiere arreglos menores)

