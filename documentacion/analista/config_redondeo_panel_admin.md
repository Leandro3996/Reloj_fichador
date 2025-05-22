# Configuración de Redondeo de Entrada y Salida

## ¿Qué es?

Permite ajustar desde el panel de administración los límites de redondeo para las horas de entrada y salida de los operarios.

---

## Modelos involucrados

- **ConfiguracionRedondeo**  
  Permite definir los minutos para redondear la hora de entrada:
  - `minutos_redondeo_baja`: Minutos máximos para redondear hacia la hora en punto (por defecto 15).
  - `minutos_redondeo_media`: Minutos máximos para redondear a la media hora (por defecto 45).

- **ConfiguracionRedondeoSalida**  
  Permite definir los minutos para redondear la hora de salida hacia abajo:
  - `minutos_redondeo_salida`: Minutos a los que se redondea la salida hacia abajo (por defecto 0).

---

## ¿Cómo funciona?

- **Entrada:**  
  El sistema toma la hora fichada y la redondea según los valores configurados en `ConfiguracionRedondeo`:
  - Si los minutos son menores a `minutos_redondeo_baja`, redondea a la hora en punto.
  - Si los minutos son menores a `minutos_redondeo_media`, redondea a la media hora.
  - Si los minutos son mayores o iguales a `minutos_redondeo_media`, redondea a la siguiente hora.

- **Salida:**  
  El sistema toma la hora fichada y la redondea hacia abajo a la hora anterior más los minutos configurados en `ConfiguracionRedondeoSalida`.

---

## ¿Dónde se configura?

Desde el panel de administración de Django:
- Ingresa como superusuario.
- Busca las secciones **Configuración de Redondeo** y **Configuración de Redondeo de Salida**.
- Ajusta los valores según la política de la empresa.

---

## Notas

- Si no existe configuración, el sistema usará los valores por defecto (15, 45 para entrada y 0 para salida).
- Solo debe haber una instancia de cada configuración para que el sistema funcione correctamente.