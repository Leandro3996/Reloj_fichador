#!/bin/bash

# Script para mantener solo los 10 backups más recientes
# Uso: ./clean_backups.sh

# Colores para mensajes
VERDE='\033[0;32m'
AZUL='\033[0;34m'
ROJO='\033[0;31m'
RESET='\033[0m'

echo -e "${AZUL}Iniciando limpieza de backups antiguos...${RESET}"

# Directorio donde se almacenan los backups
BACKUP_DIR="./backups"

# Verificar que el directorio existe
if [ ! -d "$BACKUP_DIR" ]; then
    echo -e "${ROJO}¡ERROR! El directorio $BACKUP_DIR no existe${RESET}"
    exit 1
fi

# Contar archivos de backup
TOTAL_FILES=$(find "$BACKUP_DIR" -name "*.sql" -type f | wc -l)

if [ "$TOTAL_FILES" -eq 0 ]; then
    echo -e "${AZUL}No hay archivos de backup para limpiar.${RESET}"
    exit 0
fi

echo -e "${AZUL}Encontrados $TOTAL_FILES archivos de backup${RESET}"

# Si hay más de 10 archivos, eliminar los más antiguos
if [ "$TOTAL_FILES" -gt 10 ]; then
    # Calcular cuántos archivos eliminar
    FILES_TO_DELETE=$((TOTAL_FILES - 10))
    
    echo -e "${AZUL}Se eliminarán los $FILES_TO_DELETE archivos más antiguos...${RESET}"
    
    # Obtener la lista de archivos ordenados por fecha (más antiguos primero)
    mapfile -t FILES_TO_REMOVE < <(find "$BACKUP_DIR" -name "*.sql" -type f -printf '%T@ %p\n' | sort | head -n "$FILES_TO_DELETE" | cut -d' ' -f2-)
    
    # Eliminar los archivos
    for file in "${FILES_TO_REMOVE[@]}"; do
        echo -e "${ROJO}Eliminando: $(basename "$file")${RESET}"
        rm -f "$file"
    done
    
    echo -e "${VERDE}Limpieza completada. Se han eliminado $FILES_TO_DELETE archivos.${RESET}"
else
    echo -e "${VERDE}No es necesario eliminar archivos. Se mantienen todos los backups (menos de 10).${RESET}"
fi

echo -e "${VERDE}Se conservan los 10 backups más recientes.${RESET}" 