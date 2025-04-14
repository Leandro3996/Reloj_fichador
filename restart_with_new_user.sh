#!/bin/bash

echo "🔄 Reiniciando el sistema Reloj Fichador con el nuevo usuario 'sistemas'"
echo "===================================================================="

# Detener todos los contenedores
echo "⏹️ Deteniendo todos los contenedores..."
docker-compose down

# Eliminar volúmenes de MySQL si es necesario (descomentar si se quiere empezar desde cero)
# echo "🗑️ Eliminando volúmenes de MySQL..."
# rm -rf mysql_data/*

# Iniciar solo el contenedor de la base de datos
echo "🚀 Iniciando contenedor de base de datos..."
docker-compose up -d db

# Esperar a que la base de datos esté disponible
echo "⏳ Esperando a que la base de datos esté disponible..."
./wait-for-it.sh localhost:53306 -t 120

# Ejecutar script para crear usuario superusuario
echo "👤 Creando usuario superusuario 'sistemas'..."
./create_mysql_superuser.sh

# Iniciar el resto de los contenedores
echo "🚀 Iniciando el resto de los contenedores..."
docker-compose up -d

# Mostrar el estado de los contenedores
echo "📊 Estado actual de los contenedores:"
docker-compose ps

echo "✅ Sistema reiniciado con el nuevo usuario 'sistemas'"
echo "Verifica los logs con 'docker-compose logs -f' para asegurarte de que todo funciona correctamente." 