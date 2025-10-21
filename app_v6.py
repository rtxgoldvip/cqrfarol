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

# Import da conexão de banco de dados
import pyodbc

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA - DESIGN PREMIUM (COM NOVO TÍTULO)
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="MAESTRO FAROL - Autonomous Insight System", # <-- MUDANÇA DE BRANDING
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CSS PREMIUM (COPIADO DO SEU EXEMPLO)
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
# MOTOR DE CONEXÃO COM BANCO DE DADOS (Baseado no extrator_maestro.py)
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
        st.error("Verifique suas credenciais em st.secrets.toml")
        return None

# Função para executar queries
@st.cache_data(ttl=600)
def run_query(query, _conn):
    """Executa a query e retorna um DataFrame."""
    try:
        return pd.read_sql(query, _conn)
    except Exception as e:
        st.warning(f"⚠️ Falha ao executar query: {query}. Erro: {e}")
        return pd.DataFrame()

# ═══════════════════════════════════════════════════════════════════════════════
# MOTOR DE RACIOCÍNIO QUÂNTICO (CRQ) - NÚCLEO INTELIGENTE (CORRIGIDO)
# ═══════════════════════════════════════════════════════════════════════════════

class CoreQuantumReasoning:
    """
    Núcleo de Raciocínio Quântico
    Modificado para carregar dados do banco de dados ao vivo.
    """
    
    def __init__(self):
        self.conn = init_connection()
        if self.conn:
            with st.spinner('🌌 Carregando Universo de Dados do Banco...'):
                self.dados_universo = self.load_universo_dados()
        else:
            st.error("Falha na inicialização do CRQ: Conexão com banco de dados falhou.")
            self.dados_universo = pd.DataFrame() # Inicia vazio
            
        self.estado_quantum = self.dados_universo.copy()
        self.padroes_ocultos = {}
        self.prescricoes_ativas = []
        
    def load_universo_dados(self):
        """
        Carrega o universo completo de dados do SQL Server e aplica
        o "Master Query" da especificação técnica via Pandas.
        """
        if not self.conn:
            st.error("CRQ: Sem conexão com banco de dados para carregar dados.")
            return pd.DataFrame()

        # 1. Dicionário de Queries (baseado no extrator_maestro.py)
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
            "amarra": "SELECT * FROM tb_amarradisc",
            "niv": "SELECT * FROM tb_nivel",
            "disc": "SELECT * FROM tb_disciplina"
            # Adicionar outras tabelas DIM se necessário
        }
        
        # 2. Carregar todas as tabelas em um dicionário de DataFrames
        dfs = {}
        with st.spinner("Conectando e buscando dados mestre..."):
            for name, query in QUERIES.items():
                dfs[name] = run_query(query, self.conn)
                if dfs[name].empty:
                    st.warning(f"Tabela '{name}' está vazia ou falhou ao carregar.")
        
        # 3. Verificar se as tabelas FATO e DIM principais existem
        if 'g' not in dfs or dfs['g'].empty:
            st.error("Tabela Fato (Tb_GestorFin2) está vazia. Análise impossível.")
            return pd.DataFrame()
        
        # Garantir que as Dims não estejam vazias antes de tentar acessá-las
        dims_criticas = ['p', 'tec', 'cli', 'tp', 'neg', 'st', 'cr', 'cp']
        for dim in dims_criticas:
            if dim not in dfs:
                st.warning(f"Tabela de dimensão '{dim}' não foi carregada. Criando DataFrame vazio.")
                dfs[dim] = pd.DataFrame() # Cria um DF vazio para evitar erros no merge

        # 4. Limpeza de Chaves (crucial para merges)
        # Converte chaves para numérico, tratando erros.
        try:
            dfs['g']['IdGest2'] = pd.to_numeric(dfs['g']['IdGest2'], errors='coerce')
            dfs['g']['ConsultGest'] = pd.to_numeric(dfs['g']['ConsultGest'], errors='coerce')
            dfs['g']['ProjGest'] = pd.to_numeric(dfs['g']['ProjGest'], errors='coerce')
            
            if not dfs['tec'].empty:
                dfs['tec']['AutNumTec'] = pd.to_numeric(dfs['tec']['AutNumTec'], errors='coerce')
            
            if not dfs['p'].empty:
                dfs['p']['AutNumProj'] = pd.to_numeric(dfs['p']['AutNumProj'], errors='coerce')
                dfs['p']['CodCliProj'] = pd.to_numeric(dfs['p']['CodCliProj'], errors='coerce')
                dfs['p']['TipoProj'] = pd.to_numeric(dfs['p']['TipoProj'], errors='coerce')
                dfs['p']['CodNegProj'] = pd.to_numeric(dfs['p']['CodNegProj'], errors='coerce')
                dfs['p']['StatusProj'] = pd.to_numeric(dfs['p']['StatusProj'], errors='coerce')
            
            if not dfs['cli'].empty:
                dfs['cli']['AutNumCli'] = pd.to_numeric(dfs['cli']['AutNumCli'], errors='coerce')
            if not dfs['tp'].empty:
                dfs['tp']['AutNumTipo'] = pd.to_numeric(dfs['tp']['AutNumTipo'], errors='coerce')
            if not dfs['neg'].empty:
                dfs['neg']['AutNumNeg'] = pd.to_numeric(dfs['neg']['AutNumNeg'], errors='coerce')
            if not dfs['st'].empty:
                dfs['st']['AutNumStatus'] = pd.to_numeric(dfs['st']['AutNumStatus'], errors='coerce')

            # Chaves CRÍTICAS (que quebram em 2025)
            if not dfs['cr'].empty:
                dfs['cr']['ID'] = pd.to_numeric(dfs['cr']['ID'], errors='coerce')
            if not dfs['cp'].empty:
                dfs['cp']['ID'] = pd.to_numeric(dfs['cp']['ID'], errors='coerce')

            # Limpar colunas de data/período
            dfs['g']['Ano'] = pd.to_numeric(dfs['g']['Ano'].astype(str).str.strip(), errors='coerce')
            dfs['g']['Mes'] = pd.to_numeric(dfs['g']['Mes'].astype(str).str.strip(), errors='coerce')
            
        except Exception as e:
            st.error(f"Erro na limpeza de chaves: {e}")
            return pd.DataFrame()

        # 5. Executar o "Master Join" via Pandas
        with st.spinner("Entrelaçando dimensões (Joins)..."):
            df = dfs['g'] # Começa com a tabela FATO
            
            # Funções de merge seguras
            def safe_merge(df_left, df_right, **kwargs):
                if df_right.empty:
                    st.warning(f"Skipping merge: {kwargs.get('left_on')}/{kwargs.get('right_on')} (tabela direita vazia)")
                    return df_left
                # Garantir que as chaves de merge existam no df_left
                left_key = kwargs.get('left_on')
                if left_key and left_key not in df_left.columns:
                    st.warning(f"Skipping merge: Chave '{left_key}' não encontrada no DataFrame principal.")
                    return df_left
                return pd.merge(df_left, df_right, **kwargs)

            df = safe_merge(df, dfs['tec'], left_on='ConsultGest', right_on='AutNumTec', how='left')
            df = safe_merge(df, dfs['p'], left_on='ProjGest', right_on='AutNumProj', how='left', suffixes=('', '_proj'))
            df = safe_merge(df, dfs['cli'], left_on='CodCliProj', right_on='AutNumCli', how='left')
            df = safe_merge(df, dfs['tp'], left_on='TipoProj', right_on='AutNumTipo', how='left')
            df = safe_merge(df, dfs['neg'], left_on='CodNegProj', right_on='AutNumNeg', how='left')
            df = safe_merge(df, dfs['st'], left_on='StatusProj', right_on='AutNumStatus', how='left')
            
            # 6. EXECUTAR OS JOINS DE CAIXA (OS QUE QUEBRAM EM 2025)
            df = safe_merge(df, dfs['cr'], left_on='IdGest2', right_on='ID', how='left', suffixes=('', '_cr'))
            df = safe_merge(df, dfs['cp'], left_on='IdGest2', right_on='ID', how='left', suffixes=('', '_cp'))

        # 7. Mapeamento de Colunas (Spec -> Layout)
        with st.spinner("Mapeando colunas e criando métricas..."):
            mapa_colunas = {
                'QtHrReal': 'Hrs_Real',
                'QtHrOrc': 'Hrs_Prev',
                'ReceitaReal': 'Receita',
                'CustoReal': 'Custo',
                'PercMgReal': 'Margem',
                'VlHrOrc': 'VH_Venda', # Usando VlHrOrc como Venda, conforme lógica
                'VlHrCusto': 'VH_Custo',
                'ReceitaOrc': 'Receita_Orc',
                'CustoOrc': 'Custo_Orc',
                'NomeTec': 'Consultor',
                'DescCli': 'Cliente',
                'DescProj': 'Projeto',
                'DescTipo': 'TipoProj',
                # Colunas de Caixa (pós-join)
                'VlRec': 'Caixa_Recebido',
                'DtRec': 'Caixa_DtRec',
                'VlPago': 'Caixa_Pago',
                'DtPagamento': 'Caixa_DtPag',
            }
            
            df = df.rename(columns=mapa_colunas)
            
            # Garantir que colunas numéricas pós-rename existam e sejam numéricas
            colunas_numericas_app = [
                'Hrs_Real', 'Hrs_Prev', 'Receita', 'Custo', 'Margem', 
                'VH_Venda', 'VH_Custo', 'Receita_Orc', 'Custo_Orc', 'Mes', 'Ano',
                'Caixa_Recebido', 'Caixa_Pago'
            ]
            
            for col in colunas_numericas_app:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                else:
                    df[col] = 0 
            
            # 8. Criação de dimensões quânticas (métricas avançadas do seu layout)
            df['Lucro'] = df['Receita'] - df['Custo']
            df['Desvio_Hrs'] = df['Hrs_Real'] - df['Hrs_Prev']
            df['Eficiencia'] = np.where(df['Hrs_Prev'] > 0, 
                                       (df['Hrs_Real'] / df['Hrs_Prev']) * 100, 100)
            df['ROI_Hora'] = np.where(df['Hrs_Real'] > 0, 
                                     df['Lucro'] / df['Hrs_Real'], 0)
            df['Produtividade'] = np.where(df['Hrs_Real'] > 0, 
                                          df['Receita'] / df['Hrs_Real'], 0)
            
            # Dimensão temporal
            df = df.dropna(subset=['Ano', 'Mes']) # Remover registros sem ano/mês
            df['Data'] = pd.to_datetime(df['Ano'].astype(int).astype(str) + '-' + 
                                       df['Mes'].astype(int).astype(str) + '-01', 
                                       errors='coerce')
            
            # Classificação de performance
            df['Score_Performance'] = (
                (df['Margem'] * 0.4) + # Assumindo que Margem já é 0.xx
                (np.clip(100 - abs(df['Eficiencia'] - 100), 0, 100) / 100 * 0.3) +
                (np.clip(df['ROI_Hora'] / 50, 0, 1) * 0.3)
            ) * 100
            
            # Níveis de alerta
            df['Status'] = pd.cut(df['Score_Performance'], 
                                 bins=[0, 40, 70, 100], 
                                 labels=['CRÍTICO', 'ATENÇÃO', 'EXCELENTE'],
                                 right=True)
            
            # ----------------- CORREÇÃO DO BUG AQUI -----------------
            # Preencher NaNs em colunas de string (importante para filtros)
            colunas_string_app = ['Consultor', 'Cliente', 'Projeto', 'TipoProj']
            for col_str in colunas_string_app:
                if col_str not in df.columns:
                    # Se o merge falhou e a coluna nem existe, crie-a
                    df[col_str] = 'N/A' 
                else:
                    # Se a coluna existe mas tem NaNs, preencha
                    df[col_str] = df[col_str].fillna('N/A')
            # --------------------------------------------------------

        st.success("Universo de Dados Carregado e Sincronizado.")
        return df
            
    def aplicar_colapso_quantico(self, filtros):
        """
        Colapso Quântico: Filtra o universo de possibilidades para o estado observado
        (Copiado do seu layout)
        """
        df = self.dados_universo.copy()
        
        if filtros.get('consultores') and 'TODOS' not in filtros['consultores']:
            df = df[df['Consultor'].isin(filtros['consultores'])]
        
        if filtros.get('clientes') and 'TODOS' not in filtros['clientes']:
            df = df[df['Cliente'].isin(filtros['clientes'])]
        
        if filtros.get('projetos') and 'TODOS' not in filtros['projetos']:
            df = df[df['Projeto'].isin(filtros['projetos'])]
        
        if filtros.get('tipos') and 'TODOS' not in filtros['tipos']:
            df = df[df['TipoProj'].isin(filtros['tipos'])]
        
        if filtros.get('mes') and filtros.get('ano'):
            # Garantir que os tipos são iguais para o filtro
            mes_sel = int(filtros['mes'])
            ano_sel = int(filtros['ano'])
            df = df[(df['Mes'] == mes_sel) & (df['Ano'] == ano_sel)]
        
        self.estado_quantum = df
        return df
    
    def detectar_entrelacements(self):
        """
        Entrelaçamento: Detecta correlações e dependências ocultas entre variáveis
        (Copiado do seu layout)
        """
        df = self.estado_quantum
        
        if df.empty or len(df) < 5:
            self.padroes_ocultos = {}
            return {}
        
        entrelacements = {}
        
        # Correlação entre eficiência e margem
        if len(df) >= 5:
            corr_efic_margem = df[['Eficiencia', 'Margem']].corr().iloc[0, 1]
            if abs(corr_efic_margem) > 0.6:
                entrelacements['eficiencia_margem'] = {
                    'forca': corr_efic_margem,
                    'tipo': 'FORTE' if abs(corr_efic_margem) > 0.8 else 'MODERADO',
                    'descricao': f"Correlação {'positiva' if corr_efic_margem > 0 else 'negativa'} entre eficiência e margem"
                }
        
        # Análise por consultor
        perf_consultor = df.groupby('Consultor').agg({
            'Score_Performance': 'mean',
            'ROI_Hora': 'mean',
            'Margem': 'mean'
        })
        
        if len(perf_consultor) > 1:
            variancia = perf_consultor['Score_Performance'].std()
            if variancia > 15:
                entrelacements['disparidade_consultores'] = {
                    'valor': variancia,
                    'tipo': 'ALTA' if variancia > 25 else 'MÉDIA',
                    'descricao': f"Variação significativa de performance entre consultores"
                }
        
        # Análise por tipo de projeto
        perf_tipo = df.groupby('TipoProj').agg({
            'Margem': 'mean',
            'ROI_Hora': 'mean'
        })
        
        if len(perf_tipo) > 1:
            # Garantir que não estamos lidando com NaNs
            perf_tipo = perf_tipo.fillna(0)
            # Evitar divisão por zero se ROI_Hora for 0 ou negativo
            pior_roi = max(perf_tipo['ROI_Hora'].min(), 0.01) 
            melhor_roi = max(perf_tipo['ROI_Hora'].max(), 0)

            if pior_roi > 0 and melhor_roi > 0:
                melhor_tipo = perf_tipo['ROI_Hora'].idxmax()
                pior_tipo = perf_tipo['ROI_Hora'].idxmin()
                ratio = melhor_roi / pior_roi
            
                if ratio > 1.5:
                    entrelacements['otimizacao_mix'] = {
                        'melhor': melhor_tipo,
                        'pior': pior_tipo,
                        'ratio': ratio,
                        'descricao': f"Oportunidade de otimização do mix de serviços"
                    }
        
        self.padroes_ocultos = entrelacements
        return entrelacements
    
    def gerar_prescricoes_quantum(self):
        """
        Interferência Quântica: Gera prescrições prescritivas baseadas em análise profunda
        (Copiado do seu layout)
        """
        df = self.estado_quantum
        entrelacements = self.padroes_ocultos
        
        if df.empty:
            return [{
                'tipo': 'INFO',
                'prioridade': 'BAIXA',
                'titulo': '📊 Aguardando Dados',
                'sintese': 'Selecione filtros para iniciar análise quântica',
                'analise': 'O CRQ precisa de dados para processar',
                'prescricao': 'Ajuste os filtros na sidebar',
                'impacto_estimado': 'N/A',
                'confianca': 0
            }]
        
        prescricoes = []
        
        # 0. ALERTA DE GAP DE CAIXA (NOVA PRESCRIÇÃO BASEADA NA ESPECIFICAÇÃO)
        anos_no_filtro = df['Ano'].unique()
        if any(ano >= 2025 for ano in anos_no_filtro):
            df_2025_filtrado = df[df['Ano'] >= 2025]
            if not df_2025_filtrado.empty and df_2025_filtrado['Caixa_Recebido'].sum() == 0 and df_2025_filtrado['Caixa_Pago'].sum() == 0:
                 prescricoes.append({
                    'tipo': 'ALERTA',
                    'prioridade': 'CRÍTICA',
                    'titulo': '🚨 ALERTA DE INTEGRIDADE DE DADOS: FLUXO DE CAIXA 2025',
                    'sintese': 'O Fluxo de Caixa (Recebido/Pago) para 2025 está ZERADO.',
                    'analise': 'O sistema detectou que a ligação de chave primária entre a tabela de fatos (Tb_GestorFin2.IdGest2) '
                              'e as tabelas de caixa (ContasReceber.ID, ContasPagar.ID) está quebrada para registros a partir de 2025. '
                              'Isso significa que todas as análises de Lucro de CAIXA, Gaps de Faturamento e Gaps de Custo estão comprometidas para este período.',
                    'prescricao': '1. ACIONAR EQUIPE DE DADOS/SISTEMAS URGENTEMENTE.\n'
                                 '2. Investigar o processo de ETL/Lançamento que mudou em 2025.\n'
                                 '3. Estabelecer uma nova chave de ligação (ex: Ano+Mes+Consultor/Cliente) ou corrigir a geração de IDs.\n'
                                 '4. ATÉ A CORREÇÃO: Use este dashboard focando apenas na visão CONTÁBIL (Receita, Custo, Margem) para 2025.',
                    'impacto_estimado': 'PERDA TOTAL da visão de Caixa. Risco de má gestão financeira.',
                    'confianca': 100
                })

        # 1. ANÁLISE DE SUPERÁVIT/DÉFICIT DE HORAS
        desvio_total = df['Desvio_Hrs'].sum()
        hrs_previstas_total = df['Hrs_Prev'].sum()
        
        if hrs_previstas_total > 0:
            desvio_perc = (desvio_total / hrs_previstas_total) * 100
            
            if desvio_perc > 15:
                prescricoes.append({
                    'tipo': 'ALERTA',
                    'prioridade': 'CRÍTICA',
                    'titulo': '⚠️ Superávit Crítico de Horas (Sangria)',
                    'sintese': f'{desvio_total:.0f}h acima do planejado ({desvio_perc:.1f}%)',
                    'analise': f'Análise profunda revela que a equipe está consumindo {desvio_perc:.1f}% mais horas que o previsto. '
                              f'Isso impacta diretamente a rentabilidade dos projetos de escopo fechado ("PROJETO FECHADO").',
                    'prescricao': '1. Revisar metodologia de estimativa com histórico real\n'
                                 '2. Implementar checkpoints semanais de acompanhamento\n'
                                 '3. Investigar gargalos técnicos ou de processo\n'
                                 '4. Considerar renegociação de contratos de escopo fixo',
                    'impacto_estimado': f'Potencial economia de R$ {abs(desvio_total * 65):.2f} em custos (base R$65/h)',
                    'confianca': 92
                })
            
            elif desvio_perc < -10:
                capacidade_ociosa = abs(desvio_total)
                receita_potencial = capacidade_ociosa * 115 # Base R$115/h
                
                prescricoes.append({
                    'tipo': 'OPORTUNIDADE',
                    'prioridade': 'ALTA',
                    'titulo': '🎯 Capacidade Ociosa Detectada',
                    'sintese': f'{capacidade_ociosa:.0f}h de capacidade não utilizada',
                    'analise': f'O CRQ identificou {abs(desvio_perc):.1f}% de subutilização da capacidade instalada. '
                              f'Com base no valor médio de hora da empresa, isso representa receita potencial não capturada.',
                    'prescricao': '1. Intensificar prospecção comercial imediata\n'
                                 '2. Alocar consultores em projetos internos estratégicos\n'
                                 '3. Oferecer pacotes promocionais para clientes atuais',
                    'impacto_estimado': f'Receita adicional potencial: R$ {receita_potencial:.2f}',
                    'confianca': 88
                })
        
        # 2. ANÁLISE DE RENTABILIDADE POR TIPO DE SERVIÇO
        if 'otimizacao_mix' in entrelacements:
            info = entrelacements['otimizacao_mix']
            
            perf_tipo = df.groupby('TipoProj').agg({
                'ROI_Hora': 'mean',
                'Margem': 'mean',
                'Hrs_Real': 'sum'
            }).fillna(0)
            
            melhor = perf_tipo.loc[info['melhor']]
            pior = perf_tipo.loc[info['pior']]
            
            prescricoes.append({
                'tipo': 'EFICIENCIA',
                'prioridade': 'ALTA',
                'titulo': '💎 Otimização Estratégica do Mix',
                'sintese': f'{info["melhor"]} é {info["ratio"]:.1f}x mais rentável',
                'analise': f'Análise quântica revela assimetria significativa: "{info["melhor"]}" gera '
                          f'R$ {melhor["ROI_Hora"]:.2f}/hora de lucro (margem {melhor["Margem"]*100:.1f}%), '
                          f'enquanto "{info["pior"]}" gera apenas R$ {pior["ROI_Hora"]:.2f}/hora '
                          f'(margem {pior["Margem"]*100:.1f}%).',
                'prescricao': f'1. Meta: aumentar participação de "{info["melhor"]}"\n'
                             f'2. Reposicionar comercialmente serviços tipo "{info["melhor"]}"\n'
                             f'3. Avaliar viabilidade de descontinuar "{info["pior"]}" ou repricing',
                'impacto_estimado': f'Aumento projetado de 35-45% na margem geral',
                'confianca': 94
            })
        
        # 3. ANÁLISE DE PERFORMANCE POR CONSULTOR
        if 'disparidade_consultores' in entrelacements:
            perf_cons = df.groupby('Consultor').agg({
                'Score_Performance': 'mean',
                'ROI_Hora': 'mean',
                'Margem': 'mean',
                'Eficiencia': 'mean'
            }).sort_values('Score_Performance', ascending=False).fillna(0)
            
            # Ignorar 'N/A' se for o top ou bottom
            perf_cons = perf_cons[perf_cons.index != 'N/A']
            
            if len(perf_cons) > 1:
                top_performer = perf_cons.index[0]
                top_score = perf_cons.iloc[0]
                bottom_performer = perf_cons.index[-1]
                bottom_score = perf_cons.iloc[-1]
                
                gap = top_score['Score_Performance'] - bottom_score['Score_Performance']
                
                prescricoes.append({
                    'tipo': 'TALENTO',
                    'prioridade': 'ALTA',
                    'titulo': '🏆 Assimetria de Performance Detectada',
                    'sintese': f'{gap:.1f} pontos de diferença entre top e bottom performer',
                    'analise': f'**Top Performer:** {top_performer}\n'
                              f'- Score de Performance: {top_score["Score_Performance"]:.1f}\n'
                              f'- ROI/Hora: R$ {top_score["ROI_Hora"]:.2f}\n'
                              f'- Margem Média: {top_score["Margem"]*100:.1f}%\n'
                              f'**Necessita Desenvolvimento:** {bottom_performer}\n'
                              f'- Score: {bottom_score["Score_Performance"]:.1f}\n'
                              f'- ROI/Hora: R$ {bottom_score["ROI_Hora"]:.2f}\n'
                              f'- Margem: {bottom_score["Margem"]*100:.1f}%',
                    'prescricao': f'1. Implementar programa de mentoria: {top_performer} → {bottom_performer}\n'
                                 f'2. Analisar metodologias e processos do top performer\n'
                                 f'3. Avaliar adequação de alocação de projetos\n'
                                 f'4. Criar plano de desenvolvimento individualizado',
                    'impacto_estimado': 'Nivelamento pode aumentar rentabilidade geral em 15-25%',
                    'confianca': 89
                })
        
        # Se não houver prescrições críticas (além do gap de dados), dar feedback positivo
        if len(prescricoes) == 0 or (len(prescricoes) == 1 and prescricoes[0]['prioridade'] == 'CRÍTICA'):
            margem_media = df['Margem'].mean()
            eficiencia_geral = df['Eficiencia'].mean()
            prescricoes.append({
                'tipo': 'SUCESSO',
                'prioridade': 'BAIXA',
                'titulo': '✅ Operação em Excelência (Visão Contábil)',
                'sintese': 'Indicadores contábeis dentro dos parâmetros ideais',
                'analise': f'Análise quântica não identificou anomalias contábeis. '
                          f'Margem média de {margem_media*100:.1f}%, eficiência de {eficiencia_geral:.1f}%.',
                'prescricao': '1. Manter estratégia atual\n'
                             '2. Documentar melhores práticas\n'
                             '3. FOCAR NA CORREÇÃO DO GAP DE DADOS DE CAIXA (se aplicável).',
                'impacto_estimado': 'Crescimento sustentável de 15-20% ao ano',
                'confianca': 95
            })
        
        self.prescricoes_ativas = prescricoes
        return prescricoes
    
    def calcular_metricas_consolidadas(self):
        """Calcula KPIs consolidados do estado quântico atual"""
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
        
        receita_total = df['Receita'].sum()
        custo_total = df['Custo'].sum()
        caixa_recebido_total = df['Caixa_Recebido'].sum()
        caixa_pago_total = df['Caixa_Pago'].sum()

        return {
            # Visão Contábil
            'receita': receita_total,
            'custo': custo_total,
            'lucro': df['Lucro'].sum(),
            'margem': df['Margem'].mean() if not df.empty else 0,
            'hrs_real': df['Hrs_Real'].sum(),
            'hrs_prev': df['Hrs_Prev'].sum(),
            'eficiencia': df['Eficiencia'].mean() if not df.empty else 0,
            'roi_hora': df['ROI_Hora'].mean() if not df.empty else 0,
            'consultores': df['Consultor'].nunique(),
            'clientes': df['Cliente'].nunique(),
            'projetos': df['Projeto'].nunique(),
            'score': df['Score_Performance'].mean() if not df.empty else 0,
            
            # Visão Caixa (Quebrada em 2025, mas calculada)
            'caixa_recebido': caixa_recebido_total,
            'caixa_pago': caixa_pago_total,
            'lucro_caixa': caixa_recebido_total - caixa_pago_total,
            
            # Gaps (Conforme Spec)
            'gap_faturamento': receita_total - caixa_recebido_total,
            'gap_custo': custo_total - caixa_pago_total
        }

