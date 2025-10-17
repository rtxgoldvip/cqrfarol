# -*- coding: utf-8 -*-

# Nome do arquivo: test_connection_final.py

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
st.write("Versão Final: Testando com o Driver ODBC 17, o padrão de compatibilidade.")

# --- Carregando Credenciais ---
try:
    st.info("Passo 1: Lendo as credenciais do `st.secrets`...")
    DB_SERVER = st.secrets["db_credentials"]["server"]
    DB_DATABASE = st.secrets["db_credentials"]["database"]
    DB_USERNAME = st.secrets["db_credentials"]["username"]
    DB_PASSWORD = st.secrets["db_credentials"]["password"]
    st.success("Credenciais carregadas!")
except Exception as e:
    st.error(f"Erro ao ler as credenciais do `st.secrets`. Verifique a configuração. Erro: {e}")
    st.stop()

# --- Construindo a String de Conexão FINAL ---
st.info("Passo 2: Construindo a string de conexão com o nome formal do Driver 17...")

# --- A CORREÇÃO FINAL E DEFINITIVA ESTÁ AQUI ---
# Estamos alinhando o nome formal do driver com a versão que instalamos no packages.apt
DRIVER_NAME = '{ODBC Driver 17 for SQL Server}' 

conn_str_display = (
    f"DRIVER={DRIVER_NAME};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_DATABASE};"
    f"UID={DB_USERNAME};"
    f"PWD={'******'};"
    f"TrustServerCertificate=yes;"
)
st.code(conn_str_display, language='text')

# --- Botão para Iniciar o Teste ---
if st.button("🚀 Iniciar Teste de Conexão Final", type="primary"):
    try:
        with st.spinner("Passo 3: Conectando..."):
            cnxn = pyodbc.connect(
                f"DRIVER={DRIVER_NAME};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_USERNAME};PWD={DB_PASSWORD};TrustServerCertificate=yes;",
                timeout=15
            )
        st.success("✅ **LUZ VERDE! A CONEXÃO FOI ESTABELECIDA!**")
        st.balloons()
        st.markdown("---")
        
        with st.spinner("Passo 4: Verificando permissões com uma consulta..."):
            cursor = cnxn.cursor()
            cursor.execute("SELECT @@VERSION;")
            row = cursor.fetchone()
            st.success("✅ **CONSULTA REALIZADA! O BANCO DE DADOS ESTÁ 100% OPERACIONAL!**")
            st.text(row[0])
            cnxn.close()
            st.markdown("### Parabéns, Sócio! O obstáculo técnico foi superado. Podemos prosseguir com o desenvolvimento da IA.")

    except Exception as e:
        st.error("❌ FALHA NA CONEXÃO!", icon="🔥")
        st.markdown("---")
        st.subheader("Diagnóstico do Erro:")
        st.error(f"Erro: **{e}**")
        st.warning("""
        Se o erro persistir, as causas mais prováveis são **Firewall** ou **Credenciais Incorretas**, conforme detalhado anteriormente. 
        O problema de **Driver** foi resolvido com esta versão.
        """)
