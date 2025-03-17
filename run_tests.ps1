Write-Host "======================================================" -ForegroundColor Green
Write-Host "    Ejecutando pruebas con SQLite en memoria" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Green
Write-Host ""

try {
    # Ejecutar las pruebas con la configuración de SQLite
    python manage.py test apps.reloj_fichador.tests.test_models --settings=test_settings -v 2
    
    # Verificar si las pruebas fueron exitosas
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Todas las pruebas se ejecutaron correctamente." -ForegroundColor Green
    }
    else {
        Write-Host ""
        Write-Host "❌ Se encontraron errores en las pruebas. Revisa los mensajes anteriores." -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ Error al ejecutar pruebas: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "======================================================" -ForegroundColor Green
Write-Host "              Pruebas completadas" -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Green 