# Diagramas de Flujo en ASCII Art - Sistema Reloj Fichador

> [!info] Navegación
> **Índice Principal:** [[Indice_Reloj_Fichador|Índice del Sistema]]  
> **Contexto:** [[contexto|Contexto del Proyecto]]  
> **Otras Visualizaciones:** [[Diagrama_de_flujo_Fichador|Mermaid]] | [[Diagrama_de_flujo_Visual|Visual]]  
> **Arquitectura:** [[estructura|Estructura del Proyecto]]

## 1. Proceso Principal de Fichaje

```
                        +-------------------+
                        |                   |
                        |       INICIO      |
                        |  Pantalla Fichaje |
                        |                   |
                        +--------+----------+
                                 |
                                 v
                        +--------+----------+
                        |                   |
                        |  Seleccionar tipo |
                        |   de movimiento   |
                        |                   |
                        +--------+----------+
                                 |
           +-------------------+-+------------------+------------------+
           |                   |                    |                  |
           v                   v                    v                  v
+----------+---------+ +-------+---------+ +--------+--------+ +-------+---------+
|                    | |                 | |                  | |                 |
|      ENTRADA       | | SALIDA TRANSIT. | | ENTRADA TRANSIT. | |      SALIDA     |
|      (Tecla Q)     | |    (Tecla V)    | |    (Tecla M)     | |    (Tecla P)    |
|                    | |                 | |                  | |                 |
+----------+---------+ +-------+---------+ +--------+--------+ +-------+---------+
           |                   |                    |                  |
           +-------------------+--------------------+------------------+
                                 |
                                 v
                        +--------+----------+
                        |                   |
                        |    Ingresar DNI   |
                        |                   |
                        +--------+----------+
                                 |
                                 v
                        +--------+----------+
                        |                   |
                        |  Enviar solicitud |
                        |                   |
                        +--------+----------+
                                 |
                                 v
                        +--------+----------+
                        |                   |
               +------->+ ¿Operario existe? +------+
               |        |                   |      |
               |        +--------+----------+      |
               |                 |                 |
               |                 | SI              | NO
               |                 v                 v
               |        +--------+----------+    +-+----------------+
               |        |                   |    |                  |
               |     +--|  ¿Secuencia es    |    |      ERROR       |
               |     |  |     válida?       |    | Operario no      |
               |     |  |                   |    | encontrado       |
               |     |  +--------+----------+    |                  |
               |     v                  |        +-+----------------+
               |     SI                 |               |
               |     |                  |ERROR          |
               |     v                  |               v
               |  +--+-----------+---+  |      +--------+---------+
               |  |                  |  |      |                  |
               |  | REGISTRO         |  |      | ADVERTENCIA      |
               |  | Guardar movim.   |  |      | Mostrar alerta   |
               |  |                  |  |      | Fin no puede     |
               |  |                  |  |      | continuar.       |
               |  |                  |  |      |                  |
               |  +--+---------------+  |      +--------+---------+
               |     |                  |         
               |     |                  v         
               |     |      +--------+---------+
               |     |      |                  |
               |     |      | ¿Confirmar de    |
               |     |      |  todos modos?    |
               |     |      |                  |
               |     |      +--------+---------+
               |     |               |
               |     |              +-------------++--------------+
               |     |              |                             |
               |     |              | SI                          | NO
               |     |              v                             v
               |     |     +--------+---------+         +---------+--------+
               |     |     |                  |         |                  |
               |     |     | OVERRIDE         |         | CANCELAR         |
               |     |     | Registrar con    |         | Operación        |
               |     |     | excepción/       |         | abortada         |
               |     |     |inconsistencia.   |         |                  |
               |     |     +--------+---------+         +---------+--------+
               |     |              |                             |
               |     v              v                             |
            +--+-----+--------------+--+                          |
            |                          |                          |
            | ÉXITO                    |                          |
            | Confirmar operación      |                          |
            |                          |                          |
            +----+---------------------+                          |
                 |                                                |
                 +--------------------------------+---------------+
                                                  |
                                                  v
                                         +--------+---------+
                                         |                  |
                                         |       FIN        |
                                         | Volver al inicio |
                                         |                  |
                                         +------------------+
```

## 2. Validación de Inconsistencias

