# Preparación para Migración a Producción

**Fecha del análisis:** 2025-11-27
**Objetivo:** Documentar todas las diferencias entre el entorno LOCAL y PRODUCCIÓN antes del switch.

---

## 1. Resumen Ejecutivo

Se identificaron diferencias significativas entre el sistema local (desarrollo) y producción:

- **7 migraciones** pendientes de aplicar
- **9 tablas** nuevas
- **6 dependencias** nuevas en requirements.txt
- **3 tareas Celery** nuevas programadas
- **Backups automáticos** funcionando correctamente en ambos entornos

**Conclusión principal:** Los registros de asistencia existentes NO se verán afectados. Las migraciones son aditivas (agregan campos/tablas) y las tareas Celery usan `get_or_create` para no sobrescribir datos.

---

## 2. Diferencias en Base de Datos

### 2.1 Tablas Nuevas (9 tablas)

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

### 2.2 Cambios en Tablas Existentes

#### Tabla `reloj_fichador_licencia` (Licencias Médicas)

| Campo Nuevo | Tipo | Default | Descripción |
|-------------|------|---------|-------------|
| `estado` | varchar(10) | 'pendiente' | pendiente / aprobada / rechazada |
| `aplicar_a_asistencia` | boolean | true | Si justifica ausencias automáticamente |
| `aprobada_por_id` | FK (User) | NULL | Usuario que aprobó/rechazó |
| `fecha_aprobacion` | datetime | NULL | Fecha y hora de aprobación |
| `observaciones` | text | NULL | Notas del aprobador |

**Cambio adicional:** El campo `archivo` pasó de `NOT NULL` a `NULL` (ahora es opcional).

#### Tabla `reloj_fichador_registroasistencia`

| Campo Nuevo | Tipo | Descripción |
|-------------|------|-------------|
| `licencia_relacionada_id` | FK (Licencia) | Vincula la ausencia con una licencia médica |

### 2.3 Tablas Sin Cambios

Las siguientes tablas son idénticas en ambos entornos:
- `reloj_fichador_operario`
- `reloj_fichador_registrodiario`
- `reloj_fichador_horas_trabajadas`
- `reloj_fichador_area`

---

## 3. Migraciones Pendientes

7 migraciones deben aplicarse en producción:

| # | Migración | Descripción |
|---|-----------|-------------|
| 1 | `0028_reporte` | Modelo de reportes |
| 2 | `0029_historicallicencia_licencia_aplicar_a_asistencia_and_more` | Historial licencias + campos nuevos |
| 3 | `0030_hacer_archivo_licencia_opcional` | Campo archivo nullable |
| 4 | `0032_add_calendario_laboral_y_grupo_sabado` | Calendario laboral + grupos sábado |
| 5 | `0033_add_sugerencia_feriado` | Sugerencias de feriados |
| 6 | `0034_add_horasenfermedade_model` | Modelo horas enfermedad |
| 7 | `0035_horas_totales_horas_enfermedad_and_more` | Campo horas_enfermedad en totales |

**Nota:** No existe migración 0031 (fue omitida en el desarrollo).

**Verificación de seguridad:** Ninguna migración contiene operaciones `RunPython`, `DELETE`, `UPDATE` o `TRUNCATE`. Todas son operaciones aditivas seguras.

---

## 4. Dependencias (requirements.txt)

### 4.1 Paquetes Nuevos

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| `django-axes` | 6.5.1 | Seguridad - protección contra fuerza bruta |
| `django-crispy-forms` | 2.4 | Formularios mejorados |
| `crispy-bootstrap5` | 2025.6 | Bootstrap 5 para formularios |
| `xlsxwriter` | 3.2.9 | Exportación Excel mejorada |
| `psycopg2-binary` | 2.9.9 | PostgreSQL (preparación futura) |
| `requests` | - | Cliente HTTP |

### 4.2 Paquetes Actualizados

| Paquete | Producción | Local |
|---------|------------|-------|
| `django-admin-interface` | 0.28.8 | 0.31.0 |
| `django-import-export` | 4.1.1 | 4.3.13 |
| `pandas` | 2.2.2 | 2.3.3 |
| `weasyprint` | 62.3 | 66.0 |
| `openpyxl` | 3.0.10 | 3.1.5 |
| `tablib` | 3.5.0 | 3.9.0 |

### 4.3 Paquetes a Eliminar

| Paquete | Motivo |
|---------|--------|
| `django-colorfield` | Ya no es dependencia directa (era de admin-interface antiguo) |

---

## 5. Tareas Celery

### 5.1 Tareas en Producción (actual)

| Tarea | Horario |
|-------|---------|
| `generar_registros_asistencia` | 5:00 AM diario |
| `celery.backend_cleanup` | Cada 4 horas |

### 5.2 Tareas Nuevas (se agregarán)

