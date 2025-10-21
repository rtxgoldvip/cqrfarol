# -*- coding: utf-8 -*-
# Nome do arquivo: extrator_maestro.py
# VERSÃO 3.0 - MODO DIAGNÓSTICO COMPLETO

import streamlit as st
import pandas as pd
import pyodbc
import io

# --- Configuração da Página ---
st.set_page_config(page_title="Extrator de Dados Maestro (Diagnóstico)", layout="wide")
st.markdown("""
<style>
    .main { background-color: #050818; }
    h1, h2 {
        background: -webkit-linear-gradient(45deg, #00BFFF, #FF1493);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌌 Extrator de Dados Maestro 3.0 (Modo Diagnóstico)")
st.warning("Esta versão extrai TODAS as tabelas de negócio para abas separadas em um único arquivo Excel. O objetivo é investigar as relações de dados.")

# --- Conexão Segura ---
try:
    DB_SERVER = st.secrets["db_credentials"]["server"]
    DB_DATABASE = st.secrets["db_credentials"]["database"]
    DB_USERNAME = st.secrets["db_credentials"]["username"]
    DB_PASSWORD = st.secrets["db_credentials"]["password"]
except Exception:
    st.error("As credenciais do banco de dados não foram encontradas nos `st.secrets`. Configure-as antes de continuar.")
    st.stop()

def get_connection():
    """Cria e retorna a conexão com o banco de dados."""
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USERNAME};"
        f"PWD={DB_PASSWORD};"
        f"TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str, timeout=30) # Aumentei o timeout

# --- Dicionário de Todas as Queries ---
QUERIES = {
    "Tb_GestorFin2_FATOS": "SELECT * FROM Tb_GestorFin2",
    "ContasReceber_CAIXA": "SELECT * FROM [Contas Receber]",
    "ContasPagar_CAIXA": "SELECT * FROM [Contas Pagar]",
    "Projetos_DIM": "SELECT * FROM tb_Proj",
    "Tecnicos_DIM": "SELECT * FROM tb_tec",
    "Clientes_DIM": "SELECT * FROM tb_cli",
    "Skills_N_N": "SELECT * FROM tb_amarradisc",
    "ItensProjeto_DIM": "SELECT * FROM tb_itemproj",
    "Apontamentos_DIARIO": "SELECT * FROM tb_apontamentos",
    "Agendas_DIARIO": "SELECT * FROM tb_agendas",
    "TipoProjeto_DIM": "SELECT * FROM tb_tipoproj",
    "Nivel_DIM": "SELECT * FROM tb_nivel",
    "Negocio_DIM": "SELECT * FROM tb_neg",
    "StatusProjeto_DIM": "SELECT * FROM tb_StatusProj",
    "Responsavel_DIM": "SELECT * FROM tb_respproj",
    "Disciplina_DIM": "SELECT * FROM tb_disciplina",
    "Filial_DIM": "SELECT * FROM tb_fil",
    "ClassifFinanc_DIM": "SELECT * FROM ClassifFinanc"
}

# --- Botão de Extração ---
if st.button("🚀 Extrair DADOS COMPLETOS (Diagnóstico)", type="primary"):
    try:
        cnxn = get_connection()
        
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        st.info("Conexão estabelecida. Iniciando extração de múltiplas tabelas...")
        
        summary = []
        
        # Loop para executar cada query e salvar em uma aba
        for sheet_name, query in QUERIES.items():
            try:
                with st.spinner(f"Extraindo dados da aba: {sheet_name}..."):
                    df = pd.read_sql(query, cnxn)
                
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                st.write(f"✔️ ...Aba `{sheet_name}` extraída com {len(df)} registros.")
                summary.append(f"| {sheet_name} | {len(df)} registros |")
            except Exception as e:
                st.warning(f"⚠️ ...Falha ao extrair aba `{sheet_name}`. Erro: {e}")
                summary.append(f"| {sheet_name} | FALHA NA EXTRAÇÃO |")
                
        # Fechar conexão e salvar o arquivo Excel
        cnxn.close()
        writer.close() # Salva o Excel
        excel_data = output.getvalue()
        
        st.success("✅ Extração Completa de Diagnóstico Concluída!")
        
        st.subheader("Resumo da Extração")
        st.markdown("\n".join(summary))
        
        st.markdown("---")
        
        st.download_button(
            label="📥 Baixar Arquivo Excel de Diagnóstico Completo",
            data=excel_data,
            file_name="dados_maestro_DIAGNOSTICO.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error("❌ Ocorreu um erro geral durante a extração!", icon="🔥")
        st.error(f"Detalhes do erro: {e}")

