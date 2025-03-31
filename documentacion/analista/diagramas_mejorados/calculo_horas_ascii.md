# Diagrama de Flujo ASCII Mejorado - Cálculo de Horas

## 3. Cálculo de Horas Trabajadas

```
                /=======================\
                |                       |
                |   *** INICIO ***      |
                |     CÁLCULO           |
                |                       |
                \==========+============/
                           |
                           v
          .----------------+-------------------.
          | PREPARACIÓN DE DATOS               |
          |    /===========+============\      |
          |    |                        |      |
          |    | Obtener registros      |      |
          |    | del día                |      |
          |    |                        |      |
          |    \===========+============/      |
          |                |                   |
          |                v                   |
          |    /===========+============\      |
          |    |                        |      |
          |    | ¿Registros             +------+--------> /==================\
          |    |  completos?            |      |          |                  |
          |    |                        |      |          | [!] Sin calcular |
          |    \===========+============/      |          |                  |
          |                |                   |          \=========+========/
          |                | SI                |                    |
          |                v                   |                    |
          |    /===========+============\      |                    |
          |    |                        |      |                    |
          |    | Agrupar pares          |      |                    |
          |    | entrada-salida         |      |                    |
          |    |                        |      |                    |
          |    \===========+============/      |                    |
          `-----------------+-----------------'                     |
                            |                                       |
                            v                                       |
          .----------------+-------------------.                    |
          | REGLAS DE REDONDEO                 |                    |
          |    /===========+============\      |                    |
          |    |                        |      |                    |
          |    | Por cada par           |      |                    |
          |    | entrada-salida         |      |                    |
          |    |                        |      |                    |
          |    \===========+============/      |                    |
          |                |                   |                    |
          |                v                   |                    |
          |    /===========+============\      |                    |
          |    |                        |      |                    |
          |    | [↑] Redondear entrada  |      |                    |
          |    | hacia arriba           |      |                    |
          |    |                        |      |                    |
          |    \===========+============/      |                    |
          |                |                   |                    |
          |                v                   |                    |
          |    /===========+============\      |                    |
          |    |                        |      |                    |
          |    | ¿Duración >= 8h?       |      |                    |
          |    |                        |      |                    |
          |    \===========+============/      |                    |
          |                |                   |                    |
          |       .--------+--------->.        |                    |
          |       |                   |        |                    |
          |     SI|                  NO|       |                    |
          |       v                   v        |                    |
          |    /==+===========\  /===+======\  |                    |
          |    |              |  |          |  |                    |
          |    | Aplicar regla|  | Mantener |  |                    |
          |    | especial     |  | hora     |  |                    |
          |    | (redondeo    |  | exacta   |  |                    |
          |    |  a la baja)  |  | de salida|  |                    |
          |    |              |  |          |  |                    |
          |    \==+===========\  \===+======/  |                    |
          `---------+---------------+---------'                     |
                    |               |                               |
                    '-------+-------'                               |
                            |                                       |
                            v                                       |
          /=================+==================\                    |
          |                                    |                    |
          | Calcular horas por franjas         |                    |
          |                                    |                    |
          \========+===================+=======/                    |
                   |                   |                            |
                   v                   v                            |
    /==============+===========\  /====+=====================\      |
    |                          |  |                          |      |
    | [N] HORAS NORMALES       |  | [♦] HORAS NOCTURNAS      |      |
    | (06:00 - 20:00)          |  | (20:00 - 06:00)          |      |
    |                          |  |                          |      |
    \==============+===========\  \====+=====================/      |
                   |                   |                            |
                   '--------+----------'                            |
                            |                                       |
                            v                                       |
                /===========+============\                          |
                |                        |                          |
                | ¿Es feriado o domingo? |                          |
                |                        |                          |
                \===========+============/                          |
                            |                                       |
                 .---------+----------.                             |
                 |                    |                             |
               SI|                   NO|                            |
                 v                    v                             |
      /==========+=========\  /=======+========\                    |
      |                    |  |                |                    |
      | [F] HORAS FERIADO  |  | Mantener tipo  |                    |
      |                    |  | de horas       |                    |
      |                    |  |                |                    |
      \==========+=========\  \=======+========/                    |
                 |                    |                             |
                 '--------+----------'                              |
                          |                                         |
                          v                                         |
              /===========+============\                            |
              |                        |                            |
              | ¿Excede jornada normal?|                            |
              |                        |                            |
              \===========+============/                            |
                          |                                         |
               .---------+----------.                               |
               |                    |                               |
             SI|                   NO|                              |
               v                    v                               |
    /==========+=========\  /=======+========\                      |
    |                    |  |                |                      |
    | [E] HORAS EXTRA    |  | Solo horas     |                      |
    |                    |  | normales/noct. |                      |
    |                    |  |                |                      |
    \==========+=========\  \=======+========/                      |
               |                    |                               |
               '--------+----------'                                |
                        |                                           |
                        v                                           |
            /===========+============\                              |
            |                        |                              |
            | [✓] Guardar resultados |                              |
            | en base de datos       |                              |
            |                        |                              |
            \===========+============/                              |
                        |                                           |
                        '---------------+---------------------------'
                                        |
                                        v
                           /============+===========\
                           |                        |
                           |      *** FIN ***       |
                           |       CÁLCULO          |
                           |                        |
                           \========================/
```

Este diagrama ASCII mejorado para el cálculo de horas incorpora:

1. **Agrupación lógica**: Secciones claramente delimitadas para "PREPARACIÓN DE DATOS" y "REGLAS DE REDONDEO".
2. **Símbolos distintivos**:
   - [N] para Horas Normales
   - [♦] para Horas Nocturnas
   - [F] para Horas Feriado
   - [E] para Horas Extra
   - [↑] para el redondeo hacia arriba
   - [✓] para la confirmación de guardado
3. **Claridad en decisiones**: SI/NO claramente marcados en las bifurcaciones.
4. **Flujo alternativo**: Conexión clara al punto de finalización cuando no hay registros completos.
5. **Estructura visual mejorada**: Uso de caracteres especiales para delimitar claramente cada componente.

Este diagrama mantiene la compatibilidad ASCII mientras refleja fielmente la estructura y lógica del diagrama visual, facilitando la comprensión del complejo proceso de cálculo de horas en entornos donde solo se puede usar texto. 