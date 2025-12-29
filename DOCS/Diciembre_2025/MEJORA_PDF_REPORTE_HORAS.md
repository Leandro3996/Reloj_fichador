# MEJORA: PDF Reporte de Horas - Encabezado Repetido y Formato Vertical
**Estado**: Completado
**Fecha**: 29/12/2025

---

## Resumen

Se implementaron mejoras al PDF del reporte de horas trabajadas para que:
1. El encabezado se repita en todas las páginas
2. Orientación vertical (portrait) en lugar de horizontal
3. Un operario por página (salto de página automático)
4. Eliminación de totales generales (solo subtotales por operario)

---

## Cambios Solicitados

| Mejora | Descripción | Estado |
|--------|-------------|--------|
| Ordenar por fecha | Los registros dentro de cada operario se ordenan por fecha ASC | ✅ |
| Orientación vertical | PDF en formato portrait A4 | ✅ |
| Salto de página | Una página por operario | ✅ |
| Encabezado repetido | El encabezado aparece en todas las páginas | ✅ |
| Sin totales generales | Solo se muestran subtotales por operario | ✅ |

---

## Implementación Técnica

### 1. Ordenamiento por Fecha

**Archivo**: `apps/reloj_fichador/admin.py` (línea ~1634)

```python
# Antes
horas_trabajadas = Horas_trabajadas.objects.filter(filtros).select_related('operario').order_by('operario__apellido')

# Después
horas_trabajadas = Horas_trabajadas.objects.filter(filtros).select_related('operario').order_by('operario__apellido', 'fecha')
```

### 2. Encabezado Repetido con WeasyPrint

**Archivo**: `templates/admin/reportes/pdf/reporte_horas_pdf.html`

#### CSS para encabezado repetido

```css
@page {
    size: A4 portrait;
    margin: 3.8cm 0.6cm 1.2cm 0.6cm;

    @top-left {
        content: element(pageHeader);
        width: 100%;
    }

    @top-center {
        content: "";
    }

    @top-right {
        content: "";
    }

    @bottom-center {
        content: "Reporte generado por Sistema de Reloj Fichador";
        font-size: 7px;
        color: #888;
    }
}

/* Encabezado repetido en todas las páginas */
.page-header {
    position: running(pageHeader);
    font-family: Arial, sans-serif;
    font-size: 9px;
    color: #333;
    width: 100%;
}
```

#### HTML del encabezado

```html
<body>
    <!-- Encabezado que se repite en todas las páginas -->
    <div class="page-header">
        <div class="header">
            <h1>REPORTE DE HORAS TRABAJADAS</h1>
            <p><strong>{{ mes_nombre }} {{ año }}</strong></p>
            <p>Generado el {{ fecha_generacion }}</p>
        </div>

        <div class="info-meta">
            <div>
                <strong>Período:</strong> {{ mes_nombre }} {{ año }}<br>
                <strong>Operarios:</strong> {{ operarios_filtro }}
            </div>
            <div>
                <strong>Total registros:</strong> {{ horas_trabajadas|length }}<br>
                <strong>Sistema:</strong> Reloj Fichador
            </div>
        </div>
    </div>

    <!-- Contenido del reporte -->
    ...
</body>
```

### 3. Salto de Página por Operario

```css
.operario-section {
    page-break-after: always;
    page-break-inside: avoid;
}

.operario-section:last-of-type {
    page-break-after: auto;
}
```

---

## Cómo Funciona `position: running()` en WeasyPrint

WeasyPrint implementa la especificación CSS Paged Media Module Level 3, que permite crear encabezados y pies de página repetidos mediante:

1. **`position: running(nombre)`**: Extrae el elemento del flujo normal y lo registra como un "elemento running" con el nombre especificado.

2. **`content: element(nombre)`**: En una región de margen de página (`@top-left`, `@top-center`, etc.), inserta el elemento running registrado.

3. **Herencia de estilos**: Los elementos en áreas de margen NO heredan estilos del `<body>`, por lo que es necesario re-declarar `font-family`, `font-size`, etc. en el contenedor `.page-header`.

4. **Ancho completo**: Se usa `@top-left` con `width: 100%` y se vacían `@top-center` y `@top-right` para que el encabezado ocupe todo el ancho de la página.

---

## Notas de Implementación

### Problema: Diseño modificado al envolver en contenedor

**Causa**: Al usar `position: running()`, el elemento se mueve al área de margen de la página y pierde la herencia de estilos del `<body>`.

**Solución**: Agregar estilos base directamente al `.page-header`:

```css
.page-header {
    position: running(pageHeader);
    font-family: Arial, sans-serif;  /* Re-declarar fuente */
    font-size: 9px;                   /* Re-declarar tamaño */
    color: #333;                      /* Re-declarar color */
    width: 100%;                      /* Ancho completo */
}
```

### Sincronización con Docker

Los cambios en templates requieren copiarse al contenedor:

```bash
docker cp templates/admin/reportes/pdf/reporte_horas_pdf.html reloj_fichador-web-1:/app/templates/admin/reportes/pdf/
docker compose restart web
```

---

## Archivos Modificados

| Archivo | Cambio |
|---------|--------|
| `apps/reloj_fichador/admin.py` | Añadido ordenamiento por fecha |
| `templates/admin/reportes/pdf/reporte_horas_pdf.html` | Encabezado repetido, formato vertical, saltos de página |

---

## Resultado Final

### Página 1
- Encabezado completo con título, período y metadatos
- Datos del primer operario (BAINOTTI, JORGE)
- Subtotal del operario

### Página 2 (y siguientes)
- **Mismo encabezado repetido**
- Datos del siguiente operario (BALDAZAR, RAUL)
- Subtotal del operario

---

## Referencias

- [WeasyPrint - CSS Paged Media](https://doc.courtbouillon.org/weasyprint/stable/api_reference.html#css)
- [CSS Paged Media Module Level 3](https://www.w3.org/TR/css-page-3/)
- [Running Elements](https://www.w3.org/TR/css-gcpm-3/#running-elements)

---

**Implementado por**: Claude Code
**Verificado**: Sí - PDF generado con encabezado repetido en todas las páginas
