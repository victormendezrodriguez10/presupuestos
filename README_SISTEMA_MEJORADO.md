# 🌐 Sistema Avanzado de Análisis de Licitaciones con IA

## 📋 Descripción

Sistema mejorado para analizar licitaciones públicas que extrae **todos los datos completos** del XML y utiliza **IA avanzada** para encontrar licitaciones similares y recomendar bajas estadísticas precisas.

## ✨ Características Principales

### 1. 📥 Extracción Completa de Datos XML

El sistema extrae automáticamente **TODOS** los campos necesarios:

- ✅ **Fecha de publicación** - `<cbc:IssueDate>`
- ✅ **PBL (Presupuesto Base Licitación)** - `<cbc:TaxExclusiveAmount>`
- ✅ **Importe de adjudicación** (si disponible)
- ✅ **Adjudicatario** (si disponible)
- ✅ **Número de licitadores** (si disponible)
- ✅ **Objeto del contrato** - `<cbc:Name>` en `<cac:ProcurementProject>`
- ✅ **Criterios de adjudicación** (detallados con pesos)
- ✅ **CPV** (todos los códigos con nombres)
- ✅ **Tipo de contrato** (Servicios, Obras, Suministros, etc.)
- ✅ **Localidad/Provincia**
- ✅ **Procedimiento** (Abierto, Abierto Simplificado, etc.)
- ✅ **Plazo de ejecución**

### 2. 📦 Detección Automática de Lotes

- Detecta si la licitación está dividida en lotes
- Extrae datos de **cada lote individualmente**:
  - ID del lote
  - Descripción
  - PBL del lote
  - CPV específicos del lote
  - Adjudicación del lote (si disponible)

### 3. 🤖 IA Avanzada para Búsqueda de Similitudes

Sistema de scoring inteligente basado en múltiples criterios:

| Criterio | Peso | Descripción |
|----------|------|-------------|
| **CPV** | 40 pts | Coincidencia exacta (8 dígitos), división (4 dígitos) o categoría (2 dígitos) |
| **Zona** | 30 pts | Misma localidad o zonas geográficas cercanas |
| **Importe** | 25 pts | Presupuesto similar (±20%, ±40%, ±60%) |
| **Palabras clave** | 30 pts | Análisis TF-IDF del objeto + palabras clave comunes |
| **Tipo contrato** | 15 pts | Servicios, Obras, Suministros |
| **Años anteriores** | 15 pts | Licitaciones de años previos (prioriza recientes) |
| **Bonus recencia** | 5 pts | Contratos más recientes tienen más peso |

**Total máximo:** ~160 puntos (permite identificar coincidencias múltiples)

### 4. 📊 Análisis Preciso de Bajas

- Detecta **patrones** en bajas históricas
- Busca grupos de bajas similares (±2%)
- Identifica empresas adjudicatarias más frecuentes
- Calcula baja media de cada empresa
- Considera **competitividad del sector**
- Proporciona explicación detallada de la recomendación

### 5. 📄 Informes Completos

- **Texto narrativo** listo para copiar en propuestas
- **Exportación a Excel** con múltiples hojas:
  - Resumen general
  - Objeto y CPV
  - Lotes (si existen)
  - Contratos similares encontrados
  - Criterios de adjudicación
- **Exportación a JSON** para integración
- **Visualizaciones interactivas** de distribución de bajas

## 🚀 Instalación y Uso

### Requisitos

```bash
pip install streamlit pandas numpy scikit-learn plotly requests xlsxwriter mysql-connector-python
```

### Ejecutar el Sistema

```bash
cd /Users/macintosh/Desktop/iasusar/presupuestos
streamlit run enhanced_xml_analyzer.py
```

### Cómo Usar

1. **Obtener URL del XML**
   - Ve a la Plataforma de Contratación del Estado
   - Busca la licitación que te interesa
   - Copia la URL del XML (preferiblemente la URL directa del servlet)

2. **Pegar URL en el sistema**
   - Introduce la URL en el campo correspondiente
   - El sistema detectará automáticamente si es HTML o XML

3. **Configurar análisis (opcional)**
   - Ajusta el número de contratos a analizar (1000-10000)
   - Modifica el score mínimo de similitud (20-50)

4. **Analizar**
   - Haz clic en "🚀 Analizar Licitación"
   - El sistema procesará en 4 fases:
     1. Extracción de datos del XML
     2. Búsqueda de licitaciones similares
     3. Cálculo de baja recomendada
     4. Generación de informe

5. **Usar resultados**
   - Copia el texto para tu propuesta
   - Descarga Excel para análisis detallado
   - Revisa licitaciones similares encontradas
   - Analiza adjudicatarios identificados

## 📖 Ejemplo de URL

**URL directa del XML (recomendada):**
```
https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?DocumentIdParam=...
```

**URL HTML (el sistema intentará convertir):**
```
https://contrataciondelestado.es/wps/poc?uri=deeplink:detalle_licitacion&idEvl=...
```

