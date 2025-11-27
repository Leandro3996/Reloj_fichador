# Migración a Producción - 27 de Noviembre 2025

## Resumen Ejecutivo

Se realizó exitosamente la migración del sistema Reloj Fichador desde el entorno de desarrollo local hacia producción (192.168.10.39:5080). La migración incluyó nuevas funcionalidades, correcciones y simplificaciones solicitadas por el equipo de RRHH.

---

## 1. Análisis Previo

### 1.1 Diferencias Identificadas

Antes de la migración se realizó un análisis exhaustivo comparando ambos entornos:

| Elemento | Cantidad |
|----------|----------|
| Migraciones pendientes | 7 |
| Tablas nuevas | 9 |
| Dependencias nuevas | 6 |
| Tareas Celery nuevas | 3 |

### 1.2 Tablas Nuevas Agregadas

| Tabla | Descripción |
|-------|-------------|
| `reloj_fichador_calendariolaboral` | Calendario laboral (feriados, días especiales) |
| `reloj_fichador_calendariolaboral_areas` | Relación M2M calendario-áreas |
| `reloj_fichador_gruposabado` | Grupos A/B para sábados rotativos |
| `reloj_fichador_historicallicencia` | Auditoría de cambios en licencias médicas |
| `reloj_fichador_horasenfermedad` | Horas por enfermedad |
| `reloj_fichador_sugerenciaferiado` | Sugerencias de feriados desde API |
| `axes_accessattempt` | Intentos de acceso (seguridad) |
| `axes_accessfailurelog` | Log de fallos de login |
| `axes_accesslog` | Log de accesos |

### 1.3 Cambios en Tablas Existentes

**Tabla `reloj_fichador_licencia`:**
- Nuevos campos: `estado`, `aplicar_a_asistencia`, `aprobada_por_id`, `fecha_aprobacion`, `observaciones`
- Campo `archivo` ahora es opcional (NULL permitido)

**Tabla `reloj_fichador_registroasistencia`:**
- Nuevo campo: `licencia_relacionada_id` (FK a Licencia)

### 1.4 Dependencias Nuevas

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| `django-axes` | 6.5.1 | Protección contra fuerza bruta |
| `django-crispy-forms` | 2.4 | Formularios mejorados |
| `crispy-bootstrap5` | 2025.6 | Bootstrap 5 para formularios |
| `xlsxwriter` | 3.2.9 | Exportación Excel |
| `psycopg2-binary` | 2.9.9 | PostgreSQL (preparación futura) |
| `requests` | - | Cliente HTTP |

---

## 2. Proceso de Migración

### 2.1 Pasos Ejecutados

| # | Paso | Estado | Hora |
|---|------|--------|------|
| 1 | Detener servicios en producción | ✅ | 10:00 |
| 2 | Backup de referencia identificado | ✅ | 10:01 |
| 3 | Sincronizar código local → producción | ✅ | 10:05 |
| 4 | Rebuild imágenes Docker | ✅ | 10:10 |
| 5 | Ejecutar migraciones | ✅ | 10:15 |
| 6 | Iniciar servicios | ✅ | 10:18 |
| 7 | Verificar funcionamiento | ✅ | 10:20 |
| 8 | Asignar grupos de sábado | ✅ | 10:21 |

### 2.2 Comandos Utilizados

```bash
# Detener servicios
ssh sistemas@192.168.10.39 "cd /home/sistemas/Docker_proyectos/Reloj_fichador && docker compose down"

# Build
ssh sistemas@192.168.10.39 "cd /home/sistemas/Docker_proyectos/Reloj_fichador && docker compose build --no-cache"

# Migraciones
ssh sistemas@192.168.10.39 "cd /home/sistemas/Docker_proyectos/Reloj_fichador && docker compose run --rm web python manage.py migrate"

# Iniciar
ssh sistemas@192.168.10.39 "cd /home/sistemas/Docker_proyectos/Reloj_fichador && docker compose up -d"

# Asignar grupos sábado
ssh sistemas@192.168.10.39 "cd /home/sistemas/Docker_proyectos/Reloj_fichador && docker compose exec web python manage.py auto_assign_saturday_groups"
```

### 2.3 Migraciones Aplicadas

```
Applying admin_interface.0031_theme_form_actions_sticky... OK
Applying admin_interface.0032_alter_theme_defaults... OK
Applying axes.0001_initial... OK
Applying axes.0002_auto_20151217_2044... OK
Applying axes.0003_auto_20160322_0929... OK
Applying axes.0004_auto_20181024_1538... OK
Applying axes.0005_remove_accessattempt_trusted... OK
Applying axes.0006_remove_accesslog_trusted... OK
Applying axes.0007_alter_accessattempt_unique_together... OK
Applying axes.0008_accessfailurelog... OK
Applying axes.0009_add_session_hash... OK
Applying reloj_fichador.0028_reporte... OK
Applying reloj_fichador.0029_historicallicencia_licencia_aplicar_a_asistencia_and_more... OK
Applying reloj_fichador.0030_hacer_archivo_licencia_opcional... OK
Applying reloj_fichador.0032_add_calendario_laboral_y_grupo_sabado... OK
Applying reloj_fichador.0033_add_sugerencia_feriado... OK
Applying reloj_fichador.0034_add_horasenfermedade_model... OK
Applying reloj_fichador.0035_horas_totales_horas_enfermedad_and_more... OK
```

