# Mejoras en Reporte de Horas Trabajadas

**Fecha:** 30 de Diciembre de 2025
**Autor:** Claude Code
**Estado:** Completado y desplegado a producción

---

## Resumen Ejecutivo

Se implementaron mejoras significativas en el reporte de horas trabajadas tanto en la versión HTML como en la versión PDF. Las mejoras incluyen resaltado visual de registros faltantes y la visualización completa de todos los días laborables del mes.

---

## Cambios Implementados

### 1. Resaltador Rojo para "No registró fichada"

**Problema:** El texto "No registró fichada" aparecía sin ningún formato especial, dificultando su identificación visual.

**Solución:** Se modificó el filtro `fecha_completa_es` para devolver HTML con estilo rojo cuando no hay fecha.

**Archivo modificado:** `apps/reloj_fichador/templatetags/reporte_filters.py`

```python
from django.utils.safestring import mark_safe

@register.filter
def fecha_completa_es(fecha):
    if not fecha:
        return mark_safe('<span style="color: #dc3545; font-weight: 500;">No registró fichada</span>')
    # ... resto del código
```

---

### 2. Mostrar Todos los Días Laborables (Lunes a Sábado)

**Problema:** El reporte solo mostraba los días donde existían registros de horas trabajadas. Los días sin fichadas no aparecían, dificultando identificar ausencias.

**Solución:** Se modificó la lógica del backend para iterar sobre todos los días laborables del mes (lunes a sábado), mostrando "Sin fichadas" para los días sin registros.

#### Cambios en el Backend

**Archivos modificados:** `apps/reloj_fichador/admin.py`
- Función `reporte_horas` (líneas ~1834-1988)
- Función `exportar_horas_pdf` (líneas ~2333-2560)

**Lógica implementada:**

```python
# Generar lista de todos los días laborables (lunes a sábado) del mes
dias_laborables = []
fecha_actual = mes_inicio
while fecha_actual <= mes_fin:
    if fecha_actual.weekday() < 6:  # Lunes a Sábado (0-5)
        dias_laborables.append(fecha_actual)
    fecha_actual += timedelta(days=1)

# Crear diccionario de horas_trabajadas por operario y fecha
horas_por_operario_fecha = {}
if horas_trabajadas:
    for hora in horas_trabajadas:
        key = (hora.operario.id, hora.fecha)
        horas_por_operario_fecha[key] = hora

# Para cada operario, iterar sobre TODOS los días laborables
for operario in operarios_a_mostrar:
    for dia in dias_laborables:
        hora = horas_por_operario_fecha.get((operario.id, dia))

        if hora:
            # Procesar registro existente
            registro = {
                'hora': hora,
                'fecha': dia,
                'entrada': entrada,
                'salida': salida,
                'es_primera_fila': True,
                'sin_registro': False
            }
        else:
            # Día sin ningún registro
            registro = {
                'hora': None,
                'fecha': dia,
                'entrada': None,
                'salida': None,
                'es_primera_fila': True,
                'sin_registro': True  # Flag clave para el template
            }
```

#### Cambios en Templates

**Archivos modificados:**
- `templates/admin/reportes/reporte_horas.html`
- `templates/admin/reportes/pdf/reporte_horas_pdf.html`

**Lógica del template:**

```django
{% for registro in operario_data.registros %}
<tr{% if registro.sin_registro %} style="background-color: #fff8e1;"{% endif %}>
    <td>
        {% if registro.sin_registro %}
            <span style="color: #856404;">{{ registro.fecha|fecha_corta_es }}</span>
        {% else %}
            {{ registro.hora.operario.apellido }}, {{ registro.hora.operario.nombre }}
        {% endif %}
    </td>
    <td>
        {% if registro.sin_registro %}
            <span style="color: #dc3545; font-weight: 500;">Sin fichadas</span>
        {% else %}
            {{ registro.entrada|fecha_completa_es }}
        {% endif %}
    </td>
    <!-- Columnas de horas similares -->
</tr>
{% endfor %}
```

#### Nuevo Filtro Añadido

Se añadió el filtro `fecha_corta_es` para mostrar la fecha sin hora en los días sin registro:

```python
@register.filter
def fecha_corta_es(fecha):
    """
    Formatea fecha corta en español: "Lunes 01/11/2025"
    """
    if not fecha:
        return ""
    dia = dia_es(fecha)
    fecha_str = fecha.strftime('%d/%m/%Y')
    return f"{dia} {fecha_str}"
```

---

### 3. Estilos Visuales

