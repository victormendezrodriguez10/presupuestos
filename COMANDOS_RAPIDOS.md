# ⚡ Comandos Rápidos de Referencia

## 🚀 Subir a GitHub (Primera vez)

```bash
# 1. Asegúrate de estar en el directorio correcto
cd /Users/macintosh/Desktop/iasusar/presupuestos

# 2. Conectar con GitHub (REEMPLAZA TU-USUARIO y tu-repo)
git remote add origin https://github.com/TU-USUARIO/sistema-licitaciones.git

# 3. Subir el código
git push -u origin main
```

---

## 🔄 Actualizar Código (Después de cambios)

```bash
# Ver qué cambió
git status

# Ver diferencias específicas
git diff

# Agregar todos los cambios
git add .

# Hacer commit
git commit -m "Descripción de los cambios"

# Subir a GitHub
git push

# ¡Listo! Streamlit Cloud actualizará automáticamente
```

---

## 📝 Comandos Git Comunes

```bash
# Ver historial de commits
git log --oneline

# Ver últimos 5 commits
git log --oneline -5

# Deshacer cambios (antes de commit)
git checkout -- archivo.py

# Ver ramas
git branch

# Crear nueva rama
git checkout -b feature-nueva

# Cambiar de rama
git checkout main

# Ver remoto configurado
git remote -v
```

---

## 🔐 Configurar Token de GitHub

Si pide autenticación:

1. **Crear Token:**
   - Ve a: https://github.com/settings/tokens
   - Click: "Generate new token (classic)"
   - Nombre: "Streamlit Deployment"
   - Permisos: Marca **repo** (todos)
   - Click: "Generate token"
   - **COPIA EL TOKEN** (solo se muestra una vez)

2. **Usar Token:**
   - Usuario: Tu usuario de GitHub
   - Password: El token que copiaste

3. **Guardar credenciales (opcional):**
   ```bash
   # Para no tener que ingresar cada vez
   git config --global credential.helper store
   # La próxima vez que ingreses user/token, se guardará
   ```

---

## ☁️ Streamlit Cloud - Comandos Útiles

### Reiniciar App
```
Settings → Reboot app
```

### Ver Logs en Tiempo Real
```
Manage app → View logs
```

### Actualizar Secretos
```
Settings → Secrets → Editar → Save
```

### Ver Uso/Estadísticas
```
Settings → Analytics
```

---

## 🧪 Testing Local

```bash
# Probar el sistema localmente
python3 test_sistema.py

# Ejecutar Streamlit localmente
streamlit run enhanced_xml_analyzer.py

# Verificar dependencias
pip list | grep -E 'streamlit|pandas|numpy|scikit|plotly|mysql'
```

---

## 📊 Verificar Estado del Proyecto

```bash
# Ver archivos en staging
git status

# Ver commit actual
git log -1

# Ver todos los archivos del proyecto
ls -lh

# Ver archivos ocultos (como .gitignore)
ls -la

# Contar líneas de código
wc -l enhanced_xml_analyzer.py
```

---

## 🔧 Solución Rápida de Problemas

### Error: "fatal: not a git repository"
```bash
# Reinicializar Git
git init
git add .
git commit -m "Initial commit"
```

### Error: "Authentication failed"
```bash
# Verificar remoto
git remote -v

# Reconfigurar remoto con token
git remote set-url origin https://TU-TOKEN@github.com/TU-USUARIO/tu-repo.git
```

### Error: "Updates were rejected"
```bash
# Si es la primera vez y hay conflicto
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Streamlit no actualiza
```bash
# Forzar push
git push -f origin main

# O en Streamlit Cloud:
# Settings → Reboot app
```

---

## 📦 Actualizar Dependencias

```bash
# Ver versiones actuales
pip list | grep -E 'streamlit|pandas|numpy|scikit|plotly|mysql'

# Actualizar una dependencia específica
pip install --upgrade streamlit

# Actualizar requirements.txt
pip freeze | grep -E 'streamlit|pandas|numpy|scikit|plotly|mysql' > requirements.txt

# Subir cambios
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## 🔍 Debug en Streamlit Cloud

Ver logs en tiempo real:
1. Ve a tu app en Streamlit Cloud
2. Click "Manage app"
3. Click "View logs"
4. Verás errores en tiempo real

---

## 💾 Backup Rápido

```bash
# Crear backup del código
cd /Users/macintosh/Desktop/iasusar
tar -czf presupuestos-backup-$(date +%Y%m%d).tar.gz presupuestos/

# El archivo estará en:
# presupuestos-backup-YYYYMMDD.tar.gz
```

---

## 🆘 Comandos de Emergencia

### Deshacer último commit (pero mantener cambios)
```bash
git reset --soft HEAD~1
```

### Deshacer último commit (y perder cambios)
```bash
git reset --hard HEAD~1
```

### Volver a un commit específico
```bash
# Ver commits
git log --oneline

# Volver (REEMPLAZA abc123 con el hash del commit)
git reset --hard abc123
```

### Eliminar todos los cambios locales
```bash
git checkout .
git clean -fd
```

---

## 📝 Template de Commits

Buenos mensajes de commit:

```bash
# Feature nueva
git commit -m "✨ Añadir filtro por CPV en búsqueda"

# Bug fix
git commit -m "🐛 Corregir error en extracción de lotes"

# Documentación
git commit -m "📚 Actualizar README con ejemplos"

# Performance
git commit -m "⚡ Optimizar búsqueda de similitudes"

# Refactoring
git commit -m "♻️ Refactorizar función de análisis"

# Testing
git commit -m "✅ Añadir tests para extracción XML"
```

---

## 🔗 Enlaces Útiles

```bash
# Tu repositorio (REEMPLAZA)
https://github.com/TU-USUARIO/sistema-licitaciones

# Tu app en Streamlit Cloud (REEMPLAZA)
https://sistema-licitaciones-TU-NOMBRE.streamlit.app

# Streamlit Cloud Dashboard
https://share.streamlit.io

# GitHub Settings
https://github.com/settings

# GitHub Tokens
https://github.com/settings/tokens
```

---

## 📞 Comandos de Información

```bash
# Versión de Python
python3 --version

# Versión de Git
git --version

# Versión de Streamlit
streamlit --version

# Ver todas las variables de Git configuradas
git config --list

# Ver usuario y email de Git
git config user.name
git config user.email
```

---

## 🎯 Flujo Completo Típico

```bash
# 1. Hacer cambios en el código
# (editar archivos)

# 2. Ver qué cambió
git status
git diff

# 3. Agregar cambios
git add .

# 4. Hacer commit
git commit -m "📝 Descripción de los cambios"

# 5. Subir a GitHub
git push

# 6. Verificar en Streamlit Cloud
# La app se actualiza automáticamente en 2-3 min

# 7. Verificar que funciona
# Abre la URL de tu app y prueba
```

---

**Guarda este archivo para referencia rápida!**

**Última actualización:** Septiembre 2025
