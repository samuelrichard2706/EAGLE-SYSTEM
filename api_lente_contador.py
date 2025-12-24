import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="EAGLES - Central de Inteligência", layout="wide")

# --- ESTADO DO SISTEMA (SIMULANDO BANCO DE DADOS) ---
if 'publicado_cliente' not in st.session_state:
    st.session_state.publicado_cliente = False
if 'dados_homologados' not in st.session_state:
    st.session_state.dados_homologados = None

# --- CSS DE ALTA LEGIBILIDADE ---
st.markdown("""
    <style>
    .stApp { background-color: #050b1a; color: #FFFFFF; }
    .status-badge { padding: 5px 10px; border-radius: 5px; font-weight: bold; }
    .card-master { background-color: #0a1931; border: 1px solid #00d4ff; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE PROCESSAMENTO AFIACO ---
def processar_balancete(file, contas_alvo):
    try:
        df = pd.read_csv(file) # Pode ser expandido para Excel
        # VALIDAÇÃO DE INTEGRIDADE (ERRO NÃO É BEM-VINDO)
        colunas_necessarias = ['Conta', 'Descricao', 'Saldo_Atual']
        if not all(c in df.columns for c in colunas_necessarias):
            return None, "Erro: Layout do arquivo inválido. Colunas obrigatórias ausentes."
        
        # BUSCA DAS CONTAS QUE VOCÊ PEDIR
        df_filtrado = df[df['Conta'].astype(str).str.startswith(tuple(contas_alvo))]
        return df_filtrado, "Sucesso"
    except Exception as e:
        return None, f"Erro Crítico no Processamento: {str(e)}"

# --- INTERFACE MASTER ---
st.sidebar.title("🦅 EAGLES MASTER")
usuario = st.sidebar.text_input("Identidade", value="Samuel Richard")
if usuario == "Samuel Richard":
    menu = ["Radar de Importação", "Lente do Contador", "Publicações"]
else:
    menu = ["Lente do Contador"]
escolha = st.sidebar.selectbox("Módulo", menu)

# --- MÓDULO DE IMPORTAÇÃO ---
if escolha == "Radar de Importação":
    st.title("📥 Radar de Importação de Dados")
    st.info("Configuração Afiada: O sistema busca contas específicas e aguarda seu comando para publicar.")

    with st.container():
        st.markdown('<div class="card-master">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Carregar Balancete (CSV)", type="csv")
        contas_input = st.text_input("IDs das Contas Alvo (Ex: 1.1.01, 1.1.05)", "1.1")
        
        if uploaded_file is not None:
            contas_alvo = [c.strip() for c in contas_input.split(",")]
            dados, mensagem = processar_balancete(uploaded_file, contas_alvo)
            
            if dados is not None:
                st.success(mensagem)
                st.session_state.dados_homologados = dados
                st.subheader("Visualização Prévia (Homologação Master)")
                st.dataframe(dados, use_container_width=True)
                
                if st.button("🚀 COMANDAR PUBLICAÇÃO PARA O CLIENTE"):
                    st.session_state.publicado_cliente = True
                    st.balloons()
                    st.success("Dados publicados na Lente do Cliente com sucesso.")
            else:
                st.error(mensagem)
        st.markdown('</div>', unsafe_allow_html=True)

# --- MÓDULO LENTE (O QUE O CLIENTE VÊ) ---
elif escolha == "Lente do Contador":
    st.title("🔍 Lente do Contador")
    if st.session_state.publicado_cliente:
        st.write("### Dados Oficiais Publicados")
        st.dataframe(st.session_state.dados_homologados)
    else:
        st.warning("Aguardando publicação dos dados pelo Diretor Master.")
