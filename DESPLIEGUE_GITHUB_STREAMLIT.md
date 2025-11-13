# 🚀 Guía Completa: GitHub + Streamlit Cloud

## ✅ Estado Actual

Tu proyecto está listo para desplegar:
- ✅ Git inicializado
- ✅ Commit inicial creado (12 archivos)
- ✅ `.gitignore` configurado
- ✅ `requirements.txt` listo
- ✅ Sistema adaptado para Streamlit Cloud
- ✅ Documentación completa

---

## 📦 PASO 1: Subir a GitHub

### 1.1 Crear Repositorio en GitHub

1. Ve a [https://github.com](https://github.com)
2. Haz clic en **"New repository"** (botón verde)
3. Configura:
   - **Repository name:** `sistema-licitaciones` (o el nombre que prefieras)
   - **Description:** "Sistema Avanzado de Análisis de Licitaciones con IA"
   - **Visibility:**
     - ✅ **Private** (recomendado si es interno)
     - ⚠️ **Public** (solo si quieres que sea público)
   - **NO marques** "Initialize with README" (ya lo tienes)
4. Haz clic en **"Create repository"**

### 1.2 Conectar tu Repositorio Local

GitHub te mostrará comandos. Usa estos (adapta con TU usuario):

```bash
# En tu terminal, en la carpeta del proyecto:
cd /Users/macintosh/Desktop/iasusar/presupuestos

# Conectar con GitHub (REEMPLAZA tu-usuario y tu-repo)
git remote add origin https://github.com/TU-USUARIO/sistema-licitaciones.git

# Verificar que está conectado
git remote -v

# Subir el código
git push -u origin main
```

**Si pide autenticación:**
- Usuario: Tu usuario de GitHub
- Password: **Personal Access Token** (no tu contraseña)

**Crear Token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Nombre: "Streamlit Deployment"
4. Permisos: Marca **repo** (todos los checkboxes de repo)
5. Generate token
6. **COPIA EL TOKEN** (solo se muestra una vez)
7. Úsalo como password

### 1.3 Verificar que Subió

Ve a `https://github.com/TU-USUARIO/sistema-licitaciones` y verifica que ves:
- ✅ README.md mostrándose
- ✅ 12 archivos
- ✅ Carpeta `.streamlit/`

---

## ☁️ PASO 2: Desplegar en Streamlit Cloud

### 2.1 Crear Cuenta en Streamlit Cloud

1. Ve a [https://share.streamlit.io](https://share.streamlit.io)
2. Haz clic en **"Sign up"**
3. **Conecta con GitHub** (usa la misma cuenta)
4. Autoriza a Streamlit Cloud para acceder a tus repos

### 2.2 Desplegar la App

1. En Streamlit Cloud, haz clic en **"New app"**
2. Completa:
   - **Repository:** `TU-USUARIO/sistema-licitaciones`
   - **Branch:** `main`
   - **Main file path:** `enhanced_xml_analyzer.py`
3. **Avanzado** (opcional):
   - **App URL:** `sistema-licitaciones-tu-nombre` (personaliza)
   - **Python version:** 3.11 (o la que prefieras 3.8-3.11)
4. Haz clic en **"Deploy!"**

### 2.3 Configurar Secretos (Base de Datos)

⚠️ **IMPORTANTE**: Tu app necesita acceso a la base de datos.

1. En Streamlit Cloud, ve a tu app
2. Haz clic en **"⚙️ Settings"** (arriba a la derecha)
3. Ve a **"Secrets"**
4. Pega esto en el editor (REEMPLAZA con tus datos reales):

```toml
[database]
host = "ocleminformatica.com"
port = 3306
user = "colossus"
password = "OIN2020p$j"
database = "colossus_vgarcia"
```

5. Haz clic en **"Save"**
6. La app se reiniciará automáticamente

### 2.4 Verificar Despliegue

1. Espera 2-3 minutos mientras despliega
2. Verás logs en tiempo real
3. Si todo va bien, verás: **"Your app is live! 🎉"**
4. Haz clic en la URL de tu app

---

## 🎯 PASO 3: Probar la App

### 3.1 Primera Prueba

1. Abre tu app en Streamlit Cloud
2. Deberías ver: **"✅ Conectado exitosamente a la base de datos"**
3. Pega una URL de XML de prueba
4. Haz clic en **"🚀 Analizar Licitación"**

### 3.2 Si Hay Errores

**Error: No se puede conectar a BD**
- Verifica que configuraste los secretos correctamente
- Comprueba que los datos de conexión son correctos
- Revisa que el servidor MySQL permite conexiones externas

**Error: Module not found**
- Verifica que `requirements.txt` esté correcto
- Ve a Settings → Reboot app

**Error 404 o no carga**
- Verifica que el archivo principal es `enhanced_xml_analyzer.py`
- Comprueba que está en la raíz del repo (no en subcarpeta)

---

## 🔄 PASO 4: Actualizar la App

Cuando hagas cambios en tu código:

### 4.1 Localmente

```bash
# Edita tus archivos
# Luego:

git add .
git commit -m "Descripción de los cambios"
git push origin main
```

### 4.2 En Streamlit Cloud

La app se **actualizará automáticamente** cuando hagas push a GitHub.

Si necesitas forzar actualización:
1. Ve a Settings
2. Haz clic en **"Reboot app"**

---

## 📊 PASO 5: Compartir la App

### 5.1 URL de tu App

Tu app estará en:
```
https://sistema-licitaciones-tu-nombre.streamlit.app
```

O similar (Streamlit asigna automáticamente).

### 5.2 Hacer la App Pública/Privada

**Para app pública:**
- Cualquiera con la URL puede acceder
- Perfecto si quieres compartir con clientes

**Para app privada:**
1. Ve a Settings en Streamlit Cloud
2. **Solo disponible en plan de pago**
3. Puedes restringir por email

**Alternativa gratuita para privacidad:**
- Repositorio privado en GitHub
- La app sigue siendo pública PERO
- Nadie puede ver el código fuente

---

## 🔐 SEGURIDAD

### ✅ Buenas Prácticas

1. **Nunca subas credenciales al código**
   - ✅ Ya está protegido por `.gitignore`
   - ✅ Usa `st.secrets` en Streamlit Cloud

2. **Repositorio privado recomendado**
   - Protege la lógica de negocio
   - Oculta estructura de BD

3. **Actualiza contraseñas regularmente**
   - Solo necesitas cambiar en Streamlit Secrets

4. **Revisa logs de acceso**
   - Streamlit Cloud muestra estadísticas de uso

### ⚠️ Datos Sensibles

El sistema NO guarda:
- URLs de licitaciones procesadas
- Resultados de análisis
- Datos de usuarios

Todo se procesa en tiempo real y no se almacena.

---

## 🛠️ COMANDOS ÚTILES

### Git

```bash
# Ver estado
git status

# Ver commits
git log --oneline

# Ver diferencias
git diff

# Deshacer cambios (antes de commit)
git checkout -- archivo.py

# Crear nueva rama
git checkout -b mejoras

# Cambiar de rama
git checkout main

# Ver ramas
git branch
```

### Streamlit Cloud

- **Ver logs:** Click en "Manage app" → Logs
- **Reiniciar:** Settings → Reboot app
- **Ver uso:** Settings → Analytics
- **Cambiar secretos:** Settings → Secrets

---

## 📝 CHECKLIST DE DESPLIEGUE

Marca conforme vayas completando:

### GitHub
- [ ] Repositorio creado en GitHub
- [ ] Código subido (`git push`)
- [ ] README.md visible
- [ ] 12 archivos presentes

### Streamlit Cloud
- [ ] Cuenta creada
- [ ] GitHub conectado
- [ ] App desplegada
- [ ] Secretos configurados
- [ ] App funcionando (conexión BD OK)
- [ ] Prueba realizada con XML real

### Verificación Final
- [ ] Extracción de XML funciona
- [ ] Búsqueda de similitudes funciona
- [ ] Cálculo de baja funciona
- [ ] Exportación a Excel funciona
- [ ] Texto narrativo se genera correctamente

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Problema: "git push" falla con authentication

**Solución:**
```bash
# Usa token de GitHub en lugar de contraseña
# URL: https://github.com/settings/tokens

# O configura SSH:
ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"
cat ~/.ssh/id_ed25519.pub
# Copia el contenido y añádelo en GitHub → Settings → SSH keys
```

### Problema: Streamlit no encuentra el archivo

**Solución:**
- Verifica que `enhanced_xml_analyzer.py` está en la raíz
- Comprueba que el nombre está correcto (case-sensitive)
- Reboot app

### Problema: Error al conectar a MySQL

**Solución:**
1. Verifica secretos en Streamlit Cloud
2. Comprueba que MySQL permite conexiones externas
3. Verifica firewall del servidor
4. Prueba conexión desde otro cliente

### Problema: "Module not found" en Streamlit

**Solución:**
```bash
# Verifica requirements.txt
cat requirements.txt

# Asegúrate de que todos los módulos están listados
# Si agregaste algo nuevo:
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Problema: App muy lenta

**Posibles causas:**
- Consultando muchos contratos (reduce a 3000-5000)
- Primera carga siempre es más lenta
- Conexión de red lenta a MySQL
- MySQL remoto en servidor lento

**Solución:**
- Añade caché con `@st.cache_data`
- Reduce límite de contratos
- Considera BD más cercana geográficamente

---

## 📞 RECURSOS

- **Streamlit Docs:** https://docs.streamlit.io
- **Streamlit Cloud:** https://share.streamlit.io
- **GitHub Docs:** https://docs.github.com
- **MySQL Connector:** https://dev.mysql.com/doc/connector-python/

---

## 🎉 ¡LISTO!

Una vez completados todos los pasos, tendrás:
- ✅ Código en GitHub (versionado y seguro)
- ✅ App desplegada en Streamlit Cloud
- ✅ Sistema accesible desde cualquier lugar
- ✅ Actualizaciones automáticas
- ✅ Sin costos de servidor

**URL de tu app:**
`https://tu-app.streamlit.app`

**Comparte esta URL** con tu equipo y empieza a analizar licitaciones!

---

**Última actualización:** Septiembre 2025
**Guía creada por:** Sistema de Análisis de Licitaciones
