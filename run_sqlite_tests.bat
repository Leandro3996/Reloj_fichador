@echo off
echo ======================================================
echo  Ejecutando pruebas con SQLite en memoria
echo ======================================================

cd mantenedor
python manage.py test apps.reloj_fichador.tests.test_models -v 2

echo.
echo Pruebas completadas.
echo ====================================================== 