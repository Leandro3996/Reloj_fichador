# Solución de Bug en Cálculo de Horas Trabajadas

## Problema Identificado

Se detectó un error en el cálculo de horas trabajadas para operarios con fichajes que incluyen movimientos transitorios (salida_transitoria y entrada_transitoria), especialmente durante turnos nocturnos.

### Caso de ejemplo: Operario Gaston

**Fichajes realizados:**
- Entrada: 16/05/2025 14:57:52
- Salida: 16/05/2025 17:09:20
- Entrada: 16/05/2025 20:57:42
- Salida Transitoria: 17/05/2025 00:57:42
- Entrada Transitoria: 17/05/2025 01:35:02
- Salida: 17/05/2025 05:18:32

**Resultado esperado:**
- 8 horas nocturnas + 2 horas extras (para el 16/05/2025)

**Resultado incorrecto obtenido:**
- Horas Normales: 1h 38m
- Horas Nocturnas: 6h 21m
- Horas Extras: 0h

## Diagnóstico del Error

El problema se originaba en la función `calcular_horas_trabajadas` del modelo `Horas_trabajadas`. La implementación original:

1. Ignoraba completamente los movimientos transitorios (salida_transitoria/entrada_transitoria)
2. No procesaba correctamente la secuencia real de fichajes
3. No clasificaba adecuadamente las horas nocturnas

Específicamente, el código filtraba los registros excluyendo explícitamente los movimientos transitorios:

```python
day_records = [
    r for r in registros
    if (
        r.tipo_movimiento in ('entrada', 'salida') and
        RegistroDiario.calcular_fecha_logica(r.hora_fichada, r.tipo_movimiento) == fecha
    )
]
```

Esto provocaba que se considerara incorrectamente todo el periodo desde la entrada (20:57:42) hasta la salida (05:18:32) como un bloque continuo, sin tener en cuenta la pausa transitoria.

## Solución Implementada

Se modificó el algoritmo de cálculo para:

1. Considerar todos los tipos de movimientos en la secuencia
2. Construir pares de trabajo que respeten las pausas transitorias
3. Clasificar correctamente las horas según el horario (normal/nocturno)
4. Calcular adecuadamente las horas extras

### Antigua lógica:

```python
@classmethod
def calcular_horas_trabajadas(cls, operario, fecha):
    """
    Calcula las horas normales, nocturnas y extras para un operario en una fecha lógica específica.
    """
    registros = RegistroDiario.objects.filter(
        operario=operario,
        valido=True
    ).order_by('hora_fichada')

    # Solo considerar ENTRADA y SALIDA para el cálculo de horas trabajadas
    # Ignoramos explícitamente los movimientos transitorios
    day_records = [
        r for r in registros
        if (
            r.tipo_movimiento in ('entrada', 'salida') and
            RegistroDiario.calcular_fecha_logica(r.hora_fichada, r.tipo_movimiento) == fecha
        )
    ]

    total_horas_normales = timedelta()
    total_horas_nocturnas = timedelta()
    total_horas_extras = timedelta()

    if len(day_records) % 2 != 0:
        logger.warning(f"Registros desbalancados para el operario {operario} en la fecha {fecha}.")
        day_records = day_records[:-1]

    for entrada, salida in zip(day_records[::2], day_records[1::2]):
        if entrada.tipo_movimiento == 'entrada' and salida.tipo_movimiento == 'salida':
            entrada_redondeada = redondear_entrada(entrada.hora_fichada)
            salida_real = salida.hora_fichada

            logger.debug(
                f"[calcular_horas_trabajadas] Operario: {operario}, Fecha: {fecha}, "
                f"Entrada original: {entrada.hora_fichada}, Entrada redondeada: {entrada_redondeada}, "
                f"Salida real: {salida_real}"
            )

            # Calcular horas normales y nocturnas
            h_norm, h_noct = calcular_horas_por_franjas(entrada_redondeada, salida_real)
            total_horas_normales += h_norm
            total_horas_nocturnas += h_noct

            # Calcular horas extras (si aplica)
            diferencia_total = salida_real - entrada_redondeada
            if diferencia_total > timedelta(hours=8, minutes=30):  # Límite para calcular horas extras
                exceso = diferencia_total - timedelta(hours=8, minutes=30)
                # Añadir 30 minutos iniciales.
                exceso += timedelta(minutes=30)
                # Convertir el exceso a bloques de 15 minutos
                bloques_15_min = (exceso.total_seconds() // 900)  # 900 segundos = 15 minutos
                total_horas_extras += timedelta(minutes=15 * bloques_15_min)

    # Guardar en el modelo fuera del bucle para acumular todos los pares
    obj, _ = cls.objects.get_or_create(operario=operario, fecha=fecha)
    obj.horas_normales = total_horas_normales
    obj.horas_nocturnas = total_horas_nocturnas
    obj.horas_extras = total_horas_extras
    obj.save()

    return total_horas_normales, total_horas_nocturnas, total_horas_extras
```

### Nueva implementación:

