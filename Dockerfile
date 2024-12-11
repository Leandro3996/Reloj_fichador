# Usa una imagen base de Python
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para locales, MySQL y WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
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
    # Dependencias para Celery y BIRT si es necesario
    && rm -rf /var/lib/apt/lists/*

# Configurar el locale es_ES.UTF-8
RUN echo "es_ES.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen es_ES.UTF-8 && \
    update-locale LANG=es_ES.UTF-8 LANGUAGE=es_ES:es LC_ALL=es_ES.UTF-8

# Establecer las variables de entorno de locale
ENV LANG=es_ES.UTF-8 \
    LANGUAGE=es_ES:es \
    LC_ALL=es_ES.UTF-8

# Verificar que el locale se ha generado correctamente
RUN locale -a && echo "Locale configurado correctamente."

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos y luego instálalos
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . /app/

# Otorga permisos de ejecución al script wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Asegurar que Nginx pueda leer los archivos estáticos y de medios
RUN mkdir -p /app/media && chmod -R 755 /app/staticfiles /app/media

# Exponer el puerto que estás usando
EXPOSE 58000

# Comando para correr gunicorn en el puerto especificado
CMD ["/app/wait-for-it.sh", "db:3306", "--", "gunicorn", "--workers", "3", "--bind", "0.0.0.0:58000", "mantenedor.wsgi:application"]
