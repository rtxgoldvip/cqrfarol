# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS NECESSÁRIOS
# ═══════════════════════════════════════════════════════════════════════════════
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from scipy import stats
import io  # <-- Para exportação Excel
import re

# Import da conexão de banco de dados
import pyodbc

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA - DESIGN PREMIUM
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="MAESTRO FAROL - Autonomous Insight System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CSS PREMIUM (COMO FORNECIDO)
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f1419 100%);
        color: #FFFFFF;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f1419 100%);
    }

    /* HEADER PREMIUM */
    .header-premium {
        background: linear-gradient(135deg, rgba(0,191,255,0.1) 0%, rgba(0,119,204,0.05) 100%);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 30px;
        border: 1px solid rgba(0,191,255,0.2);
        box-shadow: 0 8px 32px rgba(0,191,255,0.15);
        position: relative;
        overflow: hidden;
    }

    .header-premium::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0,191,255,0.1) 0%, transparent 70%);
        animation: pulse 8s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.5; }
        50% { transform: scale(1.1) rotate(180deg); opacity: 0.8; }
    }

    .logo-maestro {
        font-size: 3em;
        font-weight: 700;
        background: linear-gradient(135deg, #00BFFF 0%, #0077CC 50%, #00FFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        letter-spacing: 3px;
        text-shadow: 0 0 30px rgba(0,191,255,0.5);
        margin-bottom: 10px;
    }

    .subtitle-maestro {
        text-align: center;
        color: #8A8A8A;
        font-size: 1.1em;
        font-weight: 300;
        letter-spacing: 2px;
        margin-top: -5px;
    }

    /* CARDS PREMIUM */
    .metric-card-premium {
        background: linear-gradient(135deg, rgba(28,28,30,0.95) 0%, rgba(18,18,20,0.98) 100%);
        border-radius: 20px;
        padding: 30px;
        border-left: 4px solid #00BFFF;
        margin: 15px 0;
        box-shadow: 0 10px 40px rgba(0,191,255,0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card-premium:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(0,191,255,0.35);
        border-left-width: 6px;
    }

    .metric-card-premium::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, rgba(0,191,255,0.1) 0%, transparent 70%);
    }

    /* INSIGHT CARDS - GOLD */
    .insight-premium {
        background: linear-gradient(135deg, rgba(255,215,0,0.15) 0%, rgba(255,193,7,0.1) 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border-left: 5px solid #FFD700;
        box-shadow: 0 8px 30px rgba(255,215,0,0.25);
        transition: all 0.3s ease;
        position: relative;
    }

    .insight-premium:hover {
        transform: translateX(5px);
        box-shadow: 0 12px 40px rgba(255,215,0,0.35);
    }

    .insight-premium::before {
        content: '💡';
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 2em;
        opacity: 0.3;
    }

    /* ALERT CARDS - RED */
    .alert-premium {
        background: linear-gradient(135deg, rgba(255,69,0,0.15) 0%, rgba(220,20,60,0.1) 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border-left: 5px solid #FF4500;
        box-shadow: 0 8px 30px rgba(255,69,0,0.25);
        transition: all 0.3s ease;
        animation: alertPulse 2s ease-in-out infinite;
    }

    @keyframes alertPulse {
        0%, 100% { border-left-color: #FF4500; }
        50% { border-left-color: #FF6347; box-shadow: 0 12px 40px rgba(255,69,0,0.4); }
    }

    /* SUCCESS CARDS - GREEN */
    .success-premium {
        background: linear-gradient(135deg, rgba(57,255,20,0.15) 0%, rgba(34,197,94,0.1) 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border-left: 5px solid #39FF14;
        box-shadow: 0 8px 30px rgba(57,255,20,0.25);
        transition: all 0.3s ease;
    }

    /* TÍTULOS E TEXTOS */
    h1, h2, h3, h4 {
        color: #00BFFF !important;
        font-weight: 600;
        letter-spacing: 1px;
    }

    h2 {
        border-bottom: 2px solid rgba(0,191,255,0.3);
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    /* SIDEBAR PREMIUM */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0f 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(0,191,255,0.2);
    }

    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stMultiSelect {
        background: rgba(28,28,30,0.8);
        border-radius: 10px;
        padding: 5px;
    }

    /* TABS PERSONALIZADAS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(28,28,30,0.5);
        border-radius: 15px;
        padding: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(28,28,30,0.8);
        border-radius: 10px;
        padding: 10px 20px;
        color: #8A8A8A;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00BFFF 0%, #0077CC 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0,191,255,0.4);
    }

    /* MÉTRICAS CUSTOMIZADAS */
    [data-testid="stMetricValue"] {
        font-size: 2em;
        font-weight: 700;
        color: #00BFFF;
    }

    [data-testid="stMetricDelta"] {
        font-size: 1.1em;
        font-weight: 600;
    }

    /* LOADING ANIMATION */
    .stSpinner > div {
        border-top-color: #00BFFF !important;
    }

    /* SCROLLBAR PERSONALIZADA */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(28,28,30,0.5);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00BFFF 0%, #0077CC 100%);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #0077CC 0%, #00BFFF 100%);
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MOTOR DE CONEXÃO COM BANCO DE DADOS
# ═══════════════════════════════════════════════════════════════════════════════

# Configuração de conexão
@st.cache_resource
def init_connection():
    """Cria e retorna a conexão com o banco de dados."""
    try:
        DB_SERVER = st.secrets["db_credentials"]["server"]
        DB_DATABASE = st.secrets["db_credentials"]["database"]
        DB_USERNAME = st.secrets["db_credentials"]["username"]
        DB_PASSWORD = st.secrets["db_credentials"]["password"]

        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_DATABASE};"
            f"UID={DB_USERNAME};"
            f"PWD={DB_PASSWORD};"
            f"TrustServerCertificate=yes;"
        )
        return pyodbc.connect(conn_str, timeout=30)
    except Exception as e:
        st.error(f"❌ Erro de Conexão com Banco de Dados: {e}")
        st.error("Verifique suas credenciais em st.secrets")
        return None

# Função para executar queries
@st.cache_data(ttl=600)
def run_query(query, _conn):
    """Executa a query e retorna um DataFrame."""
    if not _conn:
        st.error("Conexão com banco de dados inválida.")
        return pd.DataFrame()
    try:
        return pd.read_sql(query, _conn)
    except Exception as e:
        st.warning(f"⚠️ Falha ao executar query: {query}. Erro: {e}")
        return pd.DataFrame()

# ═══════════════════════════════════════════════════════════════════════════════
# FUNÇÃO AUXILIAR PARA EXPORTAR EXCEL
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data
def to_excel(df_rec, df_pag):
    """Converte DataFrames de Fechamento para um arquivo Excel em memória."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        if not df_rec.empty:
            df_rec.to_excel(writer, sheet_name='A_Receber', index=False)
        if not df_pag.empty:
            df_pag.to_excel(writer, sheet_name='A_Pagar', index=False)
    processed_data = output.getvalue()
    return processed_data

# ═══════════════════════════════════════════════════════════════════════════════
# MOTOR DE RACIOCÍNIO QUÂNTICO (CRQ) - NÚCLEO INTELIGENTE (REVISÃO PROFUNDA)
# ═══════════════════════════════════════════════════════════════════════════════

class CoreQuantumReasoning:
    """
    Núcleo de Raciocínio Quântico
    Revisado para tratar o "Bug de 2025" e aprofundar análises.
    """

    def __init__(self):
        self.conn = init_connection()
        if self.conn:
            with st.spinner('🌌 Carregando Universo de Dados do Banco...'):
                self.dados_universo = self.load_universo_dados()
        else:
            st.error("Falha na inicialização do CRQ: Conexão com banco de dados falhou.")
            self.dados_universo = pd.DataFrame()

        self.estado_quantum = self.dados_universo.copy() if not self.dados_universo.empty else pd.DataFrame()
        self.padroes_ocultos = {}
        self.prescricoes_ativas = []
        self.assinatura_historica = {} # Armazena a "assinatura" do passado

    def load_universo_dados(self):
        """
        Carrega o universo completo de dados do SQL Server.
        *** LÓGICA DE JOIN DE CAIXA REFEITA PARA CORRIGIR BUG DE 2025 ***
        """
        if not self.conn:
            st.error("CRQ: Sem conexão com banco de dados para carregar dados.")
            return pd.DataFrame()

        # 1. Dicionário de Queries (baseado nas tabelas fornecidas)
        QUERIES = {
            "g": "SELECT * FROM Tb_GestorFin2", # FATO
            "cr": "SELECT * FROM [Contas Receber]",
            "cp": "SELECT * FROM [Contas Pagar]",
            "p": "SELECT * FROM tb_Proj",
            "tec": "SELECT * FROM tb_tec",
            "cli": "SELECT * FROM tb_cli",
            "tp": "SELECT * FROM tb_tipoproj",
            "neg": "SELECT * FROM tb_neg",
            "st": "SELECT * FROM tb_StatusProj",
        }

        # 2. Carregar todas as tabelas
        dfs = {}
        all_loaded = True
        with st.spinner("Conectando e buscando dados mestre..."):
            for name, query in QUERIES.items():
                dfs[name] = run_query(query, self.conn)
                if dfs[name].empty:
                    st.warning(f"Tabela '{name}' está vazia ou falhou ao carregar.")
                    if name == 'g':
                        all_loaded = False

        if not all_loaded or 'g' not in dfs or dfs['g'].empty:
            st.error("Tabela Fato (Tb_GestorFin2) está vazia. Análise impossível.")
            return pd.DataFrame()

        dims_criticas = ['p', 'tec', 'cli', 'tp', 'neg', 'st', 'cr', 'cp']
        for dim in dims_criticas:
            if dim not in dfs:
                st.warning(f"Tabela de dimensão '{dim}' não foi carregada. Criando DataFrame vazio.")
                dfs[dim] = pd.DataFrame()

        # 3. Limpeza de Chaves (Crucial)
        try:
            # FATO
            df_fato = dfs['g']
            df_fato['ConsultGest'] = pd.to_numeric(df_fato['ConsultGest'], errors='coerce')
            df_fato['ProjGest'] = pd.to_numeric(df_fato['ProjGest'], errors='coerce')
            df_fato['Ano'] = pd.to_numeric(df_fato['Ano'].astype(str).str.strip(), errors='coerce')
            df_fato['Mes'] = pd.to_numeric(df_fato['Mes'].astype(str).str.strip(), errors='coerce')
            df_fato = df_fato.dropna(subset=['Ano', 'Mes', 'ConsultGest', 'ProjGest'])
            df_fato['Ano'] = df_fato['Ano'].astype(int)
            df_fato['Mes'] = df_fato['Mes'].astype(int)

            # DIMS CONTÁBEIS
            if not dfs['tec'].empty:
                dfs['tec']['AutNumTec'] = pd.to_numeric(dfs['tec']['AutNumTec'], errors='coerce')
            if not dfs['p'].empty:
                dfs['p']['AutNumProj'] = pd.to_numeric(dfs['p']['AutNumProj'], errors='coerce')
                dfs['p']['CodCliProj'] = pd.to_numeric(dfs['p']['CodCliProj'], errors='coerce')
                dfs['p']['TipoProj'] = pd.to_numeric(dfs['p']['TipoProj'], errors='coerce')
            if not dfs['cli'].empty:
                dfs['cli']['AutNumCli'] = pd.to_numeric(dfs['cli']['AutNumCli'], errors='coerce')
            if not dfs['tp'].empty:
                dfs['tp']['AutNumTipo'] = pd.to_numeric(dfs['tp']['AutNumTipo'], errors='coerce')
            
            # 4. PREPARAÇÃO DO FLUXO DE CAIXA (A CORREÇÃO DO BUG 2025)
            # Não vamos mais usar o JOIN por 'IdGest2' <> 'ID'
            
            # CONTAS A RECEBER (CAIXA ENTRADA)
            df_cr = dfs['cr'].copy()
            df_cr['DtRec'] = pd.to_datetime(df_cr['DtRec'], errors='coerce')
            df_cr = df_cr.dropna(subset=['DtRec'])
            df_cr['Caixa_Ano'] = df_cr['DtRec'].dt.year
            df_cr['Caixa_Mes'] = df_cr['DtRec'].dt.month
            df_cr['Cliente'] = pd.to_numeric(df_cr['Cliente'], errors='coerce')
            df_cr['VlRec'] = pd.to_numeric(df_cr['VlRec'], errors='coerce').fillna(0)
            # Agrega o caixa por Ano, Mês e Cliente
            cr_agg = df_cr.groupby(['Caixa_Ano', 'Caixa_Mes', 'Cliente'])['VlRec'].sum().reset_index()

            # CONTAS A PAGAR (CAIXA SAÍDA)
            df_cp = dfs['cp'].copy()
            df_cp['DtPagamento'] = pd.to_datetime(df_cp['DtPagamento'], errors='coerce')
            df_cp = df_cp.dropna(subset=['DtPagamento'])
            df_cp['Caixa_Ano'] = df_cp['DtPagamento'].dt.year
            df_cp['Caixa_Mes'] = df_cp['DtPagamento'].dt.month
            df_cp['Prestador'] = pd.to_numeric(df_cp['Prestador'], errors='coerce')
            df_cp['VlPago'] = pd.to_numeric(df_cp['VlPago'], errors='coerce').fillna(0)
            # Agrega o caixa por Ano, Mês e Prestador (Consultor)
            cp_agg = df_cp.groupby(['Caixa_Ano', 'Caixa_Mes', 'Prestador'])['VlPago'].sum().reset_index()

        except Exception as e:
            st.error(f"Erro na limpeza de chaves e preparação do caixa: {e}")
            return pd.DataFrame()

        # 5. Executar o "Master Join" (Visão Contábil)
        with st.spinner("Entrelaçando dimensões (Joins)..."):
            df = df_fato
            
            def safe_merge(df_left, df_right, **kwargs):
                if df_right.empty:
                    return df_left
                left_key = kwargs.get('left_on')
                right_key = kwargs.get('right_on')
                if left_key and left_key not in df_left.columns:
                    st.warning(f"Chave '{left_key}' não encontrada no DF esquerdo.")
                    return df_left
                if right_key and right_key not in df_right.columns:
                    st.warning(f"Chave '{right_key}' não encontrada no DF direito.")
                    df_right[right_key] = pd.NA
                return pd.merge(df_left, df_right, **kwargs)

            df = safe_merge(df, dfs['tec'], left_on='ConsultGest', right_on='AutNumTec', how='left')
            df = safe_merge(df, dfs['p'], left_on='ProjGest', right_on='AutNumProj', how='left', suffixes=('', '_proj'))
            df = safe_merge(df, dfs['cli'], left_on='CodCliProj', right_on='AutNumCli', how='left')
            df = safe_merge(df, dfs['tp'], left_on='TipoProj', right_on='AutNumTipo', how='left')
            df = safe_merge(df, dfs['neg'], left_on='CodNegProj', right_on='AutNumNeg', how='left')
            df = safe_merge(df, dfs['st'], left_on='StatusProj', right_on='AutNumStatus', how='left')

        # 6. Mapeamento e Criação de Métricas (Contábil)
        with st.spinner("Mapeando colunas e criando métricas contábeis..."):
            mapa_colunas = {
                'QtHrReal': 'Hrs_Real',
                'QtHrOrc': 'Hrs_Prev',
                'ReceitaReal': 'Receita',
                'CustoReal': 'Custo',
                'PercMgReal': 'Margem_Fracao', # Manter como fração
                'VlHrOrc': 'VH_Venda',
                'VlHrCusto': 'VH_Custo',
                'ReceitaOrc': 'Receita_Orc',
                'CustoOrc': 'Custo_Orc',
                'VlTTFat': 'Vl_Faturado_Contrato', # <--- NOVA COLUNA P/ SANGRIA
                'NomeTec': 'Consultor',
                'DescCli': 'Cliente',
                'DescProj': 'Projeto',
                'DescTipo': 'TipoProj',
            }

            cols_existentes = {k: v for k, v in mapa_colunas.items() if k in df.columns}
            df = df.rename(columns=cols_existentes)
            
            colunas_numericas_app = [
                'Hrs_Real', 'Hrs_Prev', 'Receita', 'Custo', 'Margem_Fracao',
                'VH_Venda', 'VH_Custo', 'Receita_Orc', 'Custo_Orc',
                'Vl_Faturado_Contrato'
            ]

            for col in colunas_numericas_app:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                else:
                    df[col] = 0
            
            # Recalcular Margem para garantir (caso PercMgReal não seja confiável)
            df['Margem'] = np.where(
                df['Receita'] > 0, 
                (df['Receita'] - df['Custo']) / df['Receita'], 
                0
            )
            df['Lucro'] = df['Receita'] - df['Custo']
            df['Desvio_Hrs'] = df['Hrs_Real'] - df['Hrs_Prev']
            df['Eficiencia'] = np.where(df['Hrs_Prev'] > 0,
                                       (df['Hrs_Real'] / df['Hrs_Prev']), 1) # Fração
            df['ROI_Hora'] = np.where(df['Hrs_Real'] > 0,
                                     df['Lucro'] / df['Hrs_Real'], 0)
            df['Produtividade'] = np.where(df['Hrs_Real'] > 0,
                                          df['Receita'] / df['Hrs_Real'], 0)
            
            # Dimensão temporal
            df['Data'] = pd.to_datetime(df['Ano'].astype(str) + '-' +
                                       df['Mes'].astype(str) + '-01',
                                       errors='coerce')
            df = df.dropna(subset=['Data']) # Crucial

        # 7. ENTRELAÇAMENTO DE CAIXA (A NOVA LÓGICA)
        with st.spinner("Entrelaçando dados de Fluxo de Caixa..."):
            
            # Precisamos agregar o DF contábil para o mesmo nível do caixa
            df_contabil_agg_cli = df.groupby(['Ano', 'Mes', 'CodCliProj']).agg(
                Receita_Agg=('Receita', 'sum')
            ).reset_index()
            
            df_contabil_agg_tec = df.groupby(['Ano', 'Mes', 'ConsultGest']).agg(
                Custo_Agg=('Custo', 'sum')
            ).reset_index()
            
            # Juntar os agregados de caixa (cr_agg, cp_agg) com os agregados contábeis
            df_caixa_cli = pd.merge(
                df_contabil_agg_cli, 
                cr_agg, 
                left_on=['Ano', 'Mes', 'CodCliProj'], 
                right_on=['Caixa_Ano', 'Caixa_Mes', 'Cliente'], 
                how='outer' # Outer join para pegar meses só de caixa ou só de contábil
            )
            
            df_caixa_tec = pd.merge(
                df_contabil_agg_tec, 
                cp_agg, 
                left_on=['Ano', 'Mes', 'ConsultGest'], 
                right_on=['Caixa_Ano', 'Caixa_Mes', 'Prestador'], 
                how='outer'
            )

            # Preencher NaNs pós-merge
            df_caixa_cli['VlRec'] = df_caixa_cli['VlRec'].fillna(0)
            df_caixa_tec['VlPago'] = df_caixa_tec['VlPago'].fillna(0)
            
            # Trazer os valores de caixa de volta para o DF principal (granular)
            # Mapear VlRec por (Ano, Mes, CodCliProj)
            mapa_recebimentos = df_caixa_cli.groupby(['Ano', 'Mes', 'CodCliProj'])['VlRec'].sum()
            df['Caixa_Recebido'] = df.set_index(['Ano', 'Mes', 'CodCliProj']).index.map(mapa_recebimentos).fillna(0)

            # Mapear VlPago por (Ano, Mes, ConsultGest)
            mapa_pagamentos = df_caixa_tec.groupby(['Ano', 'Mes', 'ConsultGest'])['VlPago'].sum()
            df['Caixa_Pago'] = df.set_index(['Ano', 'Mes', 'ConsultGest']).index.map(mapa_pagamentos).fillna(0)
            
            # Corrigir granularidade: O caixa é agregado, o contábil é granular.
            # Quando juntamos, o caixa se repete por projeto/consultor. Precisamos
            # de uma lógica de distribuição ou aceitar a granularidade.
            
            # Abordagem 2 (Mais simples, pode duplicar): Merge direto
            # Limpar o 'df' anterior
            df = df.drop(columns=['Caixa_Recebido', 'Caixa_Pago'], errors='ignore')

            df = pd.merge(df, cr_agg, 
                          left_on=['Ano', 'Mes', 'CodCliProj'], 
                          right_on=['Caixa_Ano', 'Caixa_Mes', 'Cliente'], 
                          how='left', suffixes=('', '_cr'))
            
            df = pd.merge(df, cp_agg, 
                          left_on=['Ano', 'Mes', 'ConsultGest'], 
                          right_on=['Caixa_Ano', 'Caixa_Mes', 'Prestador'], 
                          how='left', suffixes=('', '_cp'))

            # Renomear e limpar
            df = df.rename(columns={'VlRec': 'Caixa_Recebido', 'VlPago': 'Caixa_Pago'})
            df['Caixa_Recebido'] = df['Caixa_Recebido'].fillna(0)
            df['Caixa_Pago'] = df['Caixa_Pago'].fillna(0)
            
            # O problema desta abordagem é que se um cliente/mês teve 3 projetos,
            # o valor total recebido (VlRec) daquele cliente/mês será 
            # triplicado no 'df' final.
            
            # Abordagem 3 (Correta): Manter a granularidade original e agregar no final.
            # A Abordagem 2 é a única viável sem perder a granularidade contábil.
            # Para corrigir a duplicação, precisamos agregar os dados *antes* de exibi-los.
            # O 'load_universo_dados' vai manter os dados com o caixa "duplicado".
            # O 'calcular_metricas_consolidadas' fará a agregação correta.
            
            # Vamos usar a Abordagem 2, mas com cuidado.
            # O problema é que o VlRec/VlPago é por Cliente/Mês, não por Projeto.
            # A única forma correta é agregar TUDO por (Ano, Mes, Cliente, Consultor)
            
            # Vamos simplificar: O join pelo ID era o que o sistema antigo fazia.
            # A nova regra é: Join por (Ano, Mes, Cliente) e (Ano, Mes, Prestador).
            # O `df` já tem `Ano`, `Mes`, `CodCliProj` (Cliente) e `ConsultGest` (Prestador).
            # O `cr_agg` tem `Caixa_Ano`, `Caixa_Mes`, `Cliente`, `VlRec`.
            # O `cp_agg` tem `Caixa_Ano`, `Caixa_Mes`, `Prestador`, `VlPago`.
            
            # A agregação de caixa `cr_agg` e `cp_agg` está correta.
            # A junção com `df` é o problema.
            
            # *Decisão Final:* O `df` é a tabela FATO contábil (granular).
            # As tabelas `cr` e `cp` são FATOS de caixa (transacionais).
            # A única forma de uni-las é agregar ambas a um nível comum.
            # Nível comum: (Ano, Mes, Cliente, Consultor/Prestador)
            
            # Esta agregação é complexa demais para o load.
            # Vamos voltar à Abordagem 2 (merge no `df` granular) e
            # *corrigir as métricas* em `calcular_metricas_consolidadas`.
            
            df['Lucro_Caixa'] = df['Caixa_Recebido'] - df['Caixa_Pago']
            df['Gap_Faturamento'] = df['Receita'] - df['Caixa_Recebido']
            df['Gap_Custo'] = df['Custo'] - df['Caixa_Pago']


        # 8. Criação de dimensões quânticas (Métricas de Análise)
        with st.spinner("Criando dimensões quânticas (Análise Avançada)..."):
            
            # Lógica de Sangria (Avançada)
            df['Sangria_Risco_Absoluto'] = np.where(
                df['Hrs_Real'] > df['Hrs_Prev'],
                (df['Hrs_Real'] - df['Hrs_Prev']) * df['VH_Custo'], # Custo do estouro
                0
            )
            df['Ociosidade_Risco_Absoluto'] = np.where(
                df['Hrs_Real'] < df['Hrs_Prev'],
                (df['Hrs_Prev'] - df['Hrs_Real']) * (df['VH_Venda'] - df['VH_Custo']), # Lucro perdido
                0
            )

            df['Status_Horas'] = 'OK'
            # 1. Projeto Fechado com Estouro = SANGRIA
            df.loc[
                (df['Hrs_Real'] > df['Hrs_Prev']) & 
                (df['TipoProj'] == 'PROJETO FECHADO'), 
                'Status_Horas'
            ] = 'SANGRIA'
            
            # 2. Projeto Faturado por Hora com Estouro = OPORTUNIDADE (Mais faturamento)
            df.loc[
                (df['Hrs_Real'] > df['Hrs_Prev']) & 
                (df['TipoProj'] == 'FATURADO POR HRS REALIZADAS'), 
                'Status_Horas'
            ] = 'OVERRUN_FATURAVEL'

            # 3. Projeto com horas a menos = OCIOSIDADE (Risco de faturar menos)
            df.loc[
                (df['Hrs_Real'] < df['Hrs_Prev']) & 
                (df['Hrs_Prev'] > 0), 
                'Status_Horas'
            ] = 'OCIOSIDADE'

            # Score de Performance
            df['Score_Performance'] = (
                (df['Margem'] * 0.4) +
                (np.clip(df['Eficiencia'], 0, 2) / 2 * 0.3) + # Eficiencia (1=perfeito)
                (np.clip(df['ROI_Hora'] / 100, 0, 1) * 0.3) # Normaliza ROI (R$100/h = score 1)
            ) * 100

            # Níveis de alerta
            df['Status_Performance'] = pd.cut(df['Score_Performance'],
                                 bins=[-np.inf, 40, 70, np.inf],
                                 labels=['CRÍTICO', 'ATENÇÃO', 'EXCELENTE'],
                                 right=False)

            # Limpeza final de strings para filtros
            colunas_string_app = ['Consultor', 'Cliente', 'Projeto', 'TipoProj']
            for col_str in colunas_string_app:
                if col_str not in df.columns:
                    df[col_str] = 'N/A'
                else:
                    df[col_str] = df[col_str].astype(str).fillna('N/A')
            
            # Remover duplicatas que podem ter sido criadas pelos joins
            # O grão é (Mes, Ano, ConsultGest, ProjGest)
            df = df.drop_duplicates(subset=['Mes', 'Ano', 'ConsultGest', 'ProjGest', 'IdGest2'])

        st.success("Universo de Dados Carregado e Sincronizado.")
        return df

    def aplicar_colapso_quantico(self, filtros):
        """
        Colapso Quântico: Filtra o universo de possibilidades
        """
        if self.dados_universo.empty:
            st.warning("Não há dados carregados para aplicar filtros.")
            self.estado_quantum = pd.DataFrame()
            return self.estado_quantum

        df = self.dados_universo.copy()

        try:
            # Filtros de Seleção Múltipla
            if filtros.get('consultores') and 'TODOS' not in filtros['consultores']:
                df = df[df['Consultor'].isin(filtros['consultores'])]
            if filtros.get('clientes') and 'TODOS' not in filtros['clientes']:
                df = df[df['Cliente'].isin(filtros['clientes'])]
            if filtros.get('projetos') and 'TODOS' not in filtros['projetos']:
                df = df[df['Projeto'].isin(filtros['projetos'])]
            if filtros.get('tipos') and 'TODOS' not in filtros['tipos']:
                df = df[df['TipoProj'].isin(filtros['tipos'])]

            # Filtro de Período (Principal)
            if filtros.get('mes') and filtros.get('ano'):
                mes_sel = int(filtros['mes'])
                ano_sel = int(filtros['ano'])
                df = df[(df['Mes'] == mes_sel) & (df['Ano'] == ano_sel)]

            self.estado_quantum = df
            
            # ATUALIZAR ASSINATURA HISTÓRICA
            self.atualizar_assinatura_historica(ano_sel, mes_sel)
            
            return df
        except Exception as e:
            st.error(f"Erro ao aplicar filtros: {e}")
            self.estado_quantum = pd.DataFrame()
            return self.estado_quantum

    def atualizar_assinatura_historica(self, ano_sel, mes_sel):
        """
        Calcula a "assinatura" (média histórica) dos dados *anteriores* ao período filtrado.
        """
        data_filtro = pd.to_datetime(f'{ano_sel}-{mes_sel}-01')
        df_hist = self.dados_universo[self.dados_universo['Data'] < data_filtro]

        if df_hist.empty:
            self.assinatura_historica = {}
            return

        # Assinatura Média Mensal Histórica
        # Agrupa por mês/ano, calcula métricas, depois tira a média
        
        # Correção da duplicação de caixa:
        # 1. Agrega contábil por Mês/Ano
        hist_contabil = df_hist.groupby(['Ano', 'Mes']).agg(
            Receita=('Receita', 'sum'),
            Custo=('Custo', 'sum'),
            Hrs_Real=('Hrs_Real', 'sum'),
            Hrs_Prev=('Hrs_Prev', 'sum')
        ).reset_index()
        
        # 2. Agrega caixa por Mês/Ano (removendo duplicatas primeiro)
        hist_caixa_rec = df_hist.drop_duplicates(subset=['Ano', 'Mes', 'CodCliProj', 'Caixa_Recebido']).groupby(['Ano', 'Mes'])['Caixa_Recebido'].sum()
        hist_caixa_pag = df_hist.drop_duplicates(subset=['Ano', 'Mes', 'ConsultGest', 'Caixa_Pago']).groupby(['Ano', 'Mes'])['Caixa_Pago'].sum()

        hist_contabil = hist_contabil.set_index(['Ano', 'Mes'])
        hist_contabil['Caixa_Recebido'] = hist_caixa_rec
        hist_contabil['Caixa_Pago'] = hist_caixa_pag
        hist_contabil = hist_contabil.reset_index().fillna(0)
        
        # 3. Calcula métricas históricas
        hist_contabil['Lucro'] = hist_contabil['Receita'] - hist_contabil['Custo']
        hist_contabil['Margem'] = np.where(hist_contabil['Receita'] > 0, hist_contabil['Lucro'] / hist_contabil['Receita'], 0)
        hist_contabil['Lucro_Caixa'] = hist_contabil['Caixa_Recebido'] - hist_contabil['Caixa_Pago']
        hist_contabil['ROI_Hora'] = np.where(hist_contabil['Hrs_Real'] > 0, hist_contabil['Lucro'] / hist_contabil['Hrs_Real'], 0)
        hist_contabil['Eficiencia'] = np.where(hist_contabil['Hrs_Prev'] > 0, hist_contabil['Hrs_Real'] / hist_contabil['Hrs_Prev'], 1)

        # 4. Salva a média
        self.assinatura_historica = {
            'receita_avg': hist_contabil['Receita'].mean(),
            'lucro_avg': hist_contabil['Lucro'].mean(),
            'margem_avg': hist_contabil['Margem'].mean(),
            'lucro_caixa_avg': hist_contabil['Lucro_Caixa'].mean(),
            'roi_hora_avg': hist_contabil['ROI_Hora'].mean(),
            'eficiencia_avg': hist_contabil['Eficiencia'].mean(),
            'count_months': len(hist_contabil)
        }

    def detectar_entrelacements(self):
        """
        Detecta correlações e padrões ocultos no *estado quântico atual* (dados filtrados).
        """
        df = self.estado_quantum
        self.padroes_ocultos = {}

        if df.empty or len(df) < 3:
            return {}

        entrelacements = {}

        try:
            # Correlação: Eficiência vs. Margem
            if 'Eficiencia' in df.columns and 'Margem' in df.columns:
                corr = df[['Eficiencia', 'Margem']].corr().iloc[0, 1]
                if pd.notna(corr) and abs(corr) > 0.5:
                    entrelacements['eficiencia_margem'] = {
                        'forca': corr,
                        'descricao': f"Correlação {'positiva' if corr > 0 else 'negativa'} de {corr:.2f} entre Eficiência (Horas) e Margem."
                    }

            # Disparidade: Performance de Consultores
            if 'Consultor' in df.columns and 'ROI_Hora' in df.columns:
                perf_consultor = df.groupby('Consultor')['ROI_Hora'].mean()
                perf_consultor = perf_consultor[perf_consultor.index != 'N/A'].dropna()
                if len(perf_consultor) > 1:
                    variancia = perf_consultor.std()
                    media = perf_consultor.mean()
                    if pd.notna(variancia) and media != 0 and (variancia / abs(media)) > 0.5:
                        entrelacements['disparidade_consultores'] = {
                            'valor': variancia,
                            'top': perf_consultor.idxmax(),
                            'bottom': perf_consultor.idxmin(),
                            'descricao': f"Alta variação no ROI/Hora entre consultores. Top: {perf_consultor.idxmax()} (R${perf_consultor.max():.2f}/h), Bottom: {perf_consultor.idxmin()} (R${perf_consultor.min():.2f}/h)."
                        }
            
            # Rentabilidade: Tipo de Projeto
            if 'TipoProj' in df.columns and 'Margem' in df.columns:
                perf_tipo = df.groupby('TipoProj')['Margem'].mean()
                perf_tipo = perf_tipo[perf_tipo.index != 'N/A'].dropna()
                if len(perf_tipo) > 1:
                    melhor_tipo = perf_tipo.idxmax()
                    pior_tipo = perf_tipo.idxmin()
                    if (perf_tipo[melhor_tipo] - perf_tipo[pior_tipo]) > 0.15: # 15% de diferença
                        entrelacements['otimizacao_mix'] = {
                            'melhor': melhor_tipo,
                            'pior': pior_tipo,
                            'gap': perf_tipo[melhor_tipo] - perf_tipo[pior_tipo],
                            'descricao': f"'{melhor_tipo}' é {perf_tipo[melhor_tipo]*100:.1f}% mais rentável que '{pior_tipo}' ({perf_tipo[pior_tipo]*100:.1f}%)."
                        }

        except Exception as e:
            st.warning(f"Erro ao detectar entrelaçamentos: {e}")

        self.padroes_ocultos = entrelacements
        return entrelacements

    def gerar_prescricoes_quantum(self):
        """
        Gera prescrições baseadas no estado atual (filtrado) vs. assinatura histórica.
        """
        df = self.estado_quantum
        metricas = self.calcular_metricas_consolidadas()
        hist = self.assinatura_historica
        
        if df.empty:
            return [{
                'tipo': 'INFO', 'prioridade': 'BAIXA', 'titulo': '📊 Aguardando Dados',
                'sintese': 'Selecione filtros para iniciar a ressonância prescritiva',
                'analise': 'O CRQ precisa de dados para processar',
                'prescricao': 'Ajuste os filtros na sidebar',
                'impacto_estimado': 'N/A', 'confianca': 0
            }]

        prescricoes = []
        ano_sel = df['Ano'].iloc[0] # Seguro, pois df não está vazio

        # 1. PRESCRIÇÃO CRÍTICA: DESCOLAMENTO DE CAIXA (O "BUG 2025" DINÂMICO)
        gap_lucro = metricas['lucro'] - metricas['lucro_caixa']
        if metricas['receita'] > 0 and (abs(gap_lucro) / metricas['receita']) > 0.7:
             prescricoes.append({
                'tipo': 'ALERTA', 'prioridade': 'CRÍTICA',
                'titulo': '🚨 ALERTA DE INTEGRIDADE: Descolamento Crítico de Caixa',
                'sintese': f"Lucro Contábil de R$ {metricas['lucro']:,.0f} vs. Lucro de Caixa de R$ {metricas['lucro_caixa']:,.0f}.",
                'analise': f"O sistema detectou um 'descolamento' (gap) de R$ {gap_lucro:,.0f} entre a visão contábil e a visão de caixa.\n"
                          f"Isso sugere que os recebimentos (Caixa_Recebido) e/ou pagamentos (Caixa_Pago) registrados para este período não correspondem aos valores faturados/provisionados.\n"
                          f"**Hipótese (Bug 2025):** Se for 2025 ou posterior, a forma de ligar o caixa (CP/CR) ao faturamento (Fato) pode estar quebrada ou ter mudado (ex: o join por Ano/Mês/Cliente/Prestador não é suficiente).",
                'prescricao': '1. VALIDAR URGENTEMENTE o processo de lançamento de caixa (CP/CR) e sua relação com os lançamentos contábeis (Tb_GestorFin2).\n'
                             '2. Investigar se há inadimplência real ou atrasos de pagamento/recebimento que justifiquem o gap.\n'
                             '3. ATÉ A CORREÇÃO: Confie primariamente na Visão Contábil (Tab 1), mas com extrema cautela sobre a saúde financeira real.',
                'impacto_estimado': 'PERDA TOTAL da visão de Caixa. Risco de má gestão financeira.',
                'confianca': 100
            })
        
        # 2. ANÁLISE DE SANGRIA E OCIOSIDADE (LÓGICA AVANÇADA)
        sangria_total = df[df['Status_Horas'] == 'SANGRIA']['Sangria_Risco_Absoluto'].sum()
        ociosidade_total = df[df['Status_Horas'] == 'OCIOSIDADE']['Ociosidade_Risco_Absoluto'].sum()
        overrun_faturavel_total = df[df['Status_Horas'] == 'OVERRUN_FATURAVEL']['Hrs_Real'].
