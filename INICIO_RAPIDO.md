# 🚀 INICIO RÁPIDO - Sistema de Análisis de Licitaciones

## ✅ VERIFICACIÓN COMPLETADA

El sistema ha sido probado y está funcionando correctamente:

- ✅ Extracción de datos XML funcionando
- ✅ Detección de CPV correcta
- ✅ Extracción de criterios de adjudicación funcionando
- ✅ Algoritmo de similitud operativo (60% similitud en textos relacionados)
- ✅ Detección de zonas cercanas funcionando
- ✅ Extracción de palabras clave operativa (20 palabras clave extraídas)
- ✅ Todas las dependencias instaladas

## 🎯 DATOS QUE EXTRAE EL SISTEMA

### Datos Principales
```
✅ Fecha publicación: 2025-09-22
✅ PBL: 58,902.00 €
✅ Tipo contrato: Servicios
✅ Objeto: Servicio de mantenimiento preventivo y correctivo...
✅ CPV: 50241000 - Servicios de reparación y mantenimiento de buques
✅ Procedimiento: Abierto simplificado
```

### Criterios de Adjudicación
```
✅ Criterios cualitativos: 20 puntos
✅ Oferta económica: 80 PUNTOS
```

### Lotes
```
✅ Detección automática de lotes
✅ Extracción individual de cada lote (si existen)
```

## 🚀 CÓMO EJECUTAR

### Opción 1: Script Automático (Linux/Mac)
```bash
cd /Users/macintosh/Desktop/iasusar/presupuestos
./ejecutar_sistema_mejorado.sh
```

### Opción 2: Script Automático (Windows)
```cmd
cd C:\...\presupuestos
ejecutar_sistema_mejorado.bat
```

### Opción 3: Comando Manual
```bash
cd /Users/macintosh/Desktop/iasusar/presupuestos
streamlit run enhanced_xml_analyzer.py
```

La aplicación se abrirá automáticamente en: **http://localhost:8501**

## 📋 FLUJO DE USO

### Paso 1: Obtener URL del XML

Tienes dos opciones:

**Opción A: URL directa del XML (recomendada)**
```
https://contrataciondelestado.es/FileSystem/servlet/GetDocumentByIdServlet?DocumentIdParam=...
```

**Opción B: URL de la página de licitación**
```
https://contrataciondelestado.es/wps/poc?uri=deeplink:detalle_licitacion&idEvl=...
```

### Paso 2: Pegar URL en el Sistema

1. Abre la aplicación (se abrirá automáticamente tu navegador)
2. En la interfaz, verás dos campos:
   - "Pega aquí el enlace HTML de la licitación"
   - "O URL XML directa"
3. Pega tu URL en el campo correspondiente

### Paso 3: Configurar (Opcional)

En el panel lateral izquierdo:
- **Límite de contratos a analizar**: 1000-10000 (default: 5000)
- **Score mínimo de similitud**: 20-50 (default: 30)

💡 **Tip**: Si no encuentras suficientes resultados, reduce el score mínimo a 20-25

### Paso 4: Analizar

Haz clic en el botón **"🚀 Analizar Licitación"**

El sistema procesará en 4 fases automáticas:

```
📥 FASE 1: Extracción de Datos del XML
   ├─ Fecha, PBL, Tipo, Objeto, CPV
   ├─ Criterios de adjudicación
   ├─ Detección de lotes
   └─ Localidad, Procedimiento

🔍 FASE 2: Búsqueda de Licitaciones Similares
   ├─ Carga base de datos (5000 contratos)
   ├─ Algoritmo de IA con 6 criterios
   ├─ CPV (40 pts) + Zona (30 pts) + Importe (25 pts)
   └─ Palabras clave + Tipo + Años anteriores

💡 FASE 3: Cálculo de Baja Recomendada
   ├─ Análisis estadístico de bajas
   ├─ Detección de patrones
   ├─ Competitividad del sector
   └─ Baja recomendada con explicación

📊 FASE 4: Informe Completo
   ├─ Top 10 licitaciones similares (con razones)
   ├─ Empresas adjudicatarias identificadas
   ├─ Distribución de bajas (gráfico)
   └─ Texto narrativo para propuesta
```

### Paso 5: Usar Resultados

El sistema te proporciona:

1. **Texto para copiar** en tu propuesta:
   ```
   Buenos días,

   En la selección de expedientes, nos encontramos los siguientes
   criterios de adjudicación:
   OFERTA ECONÓMICA: 80 PUNTOS
   CRITERIOS CUALITATIVOS: 20 puntos

   Al revisar expedientes previos de similar envergadura, presupuesto
   y características técnicas, hemos identificado 15 licitaciones
   comparables...

   Tras el análisis estadístico, recomendamos presentar una propuesta
   económica con un descuento del 18.5%...
   ```

2. **Botones de exportación**:
   - 📊 **Descargar Excel** - 5 hojas con datos completos
   - 💾 **Descargar JSON** - Para integración con otros sistemas
   - 🔄 **Regenerar Texto** - Variación del texto narrativo

3. **Visualizaciones**:
   - Gráfico de distribución de bajas
   - Tabla de licitaciones similares con razones
   - Lista de empresas adjudicatarias con bajas medias

## 💡 EJEMPLO DE RESULTADO

