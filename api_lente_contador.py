import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import io

# --- CONFIGURAÇÃO DE AMBIENTE MASTER ---
st.set_page_config(page_title="EAGLES - BPO Estratégico", layout="wide", initial_sidebar_state="expanded")

# --- ESTILIZAÇÃO DARK MODE AFIAÇÃO MÁXIMA ---
st.markdown("""
    <style>
    .stApp { background-color: #050b1a; color: #e0e0e0; }
    .stMetric { background-color: #0a1931; border: 1px solid #00d4ff; padding: 15px; border-radius: 10px; }
    .alerta-critico { background-color: #441010; border-left: 5px solid #ff4b4b; padding: 20px; color: #ff4b4b; font-weight: bold; }
    .card-lente { background-color: #0d1b2a; border: 1px solid #1b263b; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE DADOS (SIMULANDO SQL) ---
if 'db' not in st.session_state:
    st.session_state.db = {
        'empresas': [
            {'id': 1, 'nome': 'Alfa Comércio', 'cnae': '4711-3/00', 'gerente': 'Marcos', 'ultima_att': datetime.now() - timedelta(days=3), 'dono': 'Cliente A'}
        ],
        'estoque': [],
        'lente_notas': [],
        'pro_labore': 100.00 # [cite: 2025-12-11]
    }

# --- LÓGICA DE PROCESSAMENTO DE XML (NF-e) ---
def processar_nfe(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # Namespace da NF-e
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    produtos = []
    for det in root.findall('.//nfe:det', ns):
        prod = det.find('nfe:prod', ns)
        nome = prod.find('nfe:xProd', ns).text
        qtd = float(prod.find('nfe:qCom', ns).text)
        v_unit = float(prod.find('nfe:vUnCom', ns).text)
        # Lógica de Custo Médio Ponderado simplificada para o prompt
        produtos.append({'item': nome, 'qtd': qtd, 'valor_unit': v_unit, 'total': qtd * v_unit})
    return pd.DataFrame(produtos)

# --- SIDEBAR: IDENTIDADE E CONTROLE DE ACESSO ---
with st.sidebar:
    st.title("🦅 EAGLES SYSTEM")
    usuario_ativo = st.text_input("Identificação Master", value="Samuel Richard")
    is_master = (usuario_ativo == "Samuel Richard")
    
    st.divider()
    if is_master:
        exibir_financeiro = st.toggle("👁️ Exibir Indicadores Sensíveis (Pro-labore)")
        if exibir_financeiro:
            st.metric("Retirada Pro-labore", f"R$ {st.session_state.db['pro_labore']:.2f}")
    
    perfil = st.selectbox("Simular Visão", ["DIRETOR MASTER", "GERENTE (Mobile)", "DONO (Voo da Águia)"])

# --- INTERFACE PRINCIPAL ---

# 1. VISÃO MASTER (Samuel)
if perfil == "DIRETOR MASTER":
    st.header("Painel de Controle Master")
    
    # Monitor de Compliance 48h [cite: 2025-12-03]
    for emp in st.session_state.db['empresas']:
        atraso = datetime.now() - emp['ultima_att']
        if atraso > timedelta(days=2):
            st.markdown(f'<div class="alerta-critico">⚠️ {emp["nome"]} (CNAE {emp["cnae"]}) SEM ATUALIZAÇÃO HÁ {atraso.days} DIAS!</div>', unsafe_allow_html=True)

    tab_import, tab_gestao = st.tabs(["📥 Importação XML/Excel", "👥 Gestão de Rede"])
    
    with tab_import:
        st.subheader("Radar de Dados (NF-e e Balancetes)")
        xml_up = st.file_uploader("Arraste o XML da NF-e aqui", type="xml")
        if xml_up:
            df_nfe = processar_nfe(xml_up)
            st.write("### Itens Extraídos e Cálculo de Custo Médio")
            st.dataframe(df_nfe, use_container_width=True)
            if st.button("Aprovar e Publicar na Lente"):
                st.session_state.db['lente_notas'].append(df_nfe)
                st.success("Dados enviados para validação do Dono.")

# 2. VISÃO GERENTE (Mobile Style)
elif perfil == "GERENTE (Mobile)":
    st.header("📱 Eagles Manager")
    with st.expander("📝 Registro de Presença (Escala do Dia)", expanded=True):
        col1, col2 = st.columns([2,1])
        nome_colab = col1.text_input("Colaborador")
        status = col2.selectbox("Status", ["Presente", "Falta Justificada", "Falta Injustificada", "Atraso"])
        if st.button("Confirmar Check-in"):
            st.toast(f"Registro de {nome_colab} enviado ao Master.")

    with st.expander("📸 Captura de Despesa/Caixa"):
        st.file_uploader("Tirar foto do comprovante", type=['jpg', 'png'])
        st.number_input("Valor do Fechamento (Cego)")

# 3. VISÃO DONO (Voo da Águia)
elif perfil == "DONO (Voo da Águia)":
    st.header("🦅 Voo da Águia - Dashboard Estratégico")
    c1, c2, c3 = st.columns(3)
    c1.metric("Lucro Real (Competência)", "R$ 45.200", "+5%")
    c2.metric("Ponto de Equilíbrio", "R$ 12.800")
    c3.metric("Margem de Contribuição", "32%")

    st.subheader("🔍 Lente do Contador (Consultoria)")
    st.info("Notas e Observações de Samuel Richard")
    # Exibe o que o Samuel aprovou
    if not st.session_state.db['lente_notas']:
        st.write("Nenhuma observação crítica para este período.")
    else:
        st.success("O Custo Médio Ponderado dos seus produtos foi atualizado via XML.")
