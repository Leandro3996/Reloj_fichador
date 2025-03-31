# Diagrama de Flujo ASCII Mejorado - Generación de Reportes

## 4. Generación de Reportes

```
                          /========================\
                          |                        |
                          |    *** INICIO ***      |
                          |      REPORTE           |
                          |                        |
                          \===========+============/
                                      |
                                      v
                          /===========+============\
                          |                        |
                          |    Seleccionar tipo    |
                          |       de reporte       |
                          |                        |
                          \===========+============/
                                      |
        .---------------------.-------+-------.--------------------.
        |                     |               |                    |
        v                     v               v                    v
/=======+========\  /=========+=========\  /==+===============\  /=+===============\
|                |  |                   |  |                  |  |                 |
| [📅] DIARIO    |  | [👤] POR OPERARIO |  | [🏢] POR ÁREA    |  | [📊] MENSUAL    |
|                |  |                   |  |                  |  |                 |
\=======+========/  \=========+=========/  \==+===============/  \=+===============/
        |                     |               |                    |
        '---------------------+---------------+--------------------'
                              |
                              v
                      /=======+=======\
                      |               |
                      | Configurar    |
                      | parámetros    |
                      |               |
                      \=======+=======/
                              |
                              v
                      /=======+=======\
                      |               |
                      | Enviar a BIRT |
                      |               |
                      \=======+=======/
                              |
                              v
.-----------------------------+-----------------------------.
| PROCESAMIENTO BIRT                                        |
|    /===============+=================\                    |
|    |                                 |                    |
|    | Procesar solicitud              |                    |
|    |                                 |                    |
|    \===============+=================\                    |
|                    |                                      |
|                    v                                      |
|    /===============+=================\                    |
|    |                                 |                    |
|    | Consultar base de datos         |                    |
|    |                                 |                    |
|    \===============+=================\                    |
|                    |                                      |
|                    v                                      |
|    /===============+=================\                    |
|    |                                 |                    |
|    | Aplicar formato                 |                    |
|    |                                 |                    |
|    \===============+=================\                    |
|                    |                                      |
|                    v                                      |
|    /===============+=================\                    |
|    |                                 |                    |
|    | Generar documento               |                    |
|    |                                 |                    |
|    \===============+=================\                    |
'-----------------------+---------------------------------- '
                        |
                        v
                /=======+=======\
                |               |
                |    FORMATO    |
                |               |
                \=======+=======/
                        |
      .-----------------.+.-----------------.
      |                 |                   |
      v                 v                   v
/=====+======\  /=======+========\  /=======+=======\
|            |  |                |  |               |
| [📄] PDF   |  | [📊] EXCEL     |  | [🌐] HTML     |
|            |  |                |  |               |
\=====+======/  \=======+========/  \=======+=======/
      |                 |                   |
      '-----------------+-----------------. |
                        |                | |
                        v                | |
                /=======+=======\        | |
                |               |        | |
                | Entregar      +--------+-'
                | documento     |
                |               |
                \=======+=======/
                        |
                        v
                /=======+=======\
                |               |
                | *** FIN ***   |
                |   REPORTE     |
                |               |
                \===============/
```

Este diagrama ASCII mejorado para la generación de reportes incorpora:

1. **Iconos simbólicos**: 
   - [📅] para reporte Diario
   - [👤] para reporte Por Operario
   - [🏢] para reporte Por Área
   - [📊] para reporte Mensual
   - [📄] para formato PDF
   - [📊] para formato Excel
   - [🌐] para formato HTML

2. **Agrupación lógica**: Sección claramente delimitada para el "PROCESAMIENTO BIRT".

3. **Estructura mejorada**: Mejor visualización de las bifurcaciones y flujos alternativos.

4. **Consistencia visual**: Uso de caracteres especiales para delimitar claramente cada componente.

5. **Formato estandarizado**: Representación uniforme de los diferentes tipos de cajas y conectores.

Este diagrama mantiene la compatibilidad con texto plano mientras refleja fielmente la estructura y lógica del diagrama visual, facilitando la comprensión del proceso de generación de reportes en entornos donde solo se puede usar ASCII. 