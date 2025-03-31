# Diagrama de Flujo ASCII Mejorado - Tareas Programadas

## 5. Tareas Programadas Automatizadas

```
            /=========================\
            |                         |
            |     *** INICIO ***      |
            |       CELERY            |
            |                         |
            \===========+=============/
                        |
                        v
            /===========+============\
            |                        |
            |   Iniciar servicios    |
            |   Celery               |
            |                        |
            \===========+============/
                        |
                        v
            /===========+============\
            |                        |
            |  Cargar tareas         |
            |  programadas           |
            |                        |
            \===========+============/
                        |
       .--------.-------+-------.--------.
       |        |               |        |
       v        v               v        v
/======+======\ /======+======\ /======+======\ /======+======\
|             | |             | |             | |             |
| [1] ASISTENC| | [2] VERIFIC | | [3] CÁLCULO | | [4] BACKUP  |
|             | |             | |             | |             |
\======+======/ \======+======/ \======+======/ \======+======/
       |               |               |               |
       v               v               v               v
/======+======\ /======+======\ /======+======\ /======+======\
|             | |             | |             | |             |
| ¿Es         | | ¿Es hora    | | ¿Es fin de  | | ¿Han pasado |
| medianoche? | | programada? | | jornada?    | | 2 horas?    |
|             | |             | |             | |             |
\======+======/ \======+======/ \======+======/ \======+======/
       |               |               |               |
  .----+----.     .----+----.     .----+----.     .----+----.
  |         |     |         |     |         |     |         |
SI|        NO|   SI|        NO|   SI|        NO|   SI|        NO|
  v         |     v         |     v         |     v         |
/=+========\|    /=+======\ |    /=+======\ |    /=+======\ |
|          ||    |         ||    |         ||    |         ||
| CREAR    ||    | VERIFIC ||    | CALCULAR||    | GENERAR ||
| registros||    | asist.  ||    | horas   ||    | backup  ||
|          ||    |         ||    |         ||    |         ||
\=+========/|    \=+=======/|    \=+=======/|    \=+=======/|
  |         |      |        |      |        |      |        |
  |         |      |        |      |        |      |        |
  |         |      |        |      |        |      |        |
  |         |      v        |      |        |      |        |
  '---------+----->+<-------'------'--------+------'--------'
            |      |                         |
            |      v                         |
            |  /===+====\                    |
            |  |        |                    |
            |  | [✓] LOG|                    |
            |  |        |                    |
            |  \===+====/                    |
            |      |                         |
            |      v                         |
            |  /===+====\                    |
            |  |        |                    |
            |  | [⏳]   |                    |
            |  | ESPERA |                    |
            |  |        |                    |
            '--+>===+===/                    |
                   |                         |
                   '-------------------------'
                   |
                   v
            /======+======\
            |             |
            | REINICIAR   |
            | ciclo       |
            |             |
            \=============/
```

Este diagrama ASCII mejorado para las tareas programadas incorpora:

1. **Numeración de tareas**:
   - [1] para la tarea de Asistencia
   - [2] para la tarea de Verificación
   - [3] para la tarea de Cálculo
   - [4] para la tarea de Backup

2. **Símbolos especiales**:
   - [✓] para el registro en log
   - [⏳] para el estado de espera

3. **Claridad en decisiones**: Representación explícita de SI/NO en cada bifurcación.

4. **Flujo cíclico mejorado**: Representación más clara del reinicio del ciclo.

5. **Estructura consistente**: Formato unificado para todas las tareas y sus condiciones.

6. **Mayor legibilidad**: Mejor organización visual de los elementos y conectores.

Este diagrama ASCII mantiene la compatibilidad con texto plano mientras refleja fielmente la estructura y lógica del diagrama visual, facilitando la comprensión del sistema de tareas programadas en entornos donde solo se puede usar texto. 