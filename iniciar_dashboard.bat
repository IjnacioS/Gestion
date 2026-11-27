@echo off
title Sistema de Alerta Temprana - SCY1102
echo ========================================================
echo    INICIANDO ENTORNO Y DASHBOARD EN CLASES
echo    Proyecto: Rendimiento en Matematicas (SCY1102)
echo ========================================================
echo.

echo [1/3] Verificando instalacion de librerias necesarias...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [AVISO] Fallo pip directo, intentando con python -m pip...
    python -m pip install -r requirements.txt --quiet
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

python -m streamlit run dashboard/app.py
pause
