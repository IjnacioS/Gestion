@echo off
cd /d "%~dp0"
title Sistema de Alerta Temprana - SCY1102
echo ========================================================
echo    INICIANDO ENTORNO Y DASHBOARD EN CLASES
echo    Proyecto: Rendimiento en Matematicas (SCY1102)
echo ========================================================
echo.

echo [1/3] Verificando instalacion de librerias necesarias...
echo (Si es la primera vez en este PC, puede tardar 1 a 2 minutos)
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo [AVISO] Intentando con pip directo...
    pip install -r requirements.txt --quiet --disable-pip-version-check
)

echo.
echo [2/3] Verificando modelo y archivos...
if not exist "models\modelo_matematicas.joblib" (
    echo [ERROR] No se encuentra models\modelo_matematicas.joblib. Revisa la carpeta.
    pause
    exit /b
)
echo Modelo detectado correctamente.

echo.
echo [3/3] Abriendo Dashboard Streamlit...
echo (Se abrira automaticamente en tu navegador: http://localhost:8501)
echo Presiona Ctrl+C en esta ventana cuando quieras cerrar el Dashboard.
echo ========================================================
echo.

set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
python -m streamlit run dashboard/app.py --browser.gatherUsageStats=false
pause
