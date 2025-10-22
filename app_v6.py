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
import io
import re
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
# CSS PREMIUM
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
    .success-premium {
        background: linear-gradient(135deg, rgba(57,255,20,0.15) 0%, rgba(34,197,94,0.1) 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border-left: 5px solid #39FF14;
        box-shadow: 0 8px 30px rgba(57,255,20,0.25);
        transition: all 0.3s ease;
    }
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
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0f 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(0,191,255,0.2);
    }
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
    [data-testid="stMetricValue"] {
        font-size: 2em;
        font-weight: 700;
        color: #00BFFF;
    }
    [data-testid="stMetricDelta"] {
        font-size: 1.1em;
        font-weight: 600;
    }
    .stSpinner > div {
        border-top-color: #00BFFF !important;
    }
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
        return None

@st.cache_data(ttl=600)
def run_query(query, _conn):
    """Executa a query e retorna um DataFrame."""
    if not _conn:
        st.error("Conexão com banco de dados inválida.")
        return pd.DataFrame()
    try:
        return pd.read_sql(query, _conn)
    except Exception as e:
        st.warning(f"⚠️ Falha ao executar query: {e}")
        return pd.DataFrame()

@st.cache_data
def to_excel(df_rec, df_pag):
    """Converte DataFrames para Excel em memória."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        if not df_rec.empty:
            df_rec.to_excel(writer, sheet_name='A_Receber', index=False)
        if not df_pag.empty:
            df_pag.to_excel(writer, sheet_name='A_Pagar', index=False)
    return output.getvalue()
# ═══════════════════════════════════════════════════════════════════════════════
# MOTOR DE RACIOCÍNIO QUÂNTICO (CRQ) - CORRIGIDO
# ═══════════════════════════════════════════════════════════════════════════════

class CoreQuantumReasoning:
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
        self.assinatura_historica = {}

    def load_universo_dados(self):
        if not self.conn:
            return pd.DataFrame()

        QUERIES = {
            "g": "SELECT * FROM Tb_GestorFin2",
            "cr": "SELECT * FROM [Contas Receber]",
            "cp": "SELECT * FROM [Contas Pagar]",
            "p": "SELECT * FROM tb_Proj",
            "tec": "SELECT * FROM tb_tec",
            "cli": "SELECT * FROM tb_cli",
            "tp": "SELECT * FROM tb_tipoproj",
            "neg": "SELECT * FROM tb_neg",
            "st": "SELECT * FROM tb_StatusProj",
        }

        dfs = {}
        all_loaded = True
        with st.spinner("Conectando e buscando dados mestre..."):
            for name, query in QUERIES.items():
                dfs[name] = run_query(query, self.conn)
                if dfs[name].empty and name == 'g':
                    all_loaded = False

        if not all_loaded or 'g' not in dfs or dfs['g'].empty:
            st.error("Tabela Fato (Tb_GestorFin2) está vazia.")
            return pd.DataFrame()

        try:
            df_fato = dfs['g']
            df_fato['ConsultGest'] = pd.to_numeric(df_fato['ConsultGest'], errors='coerce')
            df_fato['ProjGest'] = pd.to_numeric(df_fato['ProjGest'], errors='coerce')
            df_fato['Ano'] = pd.to_numeric(df_fato['Ano'].astype(str).str.strip(), errors='coerce')
            df_fato['Mes'] = pd.to_numeric(df_fato['Mes'].astype(str).str.strip(), errors='coerce')
            df_fato = df_fato.dropna(subset=['Ano', 'Mes', 'ConsultGest', 'ProjGest'])
            df_fato['Ano'] = df_fato['Ano'].astype(int)
            df_fato['Mes'] = df_fato['Mes'].astype(int)

            # Preparação do Fluxo de Caixa
            df_cr = dfs['cr'].copy()
            df_cr['DtRec'] = pd.to_datetime(df_cr['DtRec'], errors='coerce')
            df_cr = df_cr.dropna(subset=['DtRec'])
            df_cr['Caixa_Ano'] = df_cr['DtRec'].dt.year
            df_cr['Caixa_Mes'] = df_cr['DtRec'].dt.month
            df_cr['Cliente'] = pd.to_numeric(df_cr['Cliente'], errors='coerce')
            df_cr['VlRec'] = pd.to_numeric(df_cr['VlRec'], errors='coerce').fillna(0)
            cr_agg = df_cr.groupby(['Caixa_Ano', 'Caixa_Mes', 'Cliente'])['VlRec'].sum().reset_index()

            df_cp = dfs['cp'].copy()
            df_cp['DtPagamento'] = pd.to_datetime(df_cp['DtPagamento'], errors='coerce')
            df_cp = df_cp.dropna(subset=['DtPagamento'])
            df_cp['Caixa_Ano'] = df_cp['DtPagamento'].dt.year
            df_cp['Caixa_Mes'] = df_cp['DtPagamento'].dt.month
            df_cp['Prestador'] = pd.to_numeric(df_cp['Prestador'], errors='coerce')
            df_cp['VlPago'] = pd.to_numeric(df_cp['VlPago'], errors='coerce').fillna(0)
            cp_agg = df_cp.groupby(['Caixa_Ano', 'Caixa_Mes', 'Prestador'])['VlPago'].sum().reset_index()

        except Exception as e:
            st.error(f"Erro na preparação dos dados: {e}")
            return pd.DataFrame()

        # Executar Joins
        with st.spinner("Entrelaçando dimensões..."):
            df = df_fato
            
            def safe_merge(df_left, df_right, **kwargs):
                if df_right.empty:
                    return df_left
                return pd.merge(df_left, df_right, **kwargs)

            df = safe_merge(df, dfs['tec'], left_on='ConsultGest', right_on='AutNumTec', how='left')
            df = safe_merge(df, dfs['p'], left_on='ProjGest', right_on='AutNumProj', how='left', suffixes=('', '_proj'))
            df = safe_merge(df, dfs['cli'], left_on='CodCliProj', right_on='AutNumCli', how='left')
            df = safe_merge(df, dfs['tp'], left_on='TipoProj', right_on='AutNumTipo', how='left')
            df = safe_merge(df, dfs['neg'], left_on='CodNegProj', right_on='AutNumNeg', how='left')
            df = safe_merge(df, dfs['st'], left_on='StatusProj', right_on='AutNumStatus', how='left')

        # Mapeamento e Métricas
        with st.spinner("Mapeando colunas e criando métricas..."):
            mapa_colunas = {
                'QtHrReal': 'Hrs_Real', 'QtHrOrc': 'Hrs_Prev', 'ReceitaReal': 'Receita',
                'CustoReal': 'Custo', 'PercMgReal': 'Margem_Fracao', 'VlHrOrc': 'VH_Venda',
                'VlHrCusto': 'VH_Custo', 'ReceitaOrc': 'Receita_Orc', 'CustoOrc': 'Custo_Orc',
                'VlTTFat': 'Vl_Faturado_Contrato', 'NomeTec': 'Consultor', 'DescCli': 'Cliente',
                'DescProj': 'Projeto', 'DescTipo': 'TipoProj',
            }

            cols_existentes = {k: v for k, v in mapa_colunas.items() if k in df.columns}
            df = df.rename(columns=cols_existentes)
            
            colunas_numericas_app = ['Hrs_Real', 'Hrs_Prev', 'Receita', 'Custo', 'Margem_Fracao',
                                   'VH_Venda', 'VH_Custo', 'Receita_Orc', 'Custo_Orc', 'Vl_Faturado_Contrato']
            
            for col in colunas_numericas_app:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                else:
                    df[col] = 0
            
            df['Margem'] = np.where(df['Receita'] > 0, (df['Receita'] - df['Custo']) / df['Receita'], 0)
            df['Lucro'] = df['Receita'] - df['Custo']
            df['Desvio_Hrs'] = df['Hrs_Real'] - df['Hrs_Prev']
            df['Eficiencia'] = np.where(df['Hrs_Prev'] > 0, (df['Hrs_Real'] / df['Hrs_Prev']), 1)
            df['ROI_Hora'] = np.where(df['Hrs_Real'] > 0, df['Lucro'] / df['Hrs_Real'], 0)
            df['Produtividade'] = np.where(df['Hrs_Real'] > 0, df['Receita'] / df['Hrs_Real'], 0)
            
            df['Data'] = pd.to_datetime(df['Ano'].astype(str) + '-' + df['Mes'].astype(str) + '-01', errors='coerce')
            df = df.dropna(subset=['Data'])

        # Entrelaçamento de Caixa
        with st.spinner("Entrelaçando dados de Fluxo de Caixa..."):
            df = pd.merge(df, cr_agg, 
                          left_on=['Ano', 'Mes', 'CodCliProj'], 
                          right_on=['Caixa_Ano', 'Caixa_Mes', 'Cliente'], 
                          how='left', suffixes=('', '_cr'))
            
            df = pd.merge(df, cp_agg, 
                          left_on=['Ano', 'Mes', 'ConsultGest'], 
                          right_on=['Caixa_Ano', 'Caixa_Mes', 'Prestador'], 
                          how='left', suffixes=('', '_cp'))

            df = df.rename(columns={'VlRec': 'Caixa_Recebido', 'VlPago': 'Caixa_Pago'})
            df['Caixa_Recebido'] = df['Caixa_Recebido'].fillna(0)
            df['Caixa_Pago'] = df['Caixa_Pago'].fillna(0)
            
            df['Lucro_Caixa'] = df['Caixa_Recebido'] - df['Caixa_Pago']
            df['Gap_Faturamento'] = df['Receita'] - df['Caixa_Recebido']
            df['Gap_Custo'] = df['Custo'] - df['Caixa_Pago']

        # Dimensões Quânticas - CORREÇÃO APLICADA AQUI
        with st.spinner("Criando dimensões quânticas..."):
            # CORREÇÃO: Resetar o índice para evitar problemas de alinhamento
            df = df.reset_index(drop=True)
            
            df['Sangria_Risco_Absoluto'] = np.where(
                df['Hrs_Real'] > df['Hrs_Prev'],
                (df['Hrs_Real'] - df['Hrs_Prev']) * df['VH_Custo'], 0
            )
            df['Ociosidade_Risco_Absoluto'] = np.where(
                df['Hrs_Real'] < df['Hrs_Prev'],
                (df['Hrs_Prev'] - df['Hrs_Real']) * (df['VH_Venda'] - df['VH_Custo']), 0
            )

            # CORREÇÃO: Usar np.select em vez de loc para evitar problemas de índice
            conditions = [
                (df['Hrs_Real'] > df['Hrs_Prev']) & (df['TipoProj'] == 'PROJETO FECHADO'),
                (df['Hrs_Real'] > df['Hrs_Prev']) & (df['TipoProj'] == 'FATURADO POR HRS REALIZADAS'),
                (df['Hrs_Real'] < df['Hrs_Prev']) & (df['Hrs_Prev'] > 0)
            ]
            choices = [
                'SANGRIA',
                'OVERRUN_FATURAVEL',
                'OCIOSIDADE'
            ]
            df['Status_Horas'] = np.select(conditions, choices, default='OK')

            df['Score_Performance'] = (
                (df['Margem'] * 0.4) +
                (np.clip(df['Eficiencia'], 0, 2) / 2 * 0.3) +
                (np.clip(df['ROI_Hora'] / 100, 0, 1) * 0.3)
            ) * 100

            df['Status_Performance'] = pd.cut(df['Score_Performance'],
                                 bins=[-np.inf, 40, 70, np.inf],
                                 labels=['CRÍTICO', 'ATENÇÃO', 'EXCELENTE'],
                                 right=False)

            colunas_string_app = ['Consultor', 'Cliente', 'Projeto', 'TipoProj']
            for col_str in colunas_string_app:
                if col_str not in df.columns:
                    df[col_str] = 'N/A'
                else:
                    df[col_str] = df[col_str].astype(str).fillna('N/A')
            
            # Remover duplicatas finais
            df = df.drop_duplicates(subset=['Mes', 'Ano', 'ConsultGest', 'ProjGest', 'IdGest2'])

        st.success("Universo de Dados Carregado e Sincronizado.")
        return df

    def aplicar_colapso_quantico(self, filtros):
        if self.dados_universo.empty:
            st.warning("Não há dados carregados para aplicar filtros.")
            self.estado_quantum = pd.DataFrame()
            return self.estado_quantum

        df = self.dados_universo.copy()

        try:
            if filtros.get('consultores') and 'TODOS' not in filtros['consultores']:
                df = df[df['Consultor'].isin(filtros['consultores'])]
            if filtros.get('clientes') and 'TODOS' not in filtros['clientes']:
                df = df[df['Cliente'].isin(filtros['clientes'])]
            if filtros.get('projetos') and 'TODOS' not in filtros['projetos']:
                df = df[df['Projeto'].isin(filtros['projetos'])]
            if filtros.get('tipos') and 'TODOS' not in filtros['tipos']:
                df = df[df['TipoProj'].isin(filtros['tipos'])]

            if filtros.get('mes') and filtros.get('ano'):
                try:
                    mes_sel = int(filtros['mes'])
                    ano_sel = int(filtros['ano'])
                    df = df[(df['Mes'] == mes_sel) & (df['Ano'] == ano_sel)]
                    
                    if not df.empty:
                        self.atualizar_assinatura_historica(ano_sel, mes_sel)
                    
                except (ValueError, TypeError) as e:
                    st.error(f"Erro ao converter filtros de data: {e}")

            self.estado_quantum = df
            return df
            
        except Exception as e:
            st.error(f"Erro ao aplicar filtros: {e}")
            self.estado_quantum = pd.DataFrame()
            return self.estado_quantum

    def atualizar_assinatura_historica(self, ano_sel, mes_sel):
        try:
            if not isinstance(ano_sel, (int, float)) or not isinstance(mes_sel, (int, float)):
                self.assinatura_historica = {}
                return

            data_filtro = pd.to_datetime(f'{int(ano_sel)}-{int(mes_sel)}-01', errors='coerce')
            if pd.isna(data_filtro):
                self.assinatura_historica = {}
                return

            df_hist = self.dados_universo[self.dados_universo['Data'] < data_filtro]

            if df_hist.empty:
                self.assinatura_historica = {}
                return

            hist_contabil = df_hist.groupby(['Ano', 'Mes']).agg(
                Receita=('Receita', 'sum'),
                Custo=('Custo', 'sum'),
                Hrs_Real=('Hrs_Real', 'sum'),
                Hrs_Prev=('Hrs_Prev', 'sum')
            ).reset_index()
            
            hist_caixa_rec = df_hist.drop_duplicates(subset=['Ano', 'Mes', 'CodCliProj', 'Caixa_Recebido']).groupby(['Ano', 'Mes'])['Caixa_Recebido'].sum()
            hist_caixa_pag = df_hist.drop_duplicates(subset=['Ano', 'Mes', 'ConsultGest', 'Caixa_Pago']).groupby(['Ano', 'Mes'])['Caixa_Pago'].sum()

            hist_contabil = hist_contabil.set_index(['Ano', 'Mes'])
            hist_contabil['Caixa_Recebido'] = hist_caixa_rec
            hist_contabil['Caixa_Pago'] = hist_caixa_pag
            hist_contabil = hist_contabil.reset_index().fillna(0)
            
            hist_contabil['Lucro'] = hist_contabil['Receita'] - hist_contabil['Custo']
            hist_contabil['Margem'] = np.where(hist_contabil['Receita'] > 0, hist_contabil['Lucro'] / hist_contabil['Receita'], 0)
            hist_contabil['Lucro_Caixa'] = hist_contabil['Caixa_Recebido'] - hist_contabil['Caixa_Pago']
            hist_contabil['ROI_Hora'] = np.where(hist_contabil['Hrs_Real'] > 0, hist_contabil['Lucro'] / hist_contabil['Hrs_Real'], 0)
            hist_contabil['Eficiencia'] = np.where(hist_contabil['Hrs_Prev'] > 0, hist_contabil['Hrs_Real'] / hist_contabil['Hrs_Prev'], 1)

            self.assinatura_historica = {
                'receita_avg': hist_contabil['Receita'].mean(),
                'lucro_avg': hist_contabil['Lucro'].mean(),
                'margem_avg': hist_contabil['Margem'].mean(),
                'lucro_caixa_avg': hist_contabil['Lucro_Caixa'].mean(),
                'roi_hora_avg': hist_contabil['ROI_Hora'].mean(),
                'eficiencia_avg': hist_contabil['Eficiencia'].mean(),
                'count_months': len(hist_contabil)
            }
            
        except Exception as e:
            st.error(f"Erro ao atualizar assinatura histórica: {e}")
            self.assinatura_historica = {}

    def detectar_entrelacements(self):
        df = self.estado_quantum
        self.padroes_ocultos = {}

        if df.empty or len(df) < 2:
            return {}

        entrelacements = {}

        try:
            if 'Eficiencia' in df.columns and 'Margem' in df.columns:
                corr = df[['Eficiencia', 'Margem']].corr().iloc[0, 1]
                if pd.notna(corr) and abs(corr) > 0.5:
                    entrelacements['eficiencia_margem'] = {
                        'forca': corr,
                        'descricao': f"Correlação {'positiva' if corr > 0 else 'negativa'} de {corr:.2f} entre Eficiência e Margem."
                    }

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
            
            if 'TipoProj' in df.columns and 'Margem' in df.columns:
                perf_tipo = df.groupby('TipoProj')['Margem'].mean()
                perf_tipo = perf_tipo[perf_tipo.index != 'N/A'].dropna()
                if len(perf_tipo) > 1:
                    melhor_tipo = perf_tipo.idxmax()
                    pior_tipo = perf_tipo.idxmin()
                    if (perf_tipo[melhor_tipo] - perf_tipo[pior_tipo]) > 0.15:
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
            
        try:
            receita_valida = metricas['receita'] > 0
            lucro_valido = abs(metricas['lucro']) > 0.01
            custo_valido = metricas['custo'] > 0
        except (KeyError, TypeError):
            receita_valida = lucro_valido = custo_valido = False

        if receita_valida:
            gap_lucro = metricas['lucro'] - metricas['lucro_caixa']
            gap_relativo = abs(gap_lucro) / metricas['receita'] if metricas['receita'] > 0 else 0
            
            if gap_relativo > 0.7:
                prescricoes.append({
                    'tipo': 'ALERTA', 'prioridade': 'CRÍTICA',
                    'titulo': '🚨 ALERTA DE INTEGRIDADE: Descolamento Crítico de Caixa',
                    'sintese': f"Lucro Contábil de R$ {metricas['lucro']:,.0f} vs. Lucro de Caixa de R$ {metricas['lucro_caixa']:,.0f}.",
                    'analise': f"O sistema detectou um 'descolamento' (gap) de R$ {gap_lucro:,.0f} entre a visão contábil e a visão de caixa.",
                    'prescricao': """1. VALIDAR URGENTEMENTE o processo de lançamento de caixa.""",
                    'impacto_estimado': 'PERDA TOTAL da visão de Caixa.',
                    'confianca': 100
                })

        try:
            if 'Status_Horas' in df.columns:
                sangria_total = df[df['Status_Horas'] == 'SANGRIA']['Sangria_Risco_Absoluto'].sum()
                ociosidade_total = df[df['Status_Horas'] == 'OCIOSIDADE']['Ociosidade_Risco_Absoluto'].sum()
                
                if custo_valido and sangria_total > (metricas['custo'] * 0.1):
                    prescricoes.append({
                        'tipo': 'ALERTA', 'prioridade': 'CRÍTICA',
                        'titulo': '🩸 SANGRIA DETECTADA em Projetos Fechados',
                        'sintese': f"R$ {sangria_total:,.0f} de custo adicional em projetos de escopo fechado.",
                        'analise': f"Detectamos {len(df[df['Status_Horas'] == 'SANGRIA'])} projetos fechados que consumiram mais horas que o orçado.",
                        'prescricao': """1. AUDITAR IMEDIATAMENTE os projetos listados na "Análise Profunda > Sangria".""",
                        'impacto_estimado': f'Recuperação de R$ {sangria_total:,.0f} em margem futura.',
                        'confianca': 95
                    })

                if lucro_valido and ociosidade_total > (metricas['lucro'] * 0.15):
                    prescricoes.append({
                        'tipo': 'OPORTUNIDADE', 'prioridade': 'ALTA',
                        'titulo': '🎯 Oportunidade Oculta (Capacidade Ociosa)',
                        'sintese': f"R$ {ociosidade_total:,.0f} de lucro potencial perdido.",
                        'analise': f"Identificamos {len(df[df['Status_Horas'] == 'OCIOSIDADE'])} projetos que consumiram menos horas que o previsto.",
                        'prescricao': """1. Verificar se o faturamento desses projetos foi completo.""",
                        'impacto_estimado': f'R$ {ociosidade_total:,.0f} de receita/lucro adicional.',
                        'confianca': 88
                    })
                    
        except KeyError as e:
            st.warning(f"Coluna não encontrada durante análise de sangria: {e}")

        if (hist and isinstance(hist, dict) and 
            'count_months' in hist and 
            hist['count_months'] > 2 and
            'margem_avg' in hist):
            
            try:
                margem_atual = metricas['margem']
                margem_hist = hist['margem_avg']
                
                if (isinstance(margem_hist, (int, float)) and 
                    isinstance(margem_atual, (int, float)) and
                    abs(margem_hist) > 0.001):
                    
                    delta_margem = (margem_atual - margem_hist) / abs(margem_hist)
                    
                    if delta_margem < -0.15:
                        prescricoes.append({
                            'tipo': 'ALERTA', 'prioridade': 'ALTA',
                            'titulo': '📉 Anomalia de Rentabilidade Detectada',
                            'sintese': f"Margem de {margem_atual*100:.1f}% neste período, {abs(delta_margem*100):.0f}% abaixo da média histórica.",
                            'analise': f"A assinatura histórica mostra uma margem média de {margem_hist*100:.1f}%.",
                            'prescricao': """1. Analisar os piores projetos na Tab 1.""",
                            'impacto_estimado': f'Recuperação para a média de {margem_hist*100:.1f}% de margem.',
                            'confianca': 92
                        })
                        
            except (TypeError, ZeroDivisionError) as e:
                st.warning(f"Erro na análise comparativa de margens: {e}")

        if hasattr(self, 'padroes_ocultos') and self.padroes_ocultos:
            if 'otimizacao_mix' in self.padroes_ocultos:
                info = self.padroes_ocultos['otimizacao_mix']
                prescricoes.append({
                    'tipo': 'EFICIENCIA', 'prioridade': 'ALTA',
                    'titulo': '💎 Otimização Estratégica do Mix de Serviços',
                    'sintese': f"'{info['melhor']}' está gerando {info['gap']*100:.1f} pp a mais de margem que '{info['pior']}'.",
                    'analise': f"Análise de entrelaçamento mostra assimetria clara no mix de serviços.",
                    'prescricao': f"""1. Focar esforços comerciais em projetos tipo "{info["melhor"]}".""",
                    'impacto_estimado': 'Aumento de 5-10% na margem consolidada.',
                    'confianca': 90
                })

        if not prescricoes:
            prescricoes.append({
                'tipo': 'SUCESSO', 'prioridade': 'BAIXA',
                'titulo': '✅ Operação em Equilíbrio Quântico',
                'sintese': 'Nenhuma anomalia crítica detectada no período.',
                'analise': 'Os indicadores do período estão dentro dos parâmetros esperados.',
                'prescricao': """1. Manter a estratégia atual.""",
                'impacto_estimado': 'Manutenção da performance e crescimento sustentável.',
                'confianca': 95
            })

        self.prescricoes_ativas = prescricoes
        return prescricoes

    def calcular_metricas_consolidadas(self):
        df = self.estado_quantum

        if df.empty:
            return {
                'receita': 0, 'custo': 0, 'lucro': 0, 'margem': 0,
                'hrs_real': 0, 'hrs_prev': 0, 'eficiencia': 0,
                'roi_hora': 0, 'consultores': 0, 'clientes': 0,
                'projetos': 0, 'score': 0,
                'caixa_recebido': 0, 'caixa_pago': 0, 'lucro_caixa': 0,
                'gap_faturamento': 0, 'gap_custo': 0
            }

        try:
            receita_total = df['Receita'].sum()
            custo_total = df['Custo'].sum()
            lucro_total = df['Lucro'].sum()
            
            df_rec_unicos = df.drop_duplicates(subset=['Ano', 'Mes', 'CodCliProj', 'Caixa_Recebido'])
            caixa_recebido_total = df_rec_unicos['Caixa_Recebido'].sum()

            df_pag_unicos = df.drop_duplicates(subset=['Ano', 'Mes', 'ConsultGest', 'Caixa_Pago'])
            caixa_pago_total = df_pag_unicos['Caixa_Pago'].sum()

            return {
                'receita': receita_total,
                'custo': custo_total,
                'lucro': lucro_total,
                'margem': (lucro_total / receita_total) if receita_total > 0 else 0,
                'hrs_real': df['Hrs_Real'].sum(),
                'hrs_prev': df['Hrs_Prev'].sum(),
                'eficiencia': df['Eficiencia'].mean() if not df.empty else 0,
                'roi_hora': df['ROI_Hora'].mean() if not df.empty else 0,
                'consultores': df['Consultor'].nunique(),
                'clientes': df['Cliente'].nunique(),
                'projetos': df['Projeto'].nunique(),
                'score': df['Score_Performance'].mean() if not df.empty else 0,
                'caixa_recebido': caixa_recebido_total,
                'caixa_pago': caixa_pago_total,
                'lucro_caixa': caixa_recebido_total - caixa_pago_total,
                'gap_faturamento': receita_total - caixa_recebido_total,
                'gap_custo': custo_total - caixa_pago_total
            }
        except Exception as e:
            st.error(f"Erro ao calcular métricas consolidadas: {e}")
            return {
                'receita': 0, 'custo': 0, 'lucro': 0, 'margem': 0,
                'hrs_real': 0, 'hrs_prev': 0, 'eficiencia': 0,
                'roi_hora': 0, 'consultores': 0, 'clientes': 0,
                'projetos': 0, 'score': 0,
                'caixa_recebido': 0, 'caixa_pago': 0, 'lucro_caixa': 0,
                'gap_faturamento': 0, 'gap_custo': 0
        }
# ═══════════════════════════════════════════════════════════════════════════════
# MOTOR DE PERGUNTAS SOCRÁTICAS (O CONSELHEIRO DIGITAL)
# ═══════════════════════════════════════════════════════════════════════════════

class SocraticQuestioningEngine:
    def __init__(self, crq_engine):
        self.crq = crq_engine
        self.perguntas_geradas = []

    def gerar_perguntas_estrategicas(self):
        df = self.crq.estado_quantum
        metricas = self.crq.calcular_metricas_consolidadas()
        hist = self.crq.assinatura_historica
        padroes = self.crq.padroes_ocultos

        if df.empty:
            return [{
                'categoria': 'INICIAL',
                'pergunta': 'Selecione um período e filtros para que eu possa analisar a realidade dos seus dados e iniciar nossa conversa estratégica.',
                'contexto': 'Aguardando colapso quântico...',
                'profundidade': 'BÁSICA',
                'icone': '🤔'
            }]

        perguntas = []

        # 1. PERGUNTA CRÍTICA: O GAP DE CAIXA
        gap_lucro = metricas['lucro'] - metricas['lucro_caixa']
        if abs(gap_lucro) > (metricas['receita'] * 0.5) and metricas['receita'] > 0:
            perguntas.append({
                'categoria': 'RISCO CRÍTICO',
                'pergunta': f"Notei um 'descolamento' de R$ {gap_lucro:,.0f} entre seu Lucro Contábil (R$ {metricas['lucro']:,.0f}) e seu Lucro de Caixa (R$ {metricas['lucro_caixa']:,.0f}). "
                           f"Sua operação está gerando faturamento, mas o caixa não está acompanhando. Sabemos se isso é inadimplência, um descasamento de prazo extremo, ou uma falha na forma como os dados de recebimento estão sendo ligados?",
                'contexto': f"Gap Contábil vs. Caixa: R$ {gap_lucro:,.0f}",
                'profundidade': 'CRÍTICA',
                'icone': '🚨',
            })

        # 2. PERGUNTA SOBRE RENTABILIDADE (vs. HISTÓRICO)
        if hist and 'margem_avg' in hist and hist['margem_avg'] != 0:
            margem_atual = metricas['margem']
            margem_hist = hist['margem_avg']
            if margem_atual < (margem_hist * 0.9):
                perguntas.append({
                    'categoria': 'RENTABILIDADE',
                    'pergunta': f"Sua margem neste período foi de {margem_atual*100:.1f}%, o que está significativamente abaixo da sua 'assinatura' histórica de {margem_hist*100:.1f}%. "
                               f"O que mudou? Nossos custos aumentaram, nossos preços caíram, ou estamos focando em um mix de projetos menos lucrativo?",
                    'contexto': f"Margem Atual: {margem_atual*100:.1f}% vs. Média Histórica: {margem_hist*100:.1f}%",
                    'profundidade': 'ESTRATÉGICA',
                    'icone': '📉',
                })

        # 3. PERGUNTA SOBRE OTIMIZAÇÃO DE MIX
        if 'otimizacao_mix' in padroes:
            info = padroes['otimizacao_mix']
            perguntas.append({
                'categoria': 'ESTRATÉGIA',
                'pergunta': f"Observei que projetos '{info['melhor']}' são {info['gap']*100:.0f} pontos de margem mais lucrativos que '{info['pior']}'. "
                           f"Isso é intencional, talvez para ganhar mercado com '{info['pior']}'? Ou estamos deixando de focar nossos esforços comerciais no que realmente gera valor?",
                'contexto': f"Oportunidade de Mix: {info['melhor']} vs. {info['pior']}",
                'profundidade': 'ESTRATÉGICA',
                'icone': '💎',
            })

        # 4. PERGUNTA SOBRE EFICIÊNCIA (SANGRIA)
        if 'Status_Horas' in df.columns:
            sangria_df = df[df['Status_Horas'] == 'SANGRIA']
            if not sangria_df.empty:
                sangria_total = sangria_df['Sangria_Risco_Absoluto'].sum()
                pior_projeto = sangria_df.loc[sangria_df['Sangria_Risco_Absoluto'].idxmax()]
                perguntas.append({
                    'categoria': 'OPERACIONAL',
                    'pergunta': f"Detectei uma 'sangria' de R$ {sangria_total:,.0f} em projetos fechados que estouraram o orçamento de horas, sendo o projeto '{pior_projeto['Projeto']}' o mais crítico. "
                               f"Em sua opinião, a causa raiz disso é um escopo mal definido na venda, sub-estimativa de esforço, ou problemas na execução?",
                    'contexto': f"{len(sangria_df)} projetos com sangria. Pior caso: '{pior_projeto['Projeto']}'",
                    'profundidade': 'CRÍTICA',
                    'icone': '🩸',
                })

        # 5. PERGUNTA SOBRE TALENTO (DISPARIDADE)
        if 'disparidade_consultores' in padroes:
            info = padroes['disparidade_consultores']
            perguntas.append({
                'categoria': 'TALENTO',
                'pergunta': f"Notei uma alta variação de performance, onde '{info['top']}' gera um ROI/Hora muito superior a '{info['bottom']}'. "
                           f"Quais são as práticas de '{info['top']}' que podemos transformar em um processo replicável para elevar o nível de toda a equipe?",
                'contexto': f"Assimetria de Performance: {info['top']} vs. {info['bottom']}",
                'profundidade': 'ESTRATÉGICA',
                'icone': '🏆',
            })

        # 6. PERGUNTA SOBRE CONCENTRAÇÃO DE RECEITA (RISCO)
        if metricas['clientes'] > 1 and metricas['receita'] > 0:
            receita_cliente = df.groupby('Cliente')['Receita'].sum()
            top_cliente_receita = receita_cliente.max()
            top_cliente_nome = receita_cliente.idxmax()
            concentracao = top_cliente_receita / metricas['receita']
            if concentracao > 0.4:
                perguntas.append({
                    'categoria': 'RISCO',
                    'pergunta': f"O cliente '{top_cliente_nome}' representou {concentracao*100:.0f}% de todo o faturamento deste período. "
                               f"Embora seja um ótimo cliente, qual é o nosso plano de contingência para proteger o negócio se, por qualquer motivo, essa receita diminuir subitamente?",
                    'contexto': f"Concentração de Receita: {concentracao*100:.0f}% em '{top_cliente_nome}'",
                    'profundidade': 'CRÍTICA',
                    'icone': '⚠️',
                })

        # 7. PERGUNTA SOBRE OCIOSIDADE
        if 'Status_Horas' in df.columns:
            ociosidade_df = df[df['Status_Horas'] == 'OCIOSIDADE']
            if not ociosidade_df.empty:
                lucro_perdido = ociosidade_df['Ociosidade_Risco_Absoluto'].sum()
                if lucro_perdido > (metricas['lucro'] * 0.1) and metricas['lucro'] > 0:
                    perguntas.append({
                        'categoria': 'OPORTUNIDADE',
                        'pergunta': f"Identifiquei um lucro potencial perdido de R$ {lucro_perdido:,.0f} devido a horas orçadas mas não realizadas. "
                                   f"Isso representa uma eficiência real que podemos vender mais, ou é capacidade ociosa que precisa ser realocada urgentemente?",
                        'contexto': f"R$ {lucro_perdido:,.0f} em Ociosidade (Lucro Perdido)",
                        'profundidade': 'ESTRATÉGICA',
                        'icone': '💡',
                    })
        
        self.perguntas_geradas = perguntas
        return perguntas

# ═══════════════════════════════════════════════════════════════════════════════
# INICIALIZAÇÃO DOS MOTORES (CRQ e Socrático)
# ═══════════════════════════════════════════════════════════════════════════════

if 'crq' not in st.session_state:
    st.session_state.crq = CoreQuantumReasoning()

if 'socratic_engine' not in st.session_state:
    if st.session_state.crq and not st.session_state.crq.dados_universo.empty:
        st.session_state.socratic_engine = SocraticQuestioningEngine(st.session_state.crq)
    else:
         st.session_state.socratic_engine = None

crq = st.session_state.crq
socratic = st.session_state.socratic_engine
# ═══════════════════════════════════════════════════════════════════════════════
# HEADER PREMIUM DO SISTEMA
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="header-premium">
    <div class="logo-maestro">⚡ MAESTRO FAROL</div>
    <div class="subtitle-maestro">AUTONOMOUS INSIGHT SYSTEM</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR INTELIGENTE COM FILTROS AVANÇADOS
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🎛️ Painel de Controle CRQ")

    if crq.dados_universo.empty:
        st.error("Carregamento inicial de dados falhou. Verifique a conexão e logs.")
        st.stop()

    st.markdown("### 🔍 Filtros Dimensionais")

    try:
        consultores_opts = ['TODOS'] + sorted(crq.dados_universo['Consultor'].unique().tolist())
        clientes_opts = ['TODOS'] + sorted(crq.dados_universo['Cliente'].unique().tolist())
        projetos_opts = ['TODOS'] + sorted(crq.dados_universo['Projeto'].unique().tolist())
        tipos_opts = ['TODOS'] + sorted(crq.dados_universo['TipoProj'].unique().tolist())
        
        meses_opts = sorted(crq.dados_universo['Mes'].astype(int).unique().tolist())
        anos_opts = sorted(crq.dados_universo['Ano'].astype(int).unique().tolist())
        
        mes_default_idx = len(meses_opts) - 1 if meses_opts else 0
        ano_default_idx = len(anos_opts) - 1 if anos_opts else 0
        
    except Exception as e:
        st.error(f"Erro ao preparar opções de filtro: {e}")
        consultores_opts, clientes_opts, projetos_opts, tipos_opts, meses_opts, anos_opts = [['TODOS']]*6
        mes_default_idx, ano_default_idx = 0, 0

    col_m, col_a = st.columns(2)
    with col_m:
        mes_sel = st.selectbox("Mês", meses_opts, index=mes_default_idx, key="mes")
    with col_a:
        ano_sel = st.selectbox("Ano", anos_opts, index=ano_default_idx, key="ano")

    cons_sel = st.multiselect("👥 Consultores", consultores_opts, default=["TODOS"])
    cli_sel = st.multiselect("🏢 Clientes", clientes_opts, default=["TODOS"])
    proj_sel = st.multiselect("📁 Projetos", projetos_opts, default=["TODOS"])
    tipo_sel = st.multiselect("🎯 Tipo de Serviço", tipos_opts, default=["TODOS"])

    st.markdown("---")
    st.markdown("### 🧠 Configurações do Sistema")

    ia_ativa = st.toggle("Ressonância Prescritiva", value=True)

    st.markdown("---")

    # Aplicar filtros
    filtros = {
        'consultores': cons_sel,
        'clientes': cli_sel,
        'projetos': proj_sel,
        'tipos': tipo_sel,
        'mes': mes_sel,
        'ano': ano_sel
    }
    
    # Colapso Quântico
    df_filtrado = crq.aplicar_colapso_quantico(filtros)

    # Análises Pós-Colapso
    crq.detectar_entrelacements()
    prescricoes = crq.gerar_prescricoes_quantum() if ia_ativa else []
    metricas = crq.calcular_metricas_consolidadas()

    # Stats rápidas
    st.markdown("### 📊 Status Quantum")
    st.metric("Registros Ativos", len(df_filtrado))
    st.metric("Score Médio", f"{metricas['score']:.1f}")
    st.metric("Padrões Ocultos", len(crq.padroes_ocultos))

    if st.button("🔄 Reprocessar Dados", use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        if 'crq' in st.session_state:
            del st.session_state['crq']
        if 'socratic_engine' in st.session_state:
            del st.session_state['socratic_engine']
        st.rerun()
    # ═══════════════════════════════════════════════════════════════════════════════
# INTERFACE PRINCIPAL - TABS
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎯 Visão Executiva",
    "💰 Fechamento",
    "💵 Fluxo de Caixa",
    "🔬 Análise Profunda",
    "🧠 Ressonância Prescritiva",
    "🤔 Consultor Socrático"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: VISÃO EXECUTIVA (GRÁFICOS PREMIUM)
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown(f"## 📈 Dashboard Executivo (Visão Contábil) - {mes_sel}/{ano_sel}")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("💰 Receita Faturada", f"R$ {metricas['receita']:,.0f}")
    with col2:
        st.metric("📊 Lucro Contábil", f"R$ {metricas['lucro']:,.0f}")
    with col3:
        margem_display = metricas['margem'] * 100
        st.metric("📈 Margem Média", f"{margem_display:.1f}%",
            delta_color="normal" if margem_display > 40 else "inverse")
    with col4:
        st.metric("⏱️ Horas Realizadas", f"{metricas['hrs_real']:.0f}h",
            delta=f"{metricas['hrs_real']-metricas['hrs_prev']:.0f}h vs Previsto",
            delta_color="inverse" if metricas['hrs_real'] > metricas['hrs_prev'] else "normal")
    with col5:
        st.metric("💎 ROI por Hora", f"R$ {metricas['roi_hora']:.2f}")

    st.markdown("---")

    col_viz1, col_viz2 = st.columns(2)

    with col_viz1:
        st.markdown(f"### 🎯 Performance por Projeto (Top 15)")
        if not df_filtrado.empty:
            try:
                perf_proj = df_filtrado.groupby('Projeto').agg(
                    Receita=('Receita', 'sum'),
                    Margem_Media=('Margem', 'mean'),
                    Horas_Trabalhadas=('Hrs_Real', 'sum'),
                    ROI_Hora=('ROI_Hora', 'mean'),
                ).nlargest(15, 'Receita').reset_index()
                perf_proj = perf_proj[perf_proj['Projeto'] != 'N/A']

                perf_proj['Margem_Media_Perc'] = perf_proj['Margem_Media'] * 100

                fig = px.scatter(
                    perf_proj,
                    x='Receita',
                    y='Margem_Media_Perc',
                    size='Horas_Trabalhadas',
                    color='ROI_Hora',
                    hover_name='Projeto',
                    color_continuous_scale='Viridis',
                    size_max=50,
                    hover_data={'Margem_Media_Perc': ':.1f%', 'Receita': ':,.0f', 'Horas_Trabalhadas': ':.0f'}
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'), xaxis_title="Receita (R$)",
                    yaxis_title="Margem Média (%)", height=450,
                    coloraxis_colorbar=dict(title="ROI/Hora")
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Erro ao gerar gráfico Performance por Projeto: {e}")
        else:
            st.info("📊 Sem dados disponíveis para este filtro")

    with col_viz2:
        st.markdown(f"### 💰 Receita & Rentabilidade por Cliente (Top 15)")
        if not df_filtrado.empty:
            try:
                rec_cliente = df_filtrado.groupby('Cliente').agg(
                    Receita_Total=('Receita', 'sum'),
                    Margem_Media=('Margem', 'mean')
                ).nlargest(15, 'Receita_Total').sort_values('Receita_Total')
                rec_cliente = rec_cliente[rec_cliente.index != 'N/A']
                rec_cliente['Margem_Media_Perc'] = rec_cliente['Margem_Media'] * 100

                fig = px.bar(
                    rec_cliente,
                    x='Receita_Total',
                    y=rec_cliente.index,
                    orientation='h',
                    color='Margem_Media_Perc',
                    color_continuous_scale='Blues',
                    text='Receita_Total',
                    hover_data={'Margem_Media_Perc': ':.1f%'}
                )
                fig.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'), xaxis_title="Receita (R$)",
                    yaxis_title="", height=450,
                    coloraxis_colorbar=dict(title="Margem Média %")
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Erro ao gerar gráfico Receita por Cliente: {e}")
        else:
            st.info("📊 Sem dados disponíveis para este filtro")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: FECHAMENTO (COM EXPORTAÇÃO EXCEL)
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown(f"## 💰 Painel de Fechamento - {mes_sel}/{ano_sel}")
    st.info("Esta visão compara o Contábil (Faturado/Custo) com o Caixa (Recebido/Pago).")

    apagar_df_export = pd.DataFrame()
    areceber_df_export = pd.DataFrame()

    col_pag, col_rec = st.columns(2)

    with col_pag:
        st.markdown("### 💸 A Pagar - Consultores")
        if not df_filtrado.empty:
            try:
                custo_contabil_agg = df_filtrado.groupby('Consultor').agg(
                    Horas_Trabalhadas=('Hrs_Real', 'sum'),
                    Total_Custo_Contabil=('Custo', 'sum')
                )
                custo_caixa_agg = df_filtrado.drop_duplicates(subset=['Consultor', 'Caixa_Pago']).groupby('Consultor')['Caixa_Pago'].sum().rename('Total_Pago')

                apagar = pd.concat([custo_contabil_agg, custo_caixa_agg], axis=1).fillna(0)
                apagar = apagar[apagar.index != 'N/A']
                apagar['Saldo_Pendente'] = apagar['Total_Custo_Contabil'] - apagar['Total_Pago']
                apagar = apagar.sort_values('Total_Custo_Contabil', ascending=False).reset_index()
                
                apagar_df_export = apagar[apagar['Total_Custo_Contabil'] > 0]
                st.dataframe(
                    apagar_df_export.style.format({
                        'Horas_Trabalhadas': '{:.0f}h',
                        'Total_Custo_Contabil': 'R$ {:,.2f}',
                        'Total_Pago': 'R$ {:,.2f}',
                        'Saldo_Pendente': 'R$ {:,.2f}'
                    }), use_container_width=True, height=400
                )
                
                st.metric("Total Custo Contábil", f"R$ {apagar['Total_Custo_Contabil'].sum():,.2f}")
                st.metric("Total Efetivamente Pago", f"R$ {apagar['Total_Pago'].sum():,.2f}",
                          delta=f"R$ {apagar['Saldo_Pendente'].sum():,.2f} Pendente",
                          delta_color="inverse" if apagar['Saldo_Pendente'].sum() > 0 else "off")
            except Exception as e:
                st.warning(f"Erro ao gerar tabela A Pagar: {e}")
        else:
            st.info("💸 Sem dados para fechamento A Pagar")

    with col_rec:
        st.markdown("### 💳 A Receber - Clientes")
        if not df_filtrado.empty:
            try:
                receita_contabil_agg = df_filtrado.groupby('Cliente').agg(
                    Horas_Faturadas=('Hrs_Real', 'sum'),
                    Total_Faturado=('Receita', 'sum')
                )
                receita_caixa_agg = df_filtrado.drop_duplicates(subset=['Cliente', 'Caixa_Recebido']).groupby('Cliente')['Caixa_Recebido'].sum().rename('Total_Recebido')
                
                areceber = pd.concat([receita_contabil_agg, receita_caixa_agg], axis=1).fillna(0)
                areceber = areceber[areceber.index != 'N/A']
                areceber['Saldo_Pendente'] = areceber['Total_Faturado'] - areceber['Total_Recebido']
                areceber = areceber.sort_values('Total_Faturado', ascending=False).reset_index()

                areceber_df_export = areceber[areceber['Total_Faturado'] > 0]
                st.dataframe(
                    areceber_df_export.style.format({
                        'Horas_Faturadas': '{:.0f}h',
                        'Total_Faturado': 'R$ {:,.2f}',
                        'Total_Recebido': 'R$ {:,.2f}',
                        'Saldo_Pendente': 'R$ {:,.2f}'
                    }), use_container_width=True, height=400
                )
                
                st.metric("Total Faturado (Contábil)", f"R$ {areceber['Total_Faturado'].sum():,.2f}")
                st.metric("Total Efetivamente Recebido", f"R$ {areceber['Total_Recebido'].sum():,.2f}",
                          delta=f"R$ {areceber['Saldo_Pendente'].sum():,.2f} Pendente",
                          delta_color="inverse" if areceber['Saldo_Pendente'].sum() > 0 else "off")
            except Exception as e:
                st.warning(f"Erro ao gerar tabela A Receber: {e}")
        else:
             st.info("💳 Sem dados para fechamento A Receber")
    
    st.markdown("---")
    
    try:
        excel_data = to_excel(areceber_df_export, apagar_df_export)
        st.download_button(
            label="📥 Exportar Fechamento para Excel",
            data=excel_data,
            file_name=f"Fechamento_Maestro_{mes_sel}_{ano_sel}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    except Exception as e:
        st.warning(f"Erro ao gerar arquivo Excel: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: FLUXO DE CAIXA
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown(f"## 💵 Fluxo de Caixa vs. Contábil - {mes_sel}/{ano_sel}")
    st.markdown("### Resumo de Caixa (Período Selecionado)")

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.markdown('<div class="metric-card-premium" style="border-left-color: #39FF14;"><h4 style="color: #39FF14;">VISÃO CAIXA</h4>', unsafe_allow_html=True)
        st.metric("💰 Total Recebido", f"R$ {metricas['caixa_recebido']:,.2f}")
        st.metric("💸 Total Pago", f"R$ {metricas['caixa_pago']:,.2f}")
        st.metric("📊 Resultado Caixa", f"R$ {metricas['lucro_caixa']:,.2f}",
                  delta_color="normal" if metricas['lucro_caixa'] > 0 else "inverse")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_c2:
        st.markdown('<div class="metric-card-premium" style="border-left-color: #00BFFF;"><h4 style="color: #00BFFF;">VISÃO CONTÁBIL</h4>', unsafe_allow_html=True)
        st.metric("💰 Faturamento Contábil", f"R$ {metricas['receita']:,.2f}")
        st.metric("💸 Custo Contábil", f"R$ {metricas['custo']:,.2f}")
        st.metric("📊 Lucro Contábil", f"R$ {metricas['lucro']:,.2f}",
                  delta_color="normal" if metricas['lucro'] > 0 else "inverse")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_c3:
        st.markdown('<div class="metric-card-premium" style="border-left-color: #FFD700;"><h4 style="color: #FFD700;">GAPS (Contábil - Caixa)</h4>', unsafe_allow_html=True)
        st.metric("Gap de Recebimento", f"R$ {metricas['gap_faturamento']:,.2f}",
                  help="Quanto foi faturado mas ainda não recebido")
        st.metric("Gap de Pagamento", f"R$ {metricas['gap_custo']:,.2f}",
                  help="Quanto foi provisionado de custo mas ainda não pago")
        st.metric("Gap de Lucro", f"R$ {metricas['lucro'] - metricas['lucro_caixa']:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

    try:
        ano_sel_int = int(ano_sel) if ano_sel else 0
        if (ano_sel_int >= 2025 and 
            metricas.get('caixa_recebido', 0) == 0 and 
            metricas.get('caixa_pago', 0) == 0 and 
            metricas.get('receita', 0) > 0):
            st.error("🚨 ATENÇÃO: Os dados de Caixa para este período estão zerados. A análise de Caixa e Gaps está comprometida. Veja a aba 'Ressonância Prescritiva'.")
    except (ValueError, TypeError) as e:
        st.warning(f"⚠️ Erro ao validar dados de caixa: {e}")

    st.markdown("---")
    st.markdown("### Evolução Temporal (Caixa vs. Contábil)")

    with st.spinner("Calculando evolução temporal..."):
        df_full = crq.dados_universo
        if not df_full.empty and 'Data' in df_full.columns and not df_full['Data'].isnull().all():
            try:
                df_full_temp = df_full.dropna(subset=['Data']).copy()
                
                contabil_hist = df_full_temp.groupby(pd.Grouper(key='Data', freq='MS')).agg(
                    Receita_Contabil=('Receita', 'sum'),
                    Custo_Contabil=('Custo', 'sum')
                )
                caixa_rec_hist = df_full_temp.drop_duplicates(subset=['Data', 'CodCliProj', 'Caixa_Recebido']) \
                                            .groupby(pd.Grouper(key='Data', freq='MS'))['Caixa_Recebido'].sum()
                caixa_pag_hist = df_full_temp.drop_duplicates(subset=['Data', 'ConsultGest', 'Caixa_Pago']) \
                                            .groupby(pd.Grouper(key='Data', freq='MS'))['Caixa_Pago'].sum()
                
                fluxo_temporal = contabil_hist
                fluxo_temporal['Receita_Caixa'] = caixa_rec_hist
                fluxo_temporal['Custo_Caixa'] = caixa_pag_hist
                fluxo_temporal = fluxo_temporal.fillna(0).reset_index()

                fluxo_temporal['Lucro_Caixa'] = fluxo_temporal['Receita_Caixa'] - fluxo_temporal['Custo_Caixa']
                fluxo_temporal['Lucro_Contabil'] = fluxo_temporal['Receita_Contabil'] - fluxo_temporal['Custo_Contabil']

                fig_evolucao = go.Figure()
                fig_evolucao.add_trace(go.Scatter(
                    x=fluxo_temporal['Data'], y=fluxo_temporal['Lucro_Contabil'],
                    name='Lucro Contábil', mode='lines+markers', line=dict(color='#00BFFF', width=4)
                ))
                fig_evolucao.add_trace(go.Scatter(
                    x=fluxo_temporal['Data'], y=fluxo_temporal['Lucro_Caixa'],
                    name='Lucro Caixa', mode='lines+markers', line=dict(color='#39FF14', width=2, dash='dot')
                ))
                fig_evolucao.add_trace(go.Bar(
                    x=fluxo_temporal['Data'], y=fluxo_temporal['Receita_Contabil'],
                    name='Faturamento Contábil', marker_color='rgba(0,191,255,0.3)',
                ))
                fig_evolucao.add_trace(go.Bar(
                    x=fluxo_temporal['Data'], y=fluxo_temporal['Receita_Caixa'],
                    name='Recebimento Caixa', marker_color='rgba(57,255,20,0.3)',
                ))
                fig_evolucao.update_layout(
                    title='Evolução Mensal: Lucro (Linhas) vs Receita (Barras)',
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'), hovermode='x unified',
                    legend=dict(orientation='h', y=1.1, yanchor='bottom'),
                    height=450, xaxis_title='Período', yaxis_title='Valor (R$)'
                )
                st.plotly_chart(fig_evolucao, use_container_width=True)
            except Exception as e:
                 st.warning(f"Erro ao gerar gráfico de evolução temporal: {e}")
        else:
            st.warning("Não foi possível gerar gráfico temporal. Verifique coluna 'Data' e se há dados carregados.")
        # ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: ANÁLISE PROFUNDA (SANGRIA E OCIOSIDADE)
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown(f"## 🔬 Análise Profunda - {mes_sel}/{ano_sel}")

    st.markdown("### 🩸 Detecção de Sangria (Projetos Fechados com Overrun)")
    if not df_filtrado.empty:
        try:
            if 'Status_Horas' in df_filtrado.columns:
                df_sangria = df_filtrado[df_filtrado['Status_Horas'] == 'SANGRIA']
                if not df_sangria.empty:
                    df_sangria_view = df_sangria[[
                        'Consultor', 'Cliente', 'Projeto', 'Hrs_Prev', 'Hrs_Real',
                        'Desvio_Hrs', 'Sangria_Risco_Absoluto', 'Receita', 'Custo', 'Lucro', 'Margem'
                    ]].sort_values('Sangria_Risco_Absoluto', ascending=False)

                    st.error(f"Identificados {len(df_sangria_view)} projetos fechados com estouro de horas (sangria). "
                             f"Custo total da sangria: R$ {df_sangria['Sangria_Risco_Absoluto'].sum():,.2f}")
                    st.dataframe(df_sangria_view.style.format({
                        'Hrs_Prev': '{:.0f}h', 'Hrs_Real': '{:.0f}h', 'Desvio_Hrs': '+{:.0f}h',
                        'Sangria_Risco_Absoluto': 'R$ {:,.2f}', 'Receita': 'R$ {:,.2f}',
                        'Custo': 'R$ {:,.2f}', 'Lucro': 'R$ {:,.2f}', 'Margem': '{:.1%}'
                    }).background_gradient(cmap='Reds', subset=['Desvio_Hrs', 'Sangria_Risco_Absoluto'])
                      .background_gradient(cmap='RdYlGn', subset=['Lucro', 'Margem']))
                else:
                    st.success("✅ Nenhum projeto fechado com estouro de horas detectado neste período.")
            else:
                st.info("ℹ️ Coluna 'Status_Horas' não encontrada nos dados")
        except Exception as e:
            st.warning(f"Erro ao analisar sangria: {e}")
    else:
        st.info("📊 Sem dados disponíveis para análise de sangria")

    st.markdown("### 💡 Detecção de Ociosidade (Horas Orçadas Não Utilizadas)")
    if not df_filtrado.empty:
        try:
            if 'Status_Horas' in df_filtrado.columns:
                df_ociosidade = df_filtrado[df_filtrado['Status_Horas'] == 'OCIOSIDADE']
                if not df_ociosidade.empty:
                    df_ociosidade_view = df_ociosidade[[
                        'Consultor', 'Cliente', 'Projeto', 'Hrs_Prev', 'Hrs_Real',
                        'Desvio_Hrs', 'Ociosidade_Risco_Absoluto', 'Receita', 'Custo', 'Lucro', 'Margem'
                    ]].sort_values('Ociosidade_Risco_Absoluto', ascending=False)
                    
                    st.warning(f"Identificados {len(df_ociosidade_view)} projetos com ociosidade. "
                             f"Lucro potencial perdido: R$ {df_ociosidade['Ociosidade_Risco_Absoluto'].sum():,.2f}")
                    st.dataframe(df_ociosidade_view.style.format({
                        'Hrs_Prev': '{:.0f}h', 'Hrs_Real': '{:.0f}h', 'Desvio_Hrs': '{:.0f}h',
                        'Ociosidade_Risco_Absoluto': 'R$ {:,.2f}', 'Receita': 'R$ {:,.2f}',
                        'Custo': 'R$ {:,.2f}', 'Lucro': 'R$ {:,.2f}', 'Margem': '{:.1%}'
                    }).background_gradient(cmap='Blues', subset=['Desvio_Hrs', 'Ociosidade_Risco_Absoluto']))
                else:
                    st.success("✅ Nenhum projeto com ociosidade significativa detectada.")
            else:
                st.info("ℹ️ Coluna 'Status_Horas' não encontrada nos dados")
        except Exception as e:
            st.warning(f"Erro ao analisar ociosidade: {e}")
    else:
        st.info("📊 Sem dados disponíveis para análise de ociosidade")

    st.markdown("---")
    st.markdown("### 🎯 Matriz de Correlação (Entrelaçamento Quântico)")
    if not df_filtrado.empty and len(df_filtrado) > 3:
        try:
            cols_analise = ['Hrs_Real', 'Hrs_Prev', 'Receita', 'Custo', 'Lucro', 'Margem', 'Eficiencia', 'ROI_Hora']
            cols_existentes = [col for col in cols_analise if col in df_filtrado.columns]
            
            if len(cols_existentes) > 1:
                df_corr = df_filtrado[cols_existentes].corr()

                fig_corr = px.imshow(
                    df_corr, text_auto='.2f', aspect='auto',
                    color_continuous_scale='RdBu_r', zmin=-1, zmax=1
                )
                fig_corr.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'), height=500
                )
                st.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.warning("📊 Colunas insuficientes para análise de correlação")
        except Exception as e:
            st.warning(f"Erro ao gerar matriz de correlação: {e}")
    else:
        st.warning("📊 Dados insuficientes para análise de correlação (mínimo 3 registros)")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5: RESSONÂNCIA PRESCRITIVA
# ═══════════════════════════════════════════════════════════════════════════════

with tab5:
    st.markdown("## 🧠 Ressonância Prescritiva Ativa")

    if ia_ativa and prescricoes:
        st.success(f"✅ **CRQ Online** - {len(prescricoes)} prescrições geradas para {mes_sel}/{ano_sel}")

        # Filtro de prioridades
        prioridades = ['TODAS'] + sorted(list(set([p['prioridade'] for p in prescricoes])))
        filtro_prior = st.selectbox("Filtrar por Prioridade", prioridades, key="filtro_prior")

        # Aplicar filtro
        if filtro_prior == 'TODAS':
            prescricoes_filtradas = prescricoes
        else:
            prescricoes_filtradas = [p for p in prescricoes if p['prioridade'] == filtro_prior]

        if not prescricoes_filtradas:
            st.info("Nenhuma prescrição encontrada para a prioridade selecionada.")
        else:
            for i, presc in enumerate(prescricoes_filtradas):
                # Definir estilo baseado na prioridade
                if presc['prioridade'] == 'CRÍTICA':
                    card_class = 'alert-premium'
                    icone = '🚨'
                elif presc['prioridade'] == 'ALTA':
                    card_class = 'insight-premium'
                    icone = '💡'
                else:
                    card_class = 'success-premium'
                    icone = '✅'
                
                cor_prior = {
                    'CRÍTICA': '#FF4500', 
                    'ALTA': '#FFD700', 
                    'MÉDIA': '#00BFFF', 
                    'BAIXA': '#39FF14'
                }

                st.markdown(f"""
                <div class="{card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3>{icone} {presc['titulo']}</h3>
                        <span style="background: {cor_prior.get(presc['prioridade'], '#8A8A8A')}20;
                              color: {cor_prior.get(presc['prioridade'], '#8A8A8A')}; 
                              border: 1px solid {cor_prior.get(presc['prioridade'], '#8A8A8A')};
                              padding: 4px 12px; border-radius: 12px; font-size: 0.85em; font-weight: 600;">
                            {presc['prioridade']}
                        </span>
                    </div>
                    <p style="font-size: 1.1em; font-weight: 600; margin: 10px 0;">
                        📊 <strong>Síntese:</strong> {presc['sintese']}
                    </p>
                    <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; margin: 15px 0;">
                        <p style="margin: 0;"><strong>🔍 Análise Profunda:</strong></p>
                        <p style="margin: 10px 0 0 0; white-space: pre-line;">{presc['analise']}</p>
                    </div>
                    <div style="background: rgba(0,191,255,0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">
                        <p style="margin: 0; color: #00BFFF;"><strong>💊 Prescrição:</strong></p>
                        <p style="margin: 10px 0 0 0; white-space: pre-line;">{presc['prescricao']}</p>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
                        <div><span style="color: #39FF14;">💰 Impacto:</span> <strong>{presc['impacto_estimado']}</strong></div>
                        <div><span style="color: #FFD700;">📈 Confiança:</span> <strong>{presc['confianca']}%</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Barra de progresso da confiança
                st.progress(presc['confianca'] / 100)
                st.markdown("<br>", unsafe_allow_html=True)

    elif not ia_ativa:
        st.info("🔧 Ressonância Prescritiva desativada. Ative na sidebar para análises avançadas.")
    else:
        st.warning("⚠️ Nenhuma prescrição gerada para os filtros atuais. Ajuste os filtros para análise.")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6: CONSULTOR SOCRÁTICO