```
        +---------+----------+                     
        |¿Tiene un registro  |          
        |de salida el día de |
        |ayer?               |              
        |                    |            
        +------+------+------+                             
               |         |
               |         |NO                           
               |         |             
               |         v 
               |        +--------+---------+
            SI |        |   ¿Es su primer  |
               |        |     registro?    |
               |        +------------------+             
               |          |              | 
               |          |              |NO
               |          |              |
               |          |              v                    
               |          |          +-------------------+
               |          |          |                   |
               |          |          | Inconsistencia    |
               |       SI |          | Se aplica lógica  |
               |          |          | de inconsistencia |
               |          |          |                   |
               |          |          +-------------------+
               |          |
               |          |
               |          |                               SALIDA TRANSITORIA
               v          v
        +-----------------+                              +-----------------+
        |                 |                              |                 |
        |     Entrada     |                              | Salida Transit. |
        |                 |                              |                 |
        +-------+---------+                              +-------+---------+
                |                                                |
                v                                                v
        +-------+---------+                              +-------+---------+
        |                 |                              |                 |
        | ¿Ya tiene       |                              | ¿Tiene entrada  |
        |  entrada?       |                              |  hoy?           |
        |                 |                              |                 |
        +--+------+-------+                              +--+------+-------+
           |      |                                         |      |
           |      |                                         |      |
        SI |      | NO                                   NO |      | SI
           |      |                                         |      |
           v      v                                         v      v
      +----+--+ +-+-----+                               +---+---+ +--------+
      |       | |       |                               |       | |        |
      | INCON | | CONS  |                               | INCON | | ¿Ya tiene  
      | SIST  | | SIST  |                               | SIST  | | salida  
      |       | |       |                               |       | | trans.? 
      +-------+ +-------+                               +-------+ +--+---+-+
                                                                    |    |
                                                                 SI |    | NO
                                                                    |    |
                                                                    v    v
                                                               +----+-+ +---+--+
                                                               |      | |      |
                                                               | INCON| | CONS |
                                                               | SIST | | SIST |
                                                               |      | |      |
                                                               +------+ +------+


             ENTRADA TRANSITORIA                                SALIDA

        +-----------------+                              +-----------------+
        |                 |                              |                 |
        | Entrada Transit.|                              |     Salida      |
        |                 |                              |                 |
        +-------+---------+                              +-------+---------+
                |                                                |
                v                                                v
        +-------+---------+                              +-------+---------+
        |                 |                              |                 |
        | ¿Tiene entrada  |                              | ¿Tiene entrada  |
        |  hoy?           |                              |  hoy?           |
        |                 |                              |                 |
        +--+------+-------+                              +--+------+-------+
           |      |                                         |      |
           |      |                                         |      |
        NO |      | SI                                   NO |      | SI
           |      |                                         |      |
           v      v                                         v      v
      +----+--+ +-+--------+                            +---+---+ +--------+
      |       | |          |                            |       | |¿Movim. |
      | INCON | | ¿Tiene   |                            | INCON | |transit.|
      | SIST  | | salida   |                            | SIST  | |pend.?  |
      |       | | trans.?  |                            |       | |        |
      +-------+ +--+-----+-+                            +-------+ +--+---+-+
                   |     |                                         |   |
                NO |     | SI                                   SI |   | NO
                   |     |                                         |   |
                   v     v                                         v   v
              +----+-+ +-+----+                               +----+-+ +---+--+
              |      | |      |                               |      | |      |
              | INCON| | CONS |                               | INCON| | CONS |
              | SIST | | SIST |                               | SIST | | SIST |
              |      | |      |                               |      | |      |
              +------+ +------+                               +------+ +------+
```

## 3. Cálculo de Horas Trabajadas

