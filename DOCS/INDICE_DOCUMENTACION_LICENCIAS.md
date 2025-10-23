# 📚 ÍNDICE DE DOCUMENTACIÓN - SISTEMA DE LICENCIAS MÉDICAS

**Actualizado:** 23 de Octubre de 2025
**Versión:** 1.0
**Estado:** ✅ DOCUMENTACIÓN COMPLETA

---

## 🗂️ Estructura de Documentación

```
DOCS/
├── REPORTE_CAMBIOS_OCT2025.md ................... Reporte completo de cambios
├── INDICE_DOCUMENTACION_LICENCIAS.md ........... Este archivo
└── [Raíz del Proyecto]/
    ├── JUSTIFICACION_RETROACTIVA.md ........... Cómo funciona la retroactividad
    ├── CALCULO_AUTOMATICO_HORAS_ENFERMEDAD.md .. Cómo se calcula automáticamente
    ├── IMPLEMENTACION_HORAS_ENFERMEDAD.md ..... Detalles de implementación
    └── COMO_FUNCIONAN_LAS_LICENCIAS_MEDICAS.md  Flujo general del sistema
```

---

## 📖 Guía de Lectura por Rol

### 👤 Para Usuarios del Sistema

**Lectura Recomendada:**
1. [COMO_FUNCIONAN_LAS_LICENCIAS_MEDICAS.md](#cómo-funcionan-las-licencias-médicas)
   - Entiende el flujo general
   - Aprende cómo funciona el sistema
   - ~5 minutos

2. [JUSTIFICACION_RETROACTIVA.md](#justificación-retroactiva)
   - Aprende cómo funciona el escenario real
   - Entiende cómo se justifican ausencias
   - ~10 minutos

3. [CALCULO_AUTOMATICO_HORAS_ENFERMEDAD.md](#cálculo-automático-horas-de-enfermedad)
   - Sabe cómo se calcula (1 día = 8 horas)
   - Aprende que es automático
   - ~5 minutos

---

### 👨‍💻 Para Desarrolladores

**Lectura Recomendada:**
1. [REPORTE_CAMBIOS_OCT2025.md](#reporte-de-cambios-e-implementaciones)
   - Vista general de todos los cambios
   - Qué archivos fueron modificados
   - ~15 minutos

2. [IMPLEMENTACION_HORAS_ENFERMEDAD.md](#implementación-de-horas-de-enfermedad)
   - Detalles técnicos del modelo
   - Cómo se integra con otros modelos
   - Cómo se calcula
   - ~15 minutos

3. [JUSTIFICACION_RETROACTIVA.md](#justificación-retroactiva)
   - Lógica de retroactividad
   - Restricciones implementadas
   - Casos límite
   - ~15 minutos

4. [CALCULO_AUTOMATICO_HORAS_ENFERMEDAD.md](#cálculo-automático-horas-de-enfermedad)
   - Código exacto del cálculo
   - Dónde se puede cambiar
   - Verificación
   - ~10 minutos

---

### 👨‍💼 Para Administradores

**Lectura Recomendada:**
1. [REPORTE_CAMBIOS_OCT2025.md](#reporte-de-cambios-e-implementaciones)
   - Resumen de cambios
   - Impacto en el sistema
   - ~10 minutos

2. [JUSTIFICACION_RETROACTIVA.md](#justificación-retroactiva)
   - Cómo procesar licencias históricas
   - Management commands disponibles
   - ~10 minutos

---

## 📄 Descripción Detallada de Documentos

### 1️⃣ REPORTE_CAMBIOS_OCT2025.md

**Contenido:**
- Resumen ejecutivo de cambios
- Nuevas características implementadas
- Cambios en modelos y configuración
- Nuevos comandos disponibles
- Lista de archivos modificados
- Tests implementados
- Verificación de cambios
- Estadísticas de impacto

**Casos de Uso:**
- ✅ Visión general del proyecto
- ✅ Qué cambió exactamente
- ✅ Dónde encontrar cada cambio
- ✅ Impacto en el sistema
- ✅ Verificación de implementación

**Audiencia:** Todos (técnico + ejecutivo)
**Tiempo de lectura:** 15-20 minutos
**Actualización:** Mensual

---

### 2️⃣ JUSTIFICACION_RETROACTIVA.md

**Ubicación:** Raíz del proyecto
**Contenido:**
- Qué es justificación retroactiva
- Escenario real de negocio
- Cómo funciona el sistema
- Restricciones implementadas
- Flujo de ejecución
- Logging y auditoría
- Casos de uso
- Troubleshooting

**Ejemplos Incluidos:**
- Licencia de 5 días (en rango coincidente)
- Licencia con atraso (hasta 30 días)
- Licencia con atraso > 30 días (fuera de límite)
- Ausencia parcial (días específicos)

**Casos de Uso:**
- ✅ Entender el escenario real
- ✅ Saber cómo el sistema maneja licencias tardías
- ✅ Verificar límites de retroactividad
- ✅ Auditar cambios realizados

**Audiencia:** Usuarios, Desarrolladores, Administradores
**Tiempo de lectura:** 10-15 minutos
**Actualización:** Cuando cambie lógica de retroactividad

---

### 3️⃣ CALCULO_AUTOMATICO_HORAS_ENFERMEDAD.md

**Ubicación:** Raíz del proyecto
**Contenido:**
- Confirmación: SÍ es automático
- Código exacto del cálculo
- Desglose del cálculo paso a paso
- Ejemplos de cálculo (1, 2, 3, 5, 30 días)
- Almacenamiento en BD
- Conversión automática días → horas
- Cómo verificar que funciona
- Cómo cambiar el valor (de 8 a otro)

**Fórmula Base:**
```
Horas = Días × 8 horas/día
```

**Casos de Uso:**
- ✅ Confirmar que es automático
- ✅ Entender cómo se calcula
- ✅ Cambiar valor (si necesario)
- ✅ Verificar cálculos en BD
- ✅ Resolver dudas sobre conversión

**Audiencia:** Usuarios, Desarrolladores
**Tiempo de lectura:** 10 minutos
**Actualización:** Si cambia fórmula

---

### 4️⃣ IMPLEMENTACION_HORAS_ENFERMEDAD.md

**Ubicación:** Raíz del proyecto
**Contenido:**
- Descripción del modelo HorasEnfermedad
- Integración con otros modelos
- Flujo de creación
- Cálculo de horas
- Almacenamiento
- Integración con reportes (admin, Excel, PDF)
- Estado actual del sistema
- Logs de procesamiento

**Modelos Involucrados:**
- Licencia (entrada)
- RegistroAsistencia (justificación)
- HorasEnfermedad (auditoría)
- Horas_totales (acumulación)

**Casos de Uso:**
- ✅ Entender arquitectura del sistema
- ✅ Saber cómo se vinculan los modelos
- ✅ Debugging de problemas
- ✅ Mejoras futuras

**Audiencia:** Desarrolladores, Administradores técnicos
**Tiempo de lectura:** 15-20 minutos
**Actualización:** Si cambia estructura

---

### 5️⃣ COMO_FUNCIONAN_LAS_LICENCIAS_MEDICAS.md

**Ubicación:** Raíz del proyecto
**Contenido:**
- Flujo general de licencias
- Estados de licencia
- Circuito: Licencia → RegistroAsistencia → HorasEnfermedad
- Cómo se integra con el sistema
- Roles involucrados
- Ejemplo paso a paso

**Flujo Simplificado:**
```
Usuario carga licencia
    ↓
Marca como "Aprobada"
    ↓
Sistema automáticamente:
├─ Justifica registros de ausencia
├─ Acumula horas de enfermedad
└─ Actualiza reportes
    ↓
Verificar en admin
```

**Casos de Uso:**
- ✅ Entender flujo global
- ✅ Saber qué sucede después de aprobar
- ✅ Onboarding de nuevos usuarios
- ✅ Demostración del sistema

**Audiencia:** Todos (especialmente usuarios nuevos)
**Tiempo de lectura:** 10 minutos
**Actualización:** Si cambia flujo general

---

## 🔍 Búsqueda Rápida por Tema

### Tema: "¿Cómo funciona la retroactividad?"
→ Leer: [JUSTIFICACION_RETROACTIVA.md](#justificación-retroactiva)
→ Sección: "Cómo Funciona"

### Tema: "¿Es automático el cálculo?"
→ Leer: [CALCULO_AUTOMATICO_HORAS_ENFERMEDAD.md](#cálculo-automático-horas-de-enfermedad)
→ Sección: "¿Cómo Funciona?"

### Tema: "¿Qué cambió en el código?"
→ Leer: [REPORTE_CAMBIOS_OCT2025.md](#reporte-de-cambios-e-implementaciones)
→ Sección: "Archivos Modificados"

### Tema: "¿Cómo crear una licencia?"
→ Leer: [COMO_FUNCIONAN_LAS_LICENCIAS_MEDICAS.md](#cómo-funcionan-las-licencias-médicas)
→ Sección: "Flujo de Creación"

### Tema: "¿Cómo procesar licencias históricas?"
→ Leer: [JUSTIFICACION_RETROACTIVA.md](#justificación-retroactiva)
→ Sección: "Management Command"

---

## 📊 Estadísticas de Documentación

| Documento | Páginas | Palabras | Ejemplos | Diagramas |
|-----------|---------|----------|----------|-----------|
| REPORTE_CAMBIOS_OCT2025.md | ~8 | 2,500+ | 5+ | 2 |
| JUSTIFICACION_RETROACTIVA.md | ~6 | 2,000+ | 4+ | 3 |
| CALCULO_AUTOMATICO_HORAS_ENFERMEDAD.md | ~5 | 1,500+ | 6+ | 1 |
| IMPLEMENTACION_HORAS_ENFERMEDAD.md | ~6 | 2,000+ | 3+ | 2 |
| COMO_FUNCIONAN_LAS_LICENCIAS_MEDICAS.md | ~4 | 1,200+ | 2+ | 1 |
| **TOTAL** | **~29** | **~9,200** | **20+** | **9** |

---

## ✅ Checklist de Documentación

- ✅ Reporte completo de cambios
- ✅ Explicación de justificación retroactiva
- ✅ Documentación de cálculo automático
- ✅ Detalles de implementación
- ✅ Guía de flujo general
- ✅ Índice de documentación (este archivo)
- ✅ Tests documentados
- ✅ Ejemplos prácticos
- ✅ Troubleshooting
- ✅ Guías por rol

---

## 🚀 Cómo Mantener Esta Documentación

### Cuando Cambies el Código
1. Actualiza el documento relevante
2. Incluye ejemplos si es lógica nueva
3. Actualiza el reporte de cambios
4. Marca "Actualizado: [fecha]"

### Cuando Agregues Nuevas Características
1. Crea documento específico si es complejo
2. Enlázalo desde este índice
3. Agrega ejemplos prácticos
4. Verifica que todos entiendan

### Cadencia de Actualización
- **Diaria:** Si cambio el código
- **Semanal:** Reporte acumulativo
- **Mensual:** Índice y reorganización

---

## 📞 Contacto y Soporte

**Para preguntas sobre:**
- **Funcionalidad del sistema:** Consultar usuario responsable
- **Implementación técnica:** Consultar desarrollador
- **Reportes y datos:** Consultar administrador
- **Documentación:** Actualizar documentos relevantes

---

## 🔗 Enlaces Útiles

**Dentro del Proyecto:**
- `/apps/reloj_fichador/models.py` - Modelos
- `/apps/reloj_fichador/tasks.py` - Lógica de procesamiento
- `/apps/reloj_fichador/admin.py` - Configuración admin
- `/TEST/test_justificacion_retroactiva.py` - Tests

**Externo:**
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)

---

## 🎓 Guía de Aprendizaje Progresivo

### Nivel 1️⃣ - Principiante (30 min)
1. Leer: COMO_FUNCIONAN_LAS_LICENCIAS_MEDICAS.md
2. Leer: JUSTIFICACION_RETROACTIVA.md
3. Usar: Admin para crear licencia de prueba

**Resultado:** Entiendes cómo funciona el flujo general

### Nivel 2️⃣ - Intermedio (1 hora)
1. Leer: CALCULO_AUTOMATICO_HORAS_ENFERMEDAD.md
2. Leer: IMPLEMENTACION_HORAS_ENFERMEDAD.md
3. Ejecutar: Command `procesar_licencias_pendientes`

**Resultado:** Entiendes detalles técnicos y puedes administrar

### Nivel 3️⃣ - Avanzado (2 horas)
1. Leer: REPORTE_CAMBIOS_OCT2025.md
2. Revisar: Código en tasks.py y models.py
3. Estudiar: Tests en test_justificacion_retroactiva.py
4. Experimentar: Modificar y testear cambios

**Resultado:** Puedes mantener, mejorar y debuggear el sistema

---

## 📅 Historial de Cambios en Documentación

| Fecha | Cambio | Documento |
|-------|--------|-----------|
| 2025-10-23 | Creación inicial | Todos |
| 2025-10-23 | Reporte completo | REPORTE_CAMBIOS_OCT2025.md |
| 2025-10-23 | Índice de documentación | INDICE_DOCUMENTACION_LICENCIAS.md |

---

**Documentación Versión:** 1.0
**Última Actualización:** 23 de Octubre de 2025
**Estado:** ✅ COMPLETA Y VERIFICADA
**Siguiente Revisión:** Cuando se realicen cambios significativos