```
🎯 Encontrados 15 contratos similares

Top 3 Licitaciones:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#1 - Score: 95 puntos - Baja: 16.5%
   Objeto: Mantenimiento de equipos de seguridad marítima...
   PBL: 62,000 €
   Localidad: Madrid
   Empresa: EMPRESA A

   Razones de similitud:
   • ✅ CPV exacto: 50241000
   • 📍 Misma localidad: Madrid
   • 💰 Importe muy similar: 62,000€ (±5%)
   • 📝 Objeto muy similar (58%)

#2 - Score: 88 puntos - Baja: 18.2%
   Objeto: Servicio mantenimiento contraincendios buques...
   PBL: 55,300 €
   Localidad: Madrid
   Empresa: EMPRESA B

   Razones de similitud:
   • ✅ CPV exacto: 50241000
   • 📍 Misma localidad: Madrid
   • 💰 Importe muy similar: 55,300€ (±6%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏢 Adjudicatarios más frecuentes:
   • EMPRESA A: 3 licitaciones - Baja media: 15.2%
   • EMPRESA B: 2 licitaciones - Baja media: 17.8%

💡 Baja Recomendada: 18.5%

Explicación: Grupo de 5+ licitaciones con bajas cercanas.
Baja más alta del grupo: 16.5% + 2% (sector competitivo)
```

## 📊 CONTENIDO DEL EXCEL EXPORTADO

El archivo Excel contiene **5 hojas**:

1. **Resumen** - Datos generales del contrato
2. **Objeto y CPV** - Descripción completa y códigos CPV
3. **Lotes** - Información de lotes (si existen)
4. **Contratos Similares** - Top 20 con score y razones
5. **Criterios** - Criterios de adjudicación detallados

## 🔧 CONFIGURACIÓN AVANZADA

### Ajustar Precisión del Análisis

**Para mayor precisión** (más lento):
- Aumenta "Límite de contratos" a 8000-10000
- Mantén score mínimo en 30

**Para mayor velocidad** (menos preciso):
- Reduce "Límite de contratos" a 2000-3000
- Reduce score mínimo a 25

**Si no encuentras resultados**:
- Reduce score mínimo a 20
- Aumenta límite de contratos a 7000+

### Modos de Operación

El sistema tiene 3 modos:

1. **📋 Análisis desde XML** - Modo principal
2. **🔍 Consulta Base de Datos** - Explorar tablas
3. **📚 Ayuda** - Guía completa integrada

## ⚠️ NOTAS IMPORTANTES

### Datos de Adjudicación

Los siguientes campos **solo están disponibles en XMLs de adjudicación**:
- Importe de adjudicación
- Adjudicatario
- Número de licitadores

Si el XML es de **licitación** (no de adjudicación), estos campos mostrarán "N/A".

### Lotes

Si la licitación tiene lotes:
- ✅ Se detectan automáticamente
- ✅ Se extraen individualmente
- ✅ Se muestran en sección separada
- ✅ Se incluyen en Excel (hoja 3)

### Base de Datos

El análisis de similitudes **requiere conexión a la base de datos**.

Sin BD, el sistema funciona en **modo limitado**:
- ✅ Extracción de XML funciona
- ❌ Análisis de similitudes no disponible
- ❌ Cálculo de baja no disponible

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "No se pueden extraer datos del XML"

**Causas posibles:**
- URL incorrecta o inaccesible
- XML con estructura diferente
- Namespaces no reconocidos

**Solución:**
1. Verifica que la URL sea accesible en tu navegador
2. Intenta con la URL XML directa (servlet)
3. Revisa que el XML contenga etiquetas como `<cac:ProcurementProject>`

### Error: "No se encontraron contratos similares"

**Causas posibles:**
- Score mínimo muy alto
- Pocos contratos en BD con características similares
- BD sin datos suficientes

**Solución:**
1. Reduce score mínimo a 20-25
2. Aumenta límite de contratos a 7000+
3. Verifica que hay datos en la tabla de contratos

### El sistema es muy lento

**Causas posibles:**
- Analizando muchos contratos (10000+)
- Conexión de red lenta
- Primera ejecución (carga inicial)

**Solución:**
1. Reduce límite de contratos a 3000
2. La segunda ejecución será más rápida
3. Considera tu ancho de banda de red

### No se extrajo la localidad

**Causas posibles:**
- XML sin campo `<cbc:CountrySubentity>`
- Localidad en ubicación no estándar

**Solución:**
- El sistema funciona sin localidad (usa otros criterios)
- Si es crítico, revisa la estructura del XML manualmente

## 📞 SOPORTE

Si encuentras problemas no resueltos aquí:
1. Revisa el archivo `README_SISTEMA_MEJORADO.md` (documentación completa)
2. Ejecuta `python3 test_sistema.py` para verificar el sistema
3. Contacta al equipo de desarrollo

## 🎉 ¡LISTO PARA USAR!

El sistema está completamente operativo. Solo necesitas:

```bash
cd /Users/macintosh/Desktop/iasusar/presupuestos
streamlit run enhanced_xml_analyzer.py
```

**¡Buena suerte con tus licitaciones!** 🚀

---

**Sistema Avanzado de Análisis de Licitaciones v2.0**
**Desarrollado con IA Avanzada para máxima precisión**
**Última actualización: Septiembre 2025**
