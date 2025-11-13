#!/bin/bash

# Script para ejecutar el Sistema Avanzado de Análisis de Licitaciones

echo "🌐 Sistema Avanzado de Análisis de Licitaciones con IA"
echo "========================================================"
echo ""
echo "Iniciando sistema..."
echo ""

# Navegar al directorio
cd "$(dirname "$0")"

# Verificar que streamlit está instalado
if ! command -v streamlit &> /dev/null; then
    echo "❌ Error: Streamlit no está instalado"
    echo ""
    echo "Instala las dependencias con:"
    echo "pip install streamlit pandas numpy scikit-learn plotly requests xlsxwriter mysql-connector-python"
    exit 1
fi

# Ejecutar la aplicación
echo "✅ Iniciando aplicación Streamlit..."
echo ""
echo "💡 El navegador se abrirá automáticamente en http://localhost:8501"
echo ""
echo "Para detener el sistema: presiona Ctrl+C"
echo ""

streamlit run enhanced_xml_analyzer.py
