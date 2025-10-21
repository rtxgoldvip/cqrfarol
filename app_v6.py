# -*- coding: utf-8 -*-

# --- Importações Essenciais ---
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
import re # Biblioteca para processamento de linguagem natural (regex)

# Tenta importar a biblioteca do banco de dados
try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False
    st.error("Biblioteca pyodbc não encontrada. Por favor, adicione 'pyodbc' ao seu arquivo requirements.txt")

warnings.filterwarnings('ignore')

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="MAESTRO QUÂNTICO - Inteligência Preditiva",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILO CSS AVANÇADO (PREMIUM) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Poppins', sans-serif; }
    .main { background-color: #050818; color: #E0E0E0; }
    .stApp { background: radial-gradient(circle at top right, #1a1a2e 0%, #050818 50%); }
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #00BFFF, #8A2BE2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    .metric-card, .insight-card, .alert-card, .success-card {
        background: rgba(28, 28, 40, 0.7);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(0, 191, 255, 0.2);
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 191, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
    .metric-card { border-left: 5px solid #00BFFF; }
    .insight-card { border-left: 5px solid #FFD700; } /* Oportunidade */
    .alert-card { border-left: 5px solid #FF4500; } /* Alerta */
    .success-card { border-left: 5px solid #39FF14; } /* Sucesso */
    .st-emotion-cache-16txtl3 {
        background-color: rgba(10, 8, 24, 0.9);
        border-right: 1px solid rgba(0, 191, 255, 0.2);
    }
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #00BFFF;
        background-color: transparent;
        color: #00BFFF;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #00BFFF;
        color: #050818;
        box-shadow: 0 0 15px #00BFFF;
    }
    .stButton>button:active { background-color: #0077CC !important; }
</style>
""", unsafe_allow_html=True)


# --- NÚCLEO DE CONEXÃO COM O BANCO DE DADOS ---
class DatabaseConnector:
    def __init__(self):
        try:
            self.server = st.secrets["database"]["server"]
            self.database = st.secrets["database"]["database"]
            self.username = st.secrets["database"]["username"]
            self.password = st.secrets["database"]["password"]
            self.SECRETS_AVAILABLE = True
        except Exception as e:
            self.SECRETS_AVAILABLE = False
            # Não exiba o erro aqui ainda, o load_data vai cuidar disso
        
        self.conn = None
        
    def connect(self):
        if not PYODBC_AVAILABLE:
            return False # Driver não encontrado
            
        if not self.SECRETS_AVAILABLE:
            return False # Segredos não configurados
            
        try:
            conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
            self.conn = pyodbc.connect(conn_str, timeout=5)
            return True
        except Exception as e:
            st.sidebar.error(f"Falha na conexão com o banco. Erro: {e}", icon="❌")
            return False

    def get_data(self):
        query = """
        SELECT
            g.IdGest2, CAST(g.Mes as INT) as Mes, CAST(g.Ano as INT) as Ano,
            g.ConsultGest, g.ProjGest,
            g.QtHrOrc as Horas_Previstas, g.QtHrReal as Horas_Realizadas,
            g.VlHrOrc as Valor_Hora_Venda_Orc, g.VlHrCusto as Valor_Hora_Custo,
            g.ReceitaOrc, g.ReceitaReal as Receita_Total,
            g.CustoOrc, g.CustoReal as Custo_Total,
            g.VlMgOrc, g.VlMgReal as Lucro_Total_Contabil,
            g.PercMgOrc, g.PercMgReal as Margem_Percentual,
            
            p.DescProj as Projeto, p.CodCliProj,
            t.DescTipo as TipoProj,
            tec.NomeTec as Consultor,
            cli.DescCli as Cliente
        FROM Tb_GestorFin2 g
        LEFT JOIN tb_Proj p ON g.ProjGest = p.AutNumProj
        LEFT JOIN tb_tipoproj t ON p.TipoProj = t.AutNumTipo
        LEFT JOIN tb_tec tec ON g.ConsultGest = tec.AutNumTec
        LEFT JOIN tb_cli cli ON p.CodCliProj = cli.AutNumCli
        WHERE tec.NomeTec IS NOT NULL AND p.DescProj IS NOTNOT NULL
        """
        try:
            df = pd.read_sql(query, self.conn)
            return df
        except Exception as e:
            st.error(f"Erro ao buscar dados: {e}")
            return pd.DataFrame() # Retorna DF vazio em caso de erro na query

    def close(self):
        if self.conn:
            self.conn.close()

# --- MOTOR DE ANÁLISE QUÂNTICO ---
class QuantumAnalyticsEngine:
    def __init__(self):
        self.dados_originais = self.load_data()
        self.dados_filtrados = self.dados_originais.copy()

    # --- CORREÇÃO 1: Decorador @st.cache_data removido daqui ---
    def load_data(self):
        db = DatabaseConnector()
        
        if db.connect():
            df = db.get_data()
            db.close()
            
            if not df.empty:
                st.sidebar.success(f"Conectado! {len(df)} registros carregados.", icon="✅")
            else:
                st.sidebar.success("Conectado! O banco de dados não retornou registros.", icon="ℹ️")
            
            return self._processar_dados(df)
        
        if not db.SECRETS_AVAILABLE:
            st.sidebar.error("Secrets não configurados. Usando dados de simulação.")
        else:
            st.sidebar.warning("Conexão falhou. Usando dados de simulação.", icon="🔌")
            
        st.toast("Usando dados de simulação interna.", icon="🔬")
        return self._processar_dados(self._create_mock_data())

    def _processar_dados(self, df):
        if df.empty:
            return df
            
        numeric_cols = ['Horas_Previstas', 'Horas_Realizadas', 'Valor_Hora_Venda_Orc', 'Valor_Hora_Custo',
                        'Receita_Total', 'Custo_Total', 'Margem_Percentual', 'Lucro_Total_Contabil']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        if 'Lucro_Total_Contabil' in df.columns:
            df['Lucro_Total'] = df['Lucro_Total_Contabil']
        else:
            df['Lucro_Total'] = df['Receita_Total'] - df['Custo_Total']
        
        df['Horas_Realizadas_Calc'] = df['Horas_Realizadas'].replace(0, 1)
        df['Horas_Previstas_Calc'] = df['Horas_Previstas'].replace(0, 1)
        
        df['Desvio_Horas'] = df['Horas_Realizadas'] - df['Horas_Previstas']
        df['Eficiencia_Horas'] = (df['Horas_Realizadas'] / df['Horas_Previstas_Calc']) * 100
        df['Rentabilidade_Hora'] = df['Lucro_Total'] / df['Horas_Realizadas_Calc']
        
        df.replace([np.inf, -np.inf], 0, inplace=True)
        return df

    def _create_mock_data(self):
        data = {
            'Mes': [1, 1, 1, 2, 2, 2, 3, 3, 3, 3],
            'Ano': [2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025],
            'Consultor': ['RAFAEL OLIVEIRA', 'CLEBER NEVES', 'ADRIANO AFONSO', 'RAFAEL OLIVEIRA', 'CLEBER NEVES', 'THIAGO MILANÊS', 'ADRIANO AFONSO', 'CLEBER NEVES', 'RAFAEL OLIVEIRA', 'THIAGO MILANÊS'],
            'Cliente': ['AUTOZONE', 'TOTVS NOROESTE', 'HYDAC', 'AUTOZONE', 'TBC', 'Investimento', 'HYDAC', 'TOTVS NOROESTE', 'TOTVS IP', 'TBC'],
            'Projeto': ['ALOCAÇÃO DE PMO', 'ALOCAÇÃO BODY SHOP', 'PROJETO FECHADO', 'ALOCAÇÃO DE PMO', 'ALOCAÇÃO BODYSHOP', 'DESENV. INTERNO', 'PROJETO FECHADO', 'MIGRAÇÃO DADOS', 'PROJETO FECHADO', 'ALOCAÇÃO BODYSHOP'],
            'TipoProj': ['Horas Realizadas', 'Horas Realizadas', 'Projeto Fechado', 'Horas Realizadas', 'Horas Realizadas', 'INTERNO', 'Projeto Fechado', 'Projeto Fechado', 'Projeto Fechado', 'Horas Realizadas'],
            'Horas_Previstas': [160, 160, 100, 160, 80, 40, 100, 50, 120, 80],
            'Horas_Realizadas': [172, 160, 125, 155, 95, 48, 85, 55, 140, 90],
            'Receita_Total': [20640, 18400, 15000, 18600, 10450, 0, 15000, 5750, 15600, 9900],
            'Custo_Total': [11180, 9600, 8750, 10075, 5225, 3360, 5950, 3300, 9100, 4950],
            'Margem_Percentual': [45.8, 47.8, 41.7, 45.8, 50.0, -100.0, 60.3, 42.6, 41.7, 50.0]
        }
        return pd.DataFrame(data)

    def aplicar_filtros(self, mes, ano, consultores, clientes, projetos):
        df = self.dados_originais.copy()
        if not df.empty:
            if mes != "TODOS": df = df[df['Mes'] == mes]
            if ano != "TODOS": df = df[df['Ano'] == ano]
            if "TODOS" not in consultores: df = df[df['Consultor'].isin(consultores)]
            if "TODOS" not in clientes: df = df[df['Cliente'].isin(clientes)]
            if "TODOS" not in projetos: df = df[df['Projeto'].isin(projetos)]
        self.dados_filtrados = df
        return df

    def gerar_insights_prescritivos(self):
        df = self.dados_filtrados
        if df.empty:
            return [{'tipo': 'info', 'texto': 'Nenhum dado encontrado para os filtros selecionados. A superposição está vazia.'}]
        
        insights = []
        
        media_eficiencia = df['Eficiencia_Horas'].mean()
        if media_eficiencia > 115:
            proj_maior_desvio = df.loc[df['Desvio_Horas'].idxmax()]
            insights.append({
                'tipo': 'alerta',
                'texto': f"**Interferência Destrutiva (Risco):** A eficiência média de horas está em **{media_eficiencia:.1f}%**, indicando subestimação crônica. O projeto '{proj_maior_desvio['Projeto']}' com o consultor '{proj_maior_desvio['Consultor']}' estourou em **{proj_maior_desvio['Desvio_Horas']:.0f} horas**. **Prescrição:** Revisar o processo de escopo para projetos similares a este."
            })
        elif media_eficiencia < 85:
             insights.append({
                'tipo': 'oportunidade',
                'texto': f"**Potencial Oculto:** A eficiência média de horas está em **{media_eficiencia:.1f}%**. Há capacidade ociosa na equipe. **Prescrição:** Avaliar a alocação de novos projetos ou treinamentos para maximizar a produtividade."
            })

        rentab_media = df['Rentabilidade_Hora'].mean()
        df_rentavel = df[df['Rentabilidade_Hora'] > 0]
        if not df_rentavel.empty:
            consultor_mais_rentavel = df_rentavel.loc[df_rentavel['Rentabilidade_Hora'].idxmax()]
            insights.append({
                'tipo': 'sucesso',
                'texto': f"**Ressonância da Verdade:** O consultor **{consultor_mais_rentavel['Consultor']}** está gerando **R$ {consultor_mais_rentavel['Rentabilidade_Hora']:.2f}/hora** no projeto '{consultor_mais_rentavel['Projeto']}', um valor significativamente acima da média de R$ {rentab_media:.2f}/hora. **Prescrição:** Entender as práticas deste consultor para replicar em toda a equipe."
            })
        
        df_margem = df[df['Margem_Percentual'] > 0]
        if not df_margem.empty:
            cliente_menor_margem = df_margem.loc[df_margem['Margem_Percentual'].idxmin()]
            if cliente_menor_margem['Margem_Percentual'] < 35:
                insights.append({
                    'tipo': 'alerta',
                    'texto': f"**Entrelaçamento Crítico:** O cliente **{cliente_menor_margem['Cliente']}** apresenta a menor margem de lucro positiva (**{cliente_menor_margem['Margem_Percentual']:.1f}%**). O custo e a receita estão em um entrelaçamento desfavorável. **Prescrição:** Renegociar valores ou otimizar a alocação de custos para este cliente."
                })

        return insights if insights else [{'tipo': 'info', 'texto': 'A orquestra está em harmonia. Todos os indicadores estão dentro dos parâmetros esperados para a seleção atual.'}]

# --- PROCESSADOR DE COMANDOS DE VOZ (SIMULADO) ---
class VoiceCommandProcessor:
    def process(self, command):
        command = command.lower().strip()
        
        if re.search(r"mostrar|abrir|ir para a aba (.*)", command):
            match = re.search(r"mostrar|abrir|ir para a aba (.*)", command)
            tab_name = match.group(1).strip()
            tabs_map = {
                "visão geral": "Visão Geral (Orquestra)", "orquestra": "Visão Geral (Orquestra)",
                "análise profunda": "Análise Profunda (Ressonância)", "ressonância": "Análise Profunda (Ressonância)",
                "consultores": "Consultores & Projetos",
                "simulador": "Simulador Quântico",
                "fechamento": "Fechamento & Financeiro",
                "assistente": "Assistente IA (Maestro)"
            }
            if tab_name in tabs_map:
                st.session_state.active_tab = tabs_map[tab_name]
                return f"Navegando para a aba '{tabs_map[tab_name]}'."
            return f"Não encontrei a aba '{tab_name}'."
        
        return "Comando não compreendido. Tente 'mostrar a aba consultores' ou 'limpar filtros'."

# --- INICIALIZAÇÃO E CACHE ---
# --- CORREÇÃO 2: Usar @st.cache_resource para criar o engine ---
@st.cache_resource
def init_engine():
    """Cria e cacheia a instância principal do motor de análise."""
    return QuantumAnalyticsEngine()

engine = init_engine()
voice_processor = VoiceCommandProcessor()

# --- LÓGICA DE FILTROS (com st.session_state) ---
if 'filtros_aplicados' not in st.session_state:
    st.session_state.filtros_aplicados = {
        "ano": "TODOS",
        "mes": "TODOS",
        "consultores": ["TODOS"],
        "clientes": ["TODOS"],
        "projetos": ["TODOS"]
    }

# --- INTERFACE PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>MAESTRO QUÂNTICO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8A8A8A; margin-top: -10px;'>Inteligência Preditiva para Gestão de Consultoria</p>", unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR DE CONTROLES (LÓGICA DO BOTÃO) ---
with st.sidebar:
    st.markdown("## 🌌 Controles da Orquestra")
    st.markdown("Filtre a superposição de dados para revelar a realidade desejada.")

    dados_disponiveis = engine.dados_originais
    
    anos = sorted(dados_disponiveis['Ano'].unique().tolist()) if not dados_disponiveis.empty else []
    meses = sorted(dados_disponiveis['Mes'].unique().tolist()) if not dados_disponiveis.empty else []
    consultores = sorted(dados_disponiveis['Consultor'].unique().tolist()) if not dados_disponiveis.empty else []
    clientes = sorted(dados_disponiveis['Cliente'].unique().tolist()) if not dados_disponiveis.empty else []
    projetos = sorted(dados_disponiveis['Projeto'].unique().tolist()) if not dados_disponiveis.empty else []

    st.selectbox("Ano", ["TODOS"] + anos, 
                 key="filtro_ano", 
                 default=st.session_state.filtros_aplicados["ano"])
    st.selectbox("Mês", ["TODOS"] + meses, 
                 key="filtro_mes", 
                 default=st.session_state.filtros_aplicados["mes"])
    st.multiselect("Consultores", ["TODOS"] + consultores, 
                   key="filtro_consultores", 
                   default=st.session_state.filtros_aplicados["consultores"])
    st.multiselect("Clientes", ["TODOS"] + clientes, 
                   key="filtro_clientes", 
                   default=st.session_state.filtros_aplicados["clientes"])
    st.multiselect("Projetos", ["TODOS"] + projetos, 
                   key="filtro_projetos", 
                   default=st.session_state.filtros_aplicados["projetos"])

    if st.button("Aplicar Filtros", use_container_width=True, type="primary"):
        st.session_state.filtros_aplicados = {
            "ano": st.session_state.filtro_ano,
            "mes": st.session_state.filtro_mes,
            "consultores": st.session_state.filtro_consultores,
            "clientes": st.session_state.filtro_clientes,
            "projetos": st.session_state.filtro_projetos
        }
        st.rerun()

    st.markdown("---")
    st.info("Desenvolvido por Jefferson de Souza em parceria com a IA Gemini da Google.", icon="💡")


# --- APLICAÇÃO DOS FILTROS ---
df_filtrado = engine.aplicar_filtros(
    st.session_state.filtros_aplicados["mes"],
    st.session_state.filtros_aplicados["ano"],
    st.session_state.filtros_aplicados["consultores"],
    st.session_state.filtros_aplicados["clientes"],
    st.session_state.filtros_aplicados["projetos"]
)

# Calcula KPIs GLOBAIS
if not df_filtrado.empty:
    kpis = {
        'receita_total': df_filtrado['Receita_Total'].sum(),
        'lucro_total': df_filtrado['Lucro_Total'].sum(),
        'margem_media': df_filtrado[df_filtrado['Lucro_Total']>0]['Margem_Percentual'].mean() if not df_filtrado[df_filtrado['Lucro_Total']>0].empty else 0,
        'eficiencia_media': df_filtrado['Eficiencia_Horas'].mean()
    }
else:
    kpis = {'receita_total': 0, 'lucro_total': 0, 'margem_media': 0, 'eficiencia_media': 0}


# --- ABAS DE NAVEGAÇÃO ---
tab_names = [
    "Visão Geral (Orquestra)", "Análise Profunda (Ressonância)", 
    "Consultores & Projetos", "Simulador Quântico", 
    "Fechamento & Financeiro", "Assistente IA (Maestro)"
]

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = tab_names[0]
if st.session_state.active_tab not in tab_names:
    st.session_state.active_tab = tab_names[0]

active_tab_index = tab_names.index(st.session_state.active_tab)
tabs = st.tabs([f"**{name}**" for name in tab_names])

# --- CONTEÚDO DAS ABAS ---

# Tab 1: Visão Geral
with tabs[0]:
    st.subheader("Primeiro Movimento: A Superposição de Resultados")
    
    if df_filtrado.empty:
        st.warning("Nenhum dado para exibir com os filtros atuais.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Receita Total", f"R$ {kpis['receita_total']:,.2f}")
        with col2:
            st.metric("Lucro Total", f"R$ {kpis['lucro_total']:,.2f}")
        with col3:
            st.metric("Margem Média", f"{kpis['margem_media']:.1f}%")
        with col4:
            st.metric("Eficiência de Horas", f"{kpis['eficiencia_media']:.1f}%")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Receita por Cliente (Top 5)")
            receita_cliente = df_filtrado.groupby('Cliente')['Receita_Total'].sum().nlargest(5)
            fig = px.pie(receita_cliente, values='Receita_Total', names=receita_cliente.index, hole=0.5,
                         color_discrete_sequence=px.colors.sequential.Plasma_r)
            fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Lucro por Tipo de Projeto")
            lucro_tipo = df_filtrado.groupby('TipoProj')['Lucro_Total'].sum()
            fig = px.bar(lucro_tipo, x=lucro_tipo.index, y='Lucro_Total', color='Lucro_Total',
                         color_continuous_scale=px.colors.sequential.Viridis)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)

# Tab 2: Análise Profunda
with tabs[1]:
    st.subheader("Segundo Movimento: O Entrelaçamento dos Dados")
    if df_filtrado.empty:
        st.warning("Nenhum dado para exibir com os filtros atuais.")
    else:
        st.markdown("#### Correlação entre Métricas Chave")
        corr_df = df_filtrado[['Receita_Total', 'Custo_Total', 'Lucro_Total', 'Horas_Realizadas', 'Margem_Percentual', 'Eficiencia_Horas']].corr()
        fig = px.imshow(corr_df, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', title="Mapa de Calor: Fatores Entrelaçados")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Matriz Risco vs. Recompensa (Projeto)")
        st.info("Ainda não temos dados de 'Atraso' na query principal. Usando 'Desvio de Horas' como proxy para Risco.")
        fig_scatter = px.scatter(df_filtrado, x='Desvio_Horas', y='Margem_Percentual', 
                                 color='TipoProj', hover_data=['Projeto', 'Consultor', 'Cliente'],
                                 title="Margem (%) vs. Desvio de Horas (Risco)")
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig_scatter, use_container_width=True)

# Tab 3: Consultores & Projetos
with tabs[2]:
    st.subheader("Performance Individual e de Projetos")
    if df_filtrado.empty:
        st.warning("Nenhum dado para exibir com os filtros atuais.")
    else:
        st.markdown("#### Análise por Consultor")
        df_consultor = df_filtrado.groupby('Consultor').agg(
            Receita_Total=('Receita_Total', 'sum'),
            Custo_Total=('Custo_Total', 'sum'),
            Lucro_Total=('Lucro_Total', 'sum'),
            Horas_Previstas=('Horas_Previstas', 'sum'),
            Horas_Realizadas=('Horas_Realizadas', 'sum'),
            Margem_Média=('Margem_Percentual', 'mean'),
            Eficiência_Média=('Eficiencia_Horas', 'mean')
        ).reset_index()
        
        df_consultor['Desvio_Horas'] = df_consultor['Horas_Realizadas'] - df_consultor['Horas_Previstas']
        
        st.dataframe(df_consultor.style.format({
            "Receita_Total": "R$ {:,.2f}", "Custo_Total": "R$ {:,.2f}", "Lucro_Total": "R$ {:,.2f}", 
            "Margem_Média": "{:.1f}%", "Eficiência_Média": "{:.1f}%",
            "Horas_Previstas": "{:,.0f}h", "Horas_Realizadas": "{:,.0f}h", "Desvio_Horas": "{:,.0f}h"
        }), use_container_width=True)
        
        st.markdown("#### Detalhamento por Projeto")
        st.dataframe(df_filtrado[['Projeto', 'Cliente', 'Consultor', 'Receita_Total', 'Custo_Total', 'Lucro_Total', 'Margem_Percentual', 'Horas_Previstas', 'Horas_Realizadas', 'Desvio_Horas']]
                     .style.format({
                         "Receita_Total": "R$ {:,.2f}", "Custo_Total": "R$ {:,.2f}", "Lucro_Total": "R$ {:,.2f}", 
                         "Margem_Percentual": "{:.1f}%", "Horas_Previstas": "{:,.0f}h", "Horas_Realizadas": "{:,.0f}h", "Desvio_Horas": "{:,.0f}h"
                     }), use_container_width=True)

# Tab 4: Simulador Quântico
with tabs[3]:
    st.subheader("Terceiro Movimento: A Interferência - Moldando o Futuro")
    st.write("Simule cenários para encontrar a ressonância da verdade antes de tomar decisões.")
    
    st.info("Este simulador é uma ferramenta 'what-if' para um *único* cenário de alocação.")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("##### Parâmetros do Cenário")
        horas_sim = st.slider("Horas Previstas", 10, 200, 160)
        venda_hora_sim = st.slider("Valor Hora Venda (R$)", 50, 250, 120)
        custo_hora_sim = st.slider("Valor Hora Custo (R$)", 30, 150, 65)
        eficiencia_sim = st.slider("Eficiência de Horas Esperada (%)", 80, 120, 100)
    
    with c2:
        st.markdown("##### Resultado Potencial")
        horas_real_sim = horas_sim * (eficiencia_sim / 100)
        receita_sim = horas_real_sim * venda_hora_sim
        custo_sim = horas_real_sim * custo_hora_sim
        lucro_sim = receita_sim - custo_sim
        margem_sim = (lucro_sim / receita_sim) * 100 if receita_sim > 0 else 0
        
        m1, m2 = st.columns(2)
        m1.metric("Receita Projetada", f"R$ {receita_sim:,.2f}")
        m1.metric("Lucro Projetado", f"R$ {lucro_sim:,.2f}")
        m2.metric("Custo Projetado", f"R$ {custo_sim:,.2f}")
        m2.metric("Margem Projetada", f"{margem_sim:.1f}%")

# Tab 5: Fechamento
with tabs[4]:
    st.subheader("Painel de Fechamento (Visão Contábil)")
    
    st.info("""
    Esta é a visão **Contábil** (baseada em `Tb_GestorFin2` - Receita e Custo).
    A visão **Caixa** (baseada em `Contas Receber` e `Contas Pagar`) será implementada
    para analisar o "Gap de Faturamento" e o fluxo de caixa real.
    """)
    
    if df_filtrado.empty:
        st.warning("Nenhum dado para exibir com os filtros atuais.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 💰 A Pagar (Custo dos Consultores)")
            df_pagar = df_filtrado.groupby('Consultor').agg(
                Custo_Total=('Custo_Total', 'sum'),
                Horas_Trabalhadas=('Horas_Realizadas', 'sum')
            ).sort_values('Custo_Total', ascending=False).reset_index()
            st.dataframe(df_pagar.style.format({"Custo_Total": "R$ {:,.2f}", "Horas_Trabalhadas": "{:,.0f}h"}), use_container_width=True)
        with c2:
            st.markdown("#### 💳 A Faturar (Receita dos Clientes)")
            df_receber = df_filtrado.groupby('Cliente').agg(
                Receita_Total=('Receita_Total', 'sum'),
                Horas_Faturadas=('Horas_Realizadas', 'sum')
            ).sort_values('Receita_Total', ascending=False).reset_index()
            st.dataframe(df_receber.style.format({"Receita_Total": "R$ {:,.2f}", "Horas_Faturadas": "{:,.0f}h"}), use_container_width=True)

# Tab 6: Assistente IA
with tabs[5]:
    st.header("O Maestro: Sua Interface com o Universo Quântico")
    
    st.subheader("💡 Feed de Prescrições Vivas")
    st.markdown("Insights gerados a partir da configuração atual dos dados.")
    
    insights_gerados = engine.gerar_insights_prescritivos()
    for insight in insights_gerados:
        card_class = {"alerta": "alert-card", "oportunidade": "insight-card", "sucesso": "success-card"}.get(insight['tipo'], "metric-card")
        icon = {"alerta": "🚨", "oportunidade": "🎯", "sucesso": "🏆"}.get(insight['tipo'], "ℹ️")
        st.markdown(f'<div class="{card_class}">{icon} {insight["texto"]}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🎤 Fale com o Maestro (Protótipo)")
    st.write("Digite um comando em linguagem natural para interagir com o sistema.")
    comando_usuario = st.text_input("Seu comando:", placeholder="Ex: 'mostrar a aba de consultores'")
    
    if comando_usuario:
        with st.spinner("Processando seu comando..."):
            resposta = voice_processor.process(comando_usuario)
            st.success(resposta)
            if "Navegando" in resposta:
                st.rerun()