```
+--------------------+
|                    |
|   INICIO CÁLCULO   |
|                    |
+---------+----------+
          |
          v
+---------+----------+
|                    |
| Obtener registros  |
| del día            |
|                    |
+---------+----------+
          |
          v
+---------+----------+
|                    |    NO      +-------------------+
| ¿Registros         +----------->+                   |
|  completos?        |            | Sin calcular      |
|                    |            |                   |
+--------+-----------+            +--------+----------+
         |                                 |
         | SI                              |
         v                                 |
+--------+-----------+                     |
|                    |                     |
| Agrupar pares      |                     |
| entrada-salida     |                     |
|                    |                     |
+--------+-----------+                     |
         |                                 |
         v                                 |
+--------+-----------+                     |
|                    |                     |
| Por cada par       |                     |
| entrada-salida     |                     |
|                    |                     |
+--------+-----------+                     |
         |                                 |
         v                                 |
+--------+-----------+                     |
|                    |                     |
| Redondear entrada  |                     |
| hacia arriba       |                     |
|                    |                     |
+--------+-----------+                     |
         |                                 |
         v                                 |
+--------+-----------+                     |
|                    |    NO    +----------+---------+
| ¿Duración >= 8h?   +---------->                    |
|                    |          | Mantener hora      |
+--------+-----------+          | exacta de salida   |
         |                      |                    |
         | SI                   +---------+----------+
         v                                |
+--------+-----------+                    |
|                    |                    |
| Aplicar regla      |                    |
| especial           |                    |
|                    |                    |
+--------+-----------+                    |
         |                                |
         +----------------+---------------+
                          |
                          v
                +---------+----------+
                |                    |
                | Calcular horas     |
                | por franjas        |
                |                    |
                +---------+----------+
                          |
          +---------------+---------------+
          |                               |
          v                               v
+---------+-----------+        +----------+---------+
|                    |        |                     |
| HORAS NORMALES     |        | HORAS NOCTURNAS     |
| (06:00 - 20:00)    |        | (20:00 - 06:00)     |
|                    |        |                     |
+---------+----------+        +---------+-----------+
          |                             |
          +-------------+---------------+
                        |
                        v
              +---------+----------+
              |                    |    SI    +-------------------+
              | ¿Es feriado o      +---------->                   |
              |  domingo?          |          | HORAS FERIADO     |
              |                    |          |                   |
              +--------+-----------+          +---------+---------+
                       |                                |
                       | NO                             |
                       v                                |
              +--------+-----------+                    |
              |                    |                    |
              | Mantener tipo      |                    |
              | de horas           |                    |
              |                    |                    |
              +--------+-----------+                    |
                       |                                |
                       +---------------+----------------+
                                       |
                                       v
                             +---------+----------+
                             |                    |    SI    +-------------------+
                             | ¿Excede jornada    +---------->                   |
                             |  normal?           |          | Calcular HORAS    |
                             |                    |          | EXTRA             |
                             +--------+-----------+          +---------+---------+
                                      |                                |
                                      | NO                             |
                                      v                                |
                             +--------+-----------+                    |
                             |                    |                    |
                             | Solo horas         |                    |
                             | normales/nocturnas |                    |
                             |                    |                    |
                             +--------+-----------+                    |
                                      |                                |
                                      +----------------+---------------+
                                                       |
                                                       v
                                             +---------+----------+
                                             |                    |
                                             | Guardar resultados |
                                             | en base de datos   |
                                             |                    |
                                             +---------+----------+
                                                       |
                                                       v
                                             +---------+----------+
                                             |                    |
                                             |    FIN CÁLCULO     |
                                             |                    |
                                             +--------------------+
```

## 4. Generación de Reportes

```
                              +--------------+
                              |              |
                              | INICIO       |
                              | REPORTE      |
                              |              |
                              +------+-------+
                                     |
                                     v
                              +------+-------+
                              |              |
                              | Seleccionar  |
                              | tipo reporte |
                              |              |
                              +------+-------+
                                     |
                +--------------------+----------------------+
                |                    |                      |                    
                v                    v                      v                    v
        +-------+------+    +-------+------+       +-------+------+     +-------+------+
        |              |    |              |       |              |     |              |
        |   DIARIO     |    | POR OPERARIO |       |   POR ÁREA   |     |   MENSUAL    |
        |              |    |              |       |              |     |              |
        +-------+------+    +-------+------+       +-------+------+     +-------+------+
                |                   |                      |                    |
                +-------------------+----------------------+--------------------+
                                    |
                                    v
                             +------+-------+
                             |              |
                             | Configurar   |
                             | parámetros   |
                             |              |
                             +------+-------+
                                    |
                                    v
                             +------+-------+
                             |              |
                             | Enviar a     |
                             | BIRT         |
                             |              |
                             +------+-------+
                                    |
                                    v
                             +------+-------+
                             |              |
                             | Procesar     |
                             | solicitud    |
                             |              |
                             +------+-------+
                                    |
                                    v
                             +------+-------+
                             |              |
                             | Consultar    |
                             | base datos   |
                             |              |
                             +------+-------+
                                    |
                                    v
                             +------+-------+
                             |              |
                             | Aplicar      |
                             | formato      |
                             |              |
                             +------+-------+
                                    |
                                    v
                             +------+-------+
                             |              |
                             | Generar      |
                             | documento    |
                             |              |
                             +------+-------+
                                    |
                     +--------------|---------------+
                     |              |               |
                     v              v               v
              +------+-------+ +----+-----+  +------+-------+
              |              | |          |  |              |
              |     PDF      | |  EXCEL   |  |    HTML      |
              |              | |          |  |              |
              +------+-------+ +----+-----+  +------+-------+
                     |              |               |
                     +--------------+---------------+
                                    |
                                    v
                             +------+-------+
                             |              |
                             | Entregar     |
                             | documento    |
                             |              |
                             +------+-------+
                                    |
                                    v
                             +------+-------+
                             |              |
                             | FIN REPORTE  |
                             |              |
                             +--------------+
```

## 5. Tareas Programadas Automatizadas

