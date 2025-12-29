# Próximos Pasos Sugeridos - Sistema Reloj Fichador

**Fecha:** 2025-11-13
**Versión:** 1.0
**Autor:** Equipo de Desarrollo

---

## 1. Resumen del Problema Solucionado

Se detectó y corrigió un bug crítico que causaba valores negativos en los modelos `Horas_trabajadas` y `Horas_totales`.

### Causa raíz identificada:
- Registros duplicados (entrada-entrada) siendo procesados como pares entrada-salida
- Cuando `entrada_redondeada >= salida_real`, se generaban timedeltas negativos
- Los registros con `inconsistencia=1` no se podían filtrar globalmente debido al flujo de trabajo real (escenario "Martín")

### Solución implementada:
- **Código preventivo:** Validación de tres capas en `calcular_horas_trabajadas()` (models.py:630-674)
- **Corrección retroactiva:** Management command `corregir_horas_negativas.py`
- **Tests:** Suite completa con 6 tests de regresión

### Archivos modificados:
- `/apps/reloj_fichador/models.py` (líneas 630-674)
- `/apps/reloj_fichador/management/commands/corregir_horas_negativas.py` (nuevo)
- `/apps/reloj_fichador/tests/test_calculo_horas.py` (líneas 479-805)

---

## 2. Estado Actual

### ✅ Completado:
- [x] Identificación del bug
- [x] Implementación de validaciones preventivas
- [x] Management command para corrección manual
- [x] Tests de regresión (6 tests, todos pasando)
- [x] Corrección de registros negativos existentes (3 en Horas_trabajadas + 3 en Horas_totales)
- [x] Verificación: 0 registros negativos en base de datos

### ⚠️ Limitación conocida:
El código corregido **previene nuevos registros negativos**, pero **NO corrige automáticamente** los registros existentes que puedan aparecer en el futuro por datos legacy o importaciones.

---

## 3. Próximos Pasos Sugeridos

### 🔄 Prioridad Alta: Automatización de Corrección con Celery

**Objetivo:** Ejecutar el comando de corrección de forma periódica y automática para garantizar la integridad de los datos.

**Implementación sugerida:**

#### A. Crear tarea Celery periódica

**Archivo:** `apps/reloj_fichador/tasks.py`

```python
from celery import shared_task
from django.core.management import call_command
import logging

logger = logging.getLogger('reloj_fichador')

@shared_task(name='corregir_horas_negativas_automatico')
def corregir_horas_negativas_automatico():
    """
    Tarea periódica para detectar y corregir registros con horas negativas.
    Se ejecuta automáticamente según el schedule configurado.
    """
    try:
        logger.info("Iniciando corrección automática de horas negativas...")

        # Ejecutar el management command
        call_command('corregir_horas_negativas', verbosity=1)

        logger.info("Corrección automática completada exitosamente")
        return "Corrección completada"

    except Exception as e:
        logger.error(f"Error en corrección automática de horas negativas: {str(e)}")
        raise
```

#### B. Configurar schedule en Celery Beat

**Archivo:** `mantenedor/settings.py`

Agregar a la configuración existente de `CELERY_BEAT_SCHEDULE`:

```python
CELERY_BEAT_SCHEDULE = {
    # ... otras tareas existentes ...

    'corregir-horas-negativas-diario': {
        'task': 'corregir_horas_negativas_automatico',
        'schedule': crontab(hour=2, minute=0),  # Todos los días a las 2 AM
        'options': {
            'expires': 3600,  # Expira en 1 hora si no se ejecuta
        },
    },
}
```

**Opciones de frecuencia alternativas:**

```python
# Opción 1: Diario a las 2 AM (recomendado)
'schedule': crontab(hour=2, minute=0),

# Opción 2: Cada 6 horas
'schedule': crontab(minute=0, hour='*/6'),

# Opción 3: Semanalmente los domingos a las 3 AM
'schedule': crontab(hour=3, minute=0, day_of_week=0),

# Opción 4: Cada hora (solo para pruebas)
'schedule': crontab(minute=0),
```

#### C. Monitoreo y alertas

**Agregar logging mejorado:**

```python
@shared_task(name='corregir_horas_negativas_automatico')
def corregir_horas_negativas_automatico():
    """Tarea con monitoreo mejorado"""
    from django.core.mail import mail_admins
    from io import StringIO
    from django.core.management import call_command

    try:
        # Capturar output del comando
        out = StringIO()
        call_command('corregir_horas_negativas', verbosity=2, stdout=out)
        output = out.getvalue()

        # Si hubo correcciones, enviar email a admins
        if "Horas_trabajadas corregidas:" in output and not "0" in output.split("corregidas:")[1].split()[0]:
            mail_admins(
                subject='[Reloj Fichador] Horas negativas corregidas automáticamente',
                message=output
            )

        logger.info(f"Corrección automática completada:\n{output}")
        return output

    except Exception as e:
        logger.error(f"Error en corrección automática: {str(e)}")
        mail_admins(
            subject='[ERROR] Corrección automática de horas negativas falló',
            message=str(e)
        )
        raise
```

#### D. Verificación de implementación

