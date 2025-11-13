# 📁 ÍNDICE DE ARCHIVOS DEL SISTEMA

## 🎯 Archivos Principales

### 1. `enhanced_xml_analyzer.py` ⭐
**Sistema principal mejorado**
- **Tamaño:** 1,633 líneas de código
- **Función:** Sistema completo de análisis de licitaciones con IA
- **Características:**
  - Extracción completa de datos XML (11+ campos)
  - Detección automática de lotes
  - IA avanzada con 6 criterios de similitud
  - Análisis preciso de bajas estadísticas
  - Generación de informes completos
  - Exportación a Excel (5 hojas) y JSON
  - Interfaz Streamlit completa

**Cómo ejecutar:**
```bash
streamlit run enhanced_xml_analyzer.py
```

---

## 📚 Documentación

### 2. `README_SISTEMA_MEJORADO.md` 📖
**Documentación completa del sistema**
- Descripción detallada de todas las características
- Explicación del algoritmo de IA
- Tabla de criterios de scoring
- Estructura del código
- Ejemplos de salida
- Solución de problemas
- Notas sobre limitaciones

### 3. `INICIO_RAPIDO.md` 🚀
**Guía de inicio rápido**
- Verificación del sistema (✅ PASÓ TODAS LAS PRUEBAS)
- Instrucciones paso a paso
- Flujo de uso completo
- Ejemplos de resultados
- Configuración avanzada
- Solución de problemas comunes
- Mejores prácticas

### 4. `INDEX_ARCHIVOS.md` 📁
**Este archivo - Índice del proyecto**
- Lista completa de archivos
- Descripción de cada archivo
- Relaciones entre componentes

---

## 🔧 Scripts de Ejecución

### 5. `ejecutar_sistema_mejorado.sh` 🐧
**Script de ejecución para Linux/Mac**
- Verifica dependencias
- Inicia Streamlit automáticamente
- Muestra instrucciones de uso

**Uso:**
```bash
chmod +x ejecutar_sistema_mejorado.sh
./ejecutar_sistema_mejorado.sh
```

### 6. `ejecutar_sistema_mejorado.bat` 🪟
**Script de ejecución para Windows**
- Verifica dependencias
- Inicia Streamlit automáticamente
- Manejo de errores

**Uso:**
```cmd
ejecutar_sistema_mejorado.bat
```

---

## 🧪 Testing

### 7. `test_sistema.py` ✅
**Suite de pruebas automatizadas**
- Prueba extracción de datos XML
- Verifica algoritmo de similitud (60% en textos relacionados)
- Prueba detección de zonas cercanas
- Prueba extracción de palabras clave
- Validación completa del sistema

**Resultado último test:** ✅ TODAS LAS PRUEBAS PASADAS

**Uso:**
```bash
python3 test_sistema.py
```

---

## 📄 Datos de Prueba

### 8. `complete_document.xml` 📋
**XML de ejemplo para pruebas**
- Licitación real del Instituto Social de la Marina
- Datos:
  - Fecha: 2025-09-22
  - PBL: 58,902 €
  - Tipo: Servicios
  - CPV: 50241000
  - Sin lotes
  - 2 criterios de adjudicación

**Usado por:** `test_sistema.py`

---

## 📊 Archivos Legacy (Sistema Anterior)

### 9. `contrato_analyzer.py`
**Sistema anterior básico**
- Análisis simple sin IA avanzada
- Extracción limitada (5 campos)
- Sin detección de lotes
- **Status:** Reemplazado por `enhanced_xml_analyzer.py`

### 10. `advanced_ai_analyzer.py`
**Prototipo de IA anterior**
- Primer intento de análisis con IA
- Funcionalidades limitadas
- **Status:** Funcionalidades integradas en sistema mejorado

### 11. `xml_scraper_generator.py`
**Generador de scrapers XML**
- Utilidad para convertir URLs HTML a XML
- **Status:** Funcionalidad integrada en sistema mejorado

---

## 🗄️ Base de Datos

### Configuración
- **Host:** ocleminformatica.com
- **Puerto:** 3306
- **Base de datos:** colossus_vgarcia
- **Usuario:** colossus

**Tablas esperadas:**
- Contratos con campos: precio, localidad, CPV, objeto, fecha, etc.

---

## 📦 Dependencias

### Requeridas (TODAS INSTALADAS ✅)
```
streamlit
pandas
numpy
scikit-learn
plotly
requests
xlsxwriter
mysql-connector-python
```

### Instalación:
```bash
pip install streamlit pandas numpy scikit-learn plotly requests xlsxwriter mysql-connector-python
```

---

## 🔄 Flujo de Trabajo del Sistema

