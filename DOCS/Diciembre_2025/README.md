# 📅 Documentación Diciembre 2025
**Sistema Reloj Fichador**

---

## Índice de Cambios

| # | Documento | Descripción | Estado |
|---|-----------|-------------|--------|
| 1 | [MEJORA_UX_REPORTE_HORAS_SIN_DATOS.md](./MEJORA_UX_REPORTE_HORAS_SIN_DATOS.md) | Mensaje informativo cuando no hay datos en el reporte de horas | ✅ Completado |
| 2 | [BUG_TEXTO_INVISIBLE_SELECTORES_CHROME.md](./BUG_TEXTO_INVISIBLE_SELECTORES_CHROME.md) | Bug: texto invisible en selectores Mes/Año en Chrome con modo oscuro | ⏳ Pendiente |

---

## Resumen del Mes

### Mejoras de UX Implementadas

#### Reporte de Horas - Feedback "Sin Datos"
- **Fecha**: 29/12/2025
- **Problema**: El usuario no recibía feedback cuando generaba un reporte sin datos
- **Solución**: Nuevo mensaje visual amarillo indicando que no hay datos
- **Archivos**: `admin.py`, `reporte_horas.html`

---

## Bugs Conocidos

### Texto invisible en selectores (Chrome)
- **Fecha**: 29/12/2025
- **Problema**: Los campos Mes/Año no muestran texto en Chrome cuando el SO está en modo oscuro
- **Causa**: `django-admin-interface` aplica variables CSS de tema oscuro que entran en conflicto
- **Solución propuesta**: Desactivar modo oscuro en django-admin-interface
- **Prioridad**: Baja

---

## Próximos Pasos

- [ ] Desactivar modo oscuro en django-admin-interface
- [ ] Aplicar el mismo patrón "sin datos" a otros reportes del sistema
- [ ] Agregar más cambios según se implementen

---

**Última actualización**: 29 de Diciembre de 2025
