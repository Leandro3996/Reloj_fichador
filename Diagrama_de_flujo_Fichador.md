# Diagrama de Flujo del Sistema Reloj Fichador

> [!info] Navegación
> **Índice Principal:** [[Indice_Reloj_Fichador|Índice del Sistema]]  
> **Contexto:** [[contexto|Contexto del Proyecto]]  
> **Otras Visualizaciones:** [[Diagrama_de_flujo_Visual|Visual]] | [[Diagrama_de_flujo_ASCII|ASCII]]  
> **Arquitectura:** [[estructura|Estructura del Proyecto]]

Este documento presenta los principales flujos de trabajo del sistema Reloj Fichador a través de diagramas para facilitar la comprensión de su funcionamiento.

## Índice
1. [Registro de Movimientos](#registro-de-movimientos)
2. [Validación de Inconsistencias](#validación-de-inconsistencias)
3. [Cálculo de Horas Trabajadas](#cálculo-de-horas-trabajadas)
4. [Generación de Reportes](#generación-de-reportes)
5. [Gestión de Licencias](#gestión-de-licencias)
6. [Ciclo de Vida de Tareas Programadas](#ciclo-de-vida-de-tareas-programadas)
7. [Algoritmo de Cálculo de Horas por Franjas](#algoritmo-de-cálculo-de-horas-por-franjas)

## Registro de Movimientos

```mermaid
flowchart TD
    A[Inicio - Pantalla Principal] --> B{Seleccionar Tipo Movimiento}
    B -->|Entrada - Q| C1[Selección: Entrada]
    B -->|Salida Trans. - V| C2[Selección: Salida Transitoria]
    B -->|Entrada Trans. - M| C3[Selección: Entrada Transitoria]
    B -->|Salida - P| C4[Selección: Salida]
    
    C1 --> D[Ingresar DNI]
    C2 --> D
    C3 --> D
    C4 --> D
    
    D --> E[Enviar Solicitud]
    E --> F{Validar Operario Existente}
    F -->|No| G[Mostrar Error: Operario no encontrado]
    F -->|Sí| H{Validar Consistencia}
    
    H -->|OK| I[Registrar Movimiento]
    H -->|Inconsistencia| J[Mostrar Modal de Inconsistencia<br>Fin no puede continuar]
    J --> K{¿Confirmar de todos modos?}
    K -->|Sí| L[Registrar con Override]
    K -->|No| M[Cancelar Operación]
    
    I --> N[Mostrar Confirmación]
    L --> N
    
    G --> O[Fin - Volver al inicio]
    M --> O
    N --> O
```

## Validación de Inconsistencias

```mermaid
flowchart TD
    A[Inicio - Validación] --> P{¿Tiene registro de salida<br>el día anterior?}
    P -->|Sí| Q[Validación especial<br>de continuidad]
    P -->|No| R{¿Es su primer<br>registro?}
    R -->|Sí| S[Continuar con<br>registro normal]
    R -->|No| T[Aplicar lógica<br>de inconsistencia]
    
    Q & S & T --> B{Tipo de Movimiento}
    
    B -->|Entrada| C1{¿Ya tiene entrada sin salida hoy?}
    C1 -->|Sí| D1[Inconsistencia: Ya tiene entrada]
    C1 -->|No| E1[Consistente]
    
    B -->|Salida Transitoria| C2{¿Tiene entrada hoy sin salida?}
    C2 -->|No| D2[Inconsistencia: No tiene entrada previa]
    C2 -->|Sí| E2{¿Ya tiene salida transitoria sin entrada transitoria?}
    E2 -->|Sí| F2[Inconsistencia: Ya tiene salida transitoria]
    E2 -->|No| G2[Consistente]
    
    B -->|Entrada Transitoria| C3{¿Tiene entrada hoy?}
    C3 -->|No| D3[Inconsistencia: No tiene entrada previa]
    C3 -->|Sí| E3{¿Tiene salida transitoria pendiente?}
    E3 -->|No| F3[Inconsistencia: No tiene salida transitoria previa]
    E3 -->|Sí| G3[Consistente]
    
    B -->|Salida| C4{¿Tiene entrada hoy sin salida?}
    C4 -->|No| D4[Inconsistencia: No tiene entrada previa]
    C4 -->|Sí| E4{¿Tiene movimientos transitorios pendientes?}
    E4 -->|Sí| F4[Inconsistencia: Tiene movimientos transitorios sin cerrar]
    E4 -->|No| G4[Consistente]
    
    D1 --> H[Devolver Resultado]
    D2 --> H
    D3 --> H
    D4 --> H
    E1 --> H
    F2 --> H
    G2 --> H
    F3 --> H
    G3 --> H
    F4 --> H
    G4 --> H
    
    H --> I[Fin]
```

## Cálculo de Horas Trabajadas

```mermaid
flowchart TD
    A[Inicio - Cálculo] --> B[Obtener registros del día]
    B --> C{¿Registros completos?}
    C -->|No| D[Terminar sin calcular]
    C -->|Sí| E[Agrupar pares entrada-salida]
    
    E --> F[Para cada par entrada-salida]
    F --> G[Redondear entrada hacia arriba]
    
    G --> I{¿Duración ≥ 8 horas?}
    I -->|Sí| J[Aplicar regla de redondeo<br>Salida hacia abajo]
    I -->|No| K[Mantener hora exacta de salida]
    
    J --> L[Calcular horas por franjas]
    K --> L
    
    L --> M{Clasificar horas}
    M -->|06:00 - 20:00| N1[Acumular horas normales]
    M -->|20:00 - 06:00| N2[Acumular horas nocturnas]
    
    N1 --> O{¿Es feriado o domingo?}
    N2 --> O
    
    O -->|Sí| P1[Convertir a horas feriado]
    O -->|No| P2[Mantener clasificación]
    
    P1 --> Q{¿Excede jornada normal?}
    P2 --> Q
    
    Q -->|Sí| R[Calcular horas extra]
    Q -->|No| S[Solo horas normales/nocturnas]
    
    R --> T[Guardar resultados]
    S --> T
    
    T --> U[Fin]
    D --> U
```

## Generación de Reportes

```mermaid
flowchart TD
    A[Inicio - Reportes] --> B[Seleccionar tipo de reporte]
    
    B --> C{Tipo de Reporte}
    C -->|Diario| D1[Seleccionar fecha]
    C -->|Por operario| D2[Seleccionar operario y período]
    C -->|Por área| D3[Seleccionar área y período]
    C -->|Mensual| D4[Seleccionar mes y año]
    
    D1 --> E[Configurar parámetros adicionales]
    D2 --> E
    D3 --> E
    D4 --> E
    
    E --> F[Enviar solicitud a BIRT]
    F --> G[BIRT procesa la solicitud]
    G --> H[Consultar datos en la BD]
    
    H --> I[Aplicar formato al reporte]
    I --> J[Generar documento]
    
    J --> K{Formato de salida}
    K -->|PDF| L1[Generar PDF]
    K -->|Excel| L2[Generar Excel]
    K -->|HTML| L3[Mostrar en navegador]
    
    L1 --> M[Devolver documento]
    L2 --> M
    L3 --> M
    
    M --> N[Fin]
```

## Gestión de Licencias

```mermaid
flowchart TD
    A[Inicio - Licencias] --> B[Acceder al panel de administración]
    B --> C[Seleccionar gestión de licencias]
    
    C --> D{Acción}
    D -->|Nueva licencia| E1[Completar formulario]
    D -->|Editar licencia| E2[Modificar licencia existente]
    D -->|Eliminar licencia| E3[Seleccionar licencia a eliminar]
    
    E1 --> F1[Seleccionar operario]
    F1 --> G1[Definir fechas inicio/fin]
    G1 --> H1[Seleccionar tipo licencia]
    H1 --> I1[Adjuntar documentación]
    I1 --> J1[Guardar licencia]
    
    E2 --> F2[Modificar campos]
    F2 --> G2[Guardar cambios]
    
    E3 --> F3{¿Confirmar eliminación?}
    F3 -->|Sí| G3[Eliminar licencia]
    F3 -->|No| H3[Cancelar]
    
    J1 --> K[Actualizar registros de asistencia]
    G2 --> K
    G3 --> K
    H3 --> L[Fin]
    
    K --> M[Notificar cambios]
    M --> L
```

## Ciclo de Vida de Tareas Programadas

```mermaid
flowchart TD
    A[Inicio - Celery] --> B[Iniciar servicios Celery]
    B --> C[Cargar tareas programadas]
    
    C --> D[Tarea: generar_registros_asistencia]
    C --> E[Tarea: verificar_asistencia]
    C --> F[Tarea: calcular_horas_trabajadas]
    C --> G[Tarea: respaldo_automatico]
    
    D --> H{¿Es medianoche?}
    H -->|Sí| I[Crear registros de asistencia<br>para todos los operarios activos]
    H -->|No| J[Esperar]
    
    E --> K{¿Es hora programada?}
    K -->|Sí| L[Verificar asistencia<br>de cada operario]
    K -->|No| M[Esperar]
    
    F --> N{¿Es fin de jornada?}
    N -->|Sí| O[Calcular horas para<br>registros completos]
    N -->|No| P[Esperar]
    
    G --> Q{¿Han pasado 2 horas?}
    Q -->|Sí| R[Generar backup de la BD]
    Q -->|No| S[Esperar]
    
    I --> T[Registrar resultado en log]
    L --> T
    O --> T
    R --> T
    
    J --> U[Continuar ciclo]
    M --> U
    P --> U
    S --> U
    T --> U
    
    U --> V[Fin - Reiniciar ciclo]
```

## Algoritmo de Cálculo de Horas por Franjas

```mermaid
flowchart TD
    classDef inicio fill:#b3e0ff,stroke:#333,stroke-width:2px,color:#000
    classDef proceso fill:#f2f2f2,stroke:#333,stroke-width:1px,color:#000
    classDef decision fill:#ffffcc,stroke:#ffcc00,stroke-width:2px,color:#000,font-weight:bold
    classDef franjas fill:#ffccff,stroke:#cc00cc,stroke-width:2px,color:#000
    
    A[Inicio - calcular_horas_por_franjas] --> B[Recibir parámetros: inicio, fin, limites]
    B --> C{¿USE_TZ está<br>habilitado?}
    C -->|Sí| D[Normalizar fechas<br>con timezone.make_aware]
    C -->|No| E{¿Se proporcionaron<br>límites?}
    D --> E
    
    E -->|No| F[Establecer límites por defecto]
    E -->|Sí| G[Usar límites proporcionados]
    
    F --> H[Definir franjas horarias]
    G --> H
    
    subgraph limites_default [Límites por defecto]
        F1[Horas nocturnas: 20:00 a 06:00]
        F2[Horas normales: 04:00 a 22:00]
    end
    
    H --> I[Inicializar variables:<br>actual = inicio<br>total_normales = 0<br>total_nocturnas = 0]
    I --> J{¿actual < fin?}
    J -->|No| K[Retornar total_normales, total_nocturnas]
    J -->|Sí| L[Determinar siguiente punto de corte]
    
    L --> M[Identificar posibles puntos de corte:<br>- fin<br>- límites relevantes > actual]
    M --> N[siguiente = min(posibles_cortes)]
    N --> O{¿siguiente <= actual?}
    O -->|Sí| P[siguiente = actual + 1 hora<br>o fin si es menor]
    O -->|No| Q{¿Es horario normal?<br>4am-21hs → 5am-22hs}
    P --> Q
    
    Q -->|Sí| R[total_normales += siguiente - actual]
    Q -->|No| S{¿Es horario nocturno?<br>20hs-5am → 21hs-6am}
    S -->|Sí| T[total_nocturnas += siguiente - actual]
    S -->|No| U[Sin clasificar]
    
    R --> V[actual = siguiente]
    T --> V
    U --> V
    
    V --> J
    
    K --> W[Fin - Devolver totales]
    
    class A,W inicio
    class B,D,I,L,M,N,P,R,T,U,V proceso
    class C,E,J,O,Q,S decision
    class F,G,F1,F2 franjas
```

## Notas adicionales

- **Redondeo de horas**: El sistema aplica reglas específicas para el redondeo de horas, considerando que la entrada se redondea hacia arriba a la próxima hora completa, y la salida hacia abajo a la hora anterior si se han trabajado al menos 8 horas.

- **Clasificación de horas**: Las horas se clasifican en normales (06:00-20:00), nocturnas (20:00-06:00), extras (excedentes a jornada regular) y feriado (trabajadas en días festivos o domingos).

- **Validación de consistencia**: El sistema realiza validaciones para evitar secuencias ilógicas de fichadas (por ejemplo, salida sin entrada previa). También se consideran registros del día anterior para mantener la consistencia entre días.

- **Validaciones previas**: Antes de evaluar la consistencia específica del tipo de movimiento, se verifica si el operario tiene un registro de salida del día anterior y si es su primer registro, lo que determina el flujo de validación a seguir.

- **Teclas de acceso rápido**: El sistema utiliza teclas específicas para cada tipo de movimiento: Q (Entrada), V (Salida Transitoria), M (Entrada Transitoria) y P (Salida).

- **Override de inconsistencias**: Aunque se detecte una inconsistencia, el sistema permite al usuario confirmar el registro si es necesario, registrando esta excepción.

- **Cálculo detallado de franjas horarias**:
  - **Horas normales**: Validadas cuando el ingreso está entre 4:00 y 21:00, y la salida entre 5:00 y 22:00.
  - **Horas nocturnas**: Validadas cuando el ingreso está entre 20:00 y 5:00, y la salida entre 21:00 y 6:00.
  - **Algoritmo iterativo**: La función calcula las horas por segmentos, avanzando a través de los límites de franjas horarias hasta llegar al fin del periodo.

---

> [!tip] Documentos Relacionados
> - Para entender el contexto y reglas de negocio, consulta [[contexto|Contexto del Proyecto]]
> - Para una visualización avanzada con colores e iconos, ve a [[Diagrama_de_flujo_Visual|Diagramas Visuales]]
> - Para una visualización en ASCII art, revisa [[Diagrama_de_flujo_ASCII|Diagramas ASCII]]
> - Para entender la estructura técnica, consulta [[estructura|Arquitectura del Proyecto]]
> - Regresa al [[Indice_Reloj_Fichador|Índice Principal]] 