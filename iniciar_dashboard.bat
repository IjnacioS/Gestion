@echo off
chcp 65001 >nul
cd /d "%~dp0"
color 0B
title Sistema de Alerta Temprana en Matematicas - SCY1102

:MENU
cls
echo.
echo  ====================================================================
echo     SISTEMA DE ALERTA TEMPRANA EN MATEMATICAS  ^|  DUOC UC (SCY1102)
echo     Equipo: Ignacio Sobarzo  -  Diego Yanez  -  Felipe Espinoza
echo  ====================================================================
echo.
echo   [1]  Iniciar Dashboard Web (Streamlit)
echo   [2]  Detener Dashboard (cierra el puerto 8501 si quedo abierto)
echo   [3]  Ejecutar Script Automatico por Lotes (Demo CSV en consola)
echo   [4]  Salir
echo.
echo  --------------------------------------------------------------------
set /p "OPCION=  Elige una opcion (1-4) y presiona Enter: "

if "%OPCION%"=="1" goto INICIAR
if "%OPCION%"=="2" goto DETENER
if "%OPCION%"=="3" goto SCRIPT_CLI
if "%OPCION%"=="4" goto SALIR

echo.
echo   [!] Opcion no valida. Intenta nuevamente.
timeout /t 2 >nul
goto MENU

:INICIAR
cls
echo.
echo  ====================================================================
echo     INICIANDO DASHBOARD INTERACTIVO (http://localhost:8501)
echo  ====================================================================
echo.
echo   [1/3] Verificando librerias de Python...
echo         (En un PC nuevo esto puede tardar 1 a 2 minutos)
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    pip install -r requirements.txt --quiet --disable-pip-version-check
)

echo.
echo   [2/3] Verificando modelo predictivo...
if not exist "models\modelo_matematicas.joblib" (
    echo   [ERROR] No se encontro models\modelo_matematicas.joblib
    echo.
    pause
    goto MENU
)
echo         OK - Modelo detectado correctamente.

echo.
echo   [3/3] Iniciando servidor web...
echo         * El navegador se abrira solo en http://localhost:8501
echo         * Para DETENER el Dashboard, vuelve aqui y presiona Ctrl+C
echo  ====================================================================
echo.
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
python -m streamlit run dashboard/app.py --browser.gatherUsageStats=false --server.port 8501
echo.
echo   [i] Dashboard detenido.
pause
goto MENU

:DETENER
cls
echo.
echo  ====================================================================
echo     DETENIENDO DASHBOARD EN PUERTO 8501
echo  ====================================================================
echo.
powershell -NoProfile -Command "$c = Get-NetTCPConnection -LocalPort 8501 -State Listen -ErrorAction SilentlyContinue; if ($c) { $c.OwningProcess | Select-Object -Unique | ForEach-Object { Stop-Process -Id $_ -Force; Write-Host '   [OK] Dashboard detenido correctamente (PID' $_ ').' } } else { Write-Host '   [i] No habia ningun Dashboard corriendo en el puerto 8501.' }"
echo.
pause
goto MENU

:SCRIPT_CLI
cls
echo.
echo  ====================================================================
echo     DEMO SCRIPT AUTOMATICO POR LOTES (CLI)
echo  ====================================================================
echo.
if not exist "data\ejemplo_curso_demo.csv" (
    echo   [ERROR] No se encontro data\ejemplo_curso_demo.csv
    pause
    goto MENU
)
python src/automatizacion_matematicas.py --entrada data/ejemplo_curso_demo.csv --salida salidas
echo.
echo   [OK] Resultados guardados en la carpeta: salidas\
echo.
pause
goto MENU

:SALIR
cls
echo.
echo   Cerrando panel de control... Hasta pronto!
timeout /t 1 >nul
exit /b
