# Mejoras en el cálculo de horas trabajadas

## Resumen
Se simplificó y robusteció la lógica de cálculo de horas normales, nocturnas y extras para los registros de asistencia de operarios. Ahora el sistema:

- Clasifica cada bloque entrada-salida como normal o nocturno según reglas claras.
- Suma todas las horas normales y nocturnas del día.
- La jornada principal (máximo 8h) se asigna al tipo con mayor cantidad (normal o nocturno).
- El excedente sobre 8h se considera horas extras, redondeadas en bloques de 15 minutos.

## Lógica de clasificación de bloques

- Si la entrada y salida son el mismo día y la entrada es antes de las 20:00, **todo el bloque es normal**.
- Si la entrada y salida son el mismo día y la entrada es a partir de las 20:00, **todo el bloque es nocturno**.
- Si la entrada y salida son días distintos y la entrada es a partir de las 20:00, **todo el bloque es nocturno**.
- Si la entrada y salida son días distintos y la entrada es antes de las 20:00, **todo el bloque es normal** (caso poco frecuente).

## Lógica de jornada principal y horas extras

- Se suman todas las horas normales y nocturnas del día.
- Si hay más horas nocturnas, la jornada principal (máximo 8h) se asigna a nocturnas.
- Si hay más horas normales, la jornada principal (máximo 8h) se asigna a normales.
- El excedente sobre 8h se considera horas extras, redondeadas en bloques de 15 minutos.

## Ejemplo de código relevante

```python
def calcular_horas_por_franjas(inicio, fin, limites=None):
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    if inicio.tzinfo is not None:
        inicio = inicio.astimezone(argentina_tz)
    else:
        inicio = argentina_tz.localize(inicio)
    if fin.tzinfo is not None:
        fin = fin.astimezone(argentina_tz)
    else:
        fin = argentina_tz.localize(fin)

    if inicio.date() == fin.date():
        if inicio.time() >= time(20, 0):
            return timedelta(0), fin - inicio  # Todo nocturno
        else:
            return fin - inicio, timedelta(0)  # Todo normal
    else:
        if inicio.time() >= time(20, 0):
            return timedelta(0), fin - inicio
        else:
            return fin - inicio, timedelta(0)
```

## Ventajas
- Simplicidad y robustez.
- No hay mezcla de horas normales y nocturnas en la misma jornada.
- El cálculo es predecible y fácil de auditar.

## Limitaciones
- No discrimina minutos nocturnos/diurnos dentro de un mismo bloque. Si un bloque cruza la franja, se clasifica solo por la hora de entrada.

---

**Última actualización:** 21/05/2025