# ═══════════════════════════════════════════════════════════════════════════════
# MOTOR DE PERGUNTAS SOCRÁTICAS (COPIADO DO SEU EXEMPLO)
# ═══════════════════════════════════════════════════════════════════════════════

class SocraticQuestioningEngine:
    """
    Motor de Questionamento Socrático - O Terapeuta Empresarial
    (Copiado do seu layout - deve funcionar se o CRQ entregar o df)
    """
    
    def __init__(self, crq_engine):
        self.crq = crq_engine
        self.perguntas_geradas = []
        
    def gerar_perguntas_estrategicas(self):
        """Gera perguntas profundas baseadas em padrões nos dados"""
        df = self.crq.estado_quantum
        
        if df.empty:
            return [{
                'categoria': 'INICIAL',
                'pergunta': 'Seus dados estão prontos para serem questionados. Aplique filtros para iniciar a jornada de descoberta.',
                'contexto': '',
                'profundidade': 'BÁSICA',
                'icone': '🤔'
            }]
        
        perguntas = []
        
        # 1. PERGUNTAS SOBRE RENTABILIDADE E ESTRATÉGIA
        perguntas.extend(self._questionar_rentabilidade(df))
        
        # 2. PERGUNTAS SOBRE EFICIÊNCIA OPERACIONAL
        perguntas.extend(self._questionar_eficiencia(df))
        
        # 3. PERGUNTAS SOBRE PESSOAS E TALENTO
        perguntas.extend(self._questionar_talento(df))
        
        # 4. PERGUNTAS SOBRE CLIENTES E PORTFÓLIO
        perguntas.extend(self._questionar_portfolio(df))
        
        # 5. PERGUNTAS SOBRE CRESCIMENTO E FUTURO
        perguntas.extend(self._questionar_crescimento(df))
        
        # 6. PERGUNTAS SOBRE RISCOS OCULTOS
        perguntas.extend(self._questionar_riscos(df))
        
        # 7. PERGUNTAS SOBRE PRECIFICAÇÃO
        perguntas.extend(self._questionar_pricing(df))
        
        self.perguntas_geradas = perguntas
        return perguntas
    
    def _questionar_rentabilidade(self, df):
        perguntas = []
        if 'TipoProj' in df.columns and len(df['TipoProj'].unique()) > 1:
            marg_tipo = df.groupby('TipoProj')['Margem'].mean()
            marg_tipo = marg_tipo.drop('N/A', errors='ignore') # Ignorar dados 'N/A'
            if len(marg_tipo) > 1:
                melhor_tipo = marg_tipo.idxmax()
                pior_tipo = marg_tipo.idxmin()
                diferenca = marg_tipo[melhor_tipo] - marg_tipo[pior_tipo]
                
                if diferenca > 0.1: # 10%
                    perguntas.append({
                        'categoria': 'ESTRATÉGIA',
                        'pergunta': f'Seus projetos de "{melhor_tipo}" têm margem {diferenca*100:.1f}% superior a "{pior_tipo}". '
                                   f'Esta disparidade é resultado de uma estratégia consciente de penetração de mercado, '
                                   f'ou revela um custo oculto que ainda não identificamos?',
                        'contexto': f'Margem "{melhor_tipo}": {marg_tipo[melhor_tipo]*100:.1f}% vs "{pior_tipo}": {marg_tipo[pior_tipo]*100:.1f}%',
                        'profundidade': 'ESTRATÉGICA',
                        'icone': '💎',
                        'dados': {
                            'melhor_tipo': melhor_tipo,
                            'pior_tipo': pior_tipo,
                            'margem_melhor': marg_tipo[melhor_tipo],
                            'margem_pior': marg_tipo[pior_tipo]
                        }
                    })
        
        margem_media = df['Margem'].mean()
        if margem_media < 0.35: # Ajustado para fração 0.xx
            perguntas.append({
                'categoria': 'FINANCEIRO',
                'pergunta': f'Sua margem média de {margem_media*100:.1f}% está abaixo do ideal de 40-50% para consultorias. '
                           f'O que você acha que está consumindo essa rentabilidade? '
                           f'São custos operacionais invisíveis, subprecificação, ou ineficiências na entrega?',
                'contexto': f'Margem atual: {margem_media*100:.1f}% | Meta recomendada: 45%',
                'profundidade': 'CRÍTICA',
                'icone': '⚠️',
                'dados': {'margem_media': margem_media}
            })
        
        return perguntas
    
    def _questionar_eficiencia(self, df):
        perguntas = []
        desvio_hrs_total = df['Desvio_Hrs'].sum()
        hrs_previstas = df['Hrs_Prev'].sum()
        
        if hrs_previstas > 0:
            desvio_perc = (desvio_hrs_total / hrs_previstas) * 100
            
            if desvio_perc > 15:
                perguntas.append({
                    'categoria': 'OPERACIONAL',
                    'pergunta': f'Seus projetos estão consumindo {desvio_perc:.1f}% mais horas que o planejado. '
                               f'Isso é um problema de estimativa (você não sabe quanto as coisas custam), '
                               f'um problema de execução (a equipe não é produtiva), '
                               f'ou um problema de escopo (o cliente sempre pede mais)?',
                    'contexto': f'{abs(desvio_hrs_total):.0f} horas acima do previsto',
                    'profundidade': 'CRÍTICA',
                    'icone': '⏱️',
                    'dados': {'desvio_horas': desvio_hrs_total, 'desvio_perc': desvio_perc}
                })
            
            elif desvio_perc < -10:
                perguntas.append({
                    'categoria': 'OPORTUNIDADE',
                    'pergunta': f'Você está usando {abs(desvio_perc):.1f}% menos horas que o previsto. '
                               f'Isso é eficiência genuína que você pode replicar, '
                               f'ou é capacidade ociosa disfarçada que deveria estar gerando receita?',
                    'contexto': f'{abs(desvio_hrs_total):.0f} horas de capacidade não utilizada',
                    'profundidade': 'ESTRATÉGICA',
                    'icone': '💡',
                    'dados': {'desvio_horas': desvio_hrs_total, 'desvio_perc': desvio_perc}
                })
        return perguntas
    
    def _questionar_talento(self, df):
        perguntas = []
        if len(df['Consultor'].unique()) > 2:
            perf = df.groupby('Consultor').agg({
                'ROI_Hora': 'mean',
                'Margem': 'mean',
                'Hrs_Real': 'sum'
            }).fillna(0)
            perf = perf.drop('N/A', errors='ignore') # Ignorar dados 'N/A'
            
            if len(perf) > 1:
                top_performer = perf['ROI_Hora'].idxmax()
                top_roi = perf.loc[top_performer, 'ROI_Hora']
                
                perguntas.append({
                    'categoria': 'TALENTO',
                    'pergunta': f'{top_performer} gera R$ {top_roi:.2f} de lucro por hora. '
                               f'Se você perdesse essa pessoa amanhã, quanto tempo levaria para substituí-la? '
                               f'E mais: você está criando outros "{top_performer}" ou ele é um milagre irrepetível?',
                    'contexto': f'Top performer: {top_performer} com ROI/hora de R$ {top_roi:.2f}',
                    'profundidade': 'ESTRATÉGICA',
                    'icone': '🏆',
                    'dados': {'top_performer': top_performer, 'top_roi': top_roi}
                })
        return perguntas
    
    def _questionar_portfolio(self, df):
        perguntas = []
        if len(df['Cliente'].unique()) > 1:
            receita_cliente = df.groupby('Cliente')['Receita'].sum().sort_values(ascending=False)
            receita_cliente = receita_cliente.drop('N/A', errors='ignore') # Ignorar dados 'N/A'

            if len(receita_cliente) > 0:
                top_cliente = receita_cliente.index[0]
                receita_top = receita_cliente.iloc[0]
                receita_total = receita_cliente.sum()
                concentracao = (receita_top / receita_total * 100) if receita_total > 0 else 0
                
                if concentracao > 50:
                    perguntas.append({
                        'categoria': 'RISCO',
                        'pergunta': f'{top_cliente} representa {concentracao:.1f}% da sua receita. '
                                   f'Se esse cliente decidir internalizar o serviço ou trocar de fornecedor amanhã, '
                                   f'sua empresa sobrevive? Por quanto tempo? '
                                   f'Você está construindo um negócio ou se tornando refém de um cliente?',
                        'contexto': f'Concentração: {concentracao:.1f}% em {top_cliente}',
                        'profundidade': 'CRÍTICA',
                        'icone': '⚠️',
                        'dados': {'cliente': top_cliente, 'concentracao': concentracao}
                    })
        return perguntas
    
    def _questionar_crescimento(self, df):
        perguntas = []
        if 'Data' in df.columns and len(df['Data'].unique()) > 1:
            receita_tempo = df.groupby('Data')['Receita'].sum().sort_index()
            
            if len(receita_tempo) >= 2:
                crescimento = receita_tempo.pct_change().mean() * 100
                
                if crescimento < -5:
                    perguntas.append({
                        'categoria': 'CRÍTICO',
                        'pergunta': f'Sua receita está em declínio (média de {crescimento:.1f}% ao mês). '
                                   f'Você está perdendo clientes, ou seus clientes estão comprando menos? '
                                   f'E mais importante: você sabe por quê, ou está apenas "esperando melhorar"?',
                        'contexto': f'Tendência: {crescimento:.1f}% ao mês',
                        'profundidade': 'CRÍTICA',
                        'icone': '📉',
                        'dados': {'crescimento': crescimento}
                    })
        return perguntas
    
    def _questionar_riscos(self, df):
        perguntas = []
        projetos_negativos = df[df['Margem'] < 0]
        
        if len(projetos_negativos) > 0:
            valor_destruido = projetos_negativos['Lucro'].sum()
            perguntas.append({
                'categoria': 'CRÍTICO',
                'pergunta': f'Você tem {len(projetos_negativos)} projetos com margem negativa, '
                           f'destruindo R$ {abs(valor_destruido):,.2f} de valor. '
                           f'Por que você mantém projetos que perdem dinheiro? '
                           f'É esperança de que "melhorem", ou você tem medo de admitir o erro?',
                'contexto': f'{len(projetos_negativos)} projetos deficitários | Perda: R$ {abs(valor_destruido):,.2f}',
                'profundidade': 'CRÍTICA',
                'icone': '🚨',
                'dados': {
                    'num_projetos_negativos': len(projetos_negativos),
                    'valor_destruido': valor_destruido
                }
            })
        return perguntas

    def _questionar_pricing(self, df):
        perguntas = []
        if 'VH_Venda' in df.columns and 'VH_Custo' in df.columns:
            # Evitar divisão por zero
            df_temp = df[df['VH_Custo'] > 0]
            if not df_temp.empty:
                markup_medio = ((df_temp['VH_Venda'] - df_temp['VH_Custo']) / df_temp['VH_Custo'] * 100).mean()
                
                if markup_medio < 80:
                    perguntas.append({
                        'categoria': 'FINANCEIRO',
                        'pergunta': f'Seu markup médio é de apenas {markup_medio:.1f}%. '
                                   f'Você está deixando margem suficiente para crescer, investir, ter lucro '
                                   f'e ainda sobreviver a uma crise? Ou está vivendo no limite?',
                        'contexto': f'Markup médio: {markup_medio:.1f}% (recomendado: > 100%)',
                        'profundidade': 'CRÍTICA',
                        'icone': '💸',
                        'dados': {'markup': markup_medio}
                    })
        return perguntas

