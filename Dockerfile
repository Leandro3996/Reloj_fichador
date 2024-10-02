# Usa una imagen base de Python
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para MySQL
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos y luego instálalos
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
# COPY . /app/

# Exponer el puerto que estás usando
EXPOSE 58000

# Comando para correr gunicorn en el puerto especificado
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:58000", "mantenedor.wsgi:application"]
