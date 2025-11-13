# Guía: Exportación Selectiva vs Total

## 🎯 Problema Resuelto

**Antes:** El botón EXPORT exportaba TODOS los registros de la tabla, aunque solo seleccionaras 10.

**Ahora:** Tienes 2 opciones de exportación según tus necesidades.

---

## 📊 Dos Formas de Exportar

### **Opción 1: Exportar TODO** (Botón EXPORT)

**Ubicación:** Botón **"EXPORT"** en la parte superior derecha

**Comportamiento:**
- Exporta TODOS los registros de la tabla
- Respeta los filtros aplicados (fecha, tipo, etc.)
- Ignora los checkboxes de selección
- Ideal para exportaciones completas

**Cuándo usar:**
- ✅ Quieres exportar toda la base de datos
- ✅ Quieres exportar todos los registros filtrados
- ✅ Backup completo de datos

**Ejemplo:**
1. Aplicar filtro: "Fecha: Noviembre 2025"
2. Click en **EXPORT**
3. Resultado: Todos los registros de noviembre

---

### **Opción 2: Exportar SOLO Seleccionados** (Nueva Action)

**Ubicación:** Dropdown **"Acciones"** después de seleccionar registros

**Comportamiento:**
- Exporta SOLO los registros que marcaste con checkbox
- Ignora filtros (solo usa lo seleccionado)
- Datos en formato legible (nombres, fechas español, Sí/No)

**Cuándo usar:**
- ✅ Quieres exportar 5, 10 o 50 registros específicos
- ✅ Necesitas un reporte de casos particulares
- ✅ Quieres compartir solo algunos registros

**Pasos:**
1. Marcar los checkboxes de los registros deseados (ej: 10 registros)
2. Seleccionar en dropdown: **"📊 Exportar seleccionados a Excel (legible)"**
3. Click en **"Ir"**
4. Resultado: Excel con SOLO esos 10 registros

---

## 🖼️ Comparación Visual

### Opción 1: EXPORT (TODO)
```
┌─────────────────────────────────────┐
│  Registros Diarios          EXPORT ← Click aquí
├─────────────────────────────────────┤
│ ☐ García, Juan - 08:00              │
│ ☐ Pérez, Ana - 08:15                │
│ ☐ López, Carlos - 08:30             │
│ ... (1000 registros más)            │
└─────────────────────────────────────┘
```
**Resultado:** Excel con 1003 registros

---

### Opción 2: Exportar Seleccionados (SOLO seleccionados)
```
┌─────────────────────────────────────┐
│  Registros Diarios          EXPORT  │
├─────────────────────────────────────┤
│ ☑ García, Juan - 08:00      ← Seleccionado
│ ☐ Pérez, Ana - 08:15                │
│ ☑ López, Carlos - 08:30     ← Seleccionado
│ ... (1000 registros más)            │
├─────────────────────────────────────┤
│ Acciones: [📊 Exportar seleccionados] [Ir]
└─────────────────────────────────────┘
```
**Resultado:** Excel con 2 registros

---

## 📝 Modelos con Exportación Selectiva

La nueva action está disponible en:

- ✅ **Registros Diarios** (`RegistroDiario`)
- ✅ **Horas Trabajadas** (`Horas_trabajadas`)
- ✅ **Operarios** (`Operario`)

---

## 🎨 Formato de los Archivos Exportados

### Ambas opciones exportan con formato legible:

| Campo | Formato Anterior | Formato Nuevo |
|-------|------------------|---------------|
| Operario | `23` (ID) | `García, Juan Manuel` |
| Tipo | `entrada` | `Entrada` |
| Válido | `True` | `Sí` |
| Fecha | `2025-11-13 08:30:00` | `13/11/2025 08:30:00` |

---

## 💡 Tips y Mejores Prácticas

### Para Exportar Muchos Registros (>1000)
✅ Usa **EXPORT** con filtros
- Más rápido
- No hay límite de selección

### Para Reportes Específicos
✅ Usa **Exportar seleccionados**
- Selecciona manualmente
- Control total sobre qué exportas

### Para Compartir con No Técnicos
✅ Ambas opciones son perfectas
- Datos en español
- Nombres legibles
- Formato familiar (Excel)

---

## 🔧 Detalles Técnicos

### Nombre del Archivo

**Botón EXPORT:**
```
RegistroDiario_2025-11-13.xlsx
```

**Action Seleccionados:**
```
registros diarios_seleccionados_20251113_143025.xlsx
```

### Mensaje de Confirmación

Al usar la action "Exportar seleccionados", verás un mensaje:
```
✅ 10 registros exportados exitosamente a Excel.
```

---

## ❓ Preguntas Frecuentes

### ¿Por qué el EXPORT no respeta mi selección?
Es el comportamiento estándar de django-import-export. El botón EXPORT está diseñado para exportaciones completas con filtros.

### ¿Puedo seleccionar todos los registros con el checkbox superior?
Sí, pero solo seleccionará los de la página actual. Para todas las páginas, usa el botón EXPORT con filtros.

### ¿Hay límite de registros seleccionados?
No hay límite técnico, pero por practicidad se recomienda:
- Menos de 100: Usa "Exportar seleccionados"
- Más de 100: Usa "EXPORT" con filtros

### ¿Puedo exportar a PDF los seleccionados?
Sí, ya existe la action "Exportar seleccionados a PDF" que funciona de la misma manera.

---

## 🚀 Ejemplos de Uso

### Caso 1: Exportar Registros de Hoy
```
1. Filtrar: Fecha = Hoy
2. Click en EXPORT
3. Resultado: Todos los registros de hoy
```

### Caso 2: Exportar 3 Registros Específicos con Inconsistencias
```
1. Buscar por nombre: "García"
2. Marcar los 3 registros con inconsistencia
3. Acciones → "📊 Exportar seleccionados a Excel (legible)"
4. Click "Ir"
5. Resultado: Excel con esos 3 registros
```

### Caso 3: Backup Mensual
```
1. Filtrar: Fecha = Noviembre 2025
2. Click en EXPORT
3. Guardar archivo: backup_noviembre_2025.xlsx
```

---

**Fecha:** 13 de Noviembre de 2025
**Versión:** django-import-export 4.3.13
