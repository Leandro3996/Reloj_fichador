# Diagrama de Flujo ASCII Mejorado - Proceso de Fichaje

## 1. Proceso Principal de Fichaje

```
                        /====================\
                        |                    |
                        |    *** INICIO ***  |
                        |  Pantalla Fichaje  |
                        |                    |
                        \=========+==========/
                                  |
                                  v
                        /=========+=========\
                        |                   |
                        |  Seleccionar tipo |
                        |   de movimiento   |
                        |                   |
                        \=========+=========/
                                  |
        .-------------------.-----+-------.-----------------.
        |                   |             |                 |
        v                   v             v                 v
+===============+  +===============+  +===============+  +===============+
|               |  |               |  |               |  |               |
|   ENTRADA     |  | SALIDA TRANS. |  | ENTRADA TRANS.|  |    SALIDA     |
|   (Tecla Q)   |  |   (Tecla V)   |  |   (Tecla M)   |  |   (Tecla P)   |
|               |  |               |  |               |  |               |
+======+========+  +======+========+  +======+========+  +======+========+
       |                  |                  |                  |
       '-----.------------'---.-------------'--------.---------'
             |                |                      |
             +----------------+----------------------+
                              |
                              v
                      /=======+=======\
                      |               |
                      |  Ingresar DNI |
                      |               |
                      \=======+=======/
                              |
                              v
                      /=======+=======\
                      |               |
                      | Enviar        |
                      | solicitud     |
                      |               |
                      \=======+=======/
                              |
                              v
              .---------------+-------------------.
              |     VALIDACIONES                  |
              |     /==========+============\     |
              |     |                       |     |
              +---->| ¿Operario existe?     +-----+
              |     |                       |     |
              |     \==========+============/     |
              |                |                  |
              |                |                  |
              |                | SI               | NO
              |                v                  v
              |     /==========+============\   /=+==============\
              |     |                       |   |                |
              |  +--| ¿Secuencia es válida? |   |  [!] ERROR     |
              |  |  |                       |   |  Operario no   |
              |  |  \==========+============/   |  encontrado    |
              |  |             |                |                |
              |  | SI          | NO             \=+==============/ 
              |  |             |                  |               
              |  v             v                  |               
              |/===+=========\ /====+===========\ |        
              ||             | |                | |        
              || [✓] REGISTRO| | [!] ADVERTENCIA| |        
              || Guardar mov.| | Mostrar alerta | |        
              ||             | |                | |        
              |\===+=========/  \====+==========/  |        
              |    |                 |            |        
              |    |                 v            |        
              |    |       /=========+=========\  |        
              |    |       |                   |  |        
              |    |       | ¿Confirmar de     |  |        
              |    |       | todos modos?      |  |        
              |    |       |                   |  |        
              |    |       \=========+=========/  |        
              |    |                 |            |        
              |    |       .---------+---------.  |        
              |    |       |                   |  |        
              |    |       | SI                | NO        
              |    |       v                   v           
              |    |/======+======\   /=======+======\     
              |    ||             |   |              |     
              |    || [!] OVERRIDE|   | [X] CANCELAR |     
              |    || Registrar   |   | Operación    |     
              |    || con excep.  |   | abortada     |     
              |    ||             |   |              |     
              |    |\======+======/   \=======+======/     
              |    |       |                  |            
              |    v       v                  |            
              |/===+================+====\    |            
              ||                        |     |            
              || [✓] ÉXITO              |     |            
              || Confirmación operación |     |            
              ||                        |     |            
              |\===+=====================/     |            
                   |                           |            
                   \-------------+-------------/
                                 |
                                 v
                        /========+=========\
                        |                  |
                        |     ** FIN **    |
                        |  Volver a inicio |
                        |                  |
                        \==================/
```

Esta versión mejorada del diagrama ASCII incorpora:

1. **Mejor delimitación visual**: Uso de caracteres dobles para los contornos de inicio/fin y caracteres especiales para las cajas.
2. **Agrupación lógica**: Sección claramente delimitada para "VALIDACIONES".
3. **Símbolos distintivos**: 
   - [✓] para operaciones exitosas
   - [!] para advertencias/excepciones 
   - [X] para cancelaciones/errores
4. **Consistencia estructural**: Mantiene la misma estructura y flujo del diagrama visual.
5. **Énfasis en decisiones**: Mejor representación visual de las decisiones SI/NO.
6. **Conectores mejorados**: Líneas más claras para seguir el flujo del proceso.

El diagrama mantiene todas las ventajas de ASCII (compatibilidad universal con editores de texto) mientras mejora significativamente la claridad visual y correspondencia con el diagrama Mermaid. 