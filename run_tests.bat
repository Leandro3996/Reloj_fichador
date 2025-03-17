@echo off
color 0A
cls
echo ========================================================================
echo                   SISTEMA DE PRUEBAS - RELOJ FICHADOR                   
echo ========================================================================
echo.

REM Verificar que Docker esté en ejecución
docker ps >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [!] ADVERTENCIA: Docker no está en ejecución.
    echo [!] Las pruebas necesitan ejecutarse en el entorno Docker para funcionar correctamente.
    echo.
    echo Opciones:
    echo [1] Iniciar Docker Desktop y volver a intentarlo
    echo [2] Continuar de todos modos (puede fallar)
    echo [3] Salir
    echo.
    set /p docker_opcion="Selecciona una opción (1-3): "
    
    if "%docker_opcion%"=="1" (
        echo Por favor inicia Docker Desktop manualmente y presiona cualquier tecla cuando esté listo...
        pause > nul
        goto :start
    ) else if "%docker_opcion%"=="2" (
        echo Intentando continuar sin Docker...
    ) else (
        exit /b
    )
)

:start
cls
color 0A
echo ========================================================================
echo                   SISTEMA DE PRUEBAS - RELOJ FICHADOR                   
echo ========================================================================
echo.
echo  MENÚ PRINCIPAL:
echo  ---------------
echo.
echo  [1] Ejecutar todas las pruebas
echo  [2] Ejecutar pruebas de modelos
echo  [3] Ejecutar pruebas de vistas
echo  [4] Ejecutar pruebas de registro diario
echo  [5] Ejecutar prueba específica
echo  [6] Ejecutar pruebas con SQLite (local, sin Docker)
echo  [7] Salir
echo.
echo ========================================================================

:menu
set /p opcion=">> Selecciona una opción (1-7): "

if "%opcion%"=="1" (
    cls
    echo ========================================================================
    echo                    EJECUTANDO TODAS LAS PRUEBAS                        
    echo ========================================================================
    echo.
    cd tests_utils
    call run_all_tests.bat
    cd ..
    echo.
    echo Presiona cualquier tecla para volver al menú principal...
    pause > nul
    goto :start
) else if "%opcion%"=="2" (
    cls
    echo ========================================================================
    echo                    EJECUTANDO PRUEBAS DE MODELOS                        
    echo ========================================================================
    echo.
    cd tests_utils
    call run_specific_test.bat apps.reloj_fichador.tests.test_models
    cd ..
    echo.
    echo Presiona cualquier tecla para volver al menú principal...
    pause > nul
    goto :start
) else if "%opcion%"=="3" (
    cls
    echo ========================================================================
    echo                    EJECUTANDO PRUEBAS DE VISTAS                        
    echo ========================================================================
    echo.
    cd tests_utils
    call run_views_tests.bat
    cd ..
    echo.
    echo Presiona cualquier tecla para volver al menú principal...
    pause > nul
    goto :start
) else if "%opcion%"=="4" (
    cls
    echo ========================================================================
    echo                    EJECUTANDO PRUEBAS DE REGISTRO DIARIO               
    echo ========================================================================
    echo.
    cd tests_utils
    call run_registro_diario_tests.bat
    cd ..
    echo.
    echo Presiona cualquier tecla para volver al menú principal...
    pause > nul
    goto :start
) else if "%opcion%"=="5" (
    cls
    echo ========================================================================
    echo                    EJECUTAR PRUEBA ESPECÍFICA                          
    echo ========================================================================
    echo.
    echo  Introduce la ruta del test específico que deseas ejecutar.
    echo.
    echo  Ejemplos:
    echo   * apps.reloj_fichador.tests.test_models.OperarioModelTest
    echo   * apps.reloj_fichador.tests.test_views.ReporteViewTest
    echo   * apps.reloj_fichador.tests.test_registro_diario.RegistroDiarioModelTest
    echo   * apps.reloj_fichador.tests.test_models.OperarioModelTest.test_dni_unico
    echo.
    echo ========================================================================
    echo.
    set /p test_path=">> Ruta del test: "
    cd tests_utils
    call run_specific_test.bat %test_path%
    cd ..
    echo.
    echo Presiona cualquier tecla para volver al menú principal...
    pause > nul
    goto :start
) else if "%opcion%"=="6" (
    cls
    echo ========================================================================
    echo                    PRUEBAS LOCALES CON SQLITE                         
    echo ========================================================================
    echo.
    echo  Para ejecutar pruebas localmente con SQLite, necesitas instalar Django:
    echo.
    echo  pip install django mysqlclient colorama
    echo.
    echo  Después, puedes ejecutar las pruebas con:
    echo.
    echo  python manage.py test apps.reloj_fichador.tests
    echo.
    echo ========================================================================
    echo.
    echo Presiona cualquier tecla para volver al menú principal...
    pause > nul
    goto :start
) else if "%opcion%"=="7" (
    cls
    echo Saliendo del sistema de pruebas...
    goto :eof
) else (
    color 0C
    echo.
    echo [!] Opción no válida. Por favor, selecciona una opción del 1 al 7.
    echo.
    color 0A
    goto :menu
)

echo.
echo Pruebas completadas.
echo ====================================================== 