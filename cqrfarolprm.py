# -*- coding: utf-8 -*-
# MAESTRO QUÂNTICO v2.0 - A Sinfonia Completa

# --- Importações Essenciais ---
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings

try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False

warnings.filterwarnings('ignore')

# --- CONFIGURAÇÃO DA PÁGINA PREMIUM ---
st.set_page_config(
    page_title="MAESTRO QUÂNTICO - Inteligência Preditiva",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILO CSS AVANÇADO ---
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
        background: rgba(28, 28, 40, 0.7); border-radius: 15px; padding: 25px;
        border: 1px solid rgba(0, 191, 255, 0.2); margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 191, 255, 0.1); backdrop-filter: blur(10px);
    }
    .metric-card { border-left: 5px solid #00BFFF; }
    .insight-card { border-left: 5px solid #FFD700; }
    .alert-card { border-left: 5px solid #FF4500; }
    .success-card { border-left: 5px solid #39FF14; }
    .st-emotion-cache-16txtl3 { background-color: rgba(10, 8, 24, 0.9); border-right: 1px solid rgba(0, 191, 255, 0.2); }
</style>
""", unsafe_allow_html=True)


# --- NÚCLEO DE CONEXÃO E EXTRAÇÃO DE DADOS ---
class DataOrchestrator:
    def __init__(self):
        self.conn_str = self._get_conn_str()

    def _get_conn_str(self):
        try:
            return (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={st.secrets['db_credentials']['server']};"
                f"DATABASE={st.secrets['db_credentials']['database']};"
                f"UID={st.secrets['db_credentials']['username']};"
                f"PWD={st.secrets['db_credentials']['password']};"
                f"TrustServerCertificate=yes;"
            )
        except (KeyError, FileNotFoundError):
            return None

    def get_data(self):
        if not PYODBC_AVAILABLE or not self.conn_str:
            return None
        
        super_query = """
        SELECT
            g.IdGest2, CAST(g.Mes as INT) as Mes, CAST(g.Ano as INT) as Ano,
            g.QtHrOrc as Horas_Previstas, g.QtHrReal as Horas_Realizadas,
            g.ReceitaReal as Receita_Total, g.CustoReal as Custo_Total,
            g.PercMgReal as Margem_Percentual, tec.NomeTec as Consultor,
            niv.DescNivel as Nivel_Consultor, p.DescProj as Projeto,
            p.ObsProj as Projeto_Descricao, t.DescTipo as Tipo_Projeto,
            neg.DescNeg as Negocio_Projeto, status.DescStatus as Status_Projeto,
            resp.NomeResp as Responsavel_Projeto, cli.DescCli as Cliente
        FROM Tb_GestorFin2 g
        LEFT JOIN tb_Proj p ON g.ProjGest = p.AutNumProj
        LEFT JOIN tb_tec tec ON g.ConsultGest = tec.AutNumTec
        LEFT JOIN tb_cli cli ON p.CodCliProj = cli.AutNumCli
        LEFT JOIN tb_tipoproj t ON p.TipoProj = t.AutNumTipo
        LEFT JOIN tb_neg neg ON p.CodNegProj = neg.AutNumNeg
        LEFT JOIN tb_StatusProj status ON p.StatusProj = status.AutNumStatus
        LEFT JOIN tb_respproj resp ON p.RespProj1 = resp.AutNumResp
        LEFT JOIN tb_amarradisc amarra ON tec.AutNumTec = amarra.CodTecAmar
        LEFT JOIN tb_nivel niv ON amarra.Nivel = niv.AutNivel
        WHERE tec.NomeTec IS NOT NULL AND p.DescProj IS NOT NULL
        GROUP BY
            g.IdGest2, g.Mes, g.Ano, g.QtHrOrc, g.QtHrReal, g.ReceitaReal, g.CustoReal,
            g.PercMgReal, tec.NomeTec, niv.DescNivel, p.DescProj, p.ObsProj,
            t.DescTipo, neg.DescNeg, status.DescStatus, resp.NomeResp, cli.DescCli;
        """
        try:
            with pyodbc.connect(self.conn_str, timeout=10) as cnxn:
                df = pd.read_sql(super_query, cnxn)
            return df
        except Exception as e:
            st.sidebar.error(f"Falha na conexão com o banco. Erro: {e}", icon="❌")
            return None

# --- MOTOR DE ANÁLISE QUÂNTICO v2.0 ---
class QuantumAnalyticsEngine:
    def __init__(self):
        self.dados_originais = self._load_data()
        self.dados_filtrados = self.dados_originais.copy()

    def _load_data(self):
        orchestrator = DataOrchestrator()
        df = orchestrator.get_data()
        if df is not None:
            if not df.empty:
                st.sidebar.success(f"Conectado! {len(df)} registros.", icon="✅")
                return self._processar_dados(df)
            else:
                st.sidebar.warning("Conectado, mas nenhum dado retornado.", icon="⚠️")
        
        st.toast("Usando dados de simulação interna.", icon="🔬")
        return self._processar_dados(self._create_mock_data())

    def _processar_dados(self, df):
        numeric_cols = ['Horas_Previstas', 'Horas_Realizadas', 'Receita_Total', 'Custo_Total', 'Margem_Percentual']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        df['Lucro_Total'] = df['Receita_Total'] - df['Custo_Total']
        # Limpeza de dados nulos nas novas colunas para evitar erros
        for col in ['Nivel_Consultor', 'Negocio_Projeto', 'Status_Projeto']:
            df[col] = df[col].fillna('Não Definido')
        return df

    def _create_mock_data(self):
        # Mock de dados agora enriquecido com a estrutura real
        data = {
            'Mes': [1, 1, 2, 2, 3], 'Ano': [2025]*5,
            'Consultor': ['RAFAEL OLIVEIRA', 'CLEBER NEVES', 'ADRIANO AFONSO', 'RAFAEL OLIVEIRA', 'CLEBER NEVES'],
            'Nivel_Consultor': ['SÊNIOR', 'PLENO', 'ESPECIALISTA', 'SÊNIOR', 'PLENO'],
            'Cliente': ['AUTOZONE', 'TOTVS NOROESTE', 'HYDAC', 'TBC', 'HYDAC'],
            'Projeto': ['ALOCAÇÃO PMO', 'BODY SHOP', 'IMPLANTAÇÃO FISCAL', 'BODY SHOP', 'SUPORTE FECHADO'],
            'Negocio_Projeto': ['OUTSOURCING - LOCAÇÃO', 'OUTSOURCING - LOCAÇÃO', 'PROJETO', 'OUTSOURCING - LOCAÇÃO', 'PROJETO'],
            'Status_Projeto': ['EM ABERTO', 'FATURADO', 'EM ABERTO', 'FATURADO', 'FATURADO'],
            'Horas_Previstas': [160, 160, 100, 80, 50],
            'Horas_Realizadas': [170, 160, 125, 95, 55],
            'Receita_Total': [26800, 18400, 25000, 10450, 6000],
            'Custo_Total': [16800, 9600, 15000, 5225, 3300],
            'Margem_Percentual': [37.3, 47.8, 40.0, 50.0, 45.0]
        }
        return pd.DataFrame(data)

    def aplicar_filtros(self, filters):
        df = self.dados_originais.copy()
        for key, value in filters.items():
            if value != "TODOS" and value != ["TODOS"]:
                if isinstance(value, list):
                    df = df[df[key].isin(value)]
                else:
                    df = df[df[key] == value]
        self.dados_filtrados = df
        return df

    def gerar_insights_prescritivos(self):
        df = self.dados_filtrados
        if df.empty or len(df) < 3:
            return [{'tipo': 'info', 'texto': 'Dados insuficientes para gerar insights. Altere os filtros para uma análise mais ampla.'}]
        
        insights = []

        # Insight 1: Análise por Nível de Consultor
        perf_nivel = df.groupby('Nivel_Consultor')['Margem_Percentual'].mean()
        if len(perf_nivel) > 1:
            nivel_max = perf_nivel.idxmax()
            margem_max = perf_nivel.max()
            insights.append({
                'tipo': 'sucesso',
                'texto': f"**Ressonância de Senioridade:** Consultores de nível **'{nivel_max}'** estão entregando a maior margem média (**{margem_max:.1f}%**). **Prescrição Estratégica:** Avalie o mix de projetos para maximizar a alocação deste nível nos contratos mais valiosos."
            })

        # Insight 2: Análise por Linha de Negócio
        perf_negocio = df.groupby('Negocio_Projeto')['Lucro_Total'].sum()
        if len(perf_negocio) > 1:
            negocio_max = perf_negocio.idxmax()
            lucro_max = perf_negocio.max()
            insights.append({
                'tipo': 'oportunidade',
                'texto': f"**Foco de Lucratividade:** A linha de negócio **'{negocio_max}'** é a mais lucrativa, gerando **R$ {lucro_max:,.2f}** de lucro total no período. **Prescrição Comercial:** Direcione os esforços de vendas para expandir a carteira de projetos nesta área."
            })

        return insights

# --- INICIALIZAÇÃO ---
@st.cache_resource
def init_engine():
    return QuantumAnalyticsEngine()

engine = init_engine()

# --- INTERFACE PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>MAESTRO QUÂNTICO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8A8A8A; margin-top: -10px;'>A Sinfonia Estratégica da Sua Consultoria</p>", unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR DE CONTROLES MULTI-DIMENSIONAIS ---
with st.sidebar:
    st.markdown("## 🌌 Controles da Orquestra")
    dados_disponiveis = engine.dados_originais
    
    filters = {
        'Ano': st.selectbox("Ano", ["TODOS"] + sorted(dados_disponiveis['Ano'].unique().tolist())),
        'Mes': st.selectbox("Mês", ["TODOS"] + sorted(dados_disponiveis['Mes'].unique().tolist())),
        'Nivel_Consultor': st.multiselect("Nível do Consultor", ["TODOS"] + sorted(dados_disponiveis['Nivel_Consultor'].unique().tolist()), default=["TODOS"]),
        'Negocio_Projeto': st.multiselect("Área de Negócio", ["TODOS"] + sorted(dados_disponiveis['Negocio_Projeto'].unique().tolist()), default=["TODOS"]),
        'Consultor': st.multiselect("Consultores", ["TODOS"] + sorted(dados_disponiveis['Consultor'].unique().tolist()), default=["TODOS"]),
    }

    if st.button("Aplicar Filtros", use_container_width=True, type="primary"):
        pass # A aplicação dos filtros acontece fora do if para rodar sempre

    st.markdown("---")
    st.info("Desenvolvido por Jefferson de Souza em parceria com a IA Gemini.", icon="💡")

df_filtrado = engine.aplicar_filtros(filters)

# --- ABAS DE NAVEGAÇÃO ---
tab_names = ["Visão Geral", "Análise Dimensional", "Consultores & Projetos", "Assistente IA"]
tabs = st.tabs([f"**{name}**" for name in tab_names])

# Tab 1: Visão Geral
with tabs[0]:
    if df_filtrado.empty: st.warning("Nenhum dado para exibir com os filtros atuais.")
    else:
        kpis = {
            'receita_total': df_filtrado['Receita_Total'].sum(),
            'lucro_total': df_filtrado['Lucro_Total'].sum(),
            'margem_media': df_filtrado['Margem_Percentual'][df_filtrado['Margem_Percentual'] > 0].mean(),
            'consultores_ativos': df_filtrado['Consultor'].nunique()
        }
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Receita Total", f"R$ {kpis['receita_total']:,.0f}")
        c2.metric("Lucro Total", f"R$ {kpis['lucro_total']:,.0f}")
        c3.metric("Margem Média", f"{kpis['margem_media']:.1f}%")
        c4.metric("Consultores Ativos", kpis['consultores_ativos'])

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Receita por Nível de Consultor")
            receita_nivel = df_filtrado.groupby('Nivel_Consultor')['Receita_Total'].sum().sort_values(ascending=False)
            fig = px.bar(receita_nivel, x=receita_nivel.index, y='Receita_Total', color=receita_nivel.index, text_auto='.2s')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("### Lucro por Área de Negócio")
            lucro_negocio = df_filtrado.groupby('Negocio_Projeto')['Lucro_Total'].sum().sort_values(ascending=False)
            fig = px.pie(lucro_negocio, values='Lucro_Total', names=lucro_negocio.index, hole=0.5)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=True)
            st.plotly_chart(fig, use_container_width=True)

# Tab 2: Análise Dimensional
with tabs[1]:
    st.subheader("Análise Dimensional Cruzada")
    if not df_filtrado.empty:
        heatmap_data = df_filtrado.pivot_table(index='Nivel_Consultor', columns='Negocio_Projeto', values='Margem_Percentual', aggfunc='mean').fillna(0)
        if not heatmap_data.empty:
            fig = px.imshow(heatmap_data, text_auto='.1f', aspect="auto",
                            labels=dict(x="Área de Negócio", y="Nível do Consultor", color="Margem Média (%)"),
                            title="Mapa de Calor: Margem Média por Nível de Consultor vs. Área de Negócio")
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Dados insuficientes para criar o mapa de calor com os filtros atuais.")
    else:
        st.warning("Nenhum dado para exibir.")

# Tab 3: Consultores & Projetos
with tabs[2]:
    st.subheader("Detalhes de Performance")
    if not df_filtrado.empty:
        cols_to_show = [
            'Consultor', 'Nivel_Consultor', 'Projeto', 'Cliente', 
            'Negocio_Projeto', 'Receita_Total', 'Lucro_Total', 'Margem_Percentual'
        ]
        st.dataframe(df_filtrado[cols_to_show].style.format({
            'Receita_Total': 'R$ {:,.2f}', 'Lucro_Total': 'R$ {:,.2f}', 'Margem_Percentual': '{:.1f}%'
        }), use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir.")

# Tab 4: Assistente IA
with tabs[3]:
    st.header("O Maestro Preditivo")
    st.subheader("💡 Feed de Prescrições Vivas")
    st.markdown(f"*Insights gerados a partir de **{len(df_filtrado)}** registros filtrados*")
    
    insights_gerados = engine.gerar_insights_prescritivos()
    for insight in insights_gerados:
        card_class = {"alerta": "alert-card", "oportunidade": "insight-card", "sucesso": "success-card"}.get(insight['tipo'], "metric-card")
        icon = {"alerta": "🚨", "oportunidade": "🎯", "sucesso": "🏆"}.get(insight['tipo'], "ℹ️")
        st.markdown(f'<div class="{card_class}">{icon} {insight["texto"]}</div>', unsafe_allow_html=True)