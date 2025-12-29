# Bug: Texto Invisible en Selectores (Chrome + Modo Oscuro)
**Estado**: Pendiente
**Prioridad**: Baja
**Fecha de Detección**: 29/12/2025

---

## Descripción del Problema

En el reporte de horas (`/admin/reloj_fichador/reporte/horas/`), los campos **"Mes"** y **"Año"** no muestran el texto seleccionado en Chrome cuando el sistema operativo está en modo oscuro.

En Firefox funciona correctamente.

---

## Causa Raíz

### 1. Django Admin Interface detecta modo oscuro
El paquete `django-admin-interface` detecta automáticamente las preferencias del sistema operativo y aplica variables CSS de tema oscuro:

```css
--body-fg: #eeeeee;  /* Texto casi blanco */
--body-bg: #121212;  /* Fondo oscuro */
```

### 2. Conflicto con estilos del template
El template `reporte_horas.html` intenta forzar colores claros:

```css
.campo-filtro select {
    background-color: #fff !important;  /* Funciona */
    color: #333 !important;             /* NO funciona en Chrome */
}
```

### 3. Resultado
- **Fondo**: Blanco (correcto)
- **Texto**: `#eeeeee` casi blanco (heredado del tema oscuro)
- **Visibilidad**: Texto blanco sobre fondo blanco = invisible

---

## ¿Por qué funciona en Firefox?

Firefox y Chrome manejan diferente:
- La especificidad CSS en elementos `<select>` nativos
- La herencia de variables CSS en controles de formulario
- El renderizado de opciones seleccionadas

---

## Soluciones Propuestas

### Opción A: Desactivar modo oscuro (Recomendada)
Desactivar completamente el modo oscuro en `django-admin-interface` ya que no es necesario para este proyecto.

**Ubicación**: Panel de admin → Admin Interface → Configuración

### Opción B: Fix CSS específico para Chrome
Agregar `-webkit-text-fill-color` que Chrome respeta:

```css
.campo-filtro select {
    color: #333 !important;
    -webkit-text-fill-color: #333 !important;
}

.campo-filtro select option {
    color: #333 !important;
    -webkit-text-fill-color: #333 !important;
}
```

### Opción C: Usar selector más específico
```css
.reporte-container .campo-filtro select,
.reporte-container .campo-filtro select option {
    color: #333 !important;
    -webkit-text-fill-color: #333 !important;
    background-color: #fff !important;
}
```

---

## Archivos Relacionados

| Archivo | Descripción |
|---------|-------------|
| `templates/admin/reportes/reporte_horas.html` | Template con estilos CSS del formulario |
| `static/admin/css/dark_mode.css` | Estilos de modo oscuro de Django |
| `static/admin_interface/css/*.css` | Estilos de django-admin-interface |

---

## Información de Diagnóstico

```javascript
// Variables CSS en modo oscuro
{
  "--body-fg": "#eeeeee",      // Texto claro
  "--body-bg": "#121212",      // Fondo oscuro
  "--border-color": "#353535",
  "--body-quiet-color": "#d0d0d0"
}

// Preferencias del sistema
prefersDarkMode: true
```

---

## Workaround Temporal

Los usuarios afectados pueden:
1. Cambiar el tema del SO a modo claro
2. Usar Firefox para este reporte específico

---

**Detectado por**: Claude Code
**Navegador afectado**: Chrome (modo oscuro del SO)
**Navegador funcional**: Firefox
