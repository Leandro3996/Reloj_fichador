@echo off
setlocal enabledelayedexpansion

REM Obtener la ruta completa del directorio del script
set "SCRIPT_DIR=%~dp0"
REM Quitar el \ final
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
REM Obtener el directorio raíz (parent del SCRIPT_DIR)
for %%I in ("%SCRIPT_DIR%") do set "ROOT_DIR=%%~dpI"
REM Quitar el \ final
set "ROOT_DIR=%ROOT_DIR:~0,-1%"

echo ======================================================
echo      EJECUTANDO PRUEBAS DE VISTAS
echo ======================================================
echo.
echo Directorio de scripts: %SCRIPT_DIR%
echo Directorio raíz: %ROOT_DIR%
echo.

REM Verificar que Docker esté en ejecución
docker ps >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker no está en ejecución. Inicia Docker Desktop y vuelve a intentarlo.
    goto :end
)

REM Usar directamente docker-compose para los comandos
cd /d "%ROOT_DIR%"

REM Crear el directorio tests_utils en el contenedor si no existe
echo Preparando entorno en el contenedor...
docker-compose exec web mkdir -p /app/tests_utils

REM Copiar archivos de configuración al contenedor
echo Copiando archivos de configuración al contenedor...
for %%F in (sqlite_settings.py datetime_helpers.py __init__.py) do (
    docker cp "%SCRIPT_DIR%\%%F" reloj_fichador-web-1:/app/tests_utils/ 2>nul
    if !ERRORLEVEL! NEQ 0 (
        docker cp "%SCRIPT_DIR%\%%F" docker-web-1:/app/tests_utils/ 2>nul
        if !ERRORLEVEL! NEQ 0 (
            echo Error al copiar %%F. Intentando con otro nombre de contenedor...
            docker cp "%SCRIPT_DIR%\%%F" web:/app/tests_utils/ 2>nul
        )
    )
)

REM Ejecutar pruebas de vistas
echo Ejecutando pruebas de vistas...
docker-compose exec web python -m django test apps.reloj_fichador.tests.test_views -v 2 --settings=tests_utils.sqlite_settings

cd /d "%SCRIPT_DIR%"

:end
echo.
echo Pruebas completadas.
echo ======================================================
echo Presiona cualquier tecla para salir...
pause > nul
endlocal 