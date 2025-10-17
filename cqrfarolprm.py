# -*- coding: utf-8 -*-
# MAESTRO QUÂNTICO v5.0 - O Oráculo Interativo

# --- Importações Essenciais ---
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
import io

try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False

warnings.filterwarnings('ignore')

# --- CONFIGURAÇÃO DA PÁGINA PREMIUM ---
st.set_page_config(page_title="MAESTRO QUÂNTICO", page_icon="🌌", layout="wide", initial_sidebar_state="expanded")

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
    .data-panel {
        background: rgba(10, 8, 24, 0.8); border-radius: 15px; padding: 25px;
        border: 1px solid rgba(0, 191, 255, 0.2); margin-bottom: 20px;
    }
    .narrative-box, .insight-card, .alert-card, .success-card {
        background: rgba(28, 28, 40, 0.7); border-radius: 15px; padding: 25px;
        border: 1px solid rgba(0, 191, 255, 0.2); margin-bottom: 15px;
    }
    .narrative-box { border-left: 5px solid #8A2BE2; }
    .insight-card { border-left: 5px solid #FFD700; }
    .alert-card { border-left: 5px solid #FF4500; }
    .success-card { border-left: 5px solid #39FF14; }
</style>
""", unsafe_allow_html=True)

# --- NÚCLEO DE CONEXÃO E EXTRAÇÃO DE DADOS ---
class DataOrchestrator:
    def __init__(self):
        self.conn_str = self._get_conn_str()
        self.super_query = """
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
        LEFT JOIN tb_Proj p ON g.ProjGest = p.AutNumProj LEFT JOIN tb_tec tec ON g.ConsultGest = tec.AutNumTec
        LEFT JOIN tb_cli cli ON p.CodCliProj = cli.AutNumCli LEFT JOIN tb_tipoproj t ON p.TipoProj = t.AutNumTipo
        LEFT JOIN tb_neg neg ON p.CodNegProj = neg.AutNumNeg LEFT JOIN tb_StatusProj status ON p.StatusProj = status.AutNumStatus
        LEFT JOIN tb_respproj resp ON p.RespProj1 = resp.AutNumResp LEFT JOIN tb_amarradisc amarra ON tec.AutNumTec = amarra.CodTecAmar
        LEFT JOIN tb_nivel niv ON amarra.Nivel = niv.AutNivel
        WHERE tec.NomeTec IS NOT NULL AND p.DescProj IS NOT NULL
        GROUP BY
            g.IdGest2, g.Mes, g.Ano, g.QtHrOrc, g.QtHrReal, g.ReceitaReal, g.CustoReal, g.PercMgReal,
            tec.NomeTec, niv.DescNivel, p.DescProj, p.ObsProj, t.DescTipo, neg.DescNeg, status.DescStatus, resp.NomeResp, cli.DescCli;
        """

    def _get_conn_str(self):
        try:
            return (f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={st.secrets['db_credentials']['server']};"
                    f"DATABASE={st.secrets['db_credentials']['database']};"
                    f"UID={st.secrets['db_credentials']['username']};"
                    f"PWD={st.secrets['db_credentials']['password']};"
                    f"TrustServerCertificate=yes;")
        except (KeyError, FileNotFoundError): return None

    def get_data(self):
        if not PYODBC_AVAILABLE or not self.conn_str: return None
        try:
            with pyodbc.connect(self.conn_str, timeout=10) as cnxn:
                return pd.read_sql(self.super_query, cnxn)
        except Exception: return None

# --- MOTOR DE ANÁLISE QUÂNTICO v5.0 ---
class QuantumAnalyticsEngine:
    def __init__(self):
        self.dados_originais = self._load_data()
        self.dados_filtrados = self.dados_originais.copy()

    def _load_data(self):
        orchestrator = DataOrchestrator()
        df = orchestrator.get_data()
        if df is not None and not df.empty:
            st.sidebar.success(f"Conectado! {len(df)} registros.", icon="✅")
            return self._processar_dados(df)
        st.toast("Usando dados de simulação interna.", icon="🔬")
        return self._processar_dados(self._create_mock_data())

    def _processar_dados(self, df):
        numeric_cols = ['Horas_Previstas', 'Horas_Realizadas', 'Receita_Total', 'Custo_Total', 'Margem_Percentual']
        for col in numeric_cols: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        df['Lucro_Total'] = df['Receita_Total'] - df['Custo_Total']
        for col in ['Nivel_Consultor', 'Negocio_Projeto', 'Status_Projeto']:
            df[col] = df[col].fillna('Não Definido')
        return df

    def _create_mock_data(self):
        data = { 'Mes': [1, 1, 2, 2, 3], 'Ano': [2025]*5, 'Consultor': ['RAFAEL OLIVEIRA', 'CLEBER NEVES', 'ADRIANO AFONSO', 'RAFAEL OLIVEIRA', 'CLEBER NEVES'], 'Nivel_Consultor': ['SÊNIOR', 'PLENO', 'ESPECIALISTA', 'SÊNIOR', 'PLENO'], 'Cliente': ['AUTOZONE', 'TOTVS NOROESTE', 'HYDAC', 'TBC', 'HYDAC'], 'Projeto': ['ALOCAÇÃO PMO', 'BODY SHOP', 'IMPLANTAÇÃO FISCAL', 'BODY SHOP', 'SUPORTE FECHADO'], 'Negocio_Projeto': ['OUTSOURCING - LOCAÇÃO', 'OUTSOURCING - LOCAÇÃO', 'PROJETOS', 'OUTSOURCING - LOCAÇÃO', 'PROJETOS'], 'Status_Projeto': ['EM ABERTO', 'FATURADO', 'EM ABERTO', 'FATURADO', 'FATURADO'], 'Horas_Previstas': [160, 160, 100, 80, 50], 'Horas_Realizadas': [170, 160, 125, 95, 55], 'Receita_Total': [26800, 18400, 25000, 10450, 6000], 'Custo_Total': [16800, 9600, 15000, 5225, 3300], 'Margem_Percentual': [37.3, 47.8, 40.0, 50.0, 45.0]}
        return pd.DataFrame(data)

    def aplicar_filtros(self, filters):
        df = self.dados_originais.copy()
        for key, value in filters.items():
            if value and value != "TODOS" and value != ["TODOS"]:
                if isinstance(value, list): df = df[df[key].isin(value)]
                else: df = df[df[key] == value]
        self.dados_filtrados = df
        return df
        
    def gerar_insights_prescritivos(self, df):
        if df.empty or len(df) < 3: return [{'tipo': 'info', 'texto': 'Dados insuficientes para gerar insights. Altere os filtros.'}]
        insights = []
        if len(df['Nivel_Consultor'].unique()) > 1:
            perf_nivel = df.groupby('Nivel_Consultor')['Margem_Percentual'].mean().drop('Não Definido', errors='ignore')
            if not perf_nivel.empty:
                insights.append({'tipo': 'sucesso', 'texto': f"**Ressonância de Senioridade:** Consultores **'{perf_nivel.idxmax()}'** entregam a maior margem média (**{perf_nivel.max():.1f}%**). **Prescrição:** Maximize a alocação deste nível nos contratos mais valiosos."})
        q1, q3 = df['Margem_Percentual'].quantile(0.25), df['Margem_Percentual'].quantile(0.75)
        anomalias = df[df['Margem_Percentual'] < (q1 - 1.5 * (q3 - q1))]
        if not anomalias.empty:
            anomalia_critica = anomalias.sort_values('Margem_Percentual').iloc[0]
            insights.append({'tipo': 'alerta', 'texto': f"**Interferência Destrutiva:** O projeto **'{anomalia_critica['Projeto']}'** apresenta margem de **{anomalia_critica['Margem_Percentual']:.1f}%**, um valor atípico. **Ação Imediata:** Revisar os custos e escopo deste projeto."})
        return insights if insights else [{'tipo': 'info', 'texto': 'A orquestra está em harmonia. Nenhuma anomalia crítica detectada.'}]

    def diagnosticar_e_narrar_variacao(self, p1, p2, p1_name, p2_name):
        if p1.empty or p2.empty: return "Dados insuficientes em um dos períodos para gerar uma narrativa."
        lucro1, lucro2 = p1['Lucro_Total'].sum(), p2['Lucro_Total'].sum()
        var_lucro = ((lucro2 - lucro1) / lucro1) * 100 if lucro1 != 0 else float('inf')
        if abs(var_lucro) < 2: return f"Performance de lucro estável entre os períodos (variação de {var_lucro:.1f}%)."
        direcao = "aumento" if var_lucro > 0 else "redução"
        narrativa = f"Observou-se um(a) **{direcao} de {abs(var_lucro):.1f}% no lucro** em {p2_name} vs. {p1_name}. "
        receita1, receita2 = p1['Receita_Total'].sum(), p2['Receita_Total'].sum()
        custo1, custo2 = p1['Custo_Total'].sum(), p2['Custo_Total'].sum()
        var_receita_abs = abs(receita2 - receita1)
        var_custo_abs = abs(custo2 - custo1)
        if var_receita_abs > var_custo_abs: narrativa += "A principal causa foi o **comportamento da receita**. "
        else: narrativa += "A principal causa foi a **gestão de custos**. "
        mix_negocio1 = p1['Negocio_Projeto'].value_counts(normalize=True); mix_negocio2 = p2['Negocio_Projeto'].value_counts(normalize=True)
        mudanca_mix = (mix_negocio2.subtract(mix_negocio1, fill_value=0)).abs().sum() > 0.2
        if mudanca_mix:
            negocio_aumento = (mix_negocio2.subtract(mix_negocio1, fill_value=0)).idxmax()
            narrativa += f"Uma análise mais profunda revela uma **mudança no mix de negócios**, com aumento em projetos **'{negocio_aumento}'**. "
        narrativa += f"**Prescrição:** Recomenda-se investigar os projetos de '{negocio_aumento if mudanca_mix else p2['Negocio_Projeto'].mode()[0]}' para replicar sucessos ou mitigar riscos."
        return narrativa

# --- INICIALIZAÇÃO ---
@st.cache_resource
def init_engine(): return QuantumAnalyticsEngine()
engine = init_engine()

# --- INTERFACE PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>MAESTRO QUÂNTICO</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🌌 Controles da Orquestra")
    dados_disponiveis = engine.dados_originais
    filters = {'Ano': st.selectbox("Ano", ["TODOS"] + sorted(dados_disponiveis['Ano'].unique())),
               'Mes': st.selectbox("Mês", ["TODOS"] + sorted(dados_disponiveis['Mes'].unique())),
               'Nivel_Consultor': st.multiselect("Nível do Consultor", ["TODOS"] + sorted(dados_disponiveis['Nivel_Consultor'].unique()), default=["TODOS"]),
               'Negocio_Projeto': st.multiselect("Área de Negócio", ["TODOS"] + sorted(dados_disponiveis['Negocio_Projeto'].unique()), default=["TODOS"]),
               'Consultor': st.multiselect("Consultores", ["TODOS"] + sorted(dados_disponiveis['Consultor'].unique()), default=["TODOS"])}
df_filtrado = engine.aplicar_filtros(filters)

tab_names = ["Visão Geral", "Análise Dimensional", "Consultores & Projetos", "Fechamento", "Comparativo", "Assistente IA"]
tabs = st.tabs([f"**{name}**" for name in tab_names])

with tabs[0]: # VISÃO GERAL
    if df_filtrado.empty: st.warning("Nenhum dado para exibir.")
    else:
        st.markdown('<div class="data-panel">', unsafe_allow_html=True)
        kpis = {'receita': df_filtrado['Receita_Total'].sum(), 'lucro': df_filtrado['Lucro_Total'].sum(),
                'margem': df_filtrado['Margem_Percentual'][df_filtrado['Margem_Percentual'] > 0].mean(),
                'horas_r': df_filtrado['Horas_Realizadas'].sum(), 'horas_p': df_filtrado['Horas_Previstas'].sum()}
        kpis['delta_h'] = kpis['horas_r'] - kpis['horas_p']
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Receita Total", f"R$ {kpis['receita']:,.0f}"); c2.metric("Lucro Total", f"R$ {kpis['lucro']:,.0f}")
        c3.metric("Margem Média", f"{kpis['margem']:.1f}%")
        c4.metric("Horas Realizadas", f"{kpis['horas_r']:.0f}h", f"{kpis['delta_h']:.0f}h vs. Orçado")
        st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]: # ANÁLISE DIMENSIONAL
    st.subheader("Mapa de Calor: Margem Média por Nível de Consultor vs. Área de Negócio")
    if not df_filtrado.empty:
        heatmap_data = df_filtrado.pivot_table(index='Nivel_Consultor', columns='Negocio_Projeto', values='Margem_Percentual', aggfunc='mean').fillna(0)
        if not heatmap_data.empty:
            fig = px.imshow(heatmap_data, text_auto='.1f', aspect="auto")
            st.plotly_chart(fig, use_container_width=True)

with tabs[2]: # CONSULTORES E PROJETOS
    st.subheader("Detalhes de Performance")
    if not df_filtrado.empty:
        st.dataframe(df_filtrado[['Consultor', 'Nivel_Consultor', 'Projeto', 'Cliente', 'Receita_Total', 'Lucro_Total', 'Margem_Percentual']].style.format(formatter={'Receita_Total': 'R$ {:,.2f}', 'Lucro_Total': 'R$ {:,.2f}', 'Margem_Percentual': '{:.1f}%'}), use_container_width=True)

with tabs[3]: # FECHAMENTO
    st.header("Fechamento Financeiro")
    if not df_filtrado.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("💰 A Pagar (Consultores)")
            df_pagar = df_filtrado.groupby(['Consultor', 'Nivel_Consultor'])['Custo_Total'].sum().reset_index().sort_values('Custo_Total', ascending=False)
            st.dataframe(df_pagar.style.format(formatter={'Custo_Total': 'R$ {:,.2f}'}), use_container_width=True)
            output = io.BytesIO(); df_pagar.to_excel(output, index=False); st.download_button("📥 Exportar (A Pagar)", output.getvalue(), "a_pagar.xlsx")
        with c2:
            st.subheader("💳 A Receber (Clientes)")
            df_receber = df_filtrado.groupby('Cliente')['Receita_Total'].sum().reset_index().sort_values('Receita_Total', ascending=False)
            st.dataframe(df_receber.style.format(formatter={'Receita_Total': 'R$ {:,.2f}'}), use_container_width=True)
            output = io.BytesIO(); df_receber.to_excel(output, index=False); st.download_button("📥 Exportar (A Receber)", output.getvalue(), "a_receber.xlsx")

with tabs[4]: # COMPARATIVO
    st.header("Análise Comparativa com Diagnóstico IA")
    anos = sorted(engine.dados_originais['Ano'].unique()); meses = sorted(engine.dados_originais['Mes'].unique())
    c1, c2 = st.columns(2)
    with c1:
        st.