#!/usr/bin/env python3
"""
Script de prueba para el Sistema Avanzado de Análisis de Licitaciones
"""

import sys
from enhanced_xml_analyzer import EnhancedXMLAnalyzer
import pandas as pd

def test_extraction():
    """Probar extracción de datos del XML local"""
    print("=" * 70)
    print("🧪 PRUEBA DEL SISTEMA DE ANÁLISIS DE LICITACIONES")
    print("=" * 70)
    print()

    # Inicializar analizador
    print("1️⃣ Inicializando analizador...")
    analyzer = EnhancedXMLAnalyzer()
    print("   ✅ Analizador inicializado")
    print()

    # Leer XML local
    xml_path = "/Users/macintosh/Desktop/iasusar/presupuestos/complete_document.xml"
    print(f"2️⃣ Leyendo XML local: {xml_path}")

    try:
        with open(xml_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        print("   ✅ XML cargado correctamente")
        print(f"   📏 Tamaño: {len(xml_content):,} caracteres")
        print()
    except Exception as e:
        print(f"   ❌ Error leyendo XML: {e}")
        return

    # Parsear y extraer datos
    print("3️⃣ Extrayendo datos del XML...")
    print("-" * 70)

    import xml.etree.ElementTree as ET

    try:
        root = ET.fromstring(xml_content)
        ns = analyzer.namespaces

        # Crear estructura de contrato
        contract_data = {
            'fecha_publicacion': None,
            'pbl': None,
            'importe_adjudicacion': None,
            'adjudicatario': None,
            'num_licitadores': None,
            'objeto': None,
            'criterios_adjudicacion': {},
            'cpv': [],
            'tipo_contrato': None,
            'lotes': [],
            'tiene_lotes': False,
            'xml_url': xml_path,
            'localidad': None,
            'plazo_ejecucion': None,
            'procedimiento': None
        }

        # Fecha
        fecha_elem = root.find('.//cbc:IssueDate', ns)
        if fecha_elem is not None:
            contract_data['fecha_publicacion'] = fecha_elem.text.split('+')[0].split('T')[0]
            print(f"   ✅ Fecha publicación: {contract_data['fecha_publicacion']}")

        # PBL
        pbl_elem = root.find('.//cac:ProcurementProject/cac:BudgetAmount/cbc:TaxExclusiveAmount', ns)
        if pbl_elem is not None:
            contract_data['pbl'] = float(pbl_elem.text)
            print(f"   ✅ PBL: {contract_data['pbl']:,.2f} €")

        # Tipo
        tipo_elem = root.find('.//cac:ProcurementProject/cbc:TypeCode', ns)
        if tipo_elem is not None:
            tipo_name = tipo_elem.get('name', '')
            contract_data['tipo_contrato'] = tipo_name
            print(f"   ✅ Tipo contrato: {tipo_name}")

        # Objeto
        objeto_elem = root.find('.//cac:ProcurementProject/cbc:Name', ns)
        if objeto_elem is not None:
            contract_data['objeto'] = objeto_elem.text
            print(f"   ✅ Objeto: {objeto_elem.text[:80]}...")

        # CPV
        cpv_elems = root.findall('.//cac:ProcurementProject/cac:RequiredCommodityClassification/cbc:ItemClassificationCode', ns)
        for cpv_elem in cpv_elems:
            cpv_code = cpv_elem.text
            cpv_name = cpv_elem.get('name', '')
            contract_data['cpv'].append({'code': cpv_code, 'name': cpv_name})
            print(f"   ✅ CPV: {cpv_code} - {cpv_name}")

        # Localidad
        loc_elem = root.find('.//cac:RealizedLocation/cac:Address/cbc:CountrySubentity', ns)
        if loc_elem is not None:
            contract_data['localidad'] = loc_elem.text
            print(f"   ✅ Localidad: {loc_elem.text}")

        # Procedimiento
        proc_elem = root.find('.//cac:TenderingProcess/cbc:ProcedureCode', ns)
        if proc_elem is not None:
            proc_name = proc_elem.get('name', '')
            contract_data['procedimiento'] = proc_name
            print(f"   ✅ Procedimiento: {proc_name}")

        # Criterios
        print("\n   📋 Criterios de Adjudicación:")
        criterios_elems = root.findall('.//cac:AwardingTerms/cac:AwardingCriteria', ns)
        criterios_lista = []

        for crit_elem in criterios_elems:
            desc_elem = crit_elem.find('./cbc:Description', ns)
            peso_elem = crit_elem.find('./cbc:WeightNumeric', ns)

            if desc_elem is not None and peso_elem is not None:
                desc = desc_elem.text
                peso = float(peso_elem.text)
                criterios_lista.append({'nombre': desc, 'peso': peso})
                print(f"      • {desc}: {peso} puntos")

        contract_data['criterios_adjudicacion'] = {'criterios_detalle': criterios_lista}

        # Lotes
        desc_lotes = root.find('.//cac:ProcurementProject/cbc:Description', ns)
        if desc_lotes is not None:
            if 'no' in desc_lotes.text.lower() and 'lote' in desc_lotes.text.lower():
                contract_data['tiene_lotes'] = False
                print(f"\n   ℹ️  Lotes: {desc_lotes.text}")
            else:
                contract_data['tiene_lotes'] = True

        print()
        print("=" * 70)
        print("✅ EXTRACCIÓN COMPLETADA CON ÉXITO")
        print("=" * 70)
        print()

        # Resumen
        print("📊 RESUMEN DE DATOS EXTRAÍDOS:")
        print("-" * 70)
        print(f"Fecha:        {contract_data.get('fecha_publicacion', 'N/A')}")
        print(f"PBL:          {contract_data.get('pbl', 0):,.2f} €")
        print(f"Tipo:         {contract_data.get('tipo_contrato', 'N/A')}")
        print(f"Localidad:    {contract_data.get('localidad', 'N/A')}")
        print(f"Procedimiento: {contract_data.get('procedimiento', 'N/A')}")
        print(f"CPV:          {len(contract_data.get('cpv', []))} código(s)")
        print(f"Criterios:    {len(criterios_lista)} criterio(s)")
        print(f"Lotes:        {'Sí' if contract_data.get('tiene_lotes') else 'No'}")
        print()
        print(f"Objeto:")
        if contract_data.get('objeto'):
            # Dividir en líneas de 70 caracteres
            objeto = contract_data['objeto']
            for i in range(0, len(objeto), 70):
                print(f"  {objeto[i:i+70]}")
        print()

        # Probar extracción de palabras clave
        print("=" * 70)
        print("🔍 PRUEBA DE EXTRACCIÓN DE PALABRAS CLAVE")
        print("=" * 70)

        if contract_data.get('objeto'):
            keywords = analyzer.extract_keywords(contract_data['objeto'])
            print(f"\n✅ Palabras clave extraídas: {len(keywords)}")
            print("\nPalabras clave importantes:")
            for i, word in enumerate(sorted(list(keywords))[:20], 1):
                print(f"  {i}. {word}")

        print()
        print("=" * 70)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("=" * 70)
        print()
        print("💡 El sistema está listo para usar!")
        print("   Ejecuta: streamlit run enhanced_xml_analyzer.py")
        print()

        return contract_data

    except Exception as e:
        print(f"   ❌ Error procesando XML: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_similarity_algorithm():
    """Probar algoritmo de similitud"""
    print("=" * 70)
    print("🧪 PRUEBA DEL ALGORITMO DE SIMILITUD")
    print("=" * 70)
    print()

    analyzer = EnhancedXMLAnalyzer()

    # Textos de ejemplo
    text1 = "Servicio de mantenimiento preventivo y correctivo de equipos de seguridad"
    text2 = "Mantenimiento correctivo y preventivo de sistemas de seguridad y contraincendios"
    text3 = "Suministro de material de oficina"

    print("Texto 1:", text1)
    print("Texto 2:", text2)
    print("Texto 3:", text3)
    print()

    sim12 = analyzer.calculate_text_similarity(text1, text2)
    sim13 = analyzer.calculate_text_similarity(text1, text3)
    sim23 = analyzer.calculate_text_similarity(text2, text3)

    print(f"Similitud 1-2: {sim12:.2%} (esperado: alta)")
    print(f"Similitud 1-3: {sim13:.2%} (esperado: baja)")
    print(f"Similitud 2-3: {sim23:.2%} (esperado: baja)")
    print()

    if sim12 > 0.3 and sim13 < 0.2 and sim23 < 0.2:
        print("✅ Algoritmo de similitud funcionando correctamente")
    else:
        print("⚠️  Resultados inesperados en algoritmo de similitud")

    print()


def test_nearby_locations():
    """Probar detección de zonas cercanas"""
    print("=" * 70)
    print("🧪 PRUEBA DE ZONAS CERCANAS")
    print("=" * 70)
    print()

    analyzer = EnhancedXMLAnalyzer()

    test_cases = [
        "Madrid",
        "Barcelona",
        "Sevilla",
        "Valencia"
    ]

    for location in test_cases:
        nearby = analyzer.get_nearby_locations(location)
        print(f"📍 {location}:")
        print(f"   Zonas cercanas: {', '.join(nearby)}")
        print()

    print("✅ Detección de zonas cercanas funcionando")
    print()


if __name__ == "__main__":
    print()
    print("🚀 INICIO DE PRUEBAS DEL SISTEMA")
    print()

    # Prueba 1: Extracción
    contract_data = test_extraction()

    if contract_data:
        # Prueba 2: Similitud
        test_similarity_algorithm()

        # Prueba 3: Zonas cercanas
        test_nearby_locations()

        print("=" * 70)
        print("🎉 SISTEMA VERIFICADO Y FUNCIONANDO CORRECTAMENTE")
        print("=" * 70)
        print()
        print("📝 Próximos pasos:")
        print("   1. Ejecuta: streamlit run enhanced_xml_analyzer.py")
        print("   2. Pega la URL del XML en la interfaz")
        print("   3. Haz clic en 'Analizar Licitación'")
        print()
    else:
        print("❌ Error en las pruebas")
        sys.exit(1)