**1. Verificar que Celery Beat está corriendo:**
```bash
docker compose logs celery-beat | tail -20
```

**2. Verificar que la tarea está registrada:**
```bash
docker compose exec celery celery -A mantenedor inspect scheduled
```

**3. Ejecutar manualmente para probar:**
```bash
docker compose exec web python -c "from apps.reloj_fichador.tasks import corregir_horas_negativas_automatico; corregir_horas_negativas_automatico.delay()"
```

**4. Verificar logs:**
```bash
docker compose logs -f celery | grep "corregir_horas_negativas"
```

---

### 📊 Prioridad Media: Dashboard de Monitoreo

**Objetivo:** Añadir al panel de administración un widget que muestre:
- Cantidad de registros con horas negativas (si existen)
- Última ejecución de la corrección automática
- Estadísticas de correcciones en el último mes

**Ubicación:** `mantenedor/utils.py` (función `dashboard_callback`)

---

### 🔍 Prioridad Baja: Análisis de Datos Históricos

**Objetivo:** Investigar por qué se generan estos registros duplicados.

**Preguntas a responder:**
1. ¿Hay algún patrón en las fechas/horas donde ocurren?
2. ¿Hay operarios específicos más afectados?
3. ¿Está relacionado con algún área o turno específico?
4. ¿Puede ser un problema de sincronización del dispositivo de fichaje?

**Consulta SQL sugerida:**
```sql
SELECT
    o.nombre,
    o.apellido,
    COUNT(*) as registros_problematicos,
    MIN(rd.fecha_logica) as primera_ocurrencia,
    MAX(rd.fecha_logica) as ultima_ocurrencia
FROM reloj_fichador_registrodiario rd
JOIN reloj_fichador_operario o ON rd.operario_id = o.id
WHERE rd.inconsistencia = 1
GROUP BY o.id
ORDER BY registros_problematicos DESC
LIMIT 20;
```

---

## 4. Checklist de Implementación

### Automatización Celery (Recomendado para esta semana)

- [ ] Crear `apps/reloj_fichador/tasks.py` con la tarea `corregir_horas_negativas_automatico`
- [ ] Agregar configuración a `CELERY_BEAT_SCHEDULE` en `settings.py`
- [ ] Reiniciar servicios Celery: `docker compose restart celery celery-beat`
- [ ] Verificar que la tarea está programada
- [ ] Ejecutar prueba manual
- [ ] Monitorear logs durante 1 semana
- [ ] Configurar alertas por email (opcional pero recomendado)

### Dashboard de Monitoreo (Opcional)

- [ ] Modificar `mantenedor/utils.py` para incluir estadísticas de horas negativas
- [ ] Crear widget en el dashboard del admin
- [ ] Agregar link directo al filtro de registros negativos

### Análisis de Datos (Investigación futura)

- [ ] Ejecutar consultas de análisis
- [ ] Documentar patrones encontrados
- [ ] Evaluar si es necesario ajustar lógica de redondeo
- [ ] Considerar validaciones en el dispositivo de fichaje

---

## 5. Comandos Útiles

### Corrección manual (cuando sea necesario)
```bash
# Ver registros afectados sin corregir
docker compose exec web python manage.py corregir_horas_negativas --dry-run

# Corregir todos los registros
docker compose exec web python manage.py corregir_horas_negativas --verbosity=2

# Corregir solo un operario específico
docker compose exec web python manage.py corregir_horas_negativas --operario=304
```

### Verificación de registros negativos
```sql
-- Contar registros negativos en Horas_trabajadas
SELECT COUNT(*)
FROM reloj_fichador_horas_trabajadas
WHERE horas_normales < 0 OR horas_nocturnas < 0 OR horas_extras < 0;

-- Contar registros negativos en Horas_totales
SELECT COUNT(*)
FROM reloj_fichador_horas_totales
WHERE horas_normales < 0 OR horas_nocturnas < 0 OR horas_extras < 0;
```

### Monitoreo de Celery
```bash
# Ver estado de workers
docker compose exec celery celery -A mantenedor status

# Ver tareas programadas
docker compose exec celery celery -A mantenedor inspect scheduled

# Ver tareas activas
docker compose exec celery celery -A mantenedor inspect active

# Logs de Celery Beat
docker compose logs -f celery-beat
```

---

## 6. Notas Adicionales

### Consideraciones de rendimiento
- La corrección actual procesa todos los registros negativos en una sola transacción
- Para bases de datos muy grandes (>10,000 registros negativos), considerar procesamiento por lotes
- El comando actual ya usa `select_related()` para optimizar queries

### Mantenimiento futuro
- Ejecutar los tests después de cualquier modificación en la lógica de cálculo de horas
- Documentar cualquier nuevo escenario encontrado en `test_calculo_horas.py`
- Mantener este documento actualizado con nuevas sugerencias

### Contacto
Para dudas o sugerencias sobre estas mejoras, contactar al equipo de desarrollo.

---

**Última actualización:** 2025-11-13
**Estado del proyecto:** Bug crítico resuelto, sistema estable
**Próxima revisión sugerida:** Después de implementar automatización Celery