| Tarea | Propósito | Impacto |
|-------|-----------|---------|
| `verificar_licencias_activas` | Justifica ausencias con licencias activas | Solo actualiza si `estado_justificacion=False` |
| `sincronizar_feriados_api` | Sincroniza feriados desde API Argentina | Solo crea sugerencias |
| `corregir_horas_negativas` | Corrige valores negativos (errores) | Solo corrige anomalías |

### 5.3 Análisis de Impacto en Registros Existentes

**Conclusión: Los registros existentes NO se modificarán destructivamente.**

| Tarea | Comportamiento | Seguro |
|-------|---------------|--------|
| `generar_registros_asistencia` | Usa `get_or_create` | ✅ No sobrescribe |
| `verificar_licencias_activas` | Solo actualiza no justificados | ✅ No modifica ya justificados |
| `procesar_licencia_aprobada` | Solo cuando RRHH aprueba licencia | ✅ Bajo demanda |
| `sincronizar_feriados_api` | Crea sugerencias, no toca asistencia | ✅ Sin impacto |
| `corregir_horas_negativas` | Solo corrige valores negativos | ✅ Solo errores |

---

## 6. Flujo de Licencias Médicas (Nueva Funcionalidad)

El sistema ahora soporta un flujo completo de gestión de licencias médicas:

```
1. Operario falta al trabajo
   └── Se crea RegistroAsistencia (estado_asistencia='ausente', estado_justificacion=False)

2. Operario presenta certificado médico
   └── Se carga Licencia (estado='pendiente')

3. RRHH aprueba la licencia
   └── Tarea Celery procesa automáticamente:
       - Justifica ausencias en el período de la licencia
       - Vincula RegistroAsistencia con la licencia (licencia_relacionada_id)
       - Calcula y registra horas de enfermedad
       - Actualiza Horas_totales del mes

4. Resultado
   └── RegistroAsistencia: estado_justificacion=True, licencia_relacionada=<licencia>
```

**Retroactividad:** El sistema puede justificar ausencias hasta 30 días antes de la fecha de inicio de la licencia.

---

## 7. Diferencias en docker-compose.yml

| Aspecto | Producción | Local |
|---------|------------|-------|
| Web command | `migrate && collectstatic && gunicorn` | `collectstatic && gunicorn --timeout 120` |
| Celery-beat | `migrate && celery beat` | `celery beat` (sin migrate) |

**Nota:** En producción se ejecuta `migrate` automáticamente al iniciar. En local, las migraciones se ejecutan manualmente.

---

## 8. Sistema de Backups

Ambos entornos tienen backups automáticos funcionando:

| Entorno | Frecuencia | Último Backup | Tamaño |
|---------|------------|---------------|--------|
| Local | Cada 30 min | 2025-11-26 15:24 | ~11MB |
| Producción | Cada 30 min | 2025-11-26 15:17 | ~11MB |

**Ubicación:** Carpeta `backups/` en cada proyecto.

---

## 9. Plan de Migración

### Pasos a Ejecutar

1. ~~Backup completo de BD producción~~ → **Ya cubierto automáticamente**

2. **Parar servicios en producción**
   ```bash
   ssh usuario@192.168.10.39
   cd /ruta/proyecto
   docker compose down
   ```

3. **Sincronizar código**
   ```bash
   rsync -avz --exclude='backups' --exclude='.env' --exclude='media' \
     /home/leandro/Proyectos_Docker/Reloj_fichador/ \
     usuario@192.168.10.39:/ruta/proyecto/
   ```

4. **Rebuild imágenes Docker**
   ```bash
   docker compose build --no-cache
   ```

5. **Ejecutar migraciones**
   ```bash
   docker compose run --rm web python manage.py migrate
   ```

6. **Iniciar servicios**
   ```bash
   docker compose up -d
   ```

7. **Verificar funcionamiento**
   - Acceder a http://192.168.10.39:5080/admin/
   - Verificar que las nuevas tablas existen
   - Verificar que Celery está procesando tareas
   - Verificar logs: `docker compose logs -f web celery`

### Rollback (si algo falla)

1. Parar servicios: `docker compose down`
2. Restaurar código anterior (git o backup)
3. Restaurar base de datos desde backup más reciente
4. Iniciar servicios: `docker compose up -d`

---

## 10. Checklist Pre-Migración

- [x] Identificar diferencias en tablas de BD
- [x] Revisar migraciones pendientes
- [x] Comparar requirements.txt
- [x] Analizar tareas Celery
- [x] Verificar impacto en registros existentes
- [x] Confirmar backups funcionando
- [x] Documentar plan de migración
- [ ] Elegir ventana de mantenimiento (fuera de horario laboral)
- [ ] Notificar a usuarios sobre el mantenimiento
- [ ] Ejecutar migración
- [ ] Verificar funcionamiento post-migración

---

## 11. Contacto y Soporte

**Proyecto:** Reloj Fichador
**Repositorio:** `/home/leandro/Proyectos_Docker/Reloj_fichador`
**Producción:** http://192.168.10.39:5080
**Local:** http://localhost:58000

---

*Documento generado durante sesión de análisis con Claude Code*
