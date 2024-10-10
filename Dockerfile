# Usa una imagen base de Python
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para MySQL y WeasyPrint
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libpango1.0-0 \
    libcairo2 \
    gobject-introspection \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libpangocairo-1.0-0 \           
    fonts-liberation2 \             
    libpangoft2-1.0-0 \             
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos y luego instálalos
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . /app/

# Otorga permisos de ejecución al script wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Exponer el puerto que estás usando
EXPOSE 58000

# Comando para correr gunicorn en el puerto especificado
CMD ["/app/wait-for-it.sh", "db:3306", "--", "gunicorn", "--workers", "3", "--bind", "0.0.0.0:58000", "mantenedor.wsgi:application"]