### 2.4 Asignación de Grupos de Sábado

Se ejecutó el comando `auto_assign_saturday_groups` con los siguientes resultados:

- **101 operarios** asignados automáticamente a grupos A/B
- **247 operarios** sin registros de sábados (no trabajan sábados o son nuevos)
- **Total procesados:** 348 operarios

---

## 3. Correcciones Post-Migración

### 3.1 Modelo Operario no visible en Admin

**Problema:** El modelo Operario no aparecía en el panel de administración.

**Causa:** Faltaba el decorador `@admin.register(Operario)` en la clase `OperarioAdmin`.

**Solución:** Se agregó el decorador:

```python
@admin.register(Operario)
class OperarioAdmin(ImportExportMixin, SimpleHistoryAdmin, admin.ModelAdmin):
    ...
```

### 3.2 Simplificación del Formulario de Licencias

**Solicitud de RRHH:** Eliminar las secciones "Configuración" y "Aprobación" del formulario de licencias, ya que no son necesarias para su flujo de trabajo.

**Cambio realizado:** Se simplificó el fieldset de `LicenciaAdmin`:

**Antes:**
- Información Básica
- Período de Licencia
- ⚙️ Configuración (estado, aplicar_a_asistencia)
- ✅ Aprobación (aprobada_por, fecha_aprobacion, observaciones)
- Metadatos

**Después:**
- Información Básica (operario, descripción, archivo)
- Período de Licencia (fecha_inicio, fecha_fin, duración)
- Metadatos (fecha_subida) - colapsado

---

## 4. Aclaración sobre Sistema de Licencias

Se identificó una confusión sobre el sistema de licencias:

### ¿Hay dos sistemas de licencias?

**No.** Existe un único modelo `Licencia` con dos puntos de entrada:

| Entrada | Ubicación | Uso |
|---------|-----------|-----|
| Botón "Cargar Licencia" | Desde cada RegistroAsistencia | Atajo rápido para cargar licencia desde una ausencia |
| Admin de Licencias | Menú principal → Licencias | Gestión completa de todas las licencias |

Ambos crean registros en la **misma tabla**.

---

## 5. Backup de Referencia

En caso de necesitar rollback:

- **Archivo:** `backup_2025-11-27_12.59.56.sql`
- **Ubicación:** `/home/sistemas/Docker_proyectos/Reloj_fichador/backups/`
- **Contenido:** BD de producción antes de aplicar migraciones

---

## 6. Nuevas Funcionalidades Disponibles

### 6.1 Calendario Laboral
- Gestión de feriados y días especiales
- Sincronización con API de feriados de Argentina
- Sugerencias automáticas de feriados

### 6.2 Grupos de Sábado
- Asignación de operarios a grupos A/B
- Rotación automática de sábados
- Comando para asignación automática basada en historial

### 6.3 Horas de Enfermedad
- Tracking de horas por licencias médicas
- Integración con Horas_totales

### 6.4 Seguridad Mejorada
- Django Axes para protección contra fuerza bruta
- Registro de intentos de acceso fallidos

### 6.5 Tareas Celery Nuevas

| Tarea | Propósito |
|-------|-----------|
| `verificar_licencias_activas` | Justifica ausencias con licencias activas |
| `sincronizar_feriados_api` | Sincroniza feriados desde API Argentina |
| `corregir_horas_negativas` | Corrige valores negativos automáticamente |

---

## 7. Verificación Final

- [x] Sistema accesible en http://192.168.10.39:5080/admin/
- [x] Login funcionando correctamente
- [x] Modelo Operario visible en admin
- [x] Nuevas secciones disponibles (Calendario, Grupos Sábado, etc.)
- [x] Registros de asistencia existentes intactos
- [x] Formulario de licencias simplificado
- [x] Grupos de sábado asignados

---

## 8. Notas Importantes

1. **Los datos NO fueron migrados** - Solo se sincronizó código. La BD de producción mantiene sus datos originales con las nuevas estructuras agregadas.

2. **Las tareas Celery** usan `get_or_create`, por lo que no sobrescriben registros existentes.

3. **El campo `licencia_relacionada`** en RegistroAsistencia quedará NULL para registros existentes, solo se vinculará cuando se aprueben nuevas licencias.

---

*Documento generado el 27 de Noviembre de 2025*
*Migración realizada con asistencia de Claude Code*
