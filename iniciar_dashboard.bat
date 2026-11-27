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
echo     INICIANDO DASHBOARD INTERACTIVO - http://localhost:8501
echo  ====================================================================
echo.
echo   [###-------] 30%% - Comprobando librerias instaladas...
python -c "import streamlit, pandas, sklearn, plotly, joblib" >nul 2>&1
if errorlevel 1 goto INSTALAR_DEPS
echo         OK - Librerias listas. Inicio rapido.
goto VERIFICAR_MODELO

:INSTALAR_DEPS
echo         Faltan librerias. Instalando automaticamente...
echo.
python -m pip install -r requirements.txt --disable-pip-version-check
if errorlevel 1 pip install -r requirements.txt --disable-pip-version-check

:VERIFICAR_MODELO
echo.
echo   [######----] 60%% - Verificando modelo y configuracion...
if not exist "models\modelo_matematicas.joblib" (
    echo   [ERROR] No se encontro models\modelo_matematicas.joblib
    echo.
    pause
    goto MENU
)

if not exist "%USERPROFILE%\.streamlit" mkdir "%USERPROFILE%\.streamlit"
if not exist "%USERPROFILE%\.streamlit\credentials.toml" (
    echo [general]> "%USERPROFILE%\.streamlit\credentials.toml"
    echo email = "">> "%USERPROFILE%\.streamlit\credentials.toml"
)
echo         OK - Modelo y credenciales listos.

echo.
echo   [##########] 100%% - Abriendo Dashboard en el navegador...
echo         * URL: http://localhost:8501
echo         * Para DETENER el Dashboard, vuelve aqui y presiona Ctrl+C
echo  ====================================================================
echo.
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
python -m streamlit run dashboard/app.py --server.headless=false --browser.gatherUsageStats=false --server.port 8501
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
echo     DEMO SCRIPT AUTOMATICO POR LOTES - CLI
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