# ═══════════════════════════════════════════════════════════════════════════════

with tab6:
    st.markdown("## 🤔 Consultor Socrático - As Perguntas Que Importam")
    st.markdown("""
    <div class="insight-premium">
        <h3 style="margin-top: 0;">💭 O Método Socrático Aplicado aos Negócios</h3>
        <p style="font-size: 1.05em; line-height: 1.6;">
            Este não é um sistema que apenas mostra números. É um <strong>parceiro de sabedoria</strong>
            que faz as perguntas certas para guiá-lo à descoberta de insights profundos sobre seu negócio,
            baseado na realidade do período selecionado.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not df_filtrado.empty and socratic:
        with st.spinner('🧠 Analisando profundamente seus dados e gerando perguntas estratégicas...'):
            try:
                perguntas = socratic.gerar_perguntas_estrategicas()
            except Exception as e:
                st.error(f"Erro ao gerar perguntas socráticas: {e}")
                perguntas = []

        if perguntas:
            # Filtro por categoria
            categorias = sorted(list(set([p['categoria'] for p in perguntas])))
            categoria_filtro = st.multiselect(
                "Filtrar por categoria:", 
                ['TODAS'] + categorias, 
                default=['TODAS'],
                key="filtro_categoria"
            )

            # Aplicar filtro
            if 'TODAS' in categoria_filtro or not categoria_filtro:
                perguntas_filtradas = perguntas
            else:
                perguntas_filtradas = [p for p in perguntas if p['categoria'] in categoria_filtro]

            # Estatísticas
            st.markdown("---")
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("📊 Total de Perguntas", len(perguntas_filtradas))
            with col_stat2:
                criticas = len([p for p in perguntas_filtradas if p['profundidade'] == 'CRÍTICA'])
                st.metric("🚨 Críticas", criticas)
            with col_stat3:
                estrategicas = len([p for p in perguntas_filtradas if p['profundidade'] == 'ESTRATÉGICA'])
                st.metric("🎯 Estratégicas", estrategicas)
            st.markdown("---")

            # Exibir perguntas
            if perguntas_filtradas:
                for i, pergunta in enumerate(perguntas_filtradas, 1):
                    # Definir cores baseadas na profundidade
                    if pergunta['profundidade'] == 'CRÍTICA':
                        card_class, cor_badge = 'alert-premium', '#FF4500'
                    elif pergunta['profundidade'] == 'ESTRATÉGICA':
                        card_class, cor_badge = 'insight-premium', '#FFD700'
                    else:
                        card_class, cor_badge = 'success-premium', '#00BFFF'

                    st.markdown(f"""
                    <div class="{card_class}">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                            <span style="font-size: 2em;">{pergunta.get('icone', '❓')}</span>
                            <span style="background: {cor_badge}30; color: {cor_badge}; padding: 4px 12px;
                                  border-radius: 12px; font-size: 0.85em; font-weight: 600; border: 1px solid {cor_badge};">
                                {pergunta.get('categoria', 'GERAL')}
                            </span>
                        </div>
                        <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 12px;
                                    border-left: 4px solid {cor_badge}; margin: 15px 0;">
                            <p style="font-size: 1.15em; line-height: 1.7; margin: 0; font-weight: 500;">
                                {pergunta.get('pergunta', 'Erro ao carregar pergunta.')}
                            </p>
                        </div>
                        <div style="background: rgba(0,191,255,0.05); padding: 15px; border-radius: 10px;
                                    margin-top: 15px; border-left: 3px solid #00BFFF;">
                            <p style="margin: 0; font-size: 0.95em; color: #8A8A8A;">
                                <strong style="color: #00BFFF;">📊 Contexto dos Dados:</strong><br>
                                {pergunta.get('contexto', 'N/A')}
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Área de reflexão
                    with st.expander(f"💭 Meu espaço de reflexão sobre a pergunta #{i}"):
                        st.text_area(
                            "Suas anotações:",
                            placeholder="Use este espaço para anotar insights, ações ou reflexões sobre esta pergunta...",
                            key=f"reflexao_{i}",
                            height=120
                        )
                    st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.info("🎯 Nenhuma pergunta gerada com os filtros aplicados. Ajuste os critérios.")
        else:
            st.info("🎯 Nenhuma pergunta socrática gerada para os dados atuais. Tente ajustar os filtros.")
    elif not socratic:
        st.warning("🔧 Motor Socrático não inicializado. Verifique o carregamento dos dados.")
    else:
        st.warning("📊 Aplique filtros na sidebar para gerar perguntas estratégicas baseadas nos seus dados.")

# ═══════════════════════════════════════════════════════════════════════════════
# RODAPÉ
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #8A8A8A; font-size: 0.9em;'>"
            f"MAESTRO FAROL - Autonomous Insight System © {datetime.now().year}"
            f"</div>", unsafe_allow_html=True)
