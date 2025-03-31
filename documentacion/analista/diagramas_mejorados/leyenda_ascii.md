# Leyenda para Diagramas ASCII Mejorados

## Simbología en Diagramas ASCII

```
/==============\         /==============\         /==============\
|              |         |              |         |              |
| Inicio/Fin   |         | Proceso      |         | Decisión     |
|              |         |              |         |              |
\==============/         \==============/         \======+=======/
                                                        |
                                                   .----+----.
                                                   |         |
                                                  SI|        NO|

/==============\         /==============\         /==============\
|              |         |              |         |              |
| Acción       |         |   Éxito      |         |   Error      |
| especial     |         | [✓]          |         | [!]          |
|              |         |              |         |              |
\==============/         \==============/         \==============/


.-------------.         |                    ----->
|             |         |                          
| Agrupación  |         | Flujo vertical      Flujo horizontal
| lógica      |         |                          
'-------------'         v                    <-----
```

## Símbolos Especiales Utilizados

| Símbolo | Significado                  | Contexto de uso                     |
|---------|------------------------------|-------------------------------------|
| [✓]     | Éxito / Confirmación         | Operaciones completadas con éxito   |
| [!]     | Advertencia / Excepción      | Situaciones que requieren atención  |
| [X]     | Error / Cancelación          | Operaciones fallidas o canceladas   |
| [↑]     | Redondeo hacia arriba        | Ajuste de tiempo hacia hora superior|
| [⏳]    | Espera / Pendiente           | Estados de espera en el flujo       |
| [N]     | Horas normales               | Clasificación de horas trabajadas   |
| [♦]     | Horas nocturnas              | Clasificación de horas trabajadas   |
| [F]     | Horas feriado                | Clasificación de horas trabajadas   |
| [E]     | Horas extra                  | Clasificación de horas trabajadas   |
| [1],[2] | Numeración de tareas         | Identificación de tareas específicas|
| [📅]    | Reporte Diario               | Tipo de reporte                     |
| [👤]    | Reporte Por Operario         | Tipo de reporte                     |
| [🏢]    | Reporte Por Área             | Tipo de reporte                     |
| [📊]    | Reporte Mensual / Excel      | Tipo de reporte / formato           |
| [📄]    | Formato PDF                  | Formato de documento                |
| [🌐]    | Formato HTML                 | Formato de documento                |

## Técnicas de Representación Visual en ASCII

1. **Delimitación**: Uso de caracteres `/ \ | - =` para crear cajas y contenedores.
2. **Agrupación**: Secciones delimitadas con `.------.` para indicar grupos lógicos.
3. **Énfasis**: Texto dentro de `***` para destacar elementos importantes como inicio/fin.
4. **Conectores**: Líneas verticales `|` y horizontales `-` para mostrar el flujo de proceso.
5. **Decisiones**: Representación explícita de SI/NO en bifurcaciones para facilitar seguimiento.
6. **Simbolismo**: Uso de caracteres Unicode para representar iconos que mejoran la interpretación.

## Notas sobre Compatibilidad

Estos diagramas ASCII han sido diseñados para:

1. Ser compatibles con cualquier editor de texto, terminal o entorno que admita texto plano.
2. Mantener legibilidad incluso si algunos símbolos Unicode no se muestran correctamente.
3. Proporcionar una alternativa accesible a diagramas gráficos más complejos.
4. Conservar la estructura y organización visual del diagrama Mermaid original.

Si algún símbolo Unicode no se muestra correctamente, se recomienda consultar la tabla de símbolos para entender su significado por el contexto.

---

*Esta leyenda se aplica a todos los diagramas ASCII mejorados del Sistema Reloj Fichador.* 