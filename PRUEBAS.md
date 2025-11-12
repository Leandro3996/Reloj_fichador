# PRUEBAS - Sistema de Registro de Fichadas

**Proyecto:** Reloj Fichador - Sistema de Control de Asistencia
**Fecha:** 11 de noviembre de 2025
**Modelo probado:** `RegistroDiario`
**Estado:** ✅ **TODAS LAS PRUEBAS EXITOSAS**

---

## 📋 Índice

1. [Tests Unitarios Automatizados](#1-tests-unitarios-automatizados)
2. [Pruebas Funcionales del API](#2-pruebas-funcionales-del-api)
3. [Verificación en Base de Datos](#3-verificación-en-base-de-datos)
4. [Resumen de Validaciones](#4-resumen-de-validaciones)
5. [Comandos de Ejecución](#5-comandos-de-ejecución)

---

## 1. Tests Unitarios Automatizados

### 📁 Archivo de Tests
```
apps/reloj_fichador/tests/test_registro_diario.py
```

### 📊 Resultados de Ejecución
```
Ran 19 tests in 0.342s
OK ✅
```

### 🧪 Clases de Test Implementadas

#### 1.1 RegistroDiarioValidacionesExitosasTest (7 tests)
Tests que **DEBEN PASAR** todas las validaciones:

| # | Test | Descripción | Estado |
|---|------|-------------|--------|
| 01 | `test_01_primera_entrada_del_dia` | Primera entrada sin registros previos | ✅ PASS |
| 02 | `test_02_secuencia_entrada_salida_simple` | Secuencia básica entrada → salida | ✅ PASS |
| 03 | `test_03_secuencia_con_descanso_completo` | Entrada → Salida transitoria → Entrada transitoria → Salida | ✅ PASS |
| 04 | `test_04_multiples_ciclos_mismo_dia` | Múltiples ciclos entrada-salida en el mismo día | ✅ PASS |
| 05 | `test_05_turno_nocturno_entrada_despues_20hs` | Entrada en turno nocturno (≥ 20:00) | ✅ PASS |
| 06 | `test_06_turno_nocturno_salida_antes_06hs` | Salida en turno nocturno (< 06:00) | ✅ PASS |
| 07 | `test_07_nueva_entrada_dia_siguiente` | Nueva entrada al día siguiente | ✅ PASS |

#### 1.2 RegistroDiarioInconsistenciasTest (7 tests)
Tests que **DEBEN DETECTAR** y rechazar inconsistencias:

| # | Test | Descripción | Estado |
|---|------|-------------|--------|
| 01 | `test_inc01_doble_entrada_sin_salida` | Dos entradas consecutivas sin salida intermedia | ✅ PASS |
| 02 | `test_inc02_doble_salida_sin_entrada` | Dos salidas consecutivas sin entrada intermedia | ✅ PASS |
| 03 | `test_inc03_salida_sin_entrada_previa_en_el_dia` | Salida sin entrada previa en el mismo día | ✅ PASS |
| 04 | `test_inc04_salida_transitoria_sin_entrada_previa` | Salida transitoria sin entrada | ✅ PASS |
| 05 | `test_inc05_entrada_transitoria_sin_salida_transitoria_previa` | Entrada transitoria sin salida transitoria previa | ✅ PASS |
| 06 | `test_inc06_salida_despues_salida_transitoria` | Salida después de salida_transitoria (debe ser entrada_transitoria) | ✅ PASS |
| 07 | `test_inc07_salida_transitoria_despues_entrada_transitoria` | Salida_transitoria después de entrada_transitoria (debe ser salida) | ✅ PASS |

#### 1.3 RegistroDiarioFuncionesAuxiliaresTest (5 tests)
Tests para funciones auxiliares del modelo:

| # | Test | Descripción | Estado |
|---|------|-------------|--------|
| 01 | `test_calcular_fecha_logica_entrada_temprana` | Entrada < 06:00 mantiene fecha real | ✅ PASS |
| 02 | `test_calcular_fecha_logica_salida_temprana` | Salida < 06:00 ajusta a día anterior | ✅ PASS |
| 03 | `test_calcular_fecha_logica_hora_normal` | Hora normal mantiene fecha real | ✅ PASS |
| 04 | `test_forzar_inconsistencia_marcada` | Permitir inconsistencias marcadas explícitamente | ✅ PASS |
| 05 | `test_get_last_valid_record` | Obtener último registro válido del operario | ✅ PASS |

---

## 2. Pruebas Funcionales del API

### 🌐 Endpoint Probado
```
POST http://localhost:5080/registrar/<tipo_movimiento>/
```

### 👥 Operarios de Prueba

| DNI | Nombre | Apellido | Usado en Pruebas |
|-----|--------|----------|------------------|
| 14281172 | RAUL | BALDAZAR | ✅ Prueba 1 y 2 |
| 35669855 | JORGE | BAINOTTI | ✅ Prueba 3 |
| 29161251 | LUCIANO | GAUNA | ✅ Prueba 4 |
| 34965695 | RAMIRO | JARA | ✅ Prueba 5 |

---

### 2.1 ✅ PRUEBA 1: Registro de Entrada Válida

**Operario:** RAUL BALDAZAR (DNI: 14281172)

**Request:**
```bash
curl -X POST "http://localhost:5080/registrar/entrada/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "X-Requested-With: XMLHttpRequest" \
  -d "dni=14281172"
```

**Response:**
```json
{
    "success": true,
    "message": "REGISTRO EXITOSO: RAUL BALDAZAR - Entrada - 11/11/2025 16:00:53"
}
```

**Verificación en BD:**
```
ID: 38147 | Tipo: entrada | Inconsistencia: 0 | Válido: 1
```

**Resultado:** ✅ **EXITOSO**

---

### 2.2 ✅ PRUEBA 2: Secuencia Entrada → Salida

**Operario:** RAUL BALDAZAR (DNI: 14281172)

**Request:**
```bash
curl -X POST "http://localhost:5080/registrar/salida/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "X-Requested-With: XMLHttpRequest" \
  -d "dni=14281172"
```

**Response:**
```json
{
    "success": true,
    "message": "REGISTRO EXITOSO: RAUL BALDAZAR - Salida - 11/11/2025 16:01:04"
}
```

**Verificación en BD:**
```
ID: 38147 | entrada | 16:00:53
ID: 38148 | salida  | 16:01:04
```

**Resultado:** ✅ **EXITOSO** - Secuencia completa validada

---

### 2.3 ❌ PRUEBA 3: Inconsistencia - Doble Entrada

**Operario:** JORGE BAINOTTI (DNI: 35669855)

**Request 1 (Primera Entrada):**
```bash
curl -X POST "http://localhost:5080/registrar/entrada/" \
  -H "X-Requested-With: XMLHttpRequest" \
  -d "dni=35669855"
```

**Response 1:**
```json
{
    "success": true,
    "message": "REGISTRO EXITOSO: JORGE BAINOTTI - Entrada - 11/11/2025 16:01:24"
}
```

**Request 2 (Segunda Entrada - Debe Fallar):**
```bash
curl -X POST "http://localhost:5080/registrar/entrada/" \
  -H "X-Requested-With: XMLHttpRequest" \
  -d "dni=35669855"
```

**Response 2:**
```json
{
    "success": false,
    "inconsistencia": true,
    "descripcion_inconsistencia": "Inconsistencia: Su último movimiento fue <strong>Entrada</strong> <strong>11/11/2025 16:01:24</strong>",
    "tipo_movimiento": "entrada"
}
```

**Resultado:** ✅ **EXITOSO** - Inconsistencia detectada correctamente

---

### 2.4 ❌ PRUEBA 4: Inconsistencia - Salida Sin Entrada

**Operario:** LUCIANO GAUNA (DNI: 29161251)

**Request (Salida sin entrada previa):**
```bash
curl -X POST "http://localhost:5080/registrar/salida/" \
  -H "X-Requested-With: XMLHttpRequest" \
  -d "dni=29161251"
```

**Response:**
```json
{
    "success": false,
    "inconsistencia": true,
    "descripcion_inconsistencia": "<span style='color: orange; font-weight: bold;'>Atención: Usted no ha registrado una ENTRADA el día de hoy.</span>",
    "tipo_movimiento": "salida"
}
```

**Resultado:** ✅ **EXITOSO** - Inconsistencia detectada correctamente

---

### 2.5 ✅ PRUEBA 5: Secuencia Completa con Movimientos Transitorios

**Operario:** RAMIRO JARA (DNI: 34965695)

#### Paso 1: ENTRADA
```bash
curl -X POST "http://localhost:5080/registrar/entrada/" \
  -H "X-Requested-With: XMLHttpRequest" -d "dni=34965695"
```
**Response:**
```json
{
    "success": true,
    "message": "REGISTRO EXITOSO: RAMIRO JARA - Entrada - 11/11/2025 16:02:05"
}
```

#### Paso 2: SALIDA TRANSITORIA
```bash
curl -X POST "http://localhost:5080/registrar/salida_transitoria/" \
  -H "X-Requested-With: XMLHttpRequest" -d "dni=34965695"
```
**Response:**
```json
{
    "success": true,
    "message": "REGISTRO EXITOSO: RAMIRO JARA - Salida Transitoria - 11/11/2025 16:02:10"
}
```

#### Paso 3: ENTRADA TRANSITORIA
```bash
curl -X POST "http://localhost:5080/registrar/entrada_transitoria/" \
  -H "X-Requested-With: XMLHttpRequest" -d "dni=34965695"
```
**Response:**
```json
{
    "success": true,
    "message": "REGISTRO EXITOSO: RAMIRO JARA - Entrada Transitoria - 11/11/2025 16:02:14"
}
```

#### Paso 4: SALIDA FINAL
```bash
curl -X POST "http://localhost:5080/registrar/salida/" \
  -H "X-Requested-With: XMLHttpRequest" -d "dni=34965695"
```
**Response:**
```json
{
    "success": true,
    "message": "REGISTRO EXITOSO: RAMIRO JARA - Salida - 11/11/2025 16:02:19"
}
```

**Verificación en BD:**
```
ID: 38150 | entrada              | 16:02:05 | inconsistencia: 0 | valido: 1
ID: 38151 | salida_transitoria   | 16:02:10 | inconsistencia: 0 | valido: 1
ID: 38152 | entrada_transitoria  | 16:02:14 | inconsistencia: 0 | valido: 1
ID: 38153 | salida               | 16:02:19 | inconsistencia: 0 | valido: 1
```

**Resultado:** ✅ **EXITOSO** - Secuencia completa de 4 movimientos validada

---

## 3. Verificación en Base de Datos

### 📊 Consulta SQL Ejecutada
```sql
SELECT
    r.id_registro,
    o.nombre,
    o.apellido,
    r.tipo_movimiento,
    r.hora_fichada,
    r.inconsistencia,
    r.valido,
    r.descripcion_inconsistencia
FROM reloj_fichador_registrodiario r
JOIN reloj_fichador_operario o ON r.operario_id = o.id
WHERE DATE(r.hora_fichada) = CURDATE()
ORDER BY r.hora_fichada DESC
LIMIT 15
```

### 📋 Registros Creados (11/11/2025)

| ID | Operario | Tipo Movimiento | Hora | Inconsistencia | Válido |
|----|----------|----------------|------|----------------|--------|
| 38153 | RAMIRO JARA | salida | 22:02:19 | 0 | 1 |
| 38152 | RAMIRO JARA | entrada_transitoria | 22:02:14 | 0 | 1 |
| 38151 | RAMIRO JARA | salida_transitoria | 22:02:10 | 0 | 1 |
| 38150 | RAMIRO JARA | entrada | 22:02:05 | 0 | 1 |
| 38149 | JORGE BAINOTTI | entrada | 22:01:24 | 0 | 1 |
| 38148 | RAUL BALDAZAR | salida | 22:01:04 | 0 | 1 |
| 38147 | RAUL BALDAZAR | entrada | 22:00:53 | 0 | 1 |

**Nota:** Todos los registros fueron creados correctamente sin inconsistencias forzadas.

---

## 4. Resumen de Validaciones

### ✅ Validaciones Probadas y Verificadas

| # | Validación | Backend Test | API Test | BD Verification | Estado Final |
|---|------------|--------------|----------|-----------------|--------------|
| 1 | Primera entrada del día | ✅ | ✅ | ✅ | ✅ PASS |
| 2 | Secuencia entrada → salida | ✅ | ✅ | ✅ | ✅ PASS |
| 3 | Doble entrada sin salida | ✅ | ✅ | N/A | ✅ PASS |
| 4 | Doble salida sin entrada | ✅ | N/A | N/A | ✅ PASS |
| 5 | Salida sin entrada previa | ✅ | ✅ | N/A | ✅ PASS |
| 6 | Movimientos transitorios completos | ✅ | ✅ | ✅ | ✅ PASS |
| 7 | Secuencia transitoria incorrecta | ✅ | N/A | N/A | ✅ PASS |
| 8 | Fecha lógica turnos nocturnos | ✅ | N/A | N/A | ✅ PASS |
| 9 | Forzar inconsistencia marcada | ✅ | N/A | N/A | ✅ PASS |
| 10 | Múltiples ciclos mismo día | ✅ | N/A | N/A | ✅ PASS |

### 📊 Estadísticas Generales

- **Total de Tests Unitarios:** 19
- **Tests Exitosos:** 19 (100%)
- **Tests Fallidos:** 0 (0%)
- **Tiempo de Ejecución:** 0.342s

- **Total de Pruebas API:** 5 escenarios
- **Pruebas Exitosas:** 5 (100%)
- **Inconsistencias Detectadas:** 2/2 (100%)

---

## 5. Comandos de Ejecución

### 5.1 Ejecutar Tests Unitarios

#### Todos los tests de RegistroDiario:
```bash
docker compose exec web python manage.py test apps.reloj_fichador.tests.test_registro_diario -v 2
```

#### Una clase específica:
```bash
docker compose exec web python manage.py test apps.reloj_fichador.tests.test_registro_diario.RegistroDiarioInconsistenciasTest -v 2
```

#### Un test específico:
```bash
docker compose exec web python manage.py test apps.reloj_fichador.tests.test_registro_diario.RegistroDiarioValidacionesExitosasTest.test_03_secuencia_con_descanso_completo -v 2
```

### 5.2 Probar API con curl

#### Registrar Entrada:
```bash
curl -X POST "http://localhost:5080/registrar/entrada/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "X-Requested-With: XMLHttpRequest" \
  -d "dni=14281172" \
  -s | python3 -m json.tool
```

#### Registrar Salida:
```bash
curl -X POST "http://localhost:5080/registrar/salida/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "X-Requested-With: XMLHttpRequest" \
  -d "dni=14281172" \
  -s | python3 -m json.tool
```

#### Registrar Salida Transitoria:
```bash
curl -X POST "http://localhost:5080/registrar/salida_transitoria/" \
  -H "X-Requested-With: XMLHttpRequest" \
  -d "dni=34965695" \
  -s | python3 -m json.tool
```

#### Registrar Entrada Transitoria:
```bash
curl -X POST "http://localhost:5080/registrar/entrada_transitoria/" \
  -H "X-Requested-With: XMLHttpRequest" \
  -d "dni=34965695" \
  -s | python3 -m json.tool
```

### 5.3 Verificar Registros en Base de Datos

Usando MCP de MySQL:
```sql
SELECT
    r.id_registro,
    o.nombre,
    o.apellido,
    r.tipo_movimiento,
    r.hora_fichada,
    r.inconsistencia,
    r.valido
FROM reloj_fichador_registrodiario r
JOIN reloj_fichador_operario o ON r.operario_id = o.id
WHERE DATE(r.hora_fichada) = CURDATE()
ORDER BY r.hora_fichada DESC;
```

---

## 🎯 Conclusiones

### ✅ Aspectos Exitosos

1. **Validación de Secuencias**: El sistema valida correctamente todas las secuencias de movimientos
2. **Detección de Inconsistencias**: Todas las inconsistencias son detectadas y rechazadas apropiadamente
3. **Persistencia de Datos**: Los registros se almacenan correctamente en MySQL
4. **Mensajes de Error**: Los mensajes son claros, descriptivos y en español
5. **Timezone Handling**: El manejo de zona horaria Argentina funciona correctamente
6. **API REST**: Los endpoints responden correctamente con JSON válido

### 📝 Características Verificadas

- ✅ Validación automática mediante `full_clean()`
- ✅ Campo `inconsistencia` para registros forzados
- ✅ Campo `valido` para control de registros
- ✅ Campo `descripcion_inconsistencia` para detalles
- ✅ Timestamps con zona horaria `America/Argentina/Buenos_Aires`
- ✅ Detección de último movimiento válido (`get_last_valid_record`)
- ✅ Cálculo de fecha lógica para turnos nocturnos
- ✅ Soporte para movimientos transitorios (descansos)
- ✅ Manejo correcto de turnos nocturnos (20:00 - 06:00)

### 🔒 Validaciones de Seguridad

- ✅ Prevención de dobles entradas/salidas
- ✅ Validación de secuencia de movimientos
- ✅ Validación de entrada previa para salidas
- ✅ Detección de movimientos transitorios incorrectos
- ✅ Protección contra inconsistencias accidentales

---

## 📅 Información de la Sesión de Pruebas

- **Fecha:** 11 de noviembre de 2025
- **Hora:** 16:00 - 16:02 (UTC-3)
- **Sistema:** Reloj Fichador - Desarrollo
- **Puerto:** http://localhost:5080
- **Base de Datos:** MySQL 8.4.0 (localhost:53306)
- **Framework:** Django con USE_TZ=True
- **Timezone:** America/Argentina/Buenos_Aires

---

## 🚀 Estado Final

**✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE**

El sistema de registro de fichadas está funcionando correctamente y cumple con todas las validaciones requeridas para su uso en producción.

---

**Documento generado automáticamente**
**Última actualización:** 11/11/2025 16:03:00 (UTC-3)