```
    +----------------------+
    |                      |
    |    INICIO CELERY     |
    |                      |
    +-----------+----------+
                |
                v
    +-----------+----------+
    |                      |
    |   Iniciar servicios  |
    |   Celery             |
    |                      |
    +-----------+----------+
                |
                v
    +-----------+----------+
    |                      |
    |  Cargar tareas       |
    |  programadas         |
    |                      |
    +-----------+----------+
                |
      +---------+--------------+--------------+
      |                        |              |
      v                        v              v                        v
+-----+------+        +--------+-----+   +----+-------+       +-------+-----+
|            |        |              |   |            |       |             |
| ASISTENCIA |        | VERIFICACIÓN |   |  CÁLCULO   |       |   BACKUP    |
|            |        |              |   |            |       |             |
+-----+------+        +--------+-----+   +----+-------+       +-------+-----+
      |                        |              |                      |
      v                        v              v                      v
+-----+------+        +--------+-----+   +----+-------+       +------+------+
|            | NO     |              |NO |            |NO     |             |NO
| ¿Es        +--+     | ¿Es hora     +-->+ ¿Es fin de +--+    | ¿Han pasado +--+
| medianoche?|  |     | programada?  |   | jornada?   |  |    | 2 horas?    |  |
|            |  |     |              |   |            |  |    |             |  |
+-----+------+  |     +--------+-----+   +----+-------+  |    +------+------+  |
      |         |              |              |          |           |         |
 SI   |         |      SI      |       SI     |          |    SI     |         |
      v         |              v              v          |           v         |
+-----+------+  |     +--------+-----+   +----+-------+  |    +------+------+  |
|            |  |     |              |   |            |  |    |             |  |
| CREAR      |  |     | VERIFICAR    |   | CALCULAR   |  |    | GENERAR     |  |
| registros  |  |     | asistencia   |   | horas      |  |    | backup      |  |
| asistencia |  |     |              |   |            |  |    |             |  |
+-----+------+  |     +--------+-----+   +----+-------+  |    +------+------+  |
      |         |              |              |          |           |         |
      |         |              |              |          |           |         |
      |         |              |              |          |           |         |
      |         |              v              |          |           |         |
      +---------+-----> +------+------+ <-----+----------+-----------+         |
                        |             |                                        |
                        | REGISTRAR   |                                        |
                        | en log      |                                        |
                        |             |                                        |
                        +------+------+                                        |
                               |                                               |
                               v                                               |
                        +------+------+                                        |
                        |             |                                        |
                        | CONTINUAR   | <-------------------------------------+
                        | ciclo       |
                        |             |
                        +------+------+
                               |
                               v
                        +------+------+
                        |             |
                        | REINICIAR   |
                        | ciclo       |
                        |             |
                        +-------------+
```

## Leyenda de Símbolos ASCII

```
+-------+    Inicio/Fin           +-------+    Proceso normal       +-------+    Decisión
|       |                         |       |                         |       |
| TEXTO |                         | TEXTO |                         | TEXTO |
|       |                         |       |                         |       |
+-------+                         +-------+                         +---+---+
                                                                        |
                                                                   SI   |    NO
                                                                       / \
                                                                      /   \

Flechas de flujo:
   |        Dirección de flujo vertical
   v     
   
   --->     Dirección de flujo horizontal

   +---+    Conexión entre elementos
       |
       v
```

## Notas sobre los Diagramas ASCII

1. **Simplificación** - Se han simplificado algunos flujos para adaptarlos a las limitaciones del ASCII art.

2. **Abreviaturas** - Se utilizan abreviaturas como "INCON" (Inconsistencia), "CONS" (Consistente), 
   "Transit." (Transitoria) para mantener las líneas en un ancho manejable.

3. **Conectores** - Se utilizan cruces y líneas para mostrar la conexión entre diferentes elementos.

4. **Alineación** - Se ha intentado mantener la alineación de elementos relacionados para facilitar
   la lectura del diagrama.

5. **Énfasis** - Algunos elementos críticos se destacan usando cajas completas, mientras que elementos
   informativos usan menos caracteres para reducir el "ruido visual".

Estos diagramas ASCII proporcionan una alternativa accesible a los diagramas Mermaid, permitiendo
visualizar la lógica del sistema incluso en entornos donde no se admiten gráficos avanzados. 

---

> [!tip] Documentos Relacionados
> - Para entender el contexto y reglas de negocio, consulta [[contexto|Contexto del Proyecto]]
> - Para ver los diagramas en formato Mermaid, ve a [[Diagrama_de_flujo_Fichador|Diagramas Mermaid]]
> - Para una visualización avanzada con colores e iconos, revisa [[Diagrama_de_flujo_Visual|Diagramas Visuales]]
> - Para entender la estructura técnica, consulta [[estructura|Arquitectura del Proyecto]]
> - Regresa al [[Indice_Reloj_Fichador|Índice Principal]] 