# -*- coding: utf-8 -*-

# Nome do arquivo: test_connection_v2.py

import streamlit as st
import pyodbc

# --- Configuração da Página ---
st.set_page_config(page_title="Teste de Conexão Quântica", layout="centered")
st.markdown("""
<style>
    .main { background-color: #050818; }
    h1 {
        background: -webkit-linear-gradient(45deg, #00BFFF, #8A2BE2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔬 Testador de Conexão Quântica")
st.write("Esta ferramenta realiza um teste definitivo de conexão com o banco de dados SQL Server a partir do ambiente do Streamlit Cloud.")

# --- Carregando Credenciais de Forma Segura ---
try:
    st.info("Passo 1: Lendo as credenciais do `st.secrets`...")
    DB_SERVER = st.secrets["db_credentials"]["server"]
    DB_DATABASE = st.secrets["db_credentials"]["database"]
    DB_USERNAME = st.secrets["db_credentials"]["username"]
    DB_PASSWORD = st.secrets["db_credentials"]["password"]
    st.success("Credenciais carregadas com sucesso!")
except Exception as e:
    st.error(f"Erro ao ler as credenciais do `st.secrets`. Verifique se o arquivo de segredos está configurado corretamente no Streamlit Cloud. Erro: {e}")
    st.stop() # Interrompe a execução se as credenciais não puderem ser lidas

# --- Construindo a String de Conexão (com a correção) ---
st.info("Passo 2: Construindo a string de conexão...")
# A correção crucial: usamos 'msodbcsql18' como o nome do driver.
DRIVER_NAME = '{msodbcsql18}' 
conn_str = (
    f"DRIVER={DRIVER_NAME};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_DATABASE};"
    f"UID={DB_USERNAME};"
    f"PWD={'******'};" # Mascarando a senha na exibição
    f"TrustServerCertificate=yes;"
)
st.code(conn_str, language='text')

# --- Botão para Iniciar o Teste ---
if st.button("🚀 Iniciar Teste de Conexão", type="primary"):
    try:
        with st.spinner("Passo 3: Tentando estabelecer a conexão com o servidor... Isso pode levar alguns segundos."):
            # Tenta estabelecer a conexão com um timeout de 15 segundos
            cnxn = pyodbc.connect(
                f"DRIVER={DRIVER_NAME};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_USERNAME};PWD={DB_PASSWORD};TrustServerCertificate=yes;",
                timeout=15
            )
        st.success("✅ **CONEXÃO BEM-SUCEDIDA!**")
        st.balloons()
        st.markdown("---")
        
        with st.spinner("Passo 4: Conexão estabelecida! Executando uma consulta de teste para verificar permissões..."):
            cursor = cnxn.cursor()
            cursor.execute("SELECT @@VERSION;")
            row = cursor.fetchone()
            st.success("✅ **CONSULTA EXECUTADA COM SUCESSO!**")
            st.subheader("Informações do Servidor:")
            st.text(row[0])
            cnxn.close()

    except Exception as e:
        st.error("❌ FALHA CRÍTICA NA CONEXÃO!", icon="🔥")
        st.markdown("---")
        st.subheader("Diagnóstico do Erro:")
        st.error(f"Ocorreu um erro ao tentar conectar ou executar a consulta: **{e}**")
        
        st.subheader("Análise e Próximos Passos:")
        st.warning("""
        **Com base neste erro, o diagnóstico mais provável é:**

        1.  **Firewall (Causa Mais Provável):** O firewall do seu servidor de banco de dados (`78.142.242.144`) **NÃO** está permitindo a conexão vinda dos servidores do Streamlit Cloud.
            -   **Ação Necessária:** Você precisa adicionar uma regra de entrada no firewall do seu servidor para liberar a porta `1433` (ou a porta que seu SQL Server usa) para **TODOS os IPs de origem**. O Streamlit usa uma faixa de IPs dinâmica, então a forma mais fácil é liberar para `0.0.0.0/0`.

        2.  **Credenciais Incorretas:** Verifique novamente o IP, nome do banco, usuário e, principalmente, a senha nos `secrets` do Streamlit. Um único caractere errado causará falha.

        3.  **Servidor Offline ou Porta Errada:** Confirme se o serviço do SQL Server está rodando no servidor e se ele está escutando na porta correta (geralmente 1433).
        """)
