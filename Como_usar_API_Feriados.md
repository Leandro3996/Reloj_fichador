La página que compartiste muestra un ejemplo directo. La forma más sencilla de consumir esta API en Python es usando la biblioteca requests.

1. Instala la biblioteca requests

Si aún no la tienes, abre tu terminal y ejecuta:
Bash

pip install requests

2. Código de ejemplo en Python

Aquí tienes un script completo para obtener y mostrar los feriados de un año específico (por ejemplo, 2024).
Python

import requests

# Define el año que quieres consultar
anio_consulta = 2024

# Esta es la URL base de la API para los feriados
# Le agregamos el año que queremos consultar
url_api = f"https://api.argentinadatos.com/v1/feriados/{anio_consulta}"

try:
    # 1. Hacemos la solicitud GET a la API
    respuesta = requests.get(url_api)

    # 2. Verificamos si la solicitud fue exitosa (código 200)
    if respuesta.status_code == 200:
        
        # 3. Convertimos la respuesta a formato JSON (una lista de feriados)
        feriados = respuesta.json()
        
        print(f"--- Feriados para el año {anio_consulta} ---")
        
        # 4. Recorremos la lista y mostramos los datos
        for feriado in feriados:
            print(f"Fecha: {feriado['fecha']}")
            print(f"Nombre: {feriado['nombre']}")
            print(f"Tipo: {feriado['tipo']}")
            print("-" * 20) # Separador
            
    else:
        print(f"Error al consultar la API: Código {respuesta.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Ocurrió un error en la conexión: {e}")

Explicación del código:

    Importar requests: Trae la biblioteca que nos permite hacer solicitudes HTTP.

    Definir la URL: Creamos la URL completa. La documentación indica que el endpoint es /v1/feriados/{año}. Reemplazamos {año} por el año que desees.

    Hacer la solicitud: requests.get(url_api) envía la petición a la API.

    Verificar el estado: respuesta.status_code == 200 comprueba que todo haya salido bien.

    Obtener el JSON: respuesta.json() decodifica la respuesta (que viene en formato JSON) y la convierte en una lista de diccionarios de Python.

    Recorrer los datos: Simplemente iteramos sobre la lista e imprimimos los valores de cada feriado usando sus claves (fecha, nombre, tipo), tal como lo indica la documentación.