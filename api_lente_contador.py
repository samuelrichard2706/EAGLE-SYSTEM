import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="EAGLES SYSTEM", layout="wide", initial_sidebar_state="expanded")

# --- INICIALIZAÇÃO DE DADOS (BANCO TEMPORÁRIO) ---
if 'db_empresas' not in st.session_state:
    st.session_state.db_empresas = []
if 'db_gerentes' not in st.session_state:
    st.session_state.db_gerentes = []
if 'lancamentos' not in st.session_state:
    st.session_state.lancamentos = []

# --- CSS PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #050b1a; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #00d4ff; color: #050b1a; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #10213e; border-radius: 5px 5px 0px 0px; padding: 10px 20px; color: white; }
    .stTabs [aria-selected="true"] { background-color: #00d4ff !important; color: #050b1a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- IDENTIDADE MASTER ---
st.sidebar.title("🦅 EAGLES SYSTEM")
usuario = st.sidebar.text_input("Usuário", value="Samuel Richard")
is_master = (usuario == "Samuel Richard")

# --- NAVEGAÇÃO POR ABAS (TIPO MOBILLS/SISTEMA PROFISSIONAL) ---
tab_dash, tab_lente, tab_lanc, tab_gestao = st.tabs([
    "📈 Dashboard Master", 
    "🔍 Lente do Contador", 
    "💸 Lançamentos Rápidos", 
    "⚙️ Gestão de Rede"
])

# --- 1. DASHBOARD ---
with tab_dash:
    st.title("Voo da Águia")
    col1, col2, col3 = st.columns(3)
    col1.metric("Pro-labore", "R$ 100,00")
    col2.metric("Empresas", len(st.session_state.db_empresas))
    col3.metric("Lançamentos", len(st.session_state.lancamentos))

# --- 2. LENTE DO CONTADOR (LEITORES) ---
with tab_lente:
    st.title("Radar de Importação (OFX/Excel/CSV)")
    tipo_arquivo = st.selectbox("Tipo de Arquivo", ["Excel (.xlsx)", "CSV (.csv)", "Extrato Bancário (.ofx)"])
    file = st.file_uploader(f"Arraste seu arquivo {tipo_arquivo} aqui", type=["xlsx", "csv", "ofx"])
    
    if file:
        st.success(f"Arquivo {file.name} carregado. Processando filtros de conta...")
        # Lógica de leitura será detalhada conforme o layout das suas planilhas

# --- 3. LANÇAMENTOS (DINÂMICA MOBILLS) ---
with tab_lanc:
    st.title("Lançamento Express")
    with st.form("form_lancamento", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        data = c1.date_input("Data")
        valor = c2.number_input("Valor", min_value=0.0, step=0.01)
        tipo = c3.selectbox("Tipo", ["Receita", "Despesa"])
        desc = st.text_input("Descrição do Lançamento")
        if st.form_submit_button("Confirmar Lançamento"):
            st.session_state.lancamentos.append({"data": data, "valor": valor, "tipo": tipo, "desc": desc})
            st.toast("Lançamento registrado!", icon='✅')

# --- 4. GESTÃO (CADASTROS) ---
with tab_gestao:
    if is_master:
        st.subheader("Cadastrar Novo Gerente")
        nome_g = st.text_input("Nome do Gerente")
        if st.button("Salvar Gerente"):
            st.session_state.db_gerentes.append(nome_g)
            st.success(f"Gerente {nome_g} cadastrado.")
        
        st.divider()
        st.subheader("Cadastrar Empresa e Vincular")
        nome_e = st.text_input("Nome da Empresa")
        gerente_e = st.selectbox("Vincular ao Gerente", st.session_state.db_gerentes if st.session_state.db_gerentes else ["Nenhum cadastrado"])
        if st.button("Salvar Empresa"):
            st.session_state.db_empresas.append({"nome": nome_e, "gerente": gerente_e})
            st.success(f"Empresa {nome_e} vinculada a {gerente_e}.")
    else:
        st.error("Acesso restrito ao Master.")