| Elemento | Estilo |
|----------|--------|
| Días sin fichadas (fila) | Fondo amarillo claro (`#fff8e1`) |
| Fecha del día sin fichadas | Texto marrón (`#856404`) |
| "Sin fichadas" | Texto rojo (`#dc3545`) |
| "No registró fichada" | Texto rojo con peso 500 |
| Horas en días sin registro | Texto gris (`#6c757d`) mostrando "00h 00m" |

---

## Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `apps/reloj_fichador/admin.py` | Lógica de días laborables en `reporte_horas` y `exportar_horas_pdf` |
| `apps/reloj_fichador/templatetags/reporte_filters.py` | Filtro `fecha_completa_es` con HTML rojo, nuevo filtro `fecha_corta_es` |
| `templates/admin/reportes/reporte_horas.html` | Manejo de `sin_registro` flag |
| `templates/admin/reportes/pdf/reporte_horas_pdf.html` | Manejo de `sin_registro` flag con verificación `and registro.hora` |

---

## Despliegue a Producción

**Servidor:** 192.168.10.39:5080

**Proceso de despliegue:**

```bash
# Copiar archivos al servidor
scp apps/reloj_fichador/admin.py sistemas@192.168.10.39:/tmp/
scp apps/reloj_fichador/templatetags/reporte_filters.py sistemas@192.168.10.39:/tmp/
scp templates/admin/reportes/reporte_horas.html sistemas@192.168.10.39:/tmp/
scp templates/admin/reportes/pdf/reporte_horas_pdf.html sistemas@192.168.10.39:/tmp/

# Copiar al contenedor Docker
ssh sistemas@192.168.10.39 "
docker cp /tmp/admin.py reloj_fichador-web-1:/app/apps/reloj_fichador/
docker cp /tmp/reporte_filters.py reloj_fichador-web-1:/app/apps/reloj_fichador/templatetags/
docker cp /tmp/reporte_horas.html reloj_fichador-web-1:/app/templates/admin/reportes/
docker cp /tmp/reporte_horas_pdf.html reloj_fichador-web-1:/app/templates/admin/reportes/pdf/
"

# Reiniciar servicio
ssh sistemas@192.168.10.39 "cd /home/sistemas/Docker_proyectos/Reloj_fichador && docker compose restart web"
```

---

## Resultado Visual

### Reporte HTML
- Días con registros: fondo blanco, datos completos
- Días sin fichadas: fondo amarillo, "Sin fichadas" en rojo
- Domingos: excluidos correctamente del reporte

### Reporte PDF
- Mismo formato visual que HTML
- Generación correcta con WeasyPrint
- Manejo seguro de `registro.hora` None

---

## Problemas Resueltos Durante la Implementación

### 1. Error en Template Django
**Problema:** `{% if not registro.hora %}` no funcionaba correctamente para detectar valores None en diccionarios.

**Solución:** Usar flag explícito `{% if registro.sin_registro %}` en lugar de verificar el valor de `hora`.

### 2. Error en PDF: "Failed lookup for key [horas_nocturnas] in None"
**Problema:** Al acceder a `registro.hora.horas_nocturnas` cuando `registro.hora` es None, Django lanzaba error.

**Solución:** Cambiar condiciones de `{% elif registro.es_primera_fila %}` a `{% elif registro.es_primera_fila and registro.hora %}` para verificar que `hora` no sea None antes de acceder a sus atributos.

### 3. Cache de Templates en Docker
**Problema:** Los cambios en templates no se reflejaban después de reiniciar el contenedor.

**Solución:** Los templates están copiados en la imagen Docker, no montados como volumen. Se usó `docker cp` para copiar los archivos actualizados al contenedor.

---

## Verificación

- [x] Reporte HTML funciona correctamente en local
- [x] Reporte PDF funciona correctamente en local
- [x] Despliegue a producción exitoso
- [x] Verificación visual en producción
- [x] Domingos excluidos correctamente
- [x] Días de licencia excluidos (no duplicados)

---

## Notas Técnicas

1. **Timezone:** Todas las fechas se manejan con timezone de Argentina (`America/Argentina/Buenos_Aires`)

2. **Días laborables:** La lógica usa `weekday() < 6` para incluir lunes (0) a sábado (5) y excluir domingo (6)

3. **OrderedDict:** Se usa para mantener el orden de los operarios por apellido y nombre

4. **Licencias:** Los días de licencia se excluyen de la iteración de días laborables para evitar duplicación con la sección de "registros_enfermedad"
