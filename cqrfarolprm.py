# -*- coding: utf-8 -*-
# Nome do arquivo: extrator_maestro.py

import streamlit as st
import pandas as pd
import pyodbc
import io

# --- Configuração da Página ---
st.set_page_config(page_title="Extrator de Dados para o Maestro", layout="centered")
st.markdown("""
<style>
    .main { background-color: #050818; }
    h1, h2 {
        background: -webkit-linear-gradient(45deg, #00BFFF, #39FF14);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌌 Extrator de Dados para o Maestro")
st.write("Esta aplicação segura extrai os dados enriquecidos do banco de dados e os prepara para análise pela IA.")
st.info("Clique no botão abaixo para iniciar a extração. O processo pode levar alguns segundos.")

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
    return pyodbc.connect(conn_str, timeout=15)

# --- A "Super Query" Final e Validada ---
SUPER_QUERY = """
SELECT
    g.IdGest2,
    CAST(g.Mes as INT) as Mes,
    CAST(g.Ano as INT) as Ano,
    g.QtHrOrc as Horas_Previstas,
    g.QtHrReal as Horas_Realizadas,
    g.ReceitaReal as Receita_Total,
    g.CustoReal as Custo_Total,
    g.PercMgReal as Margem_Percentual,
    
    -- DNA do Consultor
    tec.NomeTec as Consultor,
    niv.DescNivel as Nivel_Consultor,

    -- Anatomia do Projeto
    p.DescProj as Projeto,
    p.ObsProj as Projeto_Descricao,
    t.DescTipo as Tipo_Projeto,
    neg.DescNeg as Negocio_Projeto,
    status.DescStatus as Status_Projeto,
    resp.NomeResp as Responsavel_Projeto,

    -- Perfil do Cliente
    cli.DescCli as Cliente

FROM 
    Tb_GestorFin2 g
LEFT JOIN 
    tb_Proj p ON g.ProjGest = p.AutNumProj
LEFT JOIN 
    tb_tec tec ON g.ConsultGest = tec.AutNumTec
LEFT JOIN 
    tb_cli cli ON p.CodCliProj = cli.AutNumCli
LEFT JOIN 
    tb_tipoproj t ON p.TipoProj = t.AutNumTipo
LEFT JOIN 
    tb_neg neg ON p.CodNegProj = neg.AutNumNeg
LEFT JOIN 
    tb_StatusProj status ON p.StatusProj = status.AutNumStatus
LEFT JOIN
    tb_respproj resp ON p.RespProj1 = resp.AutNumResp
-- PONTO CHAVE: Usando a tabela de amarração para encontrar o nível
LEFT JOIN 
    tb_amarradisc amarra ON tec.AutNumTec = amarra.CodTecAmar
LEFT JOIN 
    tb_nivel niv ON amarra.Nivel = niv.AutNivel

WHERE 
    tec.NomeTec IS NOT NULL 
    AND p.DescProj IS NOT NULL
-- Agrupando para evitar duplicatas
GROUP BY
    g.IdGest2, g.Mes, g.Ano, g.QtHrOrc, g.QtHrReal, g.ReceitaReal, g.CustoReal,
    g.PercMgReal, tec.NomeTec, niv.DescNivel, p.DescProj, p.ObsProj,
    t.DescTipo, neg.DescNeg, status.DescStatus, resp.NomeResp, cli.DescCli;
"""

# --- Botão de Extração ---
if st.button("🚀 Extrair Dados Agora", type="primary"):
    try:
        with st.spinner("Conectando ao universo de dados e executando a Super Query..."):
            cnxn = get_connection()
            df = pd.read_sql(SUPER_QUERY, cnxn)
            cnxn.close()
        
        st.success(f"✅ Extração Concluída com Sucesso! {len(df)} registros de potencial encontrados.")
        st.markdown("---")
        
        st.subheader("Pré-visualização dos Dados (as 5 primeiras linhas):")
        st.dataframe(df.head())
        
        st.markdown("---")
        st.subheader("Baixar o Arquivo Completo")
        
        # Converte o dataframe para Excel em memória
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='DadosMaestro')
        
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 Baixar Arquivo Excel para o Maestro",
            data=excel_data,
            file_name="dados_maestro_extraidos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error("❌ Ocorreu um erro durante a extração!", icon="🔥")
        st.error(f"Detalhes do erro: {e}")