```
Usuario
   │
   ├─> 1. Obtiene URL del XML
   │
   ├─> 2. Pega URL en enhanced_xml_analyzer.py (Streamlit)
   │
   └─> Sistema procesa:
       │
       ├─> FASE 1: Extracción datos XML
       │   ├─ Fecha, PBL, Tipo, Objeto
       │   ├─ CPV, Criterios, Localidad
       │   └─ Detección de lotes
       │
       ├─> FASE 2: Búsqueda IA en BD
       │   ├─ Carga contratos
       │   ├─ Algoritmo similitud (6 criterios)
       │   └─ Top 20 resultados
       │
       ├─> FASE 3: Cálculo baja
       │   ├─ Análisis estadístico
       │   ├─ Detección patrones
       │   └─ Baja recomendada
       │
       └─> FASE 4: Generación informe
           ├─ Texto narrativo
           ├─ Excel (5 hojas)
           ├─ JSON
           └─ Visualizaciones
```

---

## 📈 Comparativa de Versiones

| Característica | Sistema Anterior | Sistema Mejorado |
|----------------|------------------|------------------|
| **Archivo principal** | contrato_analyzer.py | enhanced_xml_analyzer.py |
| **Líneas de código** | ~800 | 1,633 |
| **Campos extraídos** | 5 | 11+ |
| **Detección lotes** | ❌ | ✅ |
| **Criterios IA** | 3 | 6 |
| **Score máximo** | ~100 | ~160 |
| **Palabras clave** | Básico | TF-IDF avanzado |
| **Zonas cercanas** | No | ✅ |
| **Años anteriores** | No | ✅ |
| **Empresas con bajas** | Lista simple | Con bajas medias |
| **Hojas Excel** | 2-3 | 5 |
| **Documentación** | Mínima | Completa |
| **Tests** | No | Suite completa |
| **Scripts ejecución** | No | Linux/Mac + Windows |

---

## 🎯 Archivos a Usar

### Para Producción:
1. ✅ `enhanced_xml_analyzer.py` (PRINCIPAL)
2. ✅ `ejecutar_sistema_mejorado.sh` o `.bat`
3. ✅ `README_SISTEMA_MEJORADO.md`
4. ✅ `INICIO_RAPIDO.md`

### Para Desarrollo/Testing:
1. ✅ `test_sistema.py`
2. ✅ `complete_document.xml`

### Archivos Legacy (No usar):
1. ⚠️ `contrato_analyzer.py` (obsoleto)
2. ⚠️ `advanced_ai_analyzer.py` (obsoleto)
3. ⚠️ `xml_scraper_generator.py` (funcionalidad integrada)

---

## 🚀 INICIO RÁPIDO

**3 comandos para empezar:**

```bash
# 1. Navegar al directorio
cd /Users/macintosh/Desktop/iasusar/presupuestos

# 2. (Opcional) Verificar sistema
python3 test_sistema.py

# 3. Ejecutar aplicación
streamlit run enhanced_xml_analyzer.py
```

O simplemente:
```bash
./ejecutar_sistema_mejorado.sh
```

---

## 📊 Estadísticas del Proyecto

- **Total archivos principales:** 11
- **Total líneas de código:** ~2,500+
- **Total documentación:** ~1,000 líneas
- **Archivos activos:** 7
- **Archivos legacy:** 3
- **Archivos datos:** 1
- **Tests:** ✅ 100% pasados
- **Dependencias:** ✅ Todas instaladas
- **Estado:** ✅ LISTO PARA PRODUCCIÓN

---

## 🔗 Enlaces Rápidos

- **Sistema principal:** enhanced_xml_analyzer.py:1
- **Documentación completa:** README_SISTEMA_MEJORADO.md
- **Guía rápida:** INICIO_RAPIDO.md
- **Tests:** test_sistema.py
- **Ejecutar:** ejecutar_sistema_mejorado.sh

---

## 📝 Notas de Desarrollo

### Versión 2.0 - Septiembre 2025
**Mejoras implementadas:**
- ✅ Extracción completa de 11+ campos XML
- ✅ Detección automática de lotes individuales
- ✅ IA avanzada con 6 criterios (160 pts max)
- ✅ Análisis TF-IDF para palabras clave
- ✅ Detección de zonas geográficas cercanas
- ✅ Consideración de años anteriores
- ✅ Identificación de empresas con bajas medias
- ✅ Análisis de competitividad del sector
- ✅ Exportación Excel mejorada (5 hojas)
- ✅ Suite de tests automatizados
- ✅ Documentación completa
- ✅ Scripts de ejecución multiplataforma

### Próximas Mejoras Potenciales
- 🔮 Integración con API de Plataforma de Contratación
- 🔮 Cache de resultados para mayor velocidad
- 🔮 Análisis de múltiples XMLs simultáneos
- 🔮 Dashboard de estadísticas históricas
- 🔮 Alertas automáticas de nuevas licitaciones
- 🔮 Exportación a PDF con gráficos
- 🔮 API REST para integración externa

---

**Fecha de creación:** Septiembre 2025
**Última actualización:** Septiembre 2025
**Autor:** Sistema de Análisis de Licitaciones
**Versión:** 2.0 - Enhanced AI Edition
