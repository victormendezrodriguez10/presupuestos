@echo off
REM Script para ejecutar el Sistema Avanzado de Análisis de Licitaciones en Windows

echo.
echo ============================================================
echo Sistema Avanzado de Analisis de Licitaciones con IA
echo ============================================================
echo.
echo Iniciando sistema...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar que streamlit está instalado
where streamlit >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Streamlit no esta instalado
    echo.
    echo Instala las dependencias con:
    echo pip install streamlit pandas numpy scikit-learn plotly requests xlsxwriter mysql-connector-python
    echo.
    pause
    exit /b 1
)

REM Ejecutar la aplicación
echo Iniciando aplicacion Streamlit...
echo.
echo El navegador se abrira automaticamente en http://localhost:8501
echo.
echo Para detener el sistema: presiona Ctrl+C
echo.

streamlit run enhanced_xml_analyzer.py

pause
