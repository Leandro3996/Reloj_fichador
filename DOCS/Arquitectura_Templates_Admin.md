# 📐 ARQUITECTURA: TEMPLATES Y ADMIN

**Documento de Análisis de la Estructura de Templates y django-admin-interface**

---

## 📋 ÍNDICE

1. [Visión General](#visión-general)
2. [Estructura de Templates](#estructura-de-templates)
3. [Configuración django-admin-interface](#configuración-django-admin-interface)
4. [Clases Admin](#clases-admin)
5. [Funciones de Utilidad](#funciones-de-utilidad)
6. [Integración de Componentes](#integración-de-componentes)
7. [Flujos de Datos](#flujos-de-datos)

---

## 🎯 Visión General

El proyecto utiliza **django-admin-interface 0.42.0** como interfaz moderna para administración de datos, con **28 templates HTML** organizados en 6 categorías y **25 clases admin** con funcionalidades avanzadas de importación/exportación, reportes y auditoría.

| Métrica | Valor |
|---------|-------|
| **Clases Admin** | 25 modelos registrados |
| **Templates** | 28 archivos HTML |
| **Líneas en admin.py** | 3560 |
| **Líneas de config admin-interface** | 237 |
| **Funciones de exportación** | 4 formatos (PDF, Excel, histórico) |

---

## 📁 ESTRUCTURA DE TEMPLATES

### 📂 Ubicación

```
templates/
├── admin/                          # Admin de Django + admin-interface
│   ├── base_site.html             # Base customizada
│   ├── reportes/                  # Centro de reportes (6 templates)
│   └── reloj_fichador/            # Templates por modelo
│
├── reloj_fichador/                # Vistas públicas (5 templates)
│   └── base.html                  # Interfaz de entrada (462 líneas)
│
├── errors/                        # Manejo de errores (7 templates)
│   └── base_error.html            # Base para errores (185 líneas)
│
└── admin-interface/                        # Personalización admin-interface
    ├── base.html                  # Base extendida
    └── helpers/
        └── theme_switch.html      # Selector light/dark
```

### 📊 Distribución de Templates

```
Total: 28 Templates

Admin               → 10 templates
├── base_site.html
├── asignar_area.html
├── cargar_licencia_v2.html
├── reloj_fichador/* (3 modelos)
└── reportes/* (6 templates)

Vistas Públicas     → 5 templates
├── base.html (462 líneas - principal)
├── home.html
├── lista_registros.html
├── operarios_list.html
└── reporte.html

Errores             → 7 templates
├── base_error.html (185 líneas)
├── 400.html, 403.html, 404.html
├── 429.html, 500.html
└── permissions.html

admin-interface Custom       → 2 templates
├── base.html (8 líneas)
└── theme_switch.html
```

### 🎨 Templates Principales

#### **templates/reloj_fichador/base.html** (462 líneas)
**Propósito**: Interfaz de entrada de datos de asistencia (DNI)

**Características Clave:**
- ⌨️ Atajos de teclado:
  - `Q` = Entrada
  - `Z` = Salida Transitoria
  - `M` = Entrada Transitoria
  - `P` = Salida

- 🔄 Sincronización 24/7:
  - Token CSRF persistente
  - Verificación cada 2 horas
  - Detecta inactividad (30 min)

- 📊 Widgets dinámicos:
  - Reloj sincronizado con servidor
  - Clima en tiempo real (OpenWeatherMap)
  - Rotación de imágenes de fondo (60 seg)

- ⚠️ Manejo de inconsistencias con modal

#### **templates/errors/base_error.html** (185 líneas)
**Propósito**: Página profesional de errores

**Características:**
- 🔴 Código de error prominente
- 📝 Título y mensaje descriptivos
- 🔍 Detalles técnicos colapsables
- 🎯 Botones de acción (Volver, Inicio)
- 📋 Información de permisos

#### **templates/admin/reportes/centro_reportes.html** (129 líneas)
**Propósito**: Centro de control de reportes

**Funcionalidad:**
- 3 tarjetas de reporte (Asistencia, Horas, Inconsistencias)
- Grid responsivo
- Transiciones suaves
- Links a vistas específicas

---

## ⚙️ CONFIGURACIÓN django-admin-interface

### 📍 Ubicación: mantenedor/settings.py (líneas 161-397)

#### **Información del Sitio**
```python
admin-interface = {
    "SITE_TITLE": "Reloj Fichador - Administración",
    "SITE_HEADER": "Sistema de Control de Asistencia",
    "SITE_URL": "/",
}
```

#### **Iconografía**
```python
"SITE_ICON": {
    "light": lambda request: static("img/logo_hores.png"),
    "dark": lambda request: static("img/logo_hores.png"),
},
"SITE_SYMBOL": "schedule",  # Icono Material Design
```

#### **Características**
```python
"SHOW_HISTORY": True,           # ✅ Botón de historial
"SHOW_VIEW_ON_SITE": False,     # ❌ Sin botón "Ver en sitio"
```

#### **Callbacks Personalizados**
```python
"ENVIRONMENT": "mantenedor.utils.environment_callback",
"DASHBOARD_CALLBACK": "mantenedor.utils.dashboard_callback",
```

#### **Esquema de Colores - Púrpura Personalizado**
```
Primary 500: #A855F7  ← Color principal usado
Primary 600: #9333EA
Primary 700: #7E22CE
Primary 800: #6B21A8  ← Modo oscuro
```

### 🗂️ Navegación Lateral (9 Secciones)

```
Panel Principal
  ├─ 📊 Dashboard

Gestión de Personal
  ├─ 👥 Operarios
  ├─ 🏢 Áreas
  └─ 📅 Horarios

Registros de Asistencia
  ├─ ⏰ Registro Diario
  ├─ 📋 Registro de Asistencia
  └─ 📄 Licencias

Cálculos de Horas
  ├─ ⏱️ Horas Trabajadas
  ├─ ⚡ Horas Extras
  ├─ 🎉 Horas Feriado
  └─ 📊 Horas Totales

Calendario Laboral
  ├─ 📆 Calendarios Laborales
  ├─ 👥 Grupos de Sábado
  └─ 🌍 Sugerencias de Feriados

Configuración
  ├─ ⚙️ Redondeo Entrada
  └─ ⚙️ Redondeo Salida

Reportes
  ├─ 📊 Centro de Reportes

Tareas Programadas
  ├─ 📅 Periodic Tasks
  ├─ ⏱️ Intervalos
  └─ 🔄 Crontab

Administración
  ├─ 👤 Usuarios
  └─ 👥 Grupos
```

---

## 👨‍💼 CLASES ADMIN

### 📊 Resumen de 25 Clases Registradas

#### **Grupo 1: Gestión de Personal** (3)

| Clase | Modelo | Mixins | Características |
|-------|--------|--------|-----------------|
| OperarioAdmin | Operario | Export, History, admin-interface | Foto, Áreas, Acciones |
| AreaAdmin | Area | Export, PDF, admin-interface | - |
| HorarioAdmin | Horario | Export, PDF, admin-interface | - |

#### **Grupo 2: Registros de Asistencia** (4)

| Clase | Modelo | Mixins | Características |
|-------|--------|--------|-----------------|
| RegistroDiarioAdmin | RegistroDiario | Import/Export, History, admin-interface | **Importación inteligente** |
| RegistroAsistenciaAdmin | RegistroAsistencia | Export, admin-interface | Carga de licencias |
| LicenciaAdmin | Licencia | History, admin-interface | Archivos |
| LogEntryAdmin | LogEntry | Export, PDF, admin-interface | **Solo lectura (auditoría)** |

#### **Grupo 3: Cálculos de Horas** (4)

| Clase | Modelo | Mixins | Características |
|-------|--------|--------|-----------------|
| HorasTrabajadasAdmin | Horas_trabajadas | Export, admin-interface | Template personalizado |
| HorasExtrasAdmin | Horas_extras | Export, admin-interface | Filtra 0 horas |
| HorasTotalesAdmin | Horas_totales | Export, admin-interface | Template personalizado |
| HorasFeriadoAdmin | Horas_feriado | Export, admin-interface | - |

#### **Grupo 4: Configuración** (2)

| Clase | Modelo | Mixins | Características |
|-------|--------|--------|-----------------|
| ConfiguracionRedondeoAdmin | ConfiguracionRedondeo | admin-interface | **Solo superusuario** |
| ConfiguracionRedondeoSalidaAdmin | ConfiguracionRedondeoSalida | admin-interface | **Solo superusuario** |

#### **Grupo 5: Otros** (8)

- ReporteAdmin (Reporte)
- CalendarioLaboralAdmin (CalendarioLaboral)
- GrupoSabadoAdmin (GrupoSabado)
- SugerenciaFeriadoAdmin (SugerenciaFeriado)
- HorasEnfermedadAdmin (HorasEnfermedad)
- HistoricalOperarioAdmin (HistoricalOperario)
- HistoricalRegistroDiarioAdmin (HistoricalRegistroDiario)
- HistoricalLicenciaAdmin (HistoricalLicencia)
- RestrictedUserAdmin (User)
- GroupAdmin (Group)

---

## 📊 PRINCIPALES CARACTERÍSTICAS POR ADMIN

### 🔄 RegistroDiarioAdmin (Líneas 533-767)

**Importación/Exportación Inteligente:**
```
✅ Búsqueda automática de operario por DNI
✅ Validación de tipo de movimiento
✅ Múltiples formatos de fecha:
   - YYYY-MM-DD HH:MM:SS
   - DD/MM/YYYY HH:MM:SS
   - DD-MM-YYYY HH:MM:SS
✅ Conversión inteligente de booleanos
✅ Asigna origen automático ('Importado')
✅ Recalcular horas después de importar
```

**Acciones:**
- Generar reporte HTML
- Exportar Excel
- Exportar PDF
- Recalcular horas

### 📈 OperarioAdmin (Líneas 137-239)

**Características:**
- 👤 Mostrar foto del operario (max 150px)
- 🏢 Listar áreas asociadas
- 📅 Historial completo de cambios
- ⚡ Acciones masivas:
  - Asignar área
  - Generar reporte
  - Exportar Excel/PDF

### ⏱️ HorasTrabajadasAdmin (Líneas 786-949)

**Personalización:**
- 📋 Template `change_list.html`
- 🔧 Optimización `select_related('operario')`
- 📊 Métodos de formato para duraciones

### 📊 HorasTotalesAdmin (Líneas 1049-1280)

**Características:**
- 📋 Template personalizado: `change_list.html`
- 🔢 Muestra todos los tipos de horas:
  - Horas normales
  - Horas nocturnas
  - Horas extras
  - Horas feriado
  - Horas enfermedad
- 🔄 Acción: Recalcular todas las horas
- 📊 Métodos de formato avanzados

---

## 🛠️ FUNCIONES DE UTILIDAD (mantenedor/utils.py)

### 🌍 environment_callback()

```python
def environment_callback(request):
    """Muestra el entorno (Desarrollo/Producción)"""
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    if debug:
        return ("Desarrollo", "warning")      # 🟨 Amarillo
    else:
        return ("Producción", "success")      # 🟩 Verde
```

**Uso:** Badge en esquina superior del admin

### 📊 dashboard_callback()

```python
def dashboard_callback(request, context):
    """Inyecta datos en el dashboard"""

    context.update({
        'total_operarios': count,
        'registros_hoy': count,
        'operarios_presentes_hoy': count,
        'sugerencias_feriados_pendientes': queryset,
        'feriados_proximos': queryset,
    })

    return context
```

**Datos Mostrados:**
- 👥 Total de operarios activos
- 📋 Registros fichados hoy
- 🔍 Operarios presentes (entrada fichada)
- ⚠️ Sugerencias de feriados pendientes
- 📆 Próximos 5 feriados (30 días)

---

## 🔀 INTEGRACIÓN DE COMPONENTES

### 📐 Diagrama de Relaciones

```
mantenedor/settings.py
   ↓
   ├─ admin-interface config (237 líneas)
   │  └─ Callbacks → mantenedor/utils.py
   │
   ├─ Templates admin-interface
   │  └─ templates/admin-interface/
   │
   └─ INSTALLED_APPS
      └─ 'admin_interface' (debe ir PRIMERO)
         └─ Activa admin customizado
            └─ apps/reloj_fichador/admin.py
               ├─ 25 clases admin
               ├─ Templates en templates/admin/
               ├─ Importación/exportación
               ├─ Reportes PDF/Excel
               └─ Acciones masivas
```

### 🔗 Flujos de Datos

#### **Exportación de RegistroDiario:**
```
click "EXPORT"
   ↓
dehydrate_operario__dni()      → Extrae DNI
dehydrate_operario__nombre()   → Extrae Nombre
dehydrate_tipo_movimiento()    → Mapea tipos complejos
dehydrate_valido()             → Convierte a 'True'/'False'
   ↓
Archivo Excel descargado
```

#### **Importación de RegistroDiario:**
```
subir archivo Excel
   ↓
before_import_row()
├─ Busca operario por DNI
├─ Valida tipo de movimiento
├─ Parsea múltiples formatos de fecha
└─ Convierte booleanos
   ↓
get_or_init_instance()
├─ Busca por (operario_id, hora_fichada)
├─ Si existe → actualiza
└─ Si no existe → crea
   ↓
after_save_instance()
└─ Recalcula horas trabajadas
   ↓
Registros procesados
```

#### **Flujo de Acciones Masivas:**
```
Seleccionar registros + Acción
   ↓
generar_reporte()
   ↓
exportar_excel()
   ↓
exportar_pdf()
   ↓
recalcular_horas()
```

---

## 📦 RECURSOS DE IMPORTACIÓN/EXPORTACIÓN

### RegistroDiarioResource (Líneas 242-530)

**Campos Personalizados:**
```python
operario__dni           ← Búsqueda automática
operario__nombre        ← Solo lectura
operario__apellido      ← Solo lectura
tipo_movimiento         ← Validación
hora_fichada            ← Múltiples formatos
valido                  ← Booleano
inconsistencia          ← Booleano
```

**Validación Inteligente:**
```
✅ DNI → busca operario automáticamente
✅ tipo_movimiento → 'entrada', 'salida', etc.
✅ Múltiples formatos de fecha
✅ Conversión de booleanos (true/1/sí/verdadero)
✅ Asigna valores por defecto
✅ Limpia campos readonly
```

---

## 📋 TEMPLATES POR ADMIN

| Admin | Template | Ubicación |
|-------|----------|-----------|
| RegistroDiarioAdmin | change_form.html | templates/admin/reloj_fichador/registrodiario/ |
| HorasTrabajadasAdmin | change_list.html | templates/admin/reloj_fichador/horas_trabajadas/ |
| HorasTotalesAdmin | change_list.html | templates/admin/reloj_fichador/horas_totales/ |
| ReporteAdmin | centro_reportes.html | templates/admin/reportes/ |
| RegistroAsistenciaAdmin | cargar_licencia_v2.html | templates/admin/ |

---

## 🔒 RESTRICCIONES DE SEGURIDAD

### Configuración Redondeo (RESTRINGIDO)
```python
def has_add_permission(self, request):
    return request.user.is_superuser

def has_change_permission(self, request, obj=None):
    return request.user.is_superuser

def has_delete_permission(self, request, obj=None):
    return request.user.is_superuser
```

**Solo Superusuarios pueden:**
- ✏️ Crear configuraciones
- 📝 Editar redondeos
- 🗑️ Eliminar configuraciones

### LogEntry (AUDITORÍA - SOLO LECTURA)
```python
def has_add_permission(self, request):
    return False

def has_change_permission(self, request, obj=None):
    return False

def has_delete_permission(self, request, obj=None):
    return False
```

**Completamente de solo lectura para auditoría.**

---

## ⚙️ REQUISITOS TÉCNICOS

### INSTALLED_APPS (orden importante)
```python
'admin_interface',                              # ⭐ PRIMERO
'admin-interface.contrib.import_export',
'admin-interface.contrib.simple_history',
'django.contrib.admin',
'django.contrib.auth',
...
'apps.reloj_fichador',
'simple_history',
'import_export',
'rangefilter',
'django_celery_beat',
'weasyprint',
```

### Middleware Requerido
```python
'django.middleware.security.SecurityMiddleware'
'django.contrib.sessions.middleware.SessionMiddleware'
'django.middleware.locale.LocaleMiddleware'
'django.middleware.common.CommonMiddleware'
'apps.reloj_fichador.middleware.TerminalCriticoMiddleware'
'django.middleware.csrf.CsrfViewMiddleware'
'django.contrib.auth.middleware.AuthenticationMiddleware'
'django.contrib.messages.middleware.MessageMiddleware'
'django.middleware.clickjacking.XFrameOptionsMiddleware'
'simple_history.middleware.HistoryRequestMiddleware'
'axes.middleware.AxesMiddleware'
'apps.reloj_fichador.middleware.PermissionMiddleware'
'apps.reloj_fichador.middleware.ErrorHandlerMiddleware'
'apps.reloj_fichador.middleware.DisableCacheMiddleware'
```

### Colección de Static Files
```bash
docker compose exec web python manage.py collectstatic --noinput
```

---

## 📈 ESTADÍSTICAS DEL PROYECTO

| Métrica | Valor |
|---------|-------|
| **Total Templates** | 28 |
| **Clases Admin** | 25 |
| **Líneas admin.py** | 3,560 |
| **Líneas config admin-interface** | 237 |
| **Líneas utils.py** | 59 |
| **Navegación admin-interface** | 9 secciones |
| **Modelos registrados** | 25 |
| **Formatos exportación** | 4 (PDF, Excel, Histórico) |
| **Acciones masivas** | Múltiples por admin |

---

## ✅ CHECKLIST DE INTEGRACIÓN

### Verificar Instalación
- [ ] `admin-interface` en INSTALLED_APPS (PRIMERO)
- [ ] Middleware correctamente ordenado
- [ ] Static files recopilados
- [ ] Base de datos migrada
- [ ] Admin accesible en `/admin/`

### Verificar Funcionalidad
- [ ] Dashboard muestra estadísticas
- [ ] Badge de entorno visible
- [ ] Navegación lateral colapsable
- [ ] Importación/exportación funciona
- [ ] Reportes PDF se generan
- [ ] Historial visible en registros

### Verificar Seguridad
- [ ] Configuración Redondeo restringida a superuser
- [ ] LogEntry es solo lectura
- [ ] Permisos por usuario aplicados
- [ ] CSRF tokens persistentes

---

## 🎯 CONCLUSIÓN

La arquitectura de templates y admin del proyecto **Reloj Fichador** es **sofisticada y profesional**, proporcionando:

✅ Interfaz moderna con **django-admin-interface 0.42.0**
✅ **25 clases admin** con funcionalidades avanzadas
✅ **28 templates HTML** organizados estratégicamente
✅ **Importación/exportación inteligente** con validación
✅ **Reportes en PDF y Excel**
✅ **Dashboard personalizado** en tiempo real
✅ **Navegación jerárquica** en 9 secciones
✅ **Historial completo** de cambios
✅ **Seguridad robusta** con restricciones de permisos

**Resultado:** Una plataforma de administración completa, moderna y profesional para gestionar el sistema de control de asistencia.