# ═══════════════════════════════════════════════════════════════════════════════
# INICIALIZAÇÃO DOS MOTORES (CRQ e Socrático)
# ═══════════════════════════════════════════════════════════════════════════════

if 'crq' not in st.session_state:
    st.session_state.crq = CoreQuantumReasoning()

if 'socratic_engine' not in st.session_state:
    st.session_state.socratic_engine = SocraticQuestioningEngine(st.session_state.crq)

crq = st.session_state.crq
socratic = st.session_state.socratic_engine

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER PREMIUM DO SISTEMA (COM NOVO TÍTULO)
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="header-premium">
    <div class="logo-maestro">⚡ MAESTRO FAROL</div>
    <div class="subtitle-maestro">AUTONOMOUS INSIGHT SYSTEM</div>
</div>
""", unsafe_allow_html=True) # <-- MUDANÇA DE BRANDING

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR INTELIGENTE COM FILTROS AVANÇADOS
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🎛️ Painel de Controle CRQ")
    
    # Se o carregamento de dados falhou, parar aqui
    if crq.dados_universo.empty:
        st.error("Carregamento de dados falhou. Verifique a conexão e st.secrets.")
        st.stop()

    st.markdown("### 🔍 Filtros Dimensionais")
    
    # Extrair opções únicas do DF carregado
    consultores_opts = ['TODOS'] + sorted(crq.dados_universo['Consultor'].unique().tolist())
    clientes_opts = ['TODOS'] + sorted(crq.dados_universo['Cliente'].unique().tolist())
    projetos_opts = ['TODOS'] + sorted(crq.dados_universo['Projeto'].unique().tolist())
    tipos_opts = ['TODOS'] + sorted(crq.dados_universo['TipoProj'].unique().tolist())
    
    # Garantir que meses/anos são ints e únicos
    meses_opts = sorted(crq.dados_universo['Mes'].astype(int).unique().tolist())
    anos_opts = sorted(crq.dados_universo['Ano'].astype(int).unique().tolist())
    
    # Filtros
    col_m, col_a = st.columns(2)
    with col_m:
        # Usar o último mês como padrão
        mes_default_idx = len(meses_opts) - 1 if meses_opts else 0
        mes_sel = st.selectbox("Mês", meses_opts, index=mes_default_idx, key="mes")
    with col_a:
        # Usar o último ano como padrão
        ano_default_idx = len(anos_opts) - 1 if anos_opts else 0
        ano_sel = st.selectbox("Ano", anos_opts, index=ano_default_idx, key="ano")
    
    cons_sel = st.multiselect("👥 Consultores", consultores_opts, default=["TODOS"])
    cli_sel = st.multiselect("🏢 Clientes", clientes_opts, default=["TODOS"])
    proj_sel = st.multiselect("📁 Projetos", projetos_opts, default=["TODOS"])
    tipo_sel = st.multiselect("🎯 Tipo de Serviço", tipos_opts, default=["TODOS"])
    
    st.markdown("---")
    st.markdown("### 🧠 Configurações IA")
    
    ia_ativa = st.toggle("IA Prescritiva", value=True)
    
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
    st.metric("Entrelaçamentos", len(crq.padroes_ocultos))
    
    if st.button("🔄 Reprocessar Dados", use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# INTERFACE PRINCIPAL - TABS (Estrutura da Spec + Layout)
# ═══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎯 Visão Executiva",
    "💰 Fechamento",
    "💵 Fluxo de Caixa",
    "🔬 Análise Profunda",
    "🧠 IA Prescritiva",
    "🤔 Consultor Socrático"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: VISÃO EXECUTIVA (TELA 1 da Spec)
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("## 📈 Dashboard Executivo (Visão Contábil)")
    
    # KPIs Principais
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "💰 Receita Faturada",
            f"R$ {metricas['receita']:,.0f}",
            help="Receita total do período (Contábil)"
        )
    
    with col2:
        st.metric(
            "📊 Lucro Contábil",
            f"R$ {metricas['lucro']:,.0f}",
            help="Lucro após custos contábeis"
        )
    
    with col3:
        st.metric(
            "📈 Margem Média",
            f"{metricas['margem']*100:.1f}%", # Convertendo fração para %
            delta_color="normal" if metricas['margem'] > 0.4 else "inverse",
            help="Margem percentual média (Contábil)"
        )
    
    with col4:
        st.metric(
            "⏱️ Horas Realizadas",
            f"{metricas['hrs_real']:.0f}h",
            delta=f"{metricas['hrs_real']-metricas['hrs_prev']:.0f}h vs Previsto",
            delta_color="inverse" if metricas['hrs_real'] > metricas['hrs_prev'] else "normal",
            help="Total de horas realizadas vs. previstas"
        )
    
    with col5:
        st.metric(
            "💎 ROI por Hora",
            f"R$ {metricas['roi_hora']:.2f}",
            help="Lucro contábil por hora trabalhada"
        )
    
    st.markdown("---")
    
    # Gráficos Principais (Conforme Spec)
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        st.markdown(f"### 📊 Receita por Cliente (Top 10) - {mes_sel}/{ano_sel}")
        
        if not df_filtrado.empty:
            rec_cliente = df_filtrado.groupby('Cliente').agg(
                Receita_Total=('Receita', 'sum'),
                Margem_Media=('Margem', 'mean')
            ).nlargest(10, 'Receita_Total').sort_values('Receita_Total')
            
            # Converter margem para % para o gráfico
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
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Receita (R$)",
                yaxis_title="",
                height=400,
                coloraxis_colorbar=dict(title="Margem Média %")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Sem dados disponíveis")
    
    with col_viz2:
        st.markdown(f"### 🎯 Performance por Consultor - {mes_sel}/{ano_sel}")
        
        if not df_filtrado.empty:
            perf_cons = df_filtrado.groupby('Consultor').agg(
                Receita=('Receita', 'sum'),
                Margem_Media=('Margem', 'mean'),
                Horas_Trabalhadas=('Hrs_Real', 'sum'),
                ROI_Hora=('ROI_Hora', 'mean'),
                Score_Performance=('Score_Performance', 'mean')
            ).sort_values('Receita', ascending=False)
            
            # Converter margem para % para o gráfico
            perf_cons['Margem_Media_Perc'] = perf_cons['Margem_Media'] * 100
            
            fig = px.scatter(
                perf_cons,
                x='Receita',
                y='Margem_Media_Perc',
                size='Horas_Trabalhadas',
                color='ROI_Hora',
                hover_name=perf_cons.index,
                color_continuous_scale='Viridis',
                size_max=60,
                hover_data={
                    'Margem_Media_Perc': ':.1f%',
                    'Receita': ':,.0f',
                    'Horas_Trabalhadas': ':.0f'
                }
            )
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Receita Total (R$)",
                yaxis_title="Margem Média (%)",
                height=400,
                coloraxis_colorbar=dict(title="ROI/Hora")
            )
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("Ver dados detalhados dos consultores"):
                st.dataframe(perf_cons.style.format({
                    'Receita': 'R$ {:,.2f}',
                    'Margem_Media': '{:.1%}',
                    'Margem_Media_Perc': '{:.1f}%',
                    'Horas_Trabalhadas': '{:.0f}h',
                    'ROI_Hora': 'R$ {:,.2f}',
                    'Score_Performance': '{:.1f}'
                }))
        else:
            st.info("🎯 Sem dados disponíveis")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: FECHAMENTO (TELA 2 da Spec)
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown(f"## 💰 Painel de Fechamento - {mes_sel}/{ano_sel}")
    st.info("Esta visão compara o Contábil (Faturado/Custo) com o Caixa (Recebido/Pago). O Gap de 2025 será visível aqui.")

    col_pag, col_rec = st.columns(2)
    
    with col_pag:
        st.markdown("### 💸 A Pagar - Consultores")
        
        if not df_filtrado.empty:
            # Lógica da TELA 2: A Pagar (Agrupado por Consultor)
            apagar = df_filtrado.groupby('Consultor').agg(
                Horas_Trabalhadas=('Hrs_Real', 'sum'),
                Total_Custo_Contabil=('Custo', 'sum'),
                Total_Pago=('Caixa_Pago', 'sum')
            ).reset_index()
            
            apagar['Saldo_Pendente'] = apagar['Total_Custo_Contabil'] - apagar['Total_Pago']
            apagar = apagar.sort_values('Total_Custo_Contabil', ascending=False)
            
            st.dataframe(
                apagar[apagar['Total_Custo_Contabil'] > 0].style.format({
                    'Horas_Trabalhadas': '{:.0f}h',
                    'Total_Custo_Contabil': 'R$ {:,.2f}',
                    'Total_Pago': 'R$ {:,.2f}',
                    'Saldo_Pendente': 'R$ {:,.2f}'
                }),
                use_container_width=True,
                height=400
            )
            
            st.metric("Total Custo Contábil", f"R$ {apagar['Total_Custo_Contabil'].sum():,.2f}")
            st.metric("Total Efetivamente Pago", f"R$ {apagar['Total_Pago'].sum():,.2f}",
                      delta=f"R$ {apagar['Saldo_Pendente'].sum():,.2f} Pendente",
                      delta_color="inverse" if apagar['Saldo_Pendente'].sum() > 0 else "off")
            
    with col_rec:
        st.markdown("### 💳 A Receber - Clientes")
        
        if not df_filtrado.empty:
            # Lógica da TELA 2: A Receber (Agrupado por Cliente)
            areceber = df_filtrado.groupby('Cliente').agg(
                Horas_Faturadas=('Hrs_Real', 'sum'),
                Total_Faturado=('Receita', 'sum'),
                Total_Recebido=('Caixa_Recebido', 'sum')
            ).reset_index()
            
            areceber['Saldo_Pendente'] = areceber['Total_Faturado'] - areceber['Total_Recebido']
            areceber = areceber.sort_values('Total_Faturado', ascending=False)
            
            st.dataframe(
                areceber[areceber['Total_Faturado'] > 0].style.format({
                    'Horas_Faturadas': '{:.0f}h',
                    'Total_Faturado': 'R$ {:,.2f}',
                    'Total_Recebido': 'R$ {:,.2f}',
                    'Saldo_Pendente': 'R$ {:,.2f}'
                }),
                use_container_width=True,
                height=400
            )
            
            st.metric("Total Faturado (Contábil)", f"R$ {areceber['Total_Faturado'].sum():,.2f}")
            st.metric("Total Efetivamente Recebido", f"R$ {areceber['Total_Recebido'].sum():,.2f}",
                      delta=f"R$ {areceber['Saldo_Pendente'].sum():,.2f} Pendente",
                      delta_color="inverse" if areceber['Saldo_Pendente'].sum() > 0 else "off")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: FLUXO DE CAIXA (TELA 3 da Spec)
# ═══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown(f"## 💵 Fluxo de Caixa vs. Contábil - {mes_sel}/{ano_sel}")
    
    st.markdown("### Resumo de Caixa (Período Selecionado)")
    
    # KPIs da TELA 3
    col_c1, col_c2, col_c3 = st.columns(3)
    
    with col_c1:
        st.markdown("""
        <div class="metric-card-premium" style="border-left-color: #39FF14;">
            <h4 style="color: #39FF14;">VISÃO CAIXA</h4>
        """, unsafe_allow_html=True)
        st.metric("💰 Total Recebido", f"R$ {metricas['caixa_recebido']:,.2f}")
        st.metric("💸 Total Pago", f"R$ {metricas['caixa_pago']:,.2f}")
        st.metric("📊 Resultado Caixa", f"R$ {metricas['lucro_caixa']:,.2f}",
                  delta_color="normal" if metricas['lucro_caixa'] > 0 else "inverse")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_c2:
        st.markdown("""
        <div class="metric-card-premium" style="border-left-color: #00BFFF;">
            <h4 style="color: #00BFFF;">VISÃO CONTÁBIL</h4>
        """, unsafe_allow_html=True)
        st.metric("💰 Faturamento Contábil", f"R$ {metricas['receita']:,.2f}")
        st.metric("💸 Custo Contábil", f"R$ {metricas['custo']:,.2f}")
        st.metric("📊 Lucro Contábil", f"R$ {metricas['lucro']:,.2f}",
                  delta_color="normal" if metricas['lucro'] > 0 else "inverse")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_c3:
        st.markdown("""
        <div class="metric-card-premium" style="border-left-color: #FFD700;">
            <h4 style="color: #FFD700;">GAPS (Contábil - Caixa)</h4>
        """, unsafe_allow_html=True)
        st.metric("Gap de Recebimento", f"R$ {metricas['gap_faturamento']:,.2f}",
                  help="Quanto foi faturado mas ainda não recebido")
        st.metric("Gap de Pagamento", f"R$ {metricas['gap_custo']:,.2f}",
                  help="Quanto foi provisionado de custo mas ainda não pago")
        st.metric("Gap de Lucro", f"R$ {metricas['lucro'] - metricas['lucro_caixa']:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    if ano_sel >= 2025 and metricas['caixa_recebido'] == 0 and metricas['caixa_pago'] == 0:
        st.error("🚨 ATENÇÃO: Os dados de Caixa para 2025 estão zerados devido à quebra de ligação dos IDs. A análise de Caixa e Gaps está comprometida. Veja a aba 'IA Prescritiva'.")

    st.markdown("---")
    st.markdown("### Evolução Temporal (Caixa vs. Contábil)")
    
    # TELA 3: Evolução Temporal (Usando todos os dados, não apenas o filtrado)
    with st.spinner("Calculando evolução temporal..."):
        df_full = crq.dados_universo
        
        # Garantir que Data existe e não é NaT
        if 'Data' in df_full.columns and not df_full['Data'].isnull().all():
            df_full = df_full.dropna(subset=['Data'])
            
            fluxo_temporal = df_full.groupby(pd.Grouper(key='Data', freq='MS')).agg(
                Receita_Caixa=('Caixa_Recebido', 'sum'),
                Custo_Caixa=('Caixa_Pago', 'sum'),
                Receita_Contabil=('Receita', 'sum'),
                Custo_Contabil=('Custo', 'sum')
            ).reset_index()
            
            fluxo_temporal['Lucro_Caixa'] = fluxo_temporal['Receita_Caixa'] - fluxo_temporal['Custo_Caixa']
            fluxo_temporal['Lucro_Contabil'] = fluxo_temporal['Receita_Contabil'] - fluxo_temporal['Custo_Contabil']
            
            fig_evolucao = go.Figure()
            
            fig_evolucao.add_trace(go.Scatter(
                x=fluxo_temporal['Data'], y=fluxo_temporal['Lucro_Contabil'],
                name='Lucro Contábil', mode='lines+markers',
                line=dict(color='#00BFFF', width=4)
            ))
            fig_evolucao.add_trace(go.Scatter(
                x=fluxo_temporal['Data'], y=fluxo_temporal['Lucro_Caixa'],
                name='Lucro Caixa', mode='lines+markers',
                line=dict(color='#39FF14', width=2, dash='dot')
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
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                hovermode='x unified',
                legend=dict(orientation='h', y=1.1),
                height=450,
                xaxis_title='Período',
                yaxis_title='Valor (R$)'
            )
            st.plotly_chart(fig_evolucao, use_container_width=True)
        else:
            st.warning("Não foi possível gerar gráfico temporal. Verifique coluna 'Data'.")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: ANÁLISE PROFUNDA (TELA 4 da Spec)
# ═══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown(f"## 🔬 Análise Profunda - {mes_sel}/{ano_sel}")
    
    st.markdown("### 🩸 Detecção de Sangria (Projetos Fechados com Overrun)")
    
    if not df_filtrado.empty:
        # TELA 4: Detecção de Sangria
        
        # O nome do tipo de projeto pode variar. Vamos ser flexíveis.
        tipo_fechado = "PROJETO FECHADO"
        if tipo_fechado not in df_filtrado['TipoProj'].unique():
             # Tenta achar um nome similar se o nome exato falhar
             tipos_proj = df_filtrado['TipoProj'].unique()
             matches = [t for t in tipos_proj if "FECHADO" in t.upper()]
             if matches:
                 tipo_fechado = matches[0]
                 st.info(f"Usando tipo de projeto '{tipo_fechado}' para análise de sangria.")
             else:
                 st.warning("Não foi possível encontrar o tipo 'PROJETO FECHADO' nos dados.")
                 tipo_fechado = None

        if tipo_fechado:
            df_sangria = df_filtrado[
                (df_filtrado['TipoProj'] == tipo_fechado) & 
                (df_filtrado['Hrs_Real'] > df_filtrado['Hrs_Prev']) &
                (df_filtrado['Hrs_Prev'] > 0) # Evitar divisão por zero
            ]
            
            if not df_sangria.empty:
                df_sangria = df_sangria.copy() # Evitar SettingWithCopyWarning
                df_sangria['Desvio_Horas'] = df_sangria['Hrs_Real'] - df_sangria['Hrs_Prev']
                df_sangria['Perc_Sangria'] = (df_sangria['Desvio_Horas'] / df_sangria['Hrs_Prev']) * 100
                
                df_sangria_view = df_sangria[[
                    'Consultor', 'Cliente', 'Projeto', 'Hrs_Prev', 'Hrs_Real', 
                    'Desvio_Horas', 'Perc_Sangria', 'Receita', 'Custo', 'Lucro', 'Margem'
                ]].sort_values('Desvio_Horas', ascending=False)
                
                st.error(f"Identificados {len(df_sangria_view)} projetos fechados com estouro de horas (sangria).")
                
                st.dataframe(df_sangria_view.style.format({
                    'Hrs_Prev': '{:.0f}h',
                    'Hrs_Real': '{:.0f}h',
                    'Desvio_Horas': '+{:.0f}h',
                    'Perc_Sangria': '{:.1f}%',
                    'Receita': 'R$ {:,.2f}',
                    'Custo': 'R$ {:,.2f}',
                    'Lucro': 'R$ {:,.2f}',
                    'Margem': '{:.1%}'
                }).background_gradient(cmap='Reds', subset=['Desvio_Horas', 'Perc_Sangria'])
                  .background_gradient(cmap='RdYlGn', subset=['Lucro', 'Margem']))
            else:
                st.success("✅ Nenhum projeto fechado com estouro de horas detectado neste período.")
        else:
            st.warning("Não foi possível executar a análise de sangria (tipo de projeto não encontrado).")

    st.markdown("---")
    st.markdown("### 🎯 Matriz de Correlação (Entrelaçamento Quântico)")
    
    if not df_filtrado.empty and len(df_filtrado) > 3:
        cols_analise = ['Hrs_Real', 'Hrs_Prev', 'Receita', 'Custo', 'Lucro', 'Margem', 'Eficiencia', 'ROI_Hora']
        df_corr = df_filtrado[cols_analise].corr()
        
        fig_corr = px.imshow(
            df_corr,
            text_auto='.2f',
            aspect='auto',
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1
        )
        
        fig_corr.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=500
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.info("""
        **🧠 Interpretação da Matriz:**
        - Valores próximos a **+1**: Correlação positiva forte (variáveis crescem juntas)
        - Valores próximos a **-1**: Correlação negativa forte (inversamente proporcionais)
        - Valores próximos a **0**: Sem correlação significativa
        """)
    else:
        st.warning("📊 Dados insuficientes para análise de correlação (mínimo 3 registros)")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5: IA PRESCRITIVA (Copiado do seu layout)
# ═══════════════════════════════════════════════════════════════════════════════

with tab5:
    st.markdown("## 🧠 Inteligência Prescritiva Ativa")
    
    if ia_ativa and prescricoes:
        st.success(f"✅ **CRQ Online** - {len(prescricoes)} prescrições geradas")
        
        # Filtro de prioridade
        prioridades = ['TODAS'] + list(set([p['prioridade'] for p in prescricoes]))
        filtro_prior = st.selectbox("Filtrar por Prioridade", prioridades)
        
        prescricoes_filtradas = prescricoes if filtro_prior == 'TODAS' else [p for p in prescricoes if p['prioridade'] == filtro_prior]
        
        for i, presc in enumerate(prescricoes_filtradas):
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
                          color: {cor_prior.get(presc['prioridade'], '#8A8A8A')}; border: 1px solid {cor_prior.get(presc['prioridade'], '#8A8A8A')};
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
                    <div>
                        <span style="color: #39FF14;">💰 Impacto:</span> 
                        <strong>{presc['impacto_estimado']}</strong>
                    </div>
                    <div>
                        <span style="color: #FFD700;">📈 Confiança:</span> 
                        <strong>{presc['confianca']}%</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.progress(presc['confianca'] / 100)
            st.markdown("<br>", unsafe_allow_html=True)
            
    elif not ia_ativa:
        st.info("🔧 IA Prescritiva desativada. Ative na sidebar para análises avançadas.")
    else:
        st.warning("⚠️ Nenhuma prescrição gerada. Ajuste os filtros para análise.")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6: CONSULTOR SOCRÁTICO (TELA 5 da Spec / Copiado do seu layout)
# ═══════════════════════════════════════════════════════════════════════════════

with tab6:
    st.markdown("## 🤔 Consultor Socrático - As Perguntas Que Importam")
    
    st.markdown("""
    <div class="insight-premium">
        <h3 style="margin-top: 0;">💭 O Método Socrático Aplicado aos Negócios</h3>
        <p style="font-size: 1.05em; line-height: 1.6;">
            Este não é um sistema que apenas mostra números. É um <strong>parceiro de sabedoria</strong> 
            que faz as perguntas certas para guiá-lo à descoberta de insights profundos sobre seu negócio.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not df_filtrado.empty:
        with st.spinner('🧠 Analisando profundamente seus dados e gerando perguntas estratégicas...'):
            perguntas = socratic.gerar_perguntas_estrategicas()
        
        categorias_disponiveis = list(set([p['categoria'] for p in perguntas]))
        categoria_filtro = st.multiselect(
            "Filtrar por categoria:",
            ['TODAS'] + categorias_disponiveis,
            default=['TODAS']
        )
        
        if 'TODAS' not in categoria_filtro and categoria_filtro:
            perguntas_filtradas = [p for p in perguntas if p['categoria'] in categoria_filtro]
        else:
            perguntas_filtradas = perguntas
        
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
        
        if perguntas_filtradas:
            for i, pergunta in enumerate(perguntas_filtradas, 1):
                if pergunta['profundidade'] == 'CRÍTICA':
                    card_class = 'alert-premium'
                    cor_badge = '#FF4500'
                elif pergunta['profundidade'] == 'ESTRATÉGICA':
                    card_class = 'insight-premium'
                    cor_badge = '#FFD700'
                else:
                    card_class = 'success-premium'
                    cor_badge = '#00BFFF'
                
                st.markdown(f"""
                <div class="{card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 2em;">{pergunta['icone']}</span>
                            <span style="background: {cor_badge}30; color: {cor_badge}; padding: 4px 12px; 
                                  border-radius: 12px; font-size: 0.85em; font-weight: 600; border: 1px solid {cor_badge};">
                                {pergunta['categoria']}
                            </span>
                        </div>
                    </div>
                    
                    <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 12px; 
                                border-left: 4px solid {cor_badge}; margin: 15px 0;">
                        <p style="font-size: 1.15em; line-height: 1.7; margin: 0; font-weight: 500;">
                            {pergunta['pergunta']}
                        </p>
                    </div>
                    
                    <div style="background: rgba(0,191,255,0.05); padding: 15px; border-radius: 10px; 
                                margin-top: 15px; border-left: 3px solid #00BFFF;">
                        <p style="margin: 0; font-size: 0.95em; color: #8A8A8A
