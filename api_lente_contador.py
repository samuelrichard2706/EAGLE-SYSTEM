import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL EAGLES (Premium Dark Mode) ---
st.set_page_config(page_title="EAGLES - BPO Estratégico", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #262730; color: white; border: 1px solid #4a4a4a; }
    .stButton>button:hover { border: 1px solid #00ffcc; color: #00ffcc; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7bcf,#2e7bcf); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE IDENTIDADE MASTER ---
# Aqui é onde você se identifica. Quando o login for "Samuel Richard", o menu de admin aparece.
def verificar_permissoes(nome_usuario):
    if nome_usuario == "Samuel Richard":
        return "MASTER"
    return "CONTADOR_PARCEIRO"

# --- INTERFACE PRINCIPAL ---
st.sidebar.title("🦅 EAGLES SYSTEM")
usuario_logado = st.sidebar.text_input("Usuário", value="Samuel Richard") # Simulação de Login
nivel_acesso = verificar_permissoes(usuario_logado)

st.sidebar.write(f"Nível: **{nivel_acesso}**")
st.sidebar.markdown("---")

menu = ["Voo da Águia (Dashboard)", "Lente do Contador", "Gestão de Parceiros", "Configurações"]
escolha = st.sidebar.selectbox("Navegação", menu)

# --- ABA: GESTÃO DE PARCEIROS (Exclusivo para o Samuel) ---
if escolha == "Gestão de Parceiros":
    if nivel_acesso == "MASTER":
        st.title("👥 Gestão de Contadores Parceiros")
        st.subheader("Cadastre novos contadores para a rede Eagles")
        
        with st.form("form_novo_contador"):
            col1, col2 = st.columns(2)
            nome_novo = col1.text_input("Nome do Contador")
            email_novo = col2.text_input("E-mail Profissional")
            permissao = st.selectbox("Tipo de Acesso", ["Contador Pleno", "Contador Júnior"])
            
            btn_cadastrar = st.form_submit_button("Liberar Acesso")
            if btn_cadastrar:
                st.success(f"Acesso liberado para {nome_novo}! Ele agora pode cadastrar empresas.")
    else:
        st.error("Acesso Negado. Apenas o Master (Samuel) pode gerenciar parceiros.")

# --- ABA: VOO DA ÁGUIA (Visão do Dono com seu Pro-labore) ---
elif escolha == "Voo da Águia (Dashboard)":
    st.title("🦅 Voo da Águia - Dashboard Estratégico")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ponto de Equilíbrio", "R$ 15.400,00", "+2%")
    col2.metric("Seu Pro-labore", "R$ 100,00", "Fixado")
    col3.metric("Lucro Alquímico", "R$ 4.250,00", "Saudável")

    st.markdown("### 🔍 Observações da Lente do Contador")
    st.info("⚠️ **Conta: Fornecedores** - Samuel Richard observou um aumento de 15% nos custos. Sugerimos renegociar o prazo.")

# --- ABA: LENTE DO CONTADOR (Operação) ---
elif escolha == "Lente do Contador":
    st.title("🔍 A Lente do Contador")
    st.write("Selecione um lançamento para inserir sua observação estratégica.")
    
    # Simulação de dados que vêm do seu SQL
    dados_balancete = pd.DataFrame({
        'Conta': ['Energia Elétrica', 'Pro-labore', 'Estoque de Peças'],
        'Valor': [1200, 100, 5500],
        'Status': ['Analisado', 'Ok', 'Pendente']
    })
    
    st.table(dados_balancete)
    observacao = st.text_area("Insira sua análise para o Dono ver:")
    if st.button("Publicar na Visão do Dono"):
        st.success("Observação enviada para o Dashboard!")
