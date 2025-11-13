# 🌐 Sistema Avanzado de Análisis de Licitaciones con IA

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tu-app.streamlit.app)

Sistema inteligente para analizar licitaciones públicas españolas con extracción automática de datos XML y búsqueda de similitudes mediante IA avanzada.

## 🎯 Características

### Extracción Completa de Datos
- ✅ Fecha de publicación, PBL, Tipo de contrato
- ✅ Objeto completo y códigos CPV
- ✅ Criterios de adjudicación detallados
- ✅ Detección automática de lotes
- ✅ Localidad, procedimiento y plazo

### IA Avanzada para Similitudes
Sistema de scoring con 6 criterios (máx. 160 puntos):
- **CPV (40 pts)** - Coincidencia exacta, división o categoría
- **Zona (30 pts)** - Misma localidad o zonas cercanas
- **Importe (25 pts)** - Presupuesto similar (±20%, ±40%, ±60%)
- **Palabras clave (30 pts)** - Análisis TF-IDF del objeto
- **Tipo contrato (15 pts)** - Servicios, Obras, Suministros
- **Años anteriores (15 pts)** - Licitaciones previas

### Análisis de Bajas
- Patrones estadísticos y grupos de bajas similares
- Identificación de empresas adjudicatarias con bajas medias
- Consideración de competitividad del sector
- Explicación detallada de la recomendación

### Informes Completos
- Texto narrativo para propuestas
- Exportación a Excel (5 hojas)
- Exportación a JSON
- Visualizaciones interactivas

## 🚀 Inicio Rápido

### Uso en Streamlit Cloud
1. Visita la aplicación: [https://tu-app.streamlit.app](https://tu-app.streamlit.app)
2. Pega la URL del XML de la licitación
3. Haz clic en "Analizar Licitación"
4. Descarga los resultados en Excel o copia el texto

### Uso Local

#### Instalación
```bash
git clone https://github.com/TU_USUARIO/presupuestos.git
cd presupuestos
pip install -r requirements.txt
```

#### Ejecución
```bash
streamlit run enhanced_xml_analyzer.py
```

La aplicación se abrirá en `http://localhost:8501`

## 📋 Requisitos

- Python 3.8+
- Conexión a base de datos MySQL (opcional para análisis completo)

## 🔧 Configuración

### Base de Datos (Opcional)

Si quieres usar el análisis de similitudes, configura las credenciales:

**Local:** Crea `.streamlit/secrets.toml`:
```toml
[database]
host = "tu-host.com"
port = 3306
user = "tu-usuario"
password = "tu-password"
database = "tu-base-datos"
```

**Streamlit Cloud:** Ve a Settings > Secrets y añade:
```toml
[database]
host = "tu-host.com"
port = 3306
user = "tu-usuario"
password = "tu-password"
database = "tu-base-datos"
```

## 📊 Ejemplo de Uso

```python
# 1. Obtén la URL del XML de la Plataforma de Contratación del Estado
xml_url = "https://contrataciondelestado.es/FileSystem/servlet/..."

# 2. Pega la URL en la interfaz de Streamlit

# 3. El sistema automáticamente:
#    - Extrae todos los datos del XML
#    - Busca licitaciones similares con IA
#    - Calcula baja recomendada
#    - Genera informe completo
```

## 🧪 Testing

Ejecuta las pruebas:
```bash
python3 test_sistema.py
```

## 📚 Documentación

- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Guía paso a paso
- **[README_SISTEMA_MEJORADO.md](README_SISTEMA_MEJORADO.md)** - Documentación técnica
- **[INDEX_ARCHIVOS.md](INDEX_ARCHIVOS.md)** - Índice del proyecto

## 🎯 Flujo de Trabajo

```
Usuario → Pega URL XML
    ↓
FASE 1: Extracción de datos (11+ campos)
    ↓
FASE 2: Búsqueda IA (6 criterios)
    ↓
FASE 3: Cálculo baja recomendada
    ↓
FASE 4: Informe completo
    ↓
Usuario → Descarga Excel/JSON o copia texto
```

## 📈 Resultados

El sistema proporciona:
- Top 20 licitaciones similares con razones
- Empresas adjudicatarias identificadas con bajas medias
- Baja recomendada con explicación detallada
- Distribución de bajas en gráfico interactivo
- Texto narrativo listo para copiar en propuestas

## 🛠️ Tecnologías

- **Streamlit** - Interfaz web interactiva
- **Pandas & NumPy** - Análisis de datos
- **Scikit-learn** - Algoritmos de IA (TF-IDF, similitud)
- **Plotly** - Visualizaciones interactivas
- **MySQL** - Base de datos de contratos
- **XlsxWriter** - Exportación a Excel

## 📦 Estructura del Proyecto

```
presupuestos/
├── enhanced_xml_analyzer.py    # Sistema principal
├── requirements.txt            # Dependencias
├── .streamlit/
│   ├── config.toml            # Configuración Streamlit
│   └── secrets.toml.example   # Ejemplo de secretos
├── test_sistema.py            # Suite de pruebas
├── README.md                  # Este archivo
├── INICIO_RAPIDO.md          # Guía rápida
└── README_SISTEMA_MEJORADO.md # Docs técnicas
```

## 🔐 Seguridad

- Las credenciales de BD NO se incluyen en el repositorio
- Usa `.streamlit/secrets.toml` (excluido por `.gitignore`)
- En Streamlit Cloud, configura secretos en Settings

## 🐛 Solución de Problemas

### Error: No se pueden extraer datos del XML
- Verifica que la URL sea accesible
- Comprueba que el XML tenga estructura válida

### Error: No se encontraron contratos similares
- Reduce el score mínimo a 20-25
- Aumenta el límite de contratos a 7000+

### El sistema es lento
- Reduce límite de contratos a 3000
- Primera ejecución es más lenta (carga inicial)

## 📝 Notas

- Los datos de adjudicación solo están en XMLs de adjudicación
- El análisis de similitudes requiere conexión a BD
- Sin BD, el sistema funciona en modo limitado (solo extracción XML)

## 🤝 Contribuciones

Este es un proyecto interno. Para mejoras, contacta al equipo de desarrollo.

## 📄 Licencia

Uso interno de IASUSAR.

## 📧 Soporte

Para soporte técnico, contacta al equipo de desarrollo.

---

**Versión 2.0** - Sistema Mejorado con IA Avanzada
**Última actualización:** Septiembre 2025
**Desarrollado por:** Sistema de Análisis de Licitaciones
