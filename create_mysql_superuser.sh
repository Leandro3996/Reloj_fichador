#!/bin/bash

# Esperar a que la base de datos esté disponible
echo "Esperando a que la base de datos esté disponible..."
./wait-for-it.sh db:3306 -t 120

# Crear el usuario sistemas con todos los privilegios
echo "Creando usuario superusuario 'sistemas'..."
mysql -h db -u root -pS1st3mas.1999 <<EOF
-- Crear el usuario 'sistemas' si no existe
CREATE USER IF NOT EXISTS 'sistemas'@'%' IDENTIFIED BY 'S1st3mas2024!';

-- Otorgar todos los privilegios para todas las bases de datos
GRANT ALL PRIVILEGES ON *.* TO 'sistemas'@'%' WITH GRANT OPTION;

-- Otorgar privilegios específicos para administración de variables de sistema
GRANT SYSTEM_VARIABLES_ADMIN, SESSION_VARIABLES_ADMIN ON *.* TO 'sistemas'@'%';

-- Aplicar los cambios
FLUSH PRIVILEGES;
EOF

if [ $? -eq 0 ]; then
    echo "✅ Usuario 'sistemas' creado exitosamente con todos los privilegios"
else
    echo "❌ Error al crear el usuario 'sistemas'"
    exit 1
fi 