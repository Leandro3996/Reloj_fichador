# Usa una imagen base de Python
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    nano net-tools \
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
    libpangoft2-1.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Configurar locale en español
RUN echo "es_ES.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen es_ES.UTF-8 && \
    update-locale LANG=es_ES.UTF-8 LANGUAGE=es_ES:es LC_ALL=es_ES.UTF-8

# Variables de entorno para locales
ENV LANG=es_ES.UTF-8 \
    LANGUAGE=es_ES:es \
    LC_ALL=es_ES.UTF-8

# Verificar que el locale se ha generado correctamente
RUN locale -a && echo "Locale configurado correctamente."

# Establece el directorio de trabajo
WORKDIR /app

# Copiar archivos de requerimientos e instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . /app/

# Otorga permisos de ejecución al script wait-for-it.sh si existe
RUN chmod +x /app/wait-for-it.sh || true

# Asegurar que existan las carpetas necesarias
RUN mkdir -p /app/media /app/staticfiles && chmod -R 755 /app/staticfiles /app/media

# Exponer el puerto usado
EXPOSE 58000

# Definir el número de workers como variable de entorno
ENV GUNICORN_WORKERS=3

# Comando de ejecución
CMD ["/app/wait-for-it.sh", "db:3306", "--", "gunicorn", "--workers", "3", "--bind", "0.0.0.0:58000", "mantenedor.wsgi:application"]