## 🎯 Mejoras Respecto al Sistema Anterior

### Extracción de Datos
- ✅ Ahora extrae **fecha de publicación**
- ✅ Detecta y extrae **lotes individuales**
- ✅ Captura **tipo de contrato** automáticamente
- ✅ Extrae criterios con **categorización** (precio/técnico)
- ✅ Obtiene **procedimiento** y **plazo de ejecución**
- ✅ Mejor manejo de **namespaces** del XML

### Sistema de IA
- 🤖 Algoritmo de scoring **más sofisticado**
- 🔍 Búsqueda por **palabras clave** importantes
- 📍 Considera **zonas geográficas cercanas**
- 📅 Prioriza contratos de **años anteriores**
- 🎯 Score mínimo ajustable (antes fijo)
- 📊 Ordenación inteligente por múltiples factores

### Análisis de Bajas
- 📈 Detecta **grupos de bajas similares**
- 🏢 Identifica empresas más frecuentes con **sus bajas medias**
- 🎲 Considera **competitividad del sector**
- 📉 Ajusta por **variabilidad** de los datos
- 💡 Proporciona **explicación detallada** de la lógica

### Informes
- 📊 Excel con **múltiples hojas** organizadas
- 📝 Texto más **variado y natural**
- 🔢 Incluye **estadísticas visuales**
- 📦 Información de **lotes** si existen
- 💾 Exportación a **JSON** para integración

## 🔧 Estructura del Código

```
EnhancedXMLAnalyzer (Clase principal)
├── extract_complete_contract_data()      # Extracción completa
│   ├── extract_lots()                    # Detectar y extraer lotes
│   └── extract_awarding_criteria_enhanced() # Criterios mejorados
├── find_similar_contratos_ai_enhanced()  # IA avanzada
│   ├── extract_keywords()                # Palabras clave
│   └── get_nearby_locations()            # Zonas cercanas
├── calculate_recommended_baja_enhanced() # Cálculo baja
├── generate_enhanced_report()            # Informe detallado
└── generate_texto_baja()                 # Texto narrativo

main()                                    # Interfaz Streamlit
└── create_excel_report()                 # Exportación Excel
```

## 📊 Ejemplo de Salida

### Datos Extraídos:
```
Fecha: 2025-09-22
PBL: 58,902.00 €
Tipo: Servicios
Objeto: Servicio de mantenimiento preventivo...
CPV: 50241000 (Servicios de reparación y mantenimiento de buques)
Localidad: Madrid
Lotes: No dividido en lotes
Criterios:
  - Criterios cualitativos: 20 puntos
  - Oferta económica: 80 PUNTOS
```

### Análisis IA:
```
🎯 Encontrados 15 contratos similares
📊 Coincidencias:
  - CPV coincidentes: 12/15
  - Localidad coincidente: 10/15
  - Precio similar: 8/15

💡 Baja Recomendada: 18.5%
Explicación: Grupo de 5+ licitaciones con bajas cercanas.
Baja más alta del grupo: 16.5% + 2% (sector competitivo)
```

### Empresas Identificadas:
```
🏢 Adjudicatarios más frecuentes:
  - EMPRESA A: 3 licitaciones - Baja media: 15.2%
  - EMPRESA B: 2 licitaciones - Baja media: 17.8%
  - EMPRESA C: 2 licitaciones - Baja media: 12.5%
```

## ⚠️ Notas Importantes

1. **Datos de Adjudicación**: Los campos `importe_adjudicacion`, `adjudicatario` y `num_licitadores` solo están disponibles en XMLs de adjudicación, no de licitación. El sistema intentará extraerlos si existen.

2. **Calidad de la BD**: La precisión del análisis depende de la calidad y cantidad de datos en la base de datos. Cuantos más contratos históricos, mejor.

3. **Lotes**: Si una licitación tiene lotes, el sistema los detectará automáticamente. Puedes analizar cada lote por separado si es necesario.

4. **Conexión BD**: El sistema puede funcionar sin conexión a BD (solo extracción XML), pero el análisis de similitudes requiere acceso a la base de datos.

## 🐛 Solución de Problemas

**Error: No se pueden extraer datos del XML**
- Verifica que la URL del XML sea correcta y accesible
- Comprueba que el XML tenga la estructura esperada
- Algunos XMLs pueden tener namespaces diferentes

**No se encuentran contratos similares**
- Reduce el score mínimo en configuración (prueba con 20-25)
- Aumenta el número de contratos a analizar
- Verifica que hay datos en la base de datos

**El sistema es lento**
- Reduce el número de contratos a analizar (prueba con 2000-3000)
- La primera ejecución es más lenta (carga de datos)
- Considera la velocidad de tu conexión de red

## 📧 Soporte

Para problemas o mejoras, contacta al equipo de desarrollo.

---

**Versión:** 2.0 - Sistema Mejorado con IA Avanzada
**Fecha:** Septiembre 2025
**Autor:** Sistema de Análisis de Licitaciones
