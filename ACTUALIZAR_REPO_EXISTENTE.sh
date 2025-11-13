#!/bin/bash

# Script para actualizar repositorio existente en GitHub
# Este script sustituye el contenido antiguo con el nuevo sistema

echo ""
echo "🔄 ACTUALIZANDO REPOSITORIO EXISTENTE EN GITHUB"
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

# Solicitar URL del repositorio
echo "PASO 1: URL DE TU REPOSITORIO"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
read -p "Pega la URL de tu repositorio (ej: https://github.com/usuario/repo): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ Error: URL no puede estar vacía"
    exit 1
fi

# Limpiar URL si tiene .git al final
REPO_URL=${REPO_URL%.git}

echo ""
echo "✅ Repositorio: $REPO_URL"
echo ""
read -p "¿Es correcto? (s/n): " confirm

if [ "$confirm" != "s" ] && [ "$confirm" != "S" ]; then
    echo "Abortado. Ejecuta el script de nuevo."
    exit 0
fi

echo ""
echo "PASO 2: CONFIGURAR REMOTO"
echo "─────────────────────────────────────────────────────────────────────"
echo ""

# Verificar si ya hay un remoto configurado
if git remote | grep -q "origin"; then
    echo "⚠️  Remoto 'origin' ya existe. Actualizando URL..."
    git remote set-url origin "$REPO_URL.git"
else
    echo "Añadiendo remoto..."
    git remote add origin "$REPO_URL.git"
fi

echo "✅ Remoto configurado: $REPO_URL.git"
echo ""

# Verificar estado de Git
echo "PASO 3: VERIFICAR CAMBIOS"
echo "─────────────────────────────────────────────────────────────────────"
echo ""

git status --short

echo ""
echo "Los archivos que se subirán/actualizarán están arriba ↑"
echo ""
read -p "¿Continuar con la actualización? (s/n): " proceed

if [ "$proceed" != "s" ] && [ "$proceed" != "S" ]; then
    echo "Abortado."
    exit 0
fi

echo ""
echo "PASO 4: SUBIR CAMBIOS"
echo "─────────────────────────────────────────────────────────────────────"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   Si pide autenticación:"
echo "   • Usuario: Tu usuario de GitHub"
echo "   • Password: Personal Access Token"
echo ""
echo "   ¿Necesitas token? → https://github.com/settings/tokens"
echo ""
read -p "Presiona Enter para continuar... " _

# Hacer push (puede requerir forzar si hay conflictos)
echo ""
echo "Intentando push normal..."
git push origin main

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Push normal falló. Puede que necesites forzar la actualización."
    echo ""
    echo "Opciones:"
    echo "1. Hacer push con --force (SOBRESCRIBE el repo remoto)"
    echo "2. Hacer pull primero y luego push"
    echo "3. Cancelar"
    echo ""
    read -p "Elige opción (1/2/3): " option

    case $option in
        1)
            echo ""
            echo "⚠️  ADVERTENCIA: Esto sobrescribirá el contenido del repositorio remoto"
            read -p "¿Estás seguro? (escribe SI en mayúsculas): " confirm_force

            if [ "$confirm_force" = "SI" ]; then
                echo "Forzando push..."
                git push --force origin main

                if [ $? -eq 0 ]; then
                    echo ""
                    echo "✅ Push forzado exitoso"
                fi
            else
                echo "Cancelado."
                exit 0
            fi
            ;;
        2)
            echo ""
            echo "Haciendo pull primero..."
            git pull origin main --allow-unrelated-histories

            if [ $? -eq 0 ]; then
                echo ""
                echo "Ahora haciendo push..."
                git push origin main
            fi
            ;;
        3)
            echo "Cancelado."
            exit 0
            ;;
        *)
            echo "Opción inválida. Cancelado."
            exit 0
            ;;
    esac
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ ¡REPOSITORIO ACTUALIZADO EXITOSAMENTE!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🌐 Tu repositorio: $REPO_URL"
    echo ""
    echo "✅ VERIFICAR:"
    echo "   1. Abre el link de arriba"
    echo "   2. Deberías ver el README.md actualizado"
    echo "   3. Deberías ver los nuevos archivos"
    echo "   4. Los archivos antiguos ya no deberían aparecer"
    echo ""
    echo "🔄 STREAMLIT CLOUD:"
    echo "   Si ya tenías la app desplegada en Streamlit Cloud:"
    echo "   1. La app se actualizará automáticamente en 2-3 minutos"
    echo "   2. O ve a Settings → Reboot app para forzar actualización"
    echo ""
    echo "📝 Si la app está desplegada, NO olvides verificar que los"
    echo "   secretos de BD estén configurados en Settings → Secrets"
    echo ""
else
    echo ""
    echo "❌ ERROR al actualizar"
    echo ""
    echo "Posibles causas:"
    echo "• Token incorrecto o sin permisos"
    echo "• Conflictos con el contenido remoto"
    echo "• Problemas de red"
    echo ""
    echo "Contacta si necesitas ayuda específica."
fi
