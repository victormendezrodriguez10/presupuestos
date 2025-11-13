#!/bin/bash

# Script para subir a GitHub
# INSTRUCCIONES: Reemplaza TU-USUARIO con tu usuario de GitHub real

echo ""
echo "🚀 SUBIENDO SISTEMA A GITHUB"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Verificar que estás en el directorio correcto
if [ ! -f "enhanced_xml_analyzer.py" ]; then
    echo "❌ ERROR: No estás en el directorio correcto"
    echo "   Ejecuta: cd /Users/macintosh/Desktop/iasusar/presupuestos"
    exit 1
fi

echo "✅ Directorio correcto"
echo ""

# Paso 1: Instrucciones para crear repo en GitHub
echo "PASO 1: CREAR REPOSITORIO EN GITHUB"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "Abre tu navegador y:"
echo "1. Ve a https://github.com"
echo "2. Click 'New repository'"
echo "3. Name: sistema-licitaciones"
echo "4. Visibility: Private (recomendado)"
echo "5. NO marques 'Initialize with README'"
echo "6. Click 'Create repository'"
echo ""
read -p "¿Ya creaste el repositorio? (presiona Enter cuando esté listo) " _

echo ""
echo "PASO 2: INGRESAR TU USUARIO DE GITHUB"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
read -p "Ingresa tu usuario de GitHub: " GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo "❌ Error: Usuario no puede estar vacío"
    exit 1
fi

echo ""
echo "Usuario: $GITHUB_USER"
echo "Repositorio: https://github.com/$GITHUB_USER/sistema-licitaciones"
echo ""
read -p "¿Es correcto? (s/n): " confirm

if [ "$confirm" != "s" ] && [ "$confirm" != "S" ]; then
    echo "Abortado. Ejecuta el script de nuevo."
    exit 0
fi

echo ""
echo "PASO 3: CONECTAR CON GITHUB"
echo "─────────────────────────────────────────────────────────────────────"
echo ""

# Verificar si ya hay un remoto configurado
if git remote | grep -q "origin"; then
    echo "⚠️  Ya existe un remoto 'origin'. Actualizando..."
    git remote set-url origin "https://github.com/$GITHUB_USER/sistema-licitaciones.git"
else
    echo "Añadiendo remoto..."
    git remote add origin "https://github.com/$GITHUB_USER/sistema-licitaciones.git"
fi

echo "✅ Remoto configurado"
echo ""

echo "PASO 4: SUBIR CÓDIGO"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "Ejecutando: git push -u origin main"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   Usuario: $GITHUB_USER"
echo "   Password: TU PERSONAL ACCESS TOKEN (NO tu contraseña)"
echo ""
echo "¿Necesitas crear un token?"
echo "→ https://github.com/settings/tokens"
echo "→ Generate new token (classic)"
echo "→ Marca 'repo'"
echo ""
read -p "Presiona Enter para continuar con el push... " _

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ ¡CÓDIGO SUBIDO EXITOSAMENTE A GITHUB!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🌐 Tu repositorio: https://github.com/$GITHUB_USER/sistema-licitaciones"
    echo ""
    echo "✅ VERIFICAR:"
    echo "   1. Abre el link de arriba"
    echo "   2. Deberías ver el README.md"
    echo "   3. Deberías ver ~15 archivos"
    echo ""
    echo "🎯 SIGUIENTE PASO: STREAMLIT CLOUD"
    echo "   1. Ve a https://share.streamlit.io"
    echo "   2. Conecta con GitHub"
    echo "   3. Click 'New app'"
    echo "   4. Repository: $GITHUB_USER/sistema-licitaciones"
    echo "   5. Main file: enhanced_xml_analyzer.py"
    echo "   6. Deploy!"
    echo ""
    echo "📖 Guía completa: DESPLIEGUE_GITHUB_STREAMLIT.md"
    echo ""
else
    echo ""
    echo "❌ ERROR en el push"
    echo ""
    echo "Posibles causas:"
    echo "1. Token incorrecto o sin permisos 'repo'"
    echo "2. Repositorio no creado en GitHub"
    echo "3. Nombre de usuario incorrecto"
    echo ""
    echo "Soluciones:"
    echo "• Verifica tu token: https://github.com/settings/tokens"
    echo "• Verifica el repo existe: https://github.com/$GITHUB_USER/sistema-licitaciones"
    echo "• Ejecuta el script de nuevo"
    echo ""
fi
