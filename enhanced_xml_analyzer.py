import mysql.connector
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import random
import requests
import xml.etree.ElementTree as ET
from urllib.parse import unquote
import time
import io
from xlsxwriter import Workbook
import warnings
import json
from collections import Counter
warnings.filterwarnings('ignore')

class EnhancedXMLAnalyzer:
    """
    Analizador mejorado de XML con extracción completa de datos,
    detección de lotes y análisis de IA avanzado
    """
    def __init__(self):
        self.connection = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # Namespaces comunes en XML de contratación
        self.namespaces = {
            'cac': 'urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2',
            'cbc': 'urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2',
            'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
            'efac': 'http://data.europa.eu/p27/eforms-ubl-extensions/1',
            'efext': 'http://data.europa.eu/p27/eforms-ubl-extension-aggregate-components/1',
            'efbc': 'http://data.europa.eu/p27/eforms-ubl-extension-basic-components/1'
        }

    def connect_to_database(self):
        """Conectar a la base de datos MySQL"""
        try:
            # Intentar obtener credenciales desde Streamlit secrets (Cloud)
            if hasattr(st, 'secrets') and 'database' in st.secrets:
                db_config = st.secrets['database']
                self.connection = mysql.connector.connect(
                    host=db_config.get('host', 'ocleminformatica.com'),
                    port=int(db_config.get('port', 3306)),
                    user=db_config.get('user', 'colossus'),
                    password=db_config['password'],
                    database=db_config.get('database', 'colossus_vgarcia')
                )
            else:
                # Fallback: credenciales locales (solo para desarrollo)
                self.connection = mysql.connector.connect(
                    host='ocleminformatica.com',
                    port=3306,
                    user='colossus',
                    password='OIN2020p$j',
                    database='colossus_vgarcia'
                )
            return True
        except Exception as e:
            st.error(f"Error conectando a la base de datos: {e}")
            st.info("💡 Si estás en Streamlit Cloud, configura los secretos en Settings > Secrets")
            return False

    def extract_complete_contract_data(self, xml_url):
        """
        Extracción COMPLETA de todos los datos del contrato desde XML
        Incluye: fecha, PBL, objeto, CPV, tipo, criterios, lotes, etc.
        """
        try:
            st.info("🔍 Extrayendo datos completos del XML...")

            # Realizar petición al XML
            response = requests.get(xml_url, headers=self.headers, timeout=15)
            response.raise_for_status()

            # Parsear XML
            root = ET.fromstring(response.content)
            ns = self.namespaces

            contract_data = {
                'fecha_publicacion': None,
                'pbl': None,  # Presupuesto Base Licitación
                'importe_adjudicacion': None,
                'adjudicatario': None,
                'num_licitadores': None,
                'objeto': None,
                'criterios_adjudicacion': {},
                'cpv': [],
                'tipo_contrato': None,
                'lotes': [],  # Lista de lotes si existen
                'tiene_lotes': False,
                'xml_url': xml_url,
                'localidad': None,
                'plazo_ejecucion': None,
                'procedimiento': None
            }

            # 1. FECHA DE PUBLICACIÓN
            fecha_paths = [
                './/cbc:IssueDate',
                './/cbc:PublicationDate',
                './/cac:CallForTenders/cbc:IssueDate'
            ]
            for path in fecha_paths:
                elem = root.find(path, ns)
                if elem is not None and elem.text:
                    try:
                        # Parsear fecha (puede venir con timezone)
                        fecha_str = elem.text.split('+')[0].split('T')[0]
                        contract_data['fecha_publicacion'] = fecha_str
                        st.success(f"✅ Fecha publicación: {fecha_str}")
                        break
                    except:
                        continue

            # 2. TIPO DE CONTRATO
            tipo_paths = [
                './/cac:ProcurementProject/cbc:TypeCode',
                './/cbc:TypeCode[@listURI="http://contrataciondelestado.es/codice/cl/2.08/ContractCode-2.08.gc"]'
            ]
            for path in tipo_paths:
                elem = root.find(path, ns)
                if elem is not None:
                    tipo_code = elem.text if elem.text else None
                    tipo_name = elem.get('name', '')

                    # Mapeo de códigos a nombres
                    tipo_map = {
                        '1': 'Obras',
                        '2': 'Servicios',
                        '3': 'Suministros',
                        '7': 'Administrativo especial',
                        '8': 'Privado'
                    }

                    tipo_final = tipo_name if tipo_name else tipo_map.get(tipo_code, f'Tipo {tipo_code}')
                    contract_data['tipo_contrato'] = tipo_final
                    st.success(f"✅ Tipo contrato: {tipo_final}")
                    break

            # 3. PRESUPUESTO BASE DE LICITACIÓN (PBL)
            pbl_paths = [
                './/cac:ProcurementProject/cac:BudgetAmount/cbc:TaxExclusiveAmount',
                './/cac:BudgetAmount/cbc:TaxExclusiveAmount',
                './/cac:ProcurementProject/cac:BudgetAmount/cbc:EstimatedOverallContractAmount',
                './/cbc:EstimatedOverallContractAmount',
                './/cac:RequestedTenderTotal/cbc:EstimatedOverallContractAmount',
                './/cac:BudgetAmount/cbc:TotalAmount'
            ]
            for path in pbl_paths:
                elem = root.find(path, ns)
                if elem is not None and elem.text:
                    try:
                        pbl_value = float(elem.text.strip())
                        if pbl_value > 100:  # Validar que sea razonable
                            contract_data['pbl'] = pbl_value
                            st.success(f"✅ PBL encontrado: {pbl_value:,.2f} €")
                            break
                    except:
                        continue

            # 4. OBJETO DEL CONTRATO
            objeto_paths = [
                './/cac:ProcurementProject/cbc:Name',
                './cac:ProcurementProject/cbc:Name',
                './/cac:ProcurementProject/cbc:Description',
                './/cbc:Name[not(ancestor::cac:ContractingParty)]',
                './/cbc:Description[not(ancestor::cac:ContractingParty)]'
            ]
            for path in objeto_paths:
                elem = root.find(path, ns)
                if elem is not None and elem.text:
                    text = elem.text.strip()
                    # Evitar nombres del órgano de contratación
                    if len(text) > 20 and not any(word in text.lower() for word in ['instituto', 'ministerio', 'ayuntamiento'] if len(text) < 80):
                        contract_data['objeto'] = text
                        st.success(f"✅ Objeto: {text[:80]}...")
                        break

            # 5. CÓDIGOS CPV
            cpv_paths = [
                './/cac:ProcurementProject/cac:RequiredCommodityClassification/cbc:ItemClassificationCode',
                './/cac:RequiredCommodityClassification/cbc:ItemClassificationCode',
                './/cac:AdditionalCommodityClassification/cbc:ItemClassificationCode',
                './/cac:CommodityClassification/cbc:ItemClassificationCode',
                './/cbc:ItemClassificationCode'
            ]

            cpvs_found = set()
            for path in cpv_paths:
                elements = root.findall(path, ns)
                for elem in elements:
                    if elem.text:
                        cpv_code = elem.text.strip()
                        cpv_name = elem.get('name', '')
                        # Limpiar CPV - tomar solo los primeros 8 dígitos
                        cpv_clean = re.sub(r'[^\d]', '', cpv_code)[:8]
                        if len(cpv_clean) == 8:
                            cpvs_found.add((cpv_clean, cpv_name))

            contract_data['cpv'] = [{'code': cpv[0], 'name': cpv[1]} for cpv in cpvs_found]
            if contract_data['cpv']:
                st.success(f"✅ CPV encontrados: {len(contract_data['cpv'])} códigos")

            # 6. LOCALIDAD
            localidad_paths = [
                './/cac:RealizedLocation/cac:Address/cbc:CountrySubentity',
                './/cac:RealizedLocation/cbc:CountrySubentity',
                './/cac:ProcurementProject/cac:RealizedLocation/cac:Address/cbc:CountrySubentity',
                './/cac:Address/cbc:CountrySubentity',
                './/cac:RealizedLocation/cac:Address/cbc:CityName',
                './/cac:Address/cbc:CityName'
            ]
            for path in localidad_paths:
                elem = root.find(path, ns)
                if elem is not None and elem.text:
                    localidad = elem.text.strip()
                    if len(localidad) > 2:
                        contract_data['localidad'] = localidad
                        st.success(f"✅ Localidad: {localidad}")
                        break

            # 7. PROCEDIMIENTO
            proc_elem = root.find('.//cac:TenderingProcess/cbc:ProcedureCode', ns)
            if proc_elem is not None:
                proc_name = proc_elem.get('name', proc_elem.text)
                contract_data['procedimiento'] = proc_name
                st.info(f"📋 Procedimiento: {proc_name}")

            # 8. PLAZO DE EJECUCIÓN
            plazo_start = root.find('.//cac:PlannedPeriod/cbc:StartDate', ns)
            plazo_end = root.find('.//cac:PlannedPeriod/cbc:EndDate', ns)
            if plazo_start is not None and plazo_end is not None:
                try:
                    start_date = plazo_start.text.split('+')[0].split('T')[0]
                    end_date = plazo_end.text.split('+')[0].split('T')[0]
                    contract_data['plazo_ejecucion'] = f"{start_date} a {end_date}"
                except:
                    pass

            # 9. CRITERIOS DE ADJUDICACIÓN
            contract_data['criterios_adjudicacion'] = self.extract_awarding_criteria_enhanced(root, ns)

            # 10. DETECCIÓN Y EXTRACCIÓN DE LOTES
            contract_data = self.extract_lots(root, ns, contract_data)

            # 11. NÚMERO DE LICITADORES (si está disponible - normalmente en adjudicación)
            # Este dato suele estar en el XML de adjudicación, no de licitación
            num_tenderers = root.findall('.//cac:TendererParty', ns)
            if num_tenderers:
                contract_data['num_licitadores'] = len(num_tenderers)
                st.info(f"📊 Número de licitadores: {len(num_tenderers)}")

            # 12. IMPORTE DE ADJUDICACIÓN Y ADJUDICATARIO (si disponible)
            # Estos datos normalmente están en XML de adjudicación, no de licitación
            adjudicacion_elem = root.find('.//cac:AwardedTenderedProject', ns)
            if adjudicacion_elem is not None:
                # Importe adjudicación
                importe_elem = adjudicacion_elem.find('.//cbc:PayableAmount', ns)
                if importe_elem is not None and importe_elem.text:
                    try:
                        contract_data['importe_adjudicacion'] = float(importe_elem.text.strip())
                        st.success(f"✅ Importe adjudicación: {contract_data['importe_adjudicacion']:,.2f} €")
                    except:
                        pass

                # Adjudicatario
                adjudicatario_elem = adjudicacion_elem.find('.//cac:LegalMonetaryTotal/cbc:PayableAmount', ns)
                if adjudicatario_elem is not None:
                    party_name = adjudicacion_elem.find('.//cac:Party/cac:PartyName/cbc:Name', ns)
                    if party_name is not None and party_name.text:
                        contract_data['adjudicatario'] = party_name.text.strip()
                        st.success(f"✅ Adjudicatario: {contract_data['adjudicatario']}")

            # Mostrar resumen de datos extraídos
            self.show_extraction_summary(contract_data)

            return contract_data

        except requests.RequestException as e:
            st.error(f"Error al acceder al XML: {e}")
            return None
        except ET.ParseError as e:
            st.error(f"Error parseando XML: {e}")
            return None
        except Exception as e:
            st.error(f"Error procesando XML: {e}")
            import traceback
            st.error(traceback.format_exc())
            return None

    def extract_lots(self, root, ns, contract_data):
        """
        Detectar y extraer información de lotes individuales
        """
        # Buscar elementos de lotes
        lot_elements = root.findall('.//cac:ProcurementProjectLot', ns)

        if not lot_elements:
            # Verificar si hay descripción de "no hay lotes"
            desc_elem = root.find('.//cac:ProcurementProject/cbc:Description', ns)
            if desc_elem is not None and desc_elem.text:
                if 'no' in desc_elem.text.lower() and 'lote' in desc_elem.text.lower():
                    st.info("ℹ️ Licitación sin división en lotes")
                    contract_data['tiene_lotes'] = False
                    return contract_data

        if lot_elements:
            st.success(f"✅ Detectados {len(lot_elements)} lotes")
            contract_data['tiene_lotes'] = True

            for i, lot_elem in enumerate(lot_elements):
                lote_data = {
                    'numero': i + 1,
                    'id': None,
                    'descripcion': None,
                    'pbl': None,
                    'cpv': [],
                    'importe_adjudicacion': None,
                    'adjudicatario': None,
                    'num_licitadores': None
                }

                # ID del lote
                id_elem = lot_elem.find('.//cbc:ID', ns)
                if id_elem is not None and id_elem.text:
                    lote_data['id'] = id_elem.text.strip()

                # Descripción del lote
                desc_paths = [
                    './/cac:ProcurementProject/cbc:Name',
                    './/cac:ProcurementProject/cbc:Description',
                    './/cbc:Description'
                ]
                for path in desc_paths:
                    desc_elem = lot_elem.find(path, ns)
                    if desc_elem is not None and desc_elem.text:
                        lote_data['descripcion'] = desc_elem.text.strip()
                        break

                # PBL del lote
                pbl_paths = [
                    './/cac:ProcurementProject/cac:BudgetAmount/cbc:TaxExclusiveAmount',
                    './/cac:BudgetAmount/cbc:TaxExclusiveAmount'
                ]
                for path in pbl_paths:
                    pbl_elem = lot_elem.find(path, ns)
                    if pbl_elem is not None and pbl_elem.text:
                        try:
                            lote_data['pbl'] = float(pbl_elem.text.strip())
                            break
                        except:
                            continue

                # CPV del lote
                cpv_elems = lot_elem.findall('.//cac:RequiredCommodityClassification/cbc:ItemClassificationCode', ns)
                cpv_lote = []
                for cpv_elem in cpv_elems:
                    if cpv_elem.text:
                        cpv_code = re.sub(r'[^\d]', '', cpv_elem.text.strip())[:8]
                        cpv_name = cpv_elem.get('name', '')
                        if len(cpv_code) == 8:
                            cpv_lote.append({'code': cpv_code, 'name': cpv_name})
                lote_data['cpv'] = cpv_lote

                # Información de adjudicación del lote (si disponible)
                award_elem = lot_elem.find('.//cac:TenderResult', ns)
                if award_elem is not None:
                    # Importe adjudicación
                    importe_elem = award_elem.find('.//cbc:AwardedTenderedProject/cac:LegalMonetaryTotal/cbc:PayableAmount', ns)
                    if importe_elem is not None and importe_elem.text:
                        try:
                            lote_data['importe_adjudicacion'] = float(importe_elem.text.strip())
                        except:
                            pass

                    # Adjudicatario
                    party_name = award_elem.find('.//cac:WinningParty/cac:PartyName/cbc:Name', ns)
                    if party_name is not None and party_name.text:
                        lote_data['adjudicatario'] = party_name.text.strip()

                    # Número de licitadores
                    tenderers = award_elem.findall('.//cac:TendererParty', ns)
                    if tenderers:
                        lote_data['num_licitadores'] = len(tenderers)

                contract_data['lotes'].append(lote_data)

                st.info(f"📦 Lote {i+1}: {lote_data.get('descripcion', 'Sin descripción')[:60]}...")
        else:
            contract_data['tiene_lotes'] = False

        return contract_data

    def extract_awarding_criteria_enhanced(self, root, ns):
        """
        Extraer criterios de adjudicación de forma mejorada
        """
        criterios = {
            'precio_puntos': None,
            'tecnico_puntos': None,
            'total_puntos': 100,
            'criterios_detalle': [],
            'descripcion_raw': ''
        }

        try:
            # Buscar AwardingCriteria
            awarding_criteria_elems = root.findall('.//cac:AwardingTerms/cac:AwardingCriteria', ns)

            if not awarding_criteria_elems:
                # Buscar sin namespace
                awarding_criteria_elems = root.findall('.//AwardingCriteria')

            if awarding_criteria_elems:
                st.info(f"✅ Encontrados {len(awarding_criteria_elems)} criterios de adjudicación")

                for criterio_elem in awarding_criteria_elems:
                    criterio_info = {
                        'id': None,
                        'nombre': '',
                        'descripcion': '',
                        'peso': None,
                        'tipo': '',
                        'subtipo': ''
                    }

                    # ID
                    id_elem = criterio_elem.find('./cbc:ID', ns) or criterio_elem.find('ID')
                    if id_elem is not None and id_elem.text:
                        criterio_info['id'] = id_elem.text.strip()

                    # Descripción
                    desc_elem = criterio_elem.find('./cbc:Description', ns) or criterio_elem.find('Description')
                    if desc_elem is not None and desc_elem.text:
                        criterio_info['descripcion'] = desc_elem.text.strip()
                        criterio_info['nombre'] = desc_elem.text.strip()

                    # Peso
                    weight_elem = criterio_elem.find('./cbc:WeightNumeric', ns) or criterio_elem.find('WeightNumeric')
                    if weight_elem is not None and weight_elem.text:
                        try:
                            criterio_info['peso'] = float(weight_elem.text.strip())
                        except:
                            pass

                    # Tipo y subtipo
                    type_elem = criterio_elem.find('./cbc:AwardingCriteriaTypeCode', ns)
                    if type_elem is not None:
                        criterio_info['tipo'] = type_elem.get('name', type_elem.text)

                    subtype_elem = criterio_elem.find('./cbc:AwardingCriteriaSubTypeCode', ns)
                    if subtype_elem is not None:
                        criterio_info['subtipo'] = subtype_elem.get('name', subtype_elem.text)

                    # Determinar si es precio o técnico
                    nombre_lower = criterio_info['nombre'].lower()
                    desc_lower = criterio_info['descripcion'].lower()
                    subtipo_lower = criterio_info['subtipo'].lower() if criterio_info['subtipo'] else ''

                    if any(word in nombre_lower + desc_lower + subtipo_lower for word in ['precio', 'económic', 'ofertas', 'coste', 'importe']):
                        criterio_info['categoria'] = 'precio'
                    elif any(word in nombre_lower + desc_lower + subtipo_lower for word in ['técnic', 'calidad', 'memoria', 'propuesta', 'valor', 'cualitativ']):
                        criterio_info['categoria'] = 'tecnico'
                    else:
                        criterio_info['categoria'] = 'otro'

                    if criterio_info['nombre'] or criterio_info['descripcion']:
                        criterios['criterios_detalle'].append(criterio_info)

                # Calcular totales
                precio_total = sum(c['peso'] for c in criterios['criterios_detalle'] if c['peso'] and c['categoria'] == 'precio')
                tecnico_total = sum(c['peso'] for c in criterios['criterios_detalle'] if c['peso'] and c['categoria'] == 'tecnico')

                if precio_total > 0 or tecnico_total > 0:
                    criterios['precio_puntos'] = precio_total
                    criterios['tecnico_puntos'] = tecnico_total
                    criterios['total_puntos'] = precio_total + tecnico_total

                    # Normalizar a 100 si es necesario
                    if criterios['total_puntos'] != 100 and criterios['total_puntos'] > 0:
                        factor = 100 / criterios['total_puntos']
                        criterios['precio_puntos'] = round(precio_total * factor, 2)
                        criterios['tecnico_puntos'] = round(tecnico_total * factor, 2)
                        criterios['total_puntos'] = 100

        except Exception as e:
            st.warning(f"Error extrayendo criterios: {e}")

        return criterios

    def show_extraction_summary(self, contract_data):
        """
        Mostrar resumen visual de los datos extraídos
        """
        with st.expander("📋 Resumen de Datos Extraídos"):
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Datos Generales:**")
                st.write(f"- Fecha: {contract_data.get('fecha_publicacion', '❌ No encontrada')}")
                st.write(f"- PBL: {contract_data.get('pbl', 'N/A'):,.2f} €" if contract_data.get('pbl') else "- PBL: ❌ No encontrado")
                st.write(f"- Tipo: {contract_data.get('tipo_contrato', '❌ No encontrado')}")
                st.write(f"- Localidad: {contract_data.get('localidad', '❌ No encontrada')}")
                st.write(f"- Procedimiento: {contract_data.get('procedimiento', 'N/A')}")

            with col2:
                st.write("**Lotes y Adjudicación:**")
                st.write(f"- Tiene lotes: {'✅ Sí' if contract_data.get('tiene_lotes') else '❌ No'}")
                if contract_data.get('tiene_lotes'):
                    st.write(f"- Número de lotes: {len(contract_data.get('lotes', []))}")
                st.write(f"- CPV: {len(contract_data.get('cpv', []))} código(s)")

                if contract_data.get('num_licitadores'):
                    st.write(f"- Licitadores: {contract_data['num_licitadores']}")
                if contract_data.get('adjudicatario'):
                    st.write(f"- Adjudicatario: {contract_data['adjudicatario'][:40]}...")

            # Objeto
            if contract_data.get('objeto'):
                st.write("**Objeto:**")
                st.write(f"{contract_data['objeto'][:200]}{'...' if len(contract_data['objeto']) > 200 else ''}")

            # CPV
            if contract_data.get('cpv'):
                st.write("**Códigos CPV:**")
                for cpv in contract_data['cpv']:
                    st.write(f"- {cpv['code']}: {cpv['name']}")

            # Criterios
            if contract_data.get('criterios_adjudicacion', {}).get('criterios_detalle'):
                st.write("**Criterios de Adjudicación:**")
                for i, crit in enumerate(contract_data['criterios_adjudicacion']['criterios_detalle']):
                    st.write(f"{i+1}. {crit['nombre']}: {crit['peso']} pts ({crit['categoria']})")

    def find_similar_contratos_ai_enhanced(self, contract_data, all_contratos):
        """
        Sistema de IA MEJORADO para encontrar licitaciones similares
        Considera: años anteriores, zona, actividad, importe, palabras clave, CPV
        """
        st.info("🤖 Iniciando búsqueda con IA avanzada...")

        if not contract_data or all_contratos.empty:
            return []

        similar_contratos = []

        # Extraer características del contrato objetivo
        target_pbl = contract_data.get('pbl')
        target_localidad = contract_data.get('localidad', '')
        target_cpvs = [cpv['code'] for cpv in contract_data.get('cpv', [])]
        target_objeto = contract_data.get('objeto', '')
        target_tipo = contract_data.get('tipo_contrato', '')
        target_fecha = contract_data.get('fecha_publicacion')

        # Calcular año del contrato objetivo
        target_year = None
        if target_fecha:
            try:
                target_year = int(target_fecha.split('-')[0])
            except:
                pass

        st.write(f"🎯 **Buscando contratos similares a:**")
        st.write(f"- PBL: {target_pbl:,.0f} €" if target_pbl else "- PBL: No disponible")
        st.write(f"- Localidad: {target_localidad}")
        st.write(f"- CPV: {', '.join(target_cpvs[:3])}")
        st.write(f"- Año: {target_year}")

        # Tokenizar objeto para búsqueda de palabras clave
        target_words_important = self.extract_keywords(target_objeto) if target_objeto else set()

        # Iterar sobre todos los contratos de la BD
        for idx, row in all_contratos.iterrows():
            score = 0
            reasons = []
            match_factors = {
                'cpv_match': False,
                'location_match': False,
                'price_match': False,
                'keyword_match': False,
                'same_activity': False,
                'previous_year': False
            }

            # Extraer datos del contrato en BD
            row_price = None
            row_localidad = ''
            row_cpv = ''
            row_objeto = ''
            row_fecha = None

            # Buscar precio
            for col in all_contratos.columns:
                col_lower = col.lower()
                if any(price_col in col_lower for price_col in ['precio', 'importe', 'valor', 'presupuesto', 'pbl']):
                    row_price = self.extract_price_from_text(row.get(col))
                    if row_price and row_price > 1000:
                        break

            # Buscar localidad
            for col in all_contratos.columns:
                col_lower = col.lower()
                if any(loc_col in col_lower for loc_col in ['provincia', 'ubicacion', 'lugar', 'localidad', 'ciudad']):
                    row_localidad = str(row.get(col, '')).strip()
                    if row_localidad and len(row_localidad) > 2:
                        break

            # Buscar CPV
            for col in all_contratos.columns:
                col_lower = col.lower()
                if 'cpv' in col_lower:
                    row_cpv = str(row.get(col, ''))
                    break

            # Buscar objeto
            for col in all_contratos.columns:
                col_lower = col.lower()
                if any(obj_col in col_lower for obj_col in ['objeto', 'descripcion', 'servicio', 'titulo']):
                    row_objeto = str(row.get(col, ''))
                    if row_objeto and len(row_objeto) > 20:
                        break

            # Buscar fecha
            for col in all_contratos.columns:
                col_lower = col.lower()
                if any(fecha_col in col_lower for fecha_col in ['fecha', 'publicacion', 'year', 'año']):
                    row_fecha = str(row.get(col, ''))
                    break

            # Extraer año del contrato
            row_year = None
            if row_fecha:
                # Buscar año en el texto (formato YYYY)
                year_match = re.search(r'20\d{2}', row_fecha)
                if year_match:
                    row_year = int(year_match.group())

            # === CRITERIO 1: MISMO CPV (Muy importante - 40 puntos) ===
            if target_cpvs and row_cpv:
                for target_cpv in target_cpvs:
                    # CPV exacto (8 dígitos)
                    if target_cpv in row_cpv:
                        score += 40
                        reasons.append(f"✅ CPV exacto: {target_cpv}")
                        match_factors['cpv_match'] = True
                        break
                    # División CPV (4 primeros dígitos)
                    elif target_cpv[:4] in row_cpv:
                        score += 30
                        reasons.append(f"🔸 CPV división similar: {target_cpv[:4]}xxxx")
                        match_factors['cpv_match'] = True
                        break
                    # Categoría CPV (2 primeros dígitos)
                    elif target_cpv[:2] in row_cpv:
                        score += 20
                        reasons.append(f"🔹 CPV categoría: {target_cpv[:2]}xxxxxx")
                        match_factors['cpv_match'] = True
                        break

            # === CRITERIO 2: MISMA ZONA/LOCALIDAD (30 puntos) ===
            if target_localidad and row_localidad:
                # Coincidencia exacta
                if target_localidad.upper() in row_localidad.upper() or row_localidad.upper() in target_localidad.upper():
                    score += 30
                    reasons.append(f"📍 Misma localidad: {row_localidad}")
                    match_factors['location_match'] = True
                else:
                    # Zona cercana
                    zonas_cercanas = self.get_nearby_locations(target_localidad)
                    for zona in zonas_cercanas:
                        if zona.upper() in row_localidad.upper():
                            score += 20
                            reasons.append(f"📍 Zona cercana: {row_localidad}")
                            match_factors['location_match'] = True
                            break

            # === CRITERIO 3: IMPORTE SIMILAR (25 puntos) ===
            if target_pbl and row_price:
                price_diff = abs(row_price - target_pbl) / target_pbl
                if price_diff <= 0.20:  # ±20%
                    score += 25
                    reasons.append(f"💰 Importe muy similar: {row_price:,.0f}€ (±{price_diff*100:.0f}%)")
                    match_factors['price_match'] = True
                elif price_diff <= 0.40:  # ±40%
                    score += 18
                    reasons.append(f"💰 Importe similar: {row_price:,.0f}€ (±{price_diff*100:.0f}%)")
                    match_factors['price_match'] = True
                elif price_diff <= 0.60:  # ±60%
                    score += 10
                    reasons.append(f"💵 Importe cercano: {row_price:,.0f}€ (±{price_diff*100:.0f}%)")

            # === CRITERIO 4: PALABRAS CLAVE EN OBJETO (30 puntos) ===
            if target_objeto and row_objeto and len(target_objeto) > 20:
                # Similitud TF-IDF
                similarity = self.calculate_text_similarity(target_objeto, row_objeto)
                if similarity > 0.4:  # Alta similitud
                    score += 30
                    reasons.append(f"📝 Objeto muy similar ({similarity*100:.0f}%)")
                    match_factors['keyword_match'] = True
                elif similarity > 0.25:  # Similitud media
                    score += 20
                    reasons.append(f"📝 Objeto similar ({similarity*100:.0f}%)")
                    match_factors['keyword_match'] = True
                elif similarity > 0.15:  # Similitud baja
                    score += 10
                    reasons.append(f"📄 Objeto relacionado ({similarity*100:.0f}%)")

                # Palabras clave específicas
                row_words = self.extract_keywords(row_objeto)
                if target_words_important and row_words:
                    word_overlap = len(target_words_important.intersection(row_words)) / len(target_words_important.union(row_words))
                    if word_overlap > 0.3:
                        bonus_score = word_overlap * 15
                        score += bonus_score
                        reasons.append(f"🔑 Palabras clave comunes ({word_overlap*100:.0f}%)")
                        match_factors['keyword_match'] = True

            # === CRITERIO 5: MISMA ACTIVIDAD/TIPO (15 puntos) ===
            if target_tipo:
                # Buscar tipo en el contrato de BD
                for col in all_contratos.columns:
                    col_lower = col.lower()
                    if 'tipo' in col_lower:
                        row_tipo = str(row.get(col, ''))
                        if row_tipo and target_tipo.lower() in row_tipo.lower():
                            score += 15
                            reasons.append(f"🏷️ Mismo tipo: {target_tipo}")
                            match_factors['same_activity'] = True
                            break

            # === CRITERIO 6: AÑOS ANTERIORES (15 puntos) ===
            if target_year and row_year:
                year_diff = abs(target_year - row_year)
                if 0 < year_diff <= 1:  # Año anterior o siguiente
                    score += 15
                    reasons.append(f"📅 Año cercano: {row_year} (diff: {year_diff} año)")
                    match_factors['previous_year'] = True
                elif year_diff <= 3:  # Hasta 3 años de diferencia
                    score += 10
                    reasons.append(f"📅 Años anteriores: {row_year} (diff: {year_diff} años)")
                    match_factors['previous_year'] = True
                elif year_diff <= 5:
                    score += 5
                    reasons.append(f"📆 Mismo periodo: ~{row_year}")

            # === BONUS: RECENCIA (5 puntos) ===
            if row_fecha:
                try:
                    fecha_dt = pd.to_datetime(row_fecha)
                    days_ago = (datetime.now() - fecha_dt).days
                    if days_ago < 365:
                        recency_score = max(0, (365 - days_ago) / 365 * 5)
                        score += recency_score
                except:
                    pass

            # Extraer datos de adjudicación si existen
            pbl = row_price
            importe_adj = None
            empresa = None

            for col in all_contratos.columns:
                col_lower = col.lower()
                if 'adjudicacion' in col_lower or 'adjudicado' in col_lower:
                    importe_adj = self.extract_price_from_text(row.get(col))
                elif 'empresa' in col_lower or 'adjudicatario' in col_lower:
                    empresa = str(row.get(col, '')).strip()

            baja_percentage = None
            if pbl and importe_adj and pbl > 0:
                baja_percentage = ((pbl - importe_adj) / pbl) * 100

            # Umbral mínimo de score: 30 puntos (más estricto)
            if score >= 30:
                similar_contratos.append({
                    'index': idx,
                    'score': score,
                    'reasons': reasons,
                    'match_factors': match_factors,
                    'pbl': pbl,
                    'importe_adjudicacion': importe_adj,
                    'baja_percentage': baja_percentage,
                    'empresa': empresa,
                    'localidad': row_localidad,
                    'cpv': row_cpv,
                    'objeto': row_objeto[:150] + "..." if len(row_objeto) > 150 else row_objeto,
                    'fecha': row_fecha,
                    'row_data': row
                })

        # Ordenación inteligente
        def get_priority_score(contrato):
            factors = contrato['match_factors']
            # Priorizar por: CPV > Localidad > Precio > Palabras clave
            priority = (
                factors['cpv_match'] * 10000 +
                factors['location_match'] * 1000 +
                factors['price_match'] * 100 +
                factors['keyword_match'] * 10 +
                contrato['score']
            )
            return priority

        similar_contratos.sort(key=get_priority_score, reverse=True)

        # Limitar a top 20
        similar_contratos = similar_contratos[:20]

        if similar_contratos:
            st.success(f"✅ Encontrados {len(similar_contratos)} contratos similares con IA avanzada")

            # Mostrar estadísticas de coincidencias
            with st.expander("📊 Estadísticas de Coincidencias"):
                total_contratos = len(similar_contratos)
                cpv_matches = sum(1 for c in similar_contratos if c['match_factors']['cpv_match'])
                location_matches = sum(1 for c in similar_contratos if c['match_factors']['location_match'])
                price_matches = sum(1 for c in similar_contratos if c['match_factors']['price_match'])

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("CPV coincidentes", f"{cpv_matches}/{total_contratos}")
                with col2:
                    st.metric("Localidad coincidente", f"{location_matches}/{total_contratos}")
                with col3:
                    st.metric("Precio similar", f"{price_matches}/{total_contratos}")
        else:
            st.warning("⚠️ No se encontraron contratos similares suficientes")

        return similar_contratos

    def extract_keywords(self, text):
        """
        Extraer palabras clave importantes de un texto
        """
        if not text or len(text) < 10:
            return set()

        # Palabras comunes a excluir
        stopwords_es = {
            'el', 'la', 'de', 'y', 'a', 'en', 'que', 'es', 'por', 'para', 'con', 'no', 'una', 'su',
            'al', 'lo', 'como', 'más', 'del', 'pero', 'sus', 'le', 'ya', 'o', 'fue', 'este', 'ha',
            'sí', 'porque', 'esta', 'son', 'entre', 'está', 'cuando', 'muy', 'sin', 'sobre', 'ser',
            'tiene', 'también', 'me', 'hasta', 'hay', 'donde', 'han', 'quien', 'están', 'estado',
            'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'fueron',
            'ese', 'eso', 'había', 'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos',
            'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada',
            'muchos', 'cual', 'sea', 'poco', 'ella', 'estar', 'haber', 'estas', 'estaba', 'estamos',
            'los', 'las', 'un', 'del', 'según', 'cláusula', 'mediante', 'número', 'previsto'
        }

        # Tokenizar y limpiar
        words = re.findall(r'\b\w{4,}\b', text.lower())  # Palabras de 4+ letras

        # Filtrar stopwords y obtener palabras importantes
        important_words = set()
        for word in words:
            if word not in stopwords_es and len(word) >= 4:
                important_words.add(word)

        return important_words

    def get_nearby_locations(self, target_location):
        """
        Obtener zonas cercanas (igual que en el código original)
        """
        if not target_location:
            return []

        zonas_cercanas_map = {
            'Madrid': ['Comunidad de Madrid', 'Castilla-La Mancha', 'Castilla y León', 'Segovia', 'Toledo', 'Guadalajara'],
            'Barcelona': ['Cataluña', 'Catalunya', 'Lleida', 'Girona', 'Tarragona'],
            'Valencia': ['Comunidad Valenciana', 'Comunitat Valenciana', 'Alicante', 'Castellón'],
            'Sevilla': ['Andalucía', 'Cádiz', 'Córdoba', 'Huelva'],
            'Murcia': ['Región de Murcia', 'Alicante', 'Almería', 'Albacete'],
            'Andalucía': ['Sevilla', 'Córdoba', 'Granada', 'Málaga', 'Cádiz', 'Huelva', 'Jaén', 'Almería'],
            'Cataluña': ['Barcelona', 'Girona', 'Lleida', 'Tarragona'],
            'Comunidad de Madrid': ['Madrid', 'Segovia', 'Toledo', 'Guadalajara', 'Ávila'],
            'Región de Murcia': ['Murcia', 'Alicante', 'Almería'],
            'Castilla y León': ['Madrid', 'Valladolid', 'Salamanca', 'León', 'Burgos'],
            'Galicia': ['A Coruña', 'Pontevedra', 'Lugo', 'Ourense'],
            'País Vasco': ['Vizcaya', 'Guipúzcoa', 'Álava', 'Navarra'],
            'Aragón': ['Zaragoza', 'Huesca', 'Teruel', 'Navarra', 'Cataluña']
        }

        zonas_cercanas = []
        target_upper = target_location.upper()

        for region, cercanas in zonas_cercanas_map.items():
            if region.upper() in target_upper or target_upper in region.upper():
                zonas_cercanas.extend(cercanas)
                break

        if not zonas_cercanas:
            for region, cercanas in zonas_cercanas_map.items():
                for cercana in cercanas:
                    if cercana.upper() in target_upper or target_upper in cercana.upper():
                        zonas_cercanas.extend(cercanas)
                        zonas_cercanas.append(region)
                        break
                if zonas_cercanas:
                    break

        zonas_cercanas = list(set(zonas_cercanas))
        zonas_cercanas = [z for z in zonas_cercanas if z.upper() != target_upper]

        return zonas_cercanas[:5]

    def extract_price_from_text(self, text):
        """
        Extraer precio de texto (igual que original)
        """
        if pd.isna(text) or text is None:
            return None

        text_str = str(text).replace('.', '').replace(',', '.')

        patterns = [
            r'(\d+\.?\d*)\s*€',
            r'€\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*euros?',
            r'(\d{1,10}(?:\.\d{1,2})?)'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text_str, re.IGNORECASE)
            if matches:
                try:
                    value = float(matches[0].replace(',', '.'))
                    if value > 100:  # Validar que sea un precio razonable
                        return value
                except:
                    continue
        return None

    def calculate_text_similarity(self, text1, text2):
        """
        Calcular similitud TF-IDF mejorado para textos cortos y largos
        """
        if not text1 or not text2:
            return 0

        # Para textos muy cortos, usar palabras en común
        text1_lower = str(text1).lower()
        text2_lower = str(text2).lower()

        if len(text1_lower) < 50 or len(text2_lower) < 50:
            # Método simple para textos cortos
            words1 = set(text1_lower.split())
            words2 = set(text2_lower.split())
            if not words1 or not words2:
                return 0
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            return intersection / union if union > 0 else 0

        # TF-IDF para textos largos
        vectorizer = TfidfVectorizer(
            stop_words='spanish',
            lowercase=True,
            max_features=100,
            min_df=1,
            ngram_range=(1, 2)  # Usar bigramas también
        )
        try:
            tfidf_matrix = vectorizer.fit_transform([str(text1), str(text2)])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity
        except Exception as e:
            # Fallback: Jaccard similarity
            words1 = set(text1_lower.split())
            words2 = set(text2_lower.split())
            if not words1 or not words2:
                return 0
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            return intersection / union if union > 0 else 0

    def calculate_recommended_baja_enhanced(self, similar_contratos):
        """
        Calcular baja recomendada con lógica mejorada
        Considera: estadística, competitividad del sector, CPV, zona
        """
        if not similar_contratos:
            return 15.0, "No hay datos suficientes"

        # Obtener bajas válidas
        bajas = [c['baja_percentage'] for c in similar_contratos if c.get('baja_percentage') and c['baja_percentage'] > 0]

        if not bajas:
            return 15.0, "No hay bajas en los datos encontrados"

        # Ordenar bajas
        bajas_sorted = sorted(bajas)

        st.write(f"📊 **Analizando {len(bajas)} bajas encontradas**")
        st.write(f"- Rango: {min(bajas):.1f}% - {max(bajas):.1f}%")
        st.write(f"- Media: {np.mean(bajas):.1f}%")
        st.write(f"- Mediana: {np.median(bajas):.1f}%")

        # Estrategia 1: Buscar bajas similares (±2%)
        bajas_similares_grupos = []
        for baja_base in bajas:
            grupo_similar = [b for b in bajas if abs(b - baja_base) <= 2.0]
            if len(grupo_similar) >= 3:
                bajas_similares_grupos.append(grupo_similar)

        if bajas_similares_grupos:
            # Grupo con la baja más alta
            max_baja_grupos = [max(grupo) for grupo in bajas_similares_grupos]
            max_baja = max(max_baja_grupos)
            recommended_baja = max_baja + 2.0
            explicacion = f"Grupo de {len(bajas_similares_grupos[0])}+ licitaciones con bajas cercanas. Baja más alta del grupo: {max_baja:.1f}%"
        else:
            # Estrategia 2: Media de todas + margen
            media_bajas = np.mean(bajas)
            recommended_baja = media_bajas + 2.0
            explicacion = f"Media de todas las bajas encontradas: {media_bajas:.1f}%"

        # Ajustes por competitividad del sector
        # Si hay muchas licitaciones similares encontradas = sector competitivo
        if len(similar_contratos) > 15:
            recommended_baja += 1.0
            explicacion += " + 1% (sector muy competitivo)"

        # Si las bajas son muy dispersas = sector impredecible, ser conservador
        std_bajas = np.std(bajas)
        if std_bajas > 15:  # Alta variabilidad
            recommended_baja -= 1.0
            explicacion += " - 1% (alta variabilidad, enfoque conservador)"

        # Limitar al 70% máximo
        recommended_baja = min(recommended_baja, 70.0)
        recommended_baja = max(recommended_baja, 5.0)  # Mínimo 5%

        st.info(f"💡 **Lógica aplicada:** {explicacion}")

        return recommended_baja, explicacion

    def get_contratos_data(self, limit=5000):
        """
        Obtener datos de contratos de la BD
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            cursor.close()

            st.info(f"Tablas disponibles: {', '.join(tables)}")

            contratos_table = None
            for table in tables:
                if 'contrato' in table.lower():
                    contratos_table = table
                    break

            if not contratos_table:
                st.error("No se encontró tabla de contratos")
                return pd.DataFrame()

            st.info(f"Usando tabla: {contratos_table}")
            query = f"SELECT * FROM {contratos_table} LIMIT {limit}"
            return pd.read_sql(query, self.connection)

        except Exception as e:
            st.error(f"Error cargando datos: {e}")
            return pd.DataFrame()

    def generate_enhanced_report(self, contract_data, similar_contratos, recommended_baja, baja_explanation):
        """
        Generar informe mejorado con análisis preciso
        """
        st.subheader("📊 ANÁLISIS DETALLADO DE BAJA ESTADÍSTICA")

        # Resumen ejecutivo
        st.write("### 🎯 Resumen Ejecutivo")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Baja Recomendada", f"{recommended_baja:.1f}%")
        with col2:
            st.metric("Licitaciones Analizadas", len(similar_contratos))
        with col3:
            bajas_validas = [c['baja_percentage'] for c in similar_contratos if c.get('baja_percentage')]
            if bajas_validas:
                st.metric("Rango Bajas Observadas", f"{min(bajas_validas):.1f}% - {max(bajas_validas):.1f}%")

        # Licitaciones encontradas
        st.write("### 📋 Licitaciones Similares Encontradas")

        for i, contrato in enumerate(similar_contratos[:10]):
            with st.expander(f"🏆 #{i+1} - Score: {contrato['score']:.0f} puntos - Baja: {contrato.get('baja_percentage', 'N/A'):.1f}%" if contrato.get('baja_percentage') else f"🏆 #{i+1} - Score: {contrato['score']:.0f} puntos"):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.write("**Información:**")
                    st.write(f"- **Objeto:** {contrato['objeto']}")
                    if contrato.get('fecha'):
                        st.write(f"- **Fecha:** {contrato['fecha']}")
                    if contrato['pbl']:
                        st.write(f"- **PBL:** {contrato['pbl']:,.2f} €")
                    if contrato['localidad']:
                        st.write(f"- **Localidad:** {contrato['localidad']}")
                    if contrato['cpv']:
                        st.write(f"- **CPV:** {contrato['cpv']}")

                with col2:
                    st.write("**Adjudicación:**")
                    if contrato.get('importe_adjudicacion'):
                        st.write(f"- **Importe:** {contrato['importe_adjudicacion']:,.2f} €")
                    if contrato.get('baja_percentage'):
                        st.write(f"- **Baja:** {contrato['baja_percentage']:.1f}%")
                    if contrato.get('empresa'):
                        st.write(f"- **Empresa:** {contrato['empresa'][:40]}...")

                st.write("**Razones de similitud:**")
                for reason in contrato['reasons']:
                    st.write(f"  • {reason}")

        # Adjudicatarios más frecuentes
        st.write("### 🏢 Adjudicatarios Identificados")

        empresas_validas = [c['empresa'] for c in similar_contratos if c.get('empresa') and str(c['empresa']).strip() and len(str(c['empresa'])) > 3]

        if empresas_validas:
            empresa_counts = Counter(empresas_validas)
            top_empresas = empresa_counts.most_common(10)

            for empresa, count in top_empresas:
                # Calcular bajas de esta empresa
                bajas_empresa = [c['baja_percentage'] for c in similar_contratos
                               if c.get('empresa') == empresa and c.get('baja_percentage')]

                if bajas_empresa:
                    baja_media = np.mean(bajas_empresa)
                    st.write(f"- **{empresa}**: {count} licitación(es) - Baja media: {baja_media:.1f}%")
                else:
                    st.write(f"- **{empresa}**: {count} licitación(es)")
        else:
            st.info("No se identificaron adjudicatarios en los datos disponibles")

        # Análisis de bajas
        st.write("### 📈 Análisis de Bajas")

        bajas_validas = [c['baja_percentage'] for c in similar_contratos if c.get('baja_percentage') and c['baja_percentage'] > 0]

        if bajas_validas:
            # Histograma
            fig = px.histogram(bajas_validas, nbins=15,
                              title="Distribución de Bajas Observadas",
                              labels={'value': 'Baja (%)', 'count': 'Frecuencia'})
            fig.add_vline(x=recommended_baja, line_dash="dash", line_color="red",
                         annotation_text=f"Recomendada: {recommended_baja:.1f}%")
            st.plotly_chart(fig)

            # Estadísticas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Media", f"{np.mean(bajas_validas):.1f}%")
            with col2:
                st.metric("Mediana", f"{np.median(bajas_validas):.1f}%")
            with col3:
                st.metric("Mínima", f"{min(bajas_validas):.1f}%")
            with col4:
                st.metric("Máxima", f"{max(bajas_validas):.1f}%")

            st.write(f"**Explicación:** {baja_explanation}")

        # Texto para copiar
        st.write("### 📝 Texto de Baja Estadística")
        texto_baja = self.generate_texto_baja(contract_data, similar_contratos, recommended_baja, baja_explanation)
        st.text_area("Copia este texto:", texto_baja, height=400)

        return texto_baja

    def generate_texto_baja(self, contract_data, similar_contratos, recommended_baja, explanation):
        """
        Generar texto narrativo de baja estadística
        """
        saludos = [
            "Buenos días,",
            "Estimados señores,",
            "Buenas tardes,",
            "Estimado equipo,",
            "Muy buenos días,"
        ]

        despedidas = [
            "Un cordial saludo",
            "Saludos cordiales",
            "Atentamente",
            "Un saludo",
            "Cordialmente"
        ]

        saludo = random.choice(saludos)
        despedida = random.choice(despedidas)

        texto = f"{saludo}\n\n"

        # Criterios de adjudicación
        criterios = contract_data.get('criterios_adjudicacion', {})
        if criterios.get('criterios_detalle'):
            texto += "En la selección de expedientes, nos encontramos los siguientes criterios de adjudicación:\n"
            for crit in criterios['criterios_detalle']:
                if crit.get('peso') and crit.get('nombre'):
                    nombre_upper = crit['nombre'].upper()
                    texto += f"{nombre_upper}: {int(crit['peso'])} {'PUNTOS' if crit['peso'] >= 50 else 'puntos'}\n"
            texto += "\n"

        # Análisis de mercado
        texto += f"Al revisar expedientes previos de similar envergadura, presupuesto y características técnicas, hemos identificado {len(similar_contratos)} licitaciones comparables.\n\n"

        # Empresas destacadas
        empresas_validas = [c['empresa'] for c in similar_contratos[:10] if c.get('empresa') and len(str(c['empresa'])) > 3]
        if empresas_validas:
            empresas_unicas = list(set(empresas_validas))[:5]
            empresas_texto = ", ".join(empresas_unicas[:3])
            texto += f"Entre las empresas más activas en este ámbito encontramos a {empresas_texto}.\n\n"

        # Bajas observadas
        bajas_validas = [c['baja_percentage'] for c in similar_contratos if c.get('baja_percentage') and c['baja_percentage'] > 0]
        if bajas_validas:
            rango_min = min(bajas_validas)
            rango_max = max(bajas_validas)
            texto += f"Las variaciones en las ofertas económicas presentan un rango de descuentos entre {rango_min:.1f}% y {rango_max:.1f}%, evidenciando un mercado competitivo con estrategias comerciales diversas.\n\n"

        # Recomendación
        texto += f"Tras el análisis estadístico de las licitaciones similares, recomendamos presentar una propuesta económica con un descuento del {recommended_baja:.1f}%.\n\n"

        texto += f"Esta recomendación se basa en: {explanation}\n\n"

        # Consideraciones adicionales
        texto += "Además, optimizar los aspectos técnicos de la propuesta y demostrar experiencia previa en proyectos similares serán elementos diferenciadores clave.\n\n"

        texto += despedida

        return texto

def main():
    """
    Aplicación principal de Streamlit
    """
    st.set_page_config(page_title="Análisis Avanzado de Licitaciones", layout="wide")

    st.title("🌐 Sistema Avanzado de Análisis de Licitaciones con IA")
    st.markdown("### Extracción completa de datos XML + Análisis inteligente de similitudes")

    st.sidebar.title("⚙️ Configuración")

    # Inicializar analizador
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = EnhancedXMLAnalyzer()

    analyzer = st.session_state.analyzer

    # Conectar a la base de datos
    if not analyzer.connection:
        with st.spinner("Conectando a la base de datos..."):
            if analyzer.connect_to_database():
                st.success("✅ Conectado exitosamente a la base de datos")
            else:
                st.error("❌ No se pudo conectar a la base de datos")
                st.info("💡 El sistema funcionará en modo limitado (solo extracción XML)")

    # Modo de operación
    modo = st.sidebar.radio(
        "Selecciona modo de operación:",
        ["📋 Análisis desde XML", "🔍 Consulta Base de Datos", "📚 Ayuda"]
    )

    if modo == "📋 Análisis desde XML":
        st.subheader("🔗 Análisis de Licitación desde XML")

        col1, col2 = st.columns([2, 1])

        with col1:
            url_input = st.text_input(
                "Pega aquí el enlace HTML de la licitación:",
                placeholder="https://contrataciondelestado.es/wps/poc?uri=deeplink:detalle_licitacion&idEvl=...",
                help="Enlace a la página de detalle de la licitación en la Plataforma de Contratación del Estado"
            )

        with col2:
            xml_direct = st.text_input(
                "O URL XML directa:",
                placeholder="https://contrataciondelestado.es/FileSystem/servlet/...",
                help="Enlace directo al archivo XML"
            )

        # Configuración de análisis
        with st.sidebar.expander("🎛️ Configuración de Análisis"):
            num_contratos_bd = st.slider("Límite de contratos a analizar:", 1000, 10000, 5000, 500)
            score_minimo = st.slider("Score mínimo de similitud:", 20, 50, 30, 5)

        target_url = xml_direct if xml_direct else url_input

        if target_url and target_url.startswith('http'):
            if st.button("🚀 Analizar Licitación", type="primary"):
                with st.spinner("Procesando URL y extrayendo datos..."):
                    xml_url = None

                    # Determinar si es URL HTML o XML
                    if 'xml' in target_url.lower() or 'GetDocumentByIdServlet' in target_url:
                        xml_url = target_url
                        st.info("✅ URL XML detectada")
                    else:
                        st.info("🔄 URL HTML detectada, convirtiendo a XML...")
                        # Intentar convertir (implementar lógica de conversión del original)
                        # Por simplicidad, asumir que el usuario provee XML directo
                        st.warning("⚠️ Por favor, proporciona la URL XML directa del documento")
                        xml_url = target_url

                if xml_url:
                    # 1. EXTRACCIÓN DE DATOS
                    st.markdown("---")
                    st.subheader("📥 FASE 1: Extracción de Datos del XML")

                    with st.spinner("Extrayendo datos completos del XML..."):
                        contract_data = analyzer.extract_complete_contract_data(xml_url)

                    if contract_data:
                        # Mostrar lotes si existen
                        if contract_data.get('tiene_lotes') and contract_data.get('lotes'):
                            st.info(f"📦 Esta licitación está dividida en {len(contract_data['lotes'])} lotes")

                            with st.expander("Ver detalles de los lotes"):
                                for lote in contract_data['lotes']:
                                    st.write(f"**Lote {lote['numero']}** - {lote.get('id', 'Sin ID')}")
                                    st.write(f"- Descripción: {lote.get('descripcion', 'N/A')}")
                                    st.write(f"- PBL: {lote.get('pbl', 'N/A'):,.2f} €" if lote.get('pbl') else "- PBL: N/A")
                                    if lote.get('cpv'):
                                        cpv_codes = [cpv['code'] for cpv in lote['cpv']]
                                        st.write(f"- CPV: {', '.join(cpv_codes)}")
                                    st.write("---")

                        # 2. BÚSQUEDA EN BASE DE DATOS
                        if analyzer.connection:
                            st.markdown("---")
                            st.subheader("🔍 FASE 2: Búsqueda de Licitaciones Similares")

                            with st.spinner("Cargando y analizando base de datos de contratos..."):
                                contratos_data = analyzer.get_contratos_data(num_contratos_bd)

                            if not contratos_data.empty:
                                st.success(f"✅ Cargados {len(contratos_data)} contratos para análisis")

                                with st.spinner("Ejecutando algoritmo de IA para encontrar similitudes..."):
                                    similar_contratos = analyzer.find_similar_contratos_ai_enhanced(
                                        contract_data, contratos_data
                                    )

                                if similar_contratos:
                                    # 3. CÁLCULO DE BAJA RECOMENDADA
                                    st.markdown("---")
                                    st.subheader("💡 FASE 3: Cálculo de Baja Recomendada")

                                    recommended_baja, explanation = analyzer.calculate_recommended_baja_enhanced(
                                        similar_contratos
                                    )

                                    # 4. GENERACIÓN DE INFORME
                                    st.markdown("---")
                                    st.subheader("📊 FASE 4: Informe Completo")

                                    texto_baja = analyzer.generate_enhanced_report(
                                        contract_data,
                                        similar_contratos,
                                        recommended_baja,
                                        explanation
                                    )

                                    # Botones de acción
                                    col1, col2, col3 = st.columns(3)

                                    with col1:
                                        if st.button("🔄 Regenerar Texto"):
                                            nuevo_texto = analyzer.generate_texto_baja(
                                                contract_data,
                                                similar_contratos,
                                                recommended_baja,
                                                explanation
                                            )
                                            st.text_area("Nuevo texto generado:", nuevo_texto, height=300)

                                    with col2:
                                        # Exportar a Excel
                                        excel_data = create_excel_report(
                                            contract_data,
                                            similar_contratos,
                                            recommended_baja,
                                            explanation
                                        )
                                        st.download_button(
                                            label="📊 Descargar Excel",
                                            data=excel_data,
                                            file_name=f"analisis_licitacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                        )

                                    with col3:
                                        # Exportar a JSON
                                        json_data = json.dumps({
                                            'contrato': {k: v for k, v in contract_data.items() if k != 'row_data'},
                                            'similares': len(similar_contratos),
                                            'baja_recomendada': recommended_baja,
                                            'explicacion': explanation
                                        }, indent=2, ensure_ascii=False)

                                        st.download_button(
                                            label="💾 Descargar JSON",
                                            data=json_data,
                                            file_name=f"analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                            mime="application/json"
                                        )

                                else:
                                    st.warning("⚠️ No se encontraron contratos similares suficientes")
                                    st.info("💡 Intenta ajustar el score mínimo en la configuración")

                            else:
                                st.error("❌ No se pudieron cargar datos de la base de datos")
                        else:
                            st.info("ℹ️ Base de datos no disponible. Mostrando solo extracción de XML.")

                    else:
                        st.error("❌ No se pudieron extraer los datos del XML")

    elif modo == "🔍 Consulta Base de Datos":
        st.subheader("🔍 Consulta y Exploración de Base de Datos")

        if analyzer.connection:
            try:
                cursor = analyzer.connection.cursor()
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                cursor.close()

                selected_table = st.selectbox("Selecciona una tabla:", tables)

                if selected_table:
                    limit = st.number_input("Número de registros:", 10, 1000, 100)

                    if st.button("Cargar datos"):
                        query = f"SELECT * FROM {selected_table} LIMIT {limit}"
                        df = pd.read_sql(query, analyzer.connection)

                        st.write(f"**Tabla:** {selected_table} ({len(df)} registros)")
                        st.dataframe(df)

                        # Estadísticas
                        st.write("**Estadísticas:**")
                        st.write(df.describe())

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("No hay conexión a la base de datos")

    elif modo == "📚 Ayuda":
        st.subheader("📚 Guía de Uso del Sistema")

        st.markdown("""
        ### 🎯 Funcionalidades Principales

        Este sistema proporciona un análisis completo de licitaciones públicas mediante:

        #### 1. Extracción Completa de Datos XML
        El sistema extrae automáticamente:
        - ✅ Fecha de publicación
        - ✅ Presupuesto Base de Licitación (PBL)
        - ✅ Tipo de contrato
        - ✅ Objeto del contrato
        - ✅ Códigos CPV
        - ✅ Localidad/Provincia
        - ✅ Criterios de adjudicación (detallados)
        - ✅ Detección y extracción de lotes individuales
        - ✅ Procedimiento de licitación
        - ✅ Plazo de ejecución

        #### 2. Sistema de IA Avanzado
        Utiliza algoritmos de similitud basados en:
        - 🧠 **CPV (40 pts)**: Coincidencia exacta o por categoría
        - 📍 **Zona geográfica (30 pts)**: Misma localidad o zonas cercanas
        - 💰 **Importe (25 pts)**: Presupuesto similar (±20%, ±40%, ±60%)
        - 📝 **Palabras clave (30 pts)**: Análisis TF-IDF del objeto
        - 🏷️ **Tipo de contrato (15 pts)**: Servicios, Obras, Suministros
        - 📅 **Años anteriores (15 pts)**: Licitaciones de años previos

        #### 3. Análisis Preciso de Bajas
        - Detecta patrones en bajas históricas
        - Identifica empresas adjudicatarias más frecuentes
        - Calcula baja recomendada basada en estadística y competitividad del sector
        - Proporciona explicación detallada de la recomendación

        #### 4. Informes Completos
        - Texto narrativo para incluir en propuestas
        - Exportación a Excel con todos los datos
        - Exportación a JSON para integración con otros sistemas
        - Visualizaciones interactivas de distribución de bajas

        ### 🔗 Cómo Usar

        **Paso 1:** Obtén la URL de la licitación
        - Navega a la Plataforma de Contratación del Estado
        - Busca la licitación que te interesa
        - Copia la URL de la página de detalle O la URL del XML

        **Paso 2:** Pega la URL en el sistema
        - Usa el campo "enlace HTML" para URLs de la plataforma
        - Usa el campo "URL XML directa" para enlaces directos al XML

        **Paso 3:** Configura el análisis (opcional)
        - Ajusta el número de contratos a analizar (más = más preciso, pero más lento)
        - Modifica el score mínimo de similitud según tus necesidades

        **Paso 4:** Haz clic en "Analizar Licitación"
        - El sistema extraerá todos los datos automáticamente
        - Buscará licitaciones similares usando IA
        - Calculará la baja recomendada
        - Generará un informe completo

        **Paso 5:** Usa los resultados
        - Copia el texto para tu propuesta
        - Descarga el Excel para análisis detallado
        - Revisa las licitaciones similares encontradas
        - Analiza los adjudicatarios más frecuentes

        ### 💡 Consejos

        - Si la licitación tiene lotes, el sistema los detectará y extraerá individualmente
        - Cuanto más específicos sean los datos del XML, mejores serán los resultados
        - El sistema prioriza contratos con CPV y localidad coincidentes
        - La baja recomendada es una guía; siempre analiza el contexto específico
        - Puedes regenerar el texto para obtener variaciones en la redacción

        ### ⚠️ Limitaciones

        - Los datos de adjudicación (importe adjudicado, adjudicatario, nº licitadores) suelen estar en XMLs de adjudicación, no de licitación
        - La calidad del análisis depende de los datos disponibles en la base de datos
        - El sistema busca similitudes, pero cada licitación es única

        ### 🆘 Soporte

        Si encuentras algún problema:
        1. Verifica que la URL del XML sea correcta
        2. Asegúrate de que la base de datos esté conectada
        3. Revisa que el XML contenga los datos necesarios
        4. Ajusta los parámetros de configuración si no encuentras resultados
        """)


def create_excel_report(contract_data, similar_contratos, recommended_baja, explanation):
    """
    Crear reporte Excel detallado
    """
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book

        # Formatos
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#4472C4',
            'font_color': 'white',
            'border': 1
        })

        data_format = workbook.add_format({
            'text_wrap': True,
            'valign': 'top',
            'border': 1
        })

        # Hoja 1: Resumen
        resumen_data = []
        resumen_data.append(['Campo', 'Valor'])
        resumen_data.append(['Fecha Publicación', contract_data.get('fecha_publicacion', 'N/A')])
        resumen_data.append(['PBL', f"{contract_data.get('pbl', 0):,.2f} €" if contract_data.get('pbl') else 'N/A'])
        resumen_data.append(['Tipo Contrato', contract_data.get('tipo_contrato', 'N/A')])
        resumen_data.append(['Localidad', contract_data.get('localidad', 'N/A')])
        resumen_data.append(['Procedimiento', contract_data.get('procedimiento', 'N/A')])
        resumen_data.append(['Tiene Lotes', 'Sí' if contract_data.get('tiene_lotes') else 'No'])
        if contract_data.get('tiene_lotes'):
            resumen_data.append(['Número de Lotes', len(contract_data.get('lotes', []))])
        resumen_data.append(['Contratos Similares', len(similar_contratos)])
        resumen_data.append(['Baja Recomendada', f"{recommended_baja:.1f}%"])
        resumen_data.append(['Explicación', explanation])

        resumen_df = pd.DataFrame(resumen_data[1:], columns=resumen_data[0])
        resumen_df.to_excel(writer, sheet_name='Resumen', index=False)

        # Hoja 2: Objeto y CPV
        objeto_data = []
        objeto_data.append(['Concepto', 'Detalle'])
        objeto_data.append(['Objeto', contract_data.get('objeto', 'N/A')])
        if contract_data.get('cpv'):
            for cpv in contract_data['cpv']:
                objeto_data.append([f"CPV {cpv['code']}", cpv['name']])

        objeto_df = pd.DataFrame(objeto_data[1:], columns=objeto_data[0])
        objeto_df.to_excel(writer, sheet_name='Objeto y CPV', index=False)

        # Hoja 3: Lotes (si existen)
        if contract_data.get('tiene_lotes') and contract_data.get('lotes'):
            lotes_data = []
            for lote in contract_data['lotes']:
                cpv_lote = ', '.join([cpv['code'] for cpv in lote.get('cpv', [])])
                lotes_data.append({
                    'Número': lote['numero'],
                    'ID': lote.get('id', 'N/A'),
                    'Descripción': lote.get('descripcion', 'N/A'),
                    'PBL': f"{lote.get('pbl', 0):,.2f} €" if lote.get('pbl') else 'N/A',
                    'CPV': cpv_lote
                })

            lotes_df = pd.DataFrame(lotes_data)
            lotes_df.to_excel(writer, sheet_name='Lotes', index=False)

        # Hoja 4: Contratos Similares
        if similar_contratos:
            contratos_data = []
            for i, c in enumerate(similar_contratos):
                contratos_data.append({
                    'Ranking': i + 1,
                    'Score': f"{c['score']:.1f}",
                    'Objeto': c['objeto'],
                    'PBL': f"{c['pbl']:,.2f} €" if c['pbl'] else 'N/A',
                    'Importe Adj.': f"{c.get('importe_adjudicacion', 0):,.2f} €" if c.get('importe_adjudicacion') else 'N/A',
                    'Baja %': f"{c.get('baja_percentage', 0):.1f}%" if c.get('baja_percentage') else 'N/A',
                    'Empresa': c.get('empresa', 'N/A'),
                    'Localidad': c.get('localidad', 'N/A'),
                    'CPV': c.get('cpv', 'N/A'),
                    'Fecha': c.get('fecha', 'N/A'),
                    'Razones': '; '.join(c['reasons'])
                })

            contratos_df = pd.DataFrame(contratos_data)
            contratos_df.to_excel(writer, sheet_name='Contratos Similares', index=False)

        # Hoja 5: Criterios de Adjudicación
        criterios = contract_data.get('criterios_adjudicacion', {})
        if criterios.get('criterios_detalle'):
            criterios_data = []
            for crit in criterios['criterios_detalle']:
                criterios_data.append({
                    'ID': crit.get('id', 'N/A'),
                    'Nombre': crit.get('nombre', 'N/A'),
                    'Descripción': crit.get('descripcion', 'N/A'),
                    'Peso': crit.get('peso', 'N/A'),
                    'Categoría': crit.get('categoria', 'N/A'),
                    'Tipo': crit.get('tipo', 'N/A'),
                    'Subtipo': crit.get('subtipo', 'N/A')
                })

            criterios_df = pd.DataFrame(criterios_data)
            criterios_df.to_excel(writer, sheet_name='Criterios', index=False)

    output.seek(0)
    return output


if __name__ == "__main__":
    main()