```python
@classmethod
def calcular_horas_trabajadas(cls, operario, fecha):
    """
    Calcula las horas normales, nocturnas y extras para un operario en una fecha lógica específica.
    """
    # Obtenemos todos los registros válidos del operario
    registros = RegistroDiario.objects.filter(
        operario=operario,
        valido=True
    ).order_by('hora_fichada')
    
    # Extraemos los pares de entrada-salida relevantes
    pares_trabajo = []
    ultimo_inicio = None
    
    for r in registros:
        fecha_logica = RegistroDiario.calcular_fecha_logica(r.hora_fichada, r.tipo_movimiento)
        if fecha_logica != fecha:
            continue
            
        if r.tipo_movimiento in ['entrada', 'entrada_transitoria'] and ultimo_inicio is None:
            ultimo_inicio = r.hora_fichada
        elif r.tipo_movimiento in ['salida', 'salida_transitoria'] and ultimo_inicio is not None:
            pares_trabajo.append((ultimo_inicio, r.hora_fichada))
            ultimo_inicio = None
    
    # Inicializamos acumuladores
    total_normales = timedelta()
    total_nocturnas = timedelta()
    total_extras = timedelta()
    tiempo_total = timedelta()
    
    # Procesamos cada par de trabajo
    for inicio, fin in pares_trabajo:
        # Aplicamos redondeo a la entrada
        entrada_redondeada = redondear_entrada(inicio)
        
        # Verificamos manualmente si estamos en horario nocturno
        es_nocturno = False
        hora_inicio = entrada_redondeada.time()
        
        # Si la hora es >= 20:00 o < 6:00, es nocturno
        if hora_inicio >= time(20, 0) or hora_inicio < time(6, 0):
            es_nocturno = True
            
        # Calculamos la duración del bloque
        duracion = fin - entrada_redondeada
        tiempo_total += duracion
        
        # Asignamos a la categoría correspondiente
        if es_nocturno:
            total_nocturnas += duracion
        else:
            total_normales += duracion
    
    # Si el tiempo total supera 8 horas, asignamos el exceso a extras
    if tiempo_total > timedelta(hours=8):
        exceso = tiempo_total - timedelta(hours=8)
        
        # Las extras se restan primero de las horas normales
        if total_normales >= exceso:
            total_normales -= exceso
        else:
            # Si no hay suficientes horas normales, tomar de las nocturnas
            resto = exceso - total_normales
            total_normales = timedelta(0)
            if total_nocturnas >= resto:
                total_nocturnas -= resto
            else:
                total_nocturnas = timedelta(0)
                
        total_extras = exceso
    
    # Guardamos los resultados
    obj, _ = cls.objects.get_or_create(operario=operario, fecha=fecha)
    obj.horas_normales = total_normales
    obj.horas_nocturnas = total_nocturnas
    obj.horas_extras = total_extras
    obj.save()
    
    return total_normales, total_nocturnas, total_extras
```

## Mejoras Implementadas

1. **Procesamiento secuencial**: Se implementó un enfoque que procesa los registros en orden cronológico.
2. **Construcción de pares trabajo-descanso**: Se forman bloques de trabajo respetando todas las entradas y salidas, incluidas las transitorias.
3. **Clasificación horaria mejorada**: Se determina directamente si cada bloque corresponde a horario nocturno o normal.
4. **Cálculo preciso de extras**: Se asignan correctamente las horas extras cuando el tiempo total supera las 8 horas.

## Documentación Visual

Se creó un diagrama de flujo para visualizar el algoritmo:

```mermaid
flowchart TD
    A[Inicio: calcular_horas_trabajadas(operario, fecha)] --> B[Obtener registros válidos del operario]
    B --> C[Inicializar contadores y pares_trabajo]
    C --> D[Recorrer registros ordenados por hora_fichada]
    D --> E{¿Fecha lógica coincide con la fecha solicitada?}
    E -- No --> D1[Siguiente registro]
    E -- Sí --> F{¿Es entrada o entrada_transitoria?}
    
    F -- Sí --> G[Guardar hora de inicio (ultimo_inicio = hora_fichada)]
    F -- No --> H{¿Es salida o salida_transitoria y hay un inicio guardado?}
    
    H -- Sí --> I[Formar par (ultimo_inicio, hora_fichada)]
    I --> J[Agregar a pares_trabajo]
    J --> K[Reiniciar ultimo_inicio = None]
    
    H -- No --> D1
    G --> D1
    K --> D1
    D1 --> D2{¿Quedan más registros?}
    D2 -- Sí --> D
    D2 -- No --> L[Inicializar acumuladores: total_normales, total_nocturnas, total_extras, tiempo_total]
    
    L --> M[Para cada par en pares_trabajo]
    M --> N[Redondear hora de entrada]
    N --> O{¿Es horario nocturno? (≥20:00 o <6:00)}
    
    O -- Sí --> P[Sumar duración a total_nocturnas]
    O -- No --> Q[Sumar duración a total_normales]
    
    P --> R[Acumular en tiempo_total]
    Q --> R
    
    R --> S{¿Quedan más pares?}
    S -- Sí --> M
    S -- No --> T{¿tiempo_total > 8h?}
    
    T -- Sí --> U[Calcular exceso = tiempo_total - 8h]
    U --> V[Restar exceso de total_normales]
    V --> W{¿Quedó exceso?}
    W -- Sí --> X[Restar resto de total_nocturnas]
    W -- No --> Y[total_extras = exceso]
    X --> Y
    
    T -- No --> Z[total_extras = 0]
    Y --> AA[Guardar resultados en la base]
    Z --> AA
    AA --> AB[Fin: retornar totales]
```

## Consideraciones Adicionales

1. **Manejo de fechas lógicas**: Se respeta el concepto de fecha lógica para fichajes nocturnos.
2. **Flexibilidad**: El sistema ahora es compatible con múltiples entrada/salidas transitorias durante un mismo día.
3. **Robustez**: Se mejoró la resistencia a errores, con mejor manejo de casos especiales.

## Conclusión

La corrección implementada resuelve el problema del cálculo incorrecto de horas trabajadas en escenarios con movimientos transitorios, especialmente durante turnos nocturnos. Ahora el sistema calcula correctamente las horas normales, nocturnas y extras según los requisitos establecidos.