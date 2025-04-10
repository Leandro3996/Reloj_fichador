#!/bin/bash
# Script para verificar el estado de Celery Beat y monitorear errores relacionados con zonas horarias
# Ejecutar periódicamente para garantizar el correcto funcionamiento de las tareas programadas

# Colores para los mensajes
ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[0;33m'
RESET='\033[0m'

# Fecha actual para los logs
FECHA=$(date +"%Y-%m-%d %H:%M:%S")
ARCHIVO_LOG="logs/celery_monitor_$(date +"%Y%m%d").log"

# Asegurar que exista el directorio de logs
mkdir -p logs

echo -e "=== ${FECHA} - Verificación de Celery y zonas horarias ===" | tee -a "${ARCHIVO_LOG}"

# Verificar si el servicio celery-beat está activo
if docker-compose ps | grep celery-beat | grep "Up" > /dev/null; then
    echo -e "${VERDE}✓ Servicio celery-beat está en ejecución${RESET}" | tee -a "${ARCHIVO_LOG}"
else
    echo -e "${ROJO}✗ El servicio celery-beat NO está en ejecución${RESET}" | tee -a "${ARCHIVO_LOG}"
    
    # Verificar logs para identificar el error
    if docker-compose logs --tail=50 celery-beat | grep "MySQL backend does not support timezone-aware datetimes" > /dev/null; then
        echo -e "${AMARILLO}! Error detectado: Problema de zona horaria con MySQL backend${RESET}" | tee -a "${ARCHIVO_LOG}"
        echo -e "${AMARILLO}! Este error ocurre cuando el servicio celery-beat intenta guardar fechas con zona horaria en MySQL${RESET}" | tee -a "${ARCHIVO_LOG}"
        echo -e "${AMARILLO}! pero Django está configurado con USE_TZ=False${RESET}" | tee -a "${ARCHIVO_LOG}"
    fi
    
    # Preguntar si se desea reiniciar el servicio
    read -r -p "¿Desea reiniciar el servicio celery-beat? (s/n): " respuesta
    if [[ "$respuesta" =~ ^[Ss]$ ]]; then
        echo -e "Reiniciando celery-beat..." | tee -a "${ARCHIVO_LOG}"
        docker-compose restart celery-beat
        sleep 5
        if docker-compose ps | grep celery-beat | grep "Up" > /dev/null; then
            echo -e "${VERDE}✓ Servicio celery-beat reiniciado exitosamente${RESET}" | tee -a "${ARCHIVO_LOG}"
        else
            echo -e "${ROJO}✗ No se pudo reiniciar el servicio celery-beat${RESET}" | tee -a "${ARCHIVO_LOG}"
        fi
    fi
fi

# Verificar configuración de Celery
echo -e "\nVerificando configuración de zona horaria en Celery..." | tee -a "${ARCHIVO_LOG}"
if grep -q "app.conf.timezone" mantenedor/celery.py; then
    echo -e "${VERDE}✓ La zona horaria está explícitamente configurada en celery.py${RESET}" | tee -a "${ARCHIVO_LOG}"
else
    echo -e "${ROJO}✗ No se encontró configuración explícita de zona horaria en celery.py${RESET}" | tee -a "${ARCHIVO_LOG}"
    echo -e "${AMARILLO}! Recomendación: Agregar las siguientes líneas a mantenedor/celery.py:${RESET}" | tee -a "${ARCHIVO_LOG}"
    echo -e "${AMARILLO}! app.conf.timezone = 'America/Argentina/Buenos_Aires'${RESET}" | tee -a "${ARCHIVO_LOG}"
    echo -e "${AMARILLO}! app.conf.enable_utc = False${RESET}" | tee -a "${ARCHIVO_LOG}"
fi

# Verificar configuración de Django
echo -e "\nVerificando configuración de zona horaria en Django..." | tee -a "${ARCHIVO_LOG}"
DJANGO_USE_TZ=$(grep "USE_TZ" mantenedor/settings.py | grep -v "^#" | tail -1 | awk -F'=' '{print $2}' | tr -d ' ')
DJANGO_TIME_ZONE=$(grep "TIME_ZONE" mantenedor/settings.py | grep -v "^#" | tail -1 | awk -F'=' '{print $2}' | tr -d " '" | tr -d '"')

echo -e "• Django TIME_ZONE = ${DJANGO_TIME_ZONE}" | tee -a "${ARCHIVO_LOG}"
echo -e "• Django USE_TZ = ${DJANGO_USE_TZ}" | tee -a "${ARCHIVO_LOG}"

if [[ "${DJANGO_USE_TZ}" == "False" ]]; then
    echo -e "${AMARILLO}! Advertencia: USE_TZ está configurado como False${RESET}" | tee -a "${ARCHIVO_LOG}"
    echo -e "${AMARILLO}! Esto puede causar problemas con Celery y django-celery-beat${RESET}" | tee -a "${ARCHIVO_LOG}"
    echo -e "${AMARILLO}! Se recomienda cambiar a USE_TZ = True tras realizar pruebas exhaustivas${RESET}" | tee -a "${ARCHIVO_LOG}"
fi

# Verificar última ejecución de tareas programadas
echo -e "\nVerificando última ejecución de tareas programadas..." | tee -a "${ARCHIVO_LOG}"
ULTIMA_EJECUCION=$(docker-compose logs --tail=100 celery | grep "Task apps.reloj_fichador.tasks" | grep "succeeded" | tail -1)

if [[ -n "${ULTIMA_EJECUCION}" ]]; then
    FECHA_ULTIMA_EJECUCION=$(echo "${ULTIMA_EJECUCION}" | awk '{print $2}')
    TAREA=$(echo "${ULTIMA_EJECUCION}" | grep -oP "Task \K[^ ]*")
    echo -e "${VERDE}✓ Última tarea ejecutada: ${TAREA} a las ${FECHA_ULTIMA_EJECUCION}${RESET}" | tee -a "${ARCHIVO_LOG}"
else
    echo -e "${AMARILLO}! No se encontraron registros de ejecución reciente de tareas${RESET}" | tee -a "${ARCHIVO_LOG}"
fi

echo -e "\n=== Verificación completada ===" | tee -a "${ARCHIVO_LOG}"
echo -e "Resultados guardados en ${ARCHIVO_LOG}\n" 