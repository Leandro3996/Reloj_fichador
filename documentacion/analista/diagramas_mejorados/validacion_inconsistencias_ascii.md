# Diagrama de Flujo ASCII Mejorado - Validación de Inconsistencias

## 2. Validación de Inconsistencias

```
        /====================================\
        |        VALIDACIONES PREVIAS        |
        \===============+===================/
                        |
        /===============+==================\
        | ¿Tiene un registro de salida     |
        | el día de ayer?                  |
        \======+=====================+=====/
               |                     |
               | SI                  | NO
               |                     |
               |                     v
               |         /===========+===========\
               |         | ¿Es su primer registro?|
               |         \===========+===========/
               |                     |
               |          .---------+----------.
               |          |                    |
               |        SI|                   NO|
               |          v                    v
               |   /======+======\    /========+========\
               |   |             |    |                 |
               |   | Validación  |    | Aplicar lógica  |
               |   | normal      |    | de inconsistencia|
               |   |             |    |                 |
               |   \======+======/    \=================/ 
               v          v
        /======+===============================\
        |             TIPOS DE MOVIMIENTO      |
        \======+===============================/ 

.-----------.--------------.---------------.-------------.
|           |              |               |             |
v           v              v               v             v
/===========+===========\               /==+==============\
|                       |               |                  |
|       ENTRADA         |               |  SALIDA TRANS.   |
|                       |               |                  |
\===========+==========/               \==+================/
            |                             |
            v                             v
/===========+===========\     /===========+===========\
| ¿Ya tiene entrada?    |     | ¿Tiene entrada hoy?   |
\===========+==========/     \===========+==========/
            |                             |
     .------+------.               .------+------.
     |             |               |             |
   SI|            NO|             NO|            SI|
     v             v               v             v
/====+====\  /=====+====\   /======+====\  /=====+====\
|         |  |          |   |           |  |          |
| [!] INCON|  | [✓] CONS |   | [!] INCON |  | ¿Ya tiene|
| SISTENTE |  | SISTENTE |   | SISTENTE  |  | salida   |
|         |  |          |   |           |  | trans.?  |
\=========/  \==========/   \===========/  \====+=====/ 
                                                |
                                         .------+------.
                                         |             |
                                       SI|            NO|
                                         v             v
                                    /====+====\  /=====+====\
                                    |         |  |          |
                                    | [!] INCON|  | [✓] CONS |
                                    | SISTENTE |  | SISTENTE |
                                    |         |  |          |
                                    \=========/  \==========/

/===========+===========\               /==+==============\
|                       |               |                  |
|   ENTRADA TRANS.      |               |      SALIDA      |
|                       |               |                  |
\===========+==========/               \==+================/
            |                             |
            v                             v
/===========+===========\     /===========+===========\
| ¿Tiene entrada hoy?   |     | ¿Tiene entrada hoy?   |
\===========+==========/     \===========+==========/
            |                             |
     .------+------.               .------+------.
     |             |               |             |
   NO|            SI|             NO|            SI|
     v             v               v             v
/====+====\  /=====+====\   /======+====\  /=====+====\
|         |  |          |   |           |  | ¿Movim.  |
| [!] INCON|  | ¿Tiene   |   | [!] INCON |  | transit.|
| SISTENTE |  | salida   |   | SISTENTE  |  | pend.?  |
|         |  | trans.?   |   |           |  |         |
\=========/  \====+=====/ 	\===========/  \====+=====/ 
                  |                              |
            .-----+------.                 .-----+------.
            |            |                 |            |
          NO|           SI|               SI|           NO|
            v            v                 v            v
       /====+====\  /====+====\      /=====+====\  /====+====\
       |         |  |         |      |          |  |         |
       | [!] INCON|  | [✓] CONS|      | [!] INCON |  | [✓] CONS|
       | SISTENTE |  | SISTENTE|      | SISTENTE  |  | SISTENTE|
       |         |  |         |      |          |  |         |
       \=========/  \=========/      \==========/  \=========/
```

Este diagrama mejorado de validación de inconsistencias incorpora:

1. **Sección de Validaciones Previas**: Claramente delimitada al inicio del flujo.
2. **Estructura consistente**: Cada tipo de movimiento sigue el mismo patrón visual.
3. **Símbolos distintivos**:
   - [✓] para estado consistente
   - [!] para inconsistencias
4. **Agrupación mejorada**: Separación visual entre diferentes tipos de movimientos.
5. **Claridad en decisiones**: Representación más clara de SI/NO en las bifurcaciones.
6. **Delimitadores especiales**: Uso de caracteres especiales para mejorar la legibilidad.

Esta representación ASCII mantiene la compatibilidad universal mientras refleja fielmente la estructura y lógica del diagrama visual, facilitando la comprensión de las validaciones de inconsistencias en entornos donde solo se puede usar texto. 