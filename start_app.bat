@echo off
REM Script de inicio seguro de Streamlit con validación de dependencias

cd /d "C:\Users\Vicente Sanchez\Documents\VICENTE DOCKER\CODIGO PRUEBAS FREIGHTMETRICS"

echo.
echo === Validando dependencias ===
.venv\Scripts\python validate_dependencies.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Instala las dependencias que faltan y vuelve a intentar.
    pause
    exit /b 1
)

echo.
echo === Iniciando Streamlit en puerto 8500 ===
.venv\Scripts\python -m streamlit run app.py --server.port 8500

pause
