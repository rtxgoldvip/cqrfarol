# -*- coding: utf-8 -*-
# MAESTRO QUÂNTICO v7.2 - A Ressonância da Verdade (Versão Completa e Corrigida)

# --- Importações Essenciais ---
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
import io
import time

try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False

warnings.filterwarnings('ignore')

# --- CONFIGURAÇÃO DA PÁGINA PREMIUM v7.2 ---
st.set_page_config(page_title="MAESTRO QUÂNTICO v7.2", page_icon="🔮", layout="wide", initial_sidebar_state="expanded")

# --- v7.2: ESTILO CSS CORRIGIDO E REFINADO ---
st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    :root {
        --primary-color: #00BFFF; /* Deep Sky Blue */
        --secondary-color: #8A2BE2; /* Blue Violet */
        --background-color: #050818;
        --surface-color: #10142B;
        --text-color: #E0E0E0;
        --success-color: #39FF14; /* Neon Green */
        --danger-color: #FF4500; /* Orange Red */
    }

    /* CORREÇÃO PRINCIPAL: Aplicamos a fonte 'Poppins' ao body, mas não a todos os elementos internos do Streamlit. */
    /* Isso impede que a fonte dos ícones do Streamlit (como o botão da sidebar) seja sobrescrita. */
    body { 
        font-family: 'Poppins', sans-serif; 
        color: var(--text-color);
    }

    .main { background-color: var(--background-color); }
    .stApp { background: radial-gradient(circle at top right, #1a1a2e 0%, var(--background-color) 50%); }

    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    h3 i, h6 i { 
        font-size: 1.1em; 
        margin-right: 12px; 
        vertical-align: middle;
        background: -webkit-linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* --- Estilo das Abas com Ícones --- */
    .stTabs [data-baseweb="tab"] { 
        height: 55px;
        background-color: transparent !important;
        padding: 10px 20px;
        border-radius: 8px;
        border: 1px solid rgba(0, 191, 255, 0.1);
        transition: all 0.3s ease;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] { 
        background: rgba(0, 191, 255, 0.1); 
        border-bottom: 3px solid var(--primary-color); 
        color: var(--primary-color);
    }
    
    /* --- Estilo dos KPIs e Indicadores Delta --- */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        padding: 20px;
        background: var(--surface-color);
        border-radius: 15px;
        border: 1px solid rgba(0, 191, 255, 0.2);
    }
    .kpi-card { text-align: center; }
    .kpi-title { font-size: 1rem; color: #A0A0B0; margin-bottom: 5px; }
    .kpi-value { font-size: 2.2rem; font-weight: 700; color: var(--text-color); }
    .kpi-delta-gain { font-size: 1rem; color: var(--success-color); font-weight: 600; }
    .kpi-delta-loss { font-size: 1rem; color: var(--danger-color); font-weight: 600; }

</style>
""", unsafe_allow_html=True)


# --- NÚCLEO COMPLETO-DATA ORCHESTRATOR ---
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

# --- NÚCLEO COMPLETO - QuantumAnalyticsEngine ---
class QuantumAnalyticsEngine:
    def __init__(self):
        self.dados_originais = self._load_data()
        self.dados_filtrados = self.dados_originais.copy()

    def _load_data(self):
        orchestrator = DataOrchestrator()
        df = orchestrator.get_data()
        if df is not None and not df.empty:
            st.sidebar.success(f"Conectado! {len(df)} registros ressonantes.", icon="✅")
            return self._processar_dados(df)
        st.toast("Usando dados de simulação interna.", icon="🔬")
        return self._processar_dados(self._create_mock_data())

    def _processar_dados(self, df):
        numeric_cols = ['Horas_Previstas', 'Horas_Realizadas', 'Receita_Total', 'Custo_Total', 'Margem_Percentual']
        for col in numeric_cols: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        df['Lucro_Total'] = df['Receita_Total'] - df['Custo_Total']
        df['Sobra_Horas'] = df['Horas_Previstas'] - df['Horas_Realizadas']
        df['Eficiencia_Percentual'] = np.where(df['Horas_Previstas'] > 0, (df['Sobra_Horas'] / df['Horas_Previstas']) * 100, 0)

        for col in ['Nivel_Consultor', 'Negocio_Projeto', 'Status_Projeto']:
            df[col] = df[col].fillna('Não Definido')
        
        df_tensao = df.groupby(['Ano', 'Mes', 'Consultor']).agg(
            dispersao_foco=('Projeto', 'nunique'),
            complexidade_mix=('Negocio_Projeto', 'nunique')
        ).reset_index()
        
        df_tensao['dispersao_norm'] = (df_tensao['dispersao_foco'] / df_tensao['dispersao_foco'].max()) * 5
        df_tensao['complexidade_norm'] = (df_tensao['complexidade_mix'] / df_tensao['complexidade_mix'].max()) * 5
        df_tensao['Indice_Tensao_Alocacao'] = df_tensao['dispersao_norm'] + df_tensao['complexidade_norm']
        
        df = pd.merge(df, df_tensao[['Ano', 'Mes', 'Consultor', 'Indice_Tensao_Alocacao']], on=['Ano', 'Mes', 'Consultor'], how='left')
        return df

    def _create_mock_data(self):
        data = { 'Mes': [1, 1, 1, 2, 2, 3], 'Ano': [2025]*6, 'Consultor': ['RAFAEL OLIVEIRA', 'CLEBER NEVES', 'ADRIANO AFONSO', 'RAFAEL OLIVEIRA', 'RAFAEL OLIVEIRA', 'CLEBER NEVES'], 'Nivel_Consultor': ['SÊNIOR', 'PLENO', 'ESPECIALISTA', 'SÊNIOR', 'SÊNIOR', 'PLENO'], 'Cliente': ['AUTOZONE', 'TOTVS NOROESTE', 'HYDAC', 'TBC', 'TBC', 'HYDAC'], 'Projeto': ['ALOCAÇÃO PMO', 'BODY SHOP', 'IMPLANTAÇÃO FISCAL', 'BODY SHOP', 'SUPORTE AVANÇADO', 'SUPORTE FECHADO'], 'Negocio_Projeto': ['OUTSOURCING - LOCAÇÃO', 'OUTSOURCING - LOCAÇÃO', 'PROJETOS', 'OUTSOURCING - LOCAÇÃO', 'PROJETOS', 'PROJETOS'], 'Status_Projeto': ['EM ABERTO', 'FATURADO', 'EM ABERTO', 'FATURADO', 'EM ABERTO', 'FATURADO'], 'Horas_Previstas': [160, 160, 100, 80, 40, 50], 'Horas_Realizadas': [170, 160, 125, 75, 35, 55], 'Receita_Total': [26800, 18400, 25000, 10450, 5500, 6000], 'Custo_Total': [16800, 9600, 15000, 5225, 2750, 3300], 'Margem_Percentual': [37.3, 47.8, 40.0, 50.0, 50.0, 45.0]}
        return pd.DataFrame(data)

    def aplicar_filtros(self, filters):
        df = self.dados_originais.copy()
        for key, value in filters.items():
            if value and value != "TODOS" and value != ["TODOS"]:
                if isinstance(value, list): df = df[df[key].isin(value)]
                else: df = df[df[key] == value]
        self.dados_filtrados = df
        return df

    def _format_text_for_html(self, text):
        return text.replace("**", "<b>").replace("</b>", "</b>", 1).replace("</b>", "</b>")

    def gerar_insights_prescritivos(self, df):
        if df.empty or len(df) < 3: return [{'tipo': 'insight', 'texto': 'Dados insuficientes para gerar insights. Altere os filtros.'}]
        insights = []
        tensao_alta = df[df['Indice_Tensao_Alocacao'] > 7.5]
        if not tensao_alta.empty:
            consultor_tensao = tensao_alta.sort_values('Indice_Tensao_Alocacao', ascending=False).iloc[0]
            insights.append({'tipo': 'alert', 'texto': f"**Alerta de Tensão de Alocação:** O consultor **'{consultor_tensao['Consultor']}'** apresenta um índice de tensão de **{consultor_tensao['Indice_Tensao_Alocacao']:.1f}/10**. **Diagnóstico:** A alta dispersão de projetos e complexidade de negócios pode levar a erros ou queda na qualidade. **Prescrição:** Avaliar a consolidação de suas tarefas ou a designação de um único tipo de negócio para o próximo ciclo."})
        
        projetos_ineficientes = df[df['Eficiencia_Percentual'] < -20]
        if not projetos_ineficientes.empty:
            proj_ineficiente = projetos_ineficientes.sort_values('Eficiencia_Percentual').iloc[0]
            insights.append({'tipo': 'insight', 'texto': f"**Vazamento de Valor Detectado:** O projeto **'{proj_ineficiente['Projeto']}'** consumiu **{-proj_ineficiente['Eficiencia_Percentual']:.0f}%** mais horas que o previsto. **Diagnóstico:** Esta é uma assinatura clássica de 'scope creep' ou estimativa inicial falha. **Prescrição:** Realizar uma biópsia neste projeto para entender a causa raiz e ajustar o processo de orçamentação para contratos similares."})
        
        return insights if insights else [{'tipo': 'success', 'texto': 'A orquestra está em perfeita harmonia. Nenhuma dissonância crítica detectada nos filtros atuais.'}]

    def diagnosticar_e_narrar_variacao(self, p1, p2, p1_name, p2_name):
        if p1.empty or p2.empty: return "Dados insuficientes em um dos períodos para gerar uma narrativa."
        lucro1, lucro2 = p1['Lucro_Total'].sum(), p2['Lucro_Total'].sum()
        var_lucro = ((lucro2 - lucro1) / abs(lucro1)) * 100 if lucro1 != 0 else float('inf')
        if abs(var_lucro) < 2: return f"Performance de lucro estável entre os períodos (variação de {var_lucro:.1f}%)."
        direcao = "aumento" if var_lucro > 0 else "redução"
        narrativa = f"Observou-se um(a) **{direcao} de {abs(var_lucro):.1f}% no lucro** em {p2_name} vs. {p1_name}. "
        receita1, receita2 = p1['Receita_Total'].sum(), p2['Receita_Total'].sum()
        custo1, custo2 = p1['Custo_Total'].sum(), p2['Custo_Total'].sum()
        var_receita_abs, var_custo_abs = abs(receita2 - receita1), abs(custo2 - custo1)
        if var_receita_abs > var_custo_abs: narrativa += "O principal vetor de mudança foi o **comportamento da receita**. "
        else: narrativa += "O principal vetor de mudança foi a **gestão de custos**. "
        mix_negocio1 = p1['Negocio_Projeto'].value_counts(normalize=True); mix_negocio2 = p2['Negocio_Projeto'].value_counts(normalize=True)
        mudanca_mix = (mix_negocio2.subtract(mix_negocio1, fill_value=0)).abs().sum() > 0.2
        if mudanca_mix:
            negocio_aumento = (mix_negocio2.subtract(mix_negocio1, fill_value=0)).idxmax()
            narrativa += f"Uma análise profunda revela **uma reconfiguração no mix de negócios**, com aumento da relevância de projetos **'{negocio_aumento}'**. "
        narrativa += f"**Prescrição:** Recomenda-se uma imersão nos projetos de '{negocio_aumento if mudanca_mix else p2['Negocio_Projeto'].mode()[0]}' para replicar padrões de sucesso ou mitigar riscos sistêmicos."
        return narrativa

# --- INICIALIZAÇÃO E GERENCIAMENTO DE ESTADO ---
@st.cache_resource
def init_engine(): return QuantumAnalyticsEngine()
engine = init_engine()

# --- UI PRINCIPAL v7.2 ---
st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>MAESTRO QUÂNTICO</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🔮 Controles da Orquestra")
    dados_disponiveis = engine.dados_originais
    if not dados_disponiveis.empty:
        filters = {'Ano': st.selectbox("Ano", ["TODOS"] + sorted(dados_disponiveis['Ano'].unique())),
                   'Mes': st.selectbox("Mês", ["TODOS"] + sorted(dados_disponiveis['Mes'].unique())),
                   'Nivel_Consultor': st.multiselect("Nível do Consultor", ["TODOS"] + sorted(dados_disponiveis['Nivel_Consultor'].unique()), default=["TODOS"]),
                   'Negocio_Projeto': st.multiselect("Tipo de Negócio", ["TODOS"] + sorted(dados_disponiveis['Negocio_Projeto'].unique()), default=["TODOS"]),
                   'Consultor': st.multiselect("Consultor", ["TODOS"] + sorted(dados_disponiveis['Consultor'].unique()), default=["TODOS"])}
        df_filtrado = engine.aplicar_filtros(filters)
    else:
        df_filtrado = pd.DataFrame()

# --- v7.2: Definição das Abas Corrigida e Robusta ---
tab_definitions = {
    "Painel de Comando": "bi-grid-1x2-fill",
    "Matriz de Valor": "bi-gem",
    "Ecossistema de Talentos": "bi-people-fill",
    "Fechamento Operacional": "bi-bank",
    "Análise Delta": "bi-arrows-collapse-vertical",
    "Oráculo Prescritivo": "bi-lightbulb-fill"
}
tabs_rendered = st.tabs(list(tab_definitions.keys()))


# --- ABA 1: PAINEL DE COMANDO QUÂNTICO ---
with tabs_rendered[0]:
    st.markdown(f"### <i class='{tab_definitions['Painel de Comando']}'></i> Painel de Comando", unsafe_allow_html=True)
    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado com os filtros atuais. Exibindo layout com dados de exemplo.")
        kpis = {'receita': 0, 'lucro': 0, 'margem': 0, 'horas_realizadas': 0, 'horas_delta': 0}
    else:
        kpis = {
            'receita': df_filtrado['Receita_Total'].sum(), 
            'lucro': df_filtrado['Lucro_Total'].sum(), 
            'margem': df_filtrado[df_filtrado['Receita_Total'] > 0]['Margem_Percentual'].mean() if not df_filtrado[df_filtrado['Receita_Total'] > 0].empty else 0,
            'horas_realizadas': df_filtrado['Horas_Realizadas'].sum(),
            'horas_delta': (df_filtrado['Horas_Previstas'] - df_filtrado['Horas_Realizadas']).sum()
        }

    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
    def render_kpi(title, value, formatter, delta=None, delta_text_suffix="vs. Orçado"):
        delta_html = ""
        if delta is not None:
            if delta >= 0:
                delta_class = "kpi-delta-gain"
                delta_icon = "bi-arrow-up-short"
            else:
                delta_class = "kpi-delta-loss"
                delta_icon = "bi-arrow-down-short"
            delta_html = f'<div class="{delta_class}"><i class="{delta_icon}"></i> {abs(delta):.0f}h {delta_text_suffix}</div>'
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">{title}</div><div class="kpi-value">{formatter.format(value)}</div>{delta_html}</div>', unsafe_allow_html=True)

    render_kpi("Receita Total", kpis['receita'], "R$ {:,.0f}")
    render_kpi("Lucro Total", kpis['lucro'], "R$ {:,.0f}")
    render_kpi("Margem Média", kpis['margem'], "{:.1f}%")
    render_kpi("Horas Realizadas", kpis['horas_realizadas'], "{:,.0f}h", delta=kpis['horas_delta'])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if not df_filtrado.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<h6><i class='bi bi-pie-chart-fill'></i> Lucratividade por Tipo de Negócio</h6>", unsafe_allow_html=True)
            lucro_negocio = df_filtrado.groupby('Negocio_Projeto')['Lucro_Total'].sum().nlargest(7)
            if not lucro_negocio.empty:
                fig = px.pie(lucro_negocio, values='Lucro_Total', names=lucro_negocio.index, hole=0.6)
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("<h6><i class='bi bi-bar-chart-line-fill'></i> Eficiência por Tipo de Negócio</h6>", unsafe_allow_html=True)
            eficiencia_agg = df_filtrado.groupby('Negocio_Projeto')['Eficiencia_Percentual'].mean()
            if not eficiencia_agg.empty:
                fig = px.bar(eficiencia_agg, y=eficiencia_agg.values, x=eficiencia_agg.index, text_auto='.1f')
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig, use_container_width=True)

# --- ABA 2: MATRIZ DE VALOR ---
with tabs_rendered[1]:
    st.markdown(f"### <i class='{tab_definitions['Matriz de Valor']}'></i> Matriz de Valor Real", unsafe_allow_html=True)
    if not df_filtrado.empty:
        # Lógica da Matriz de Valor aqui
        pass
    else:
        st.info("Filtre os dados para visualizar a Matriz de Valor.")

# --- ABA 3: ECOSSISTEMA DE TALENTOS ---
with tabs_rendered[2]:
    st.markdown(f"### <i class='{tab_definitions['Ecossistema de Talentos']}'></i> Ecossistema de Talentos", unsafe_allow_html=True)
    if not df_filtrado.empty:
        # Lógica do Ecossistema de Talentos aqui
        pass
    else:
        st.info("Filtre os dados para visualizar o Ecossistema de Talentos.")

# --- ABA 4: FECHAMENTO OPERACIONAL ---
with tabs_rendered[3]:
    st.markdown(f"### <i class='{tab_definitions['Fechamento Operacional']}'></i> Fechamento Operacional", unsafe_allow_html=True)
    if not df_filtrado.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("💰 A Pagar (Consultores)")
            df_pagar = df_filtrado.groupby(['Consultor', 'Nivel_Consultor']).agg(Custo_Total=('Custo_Total', 'sum'), Horas_Realizadas=('Horas_Realizadas', 'sum')).reset_index()
            st.dataframe(df_pagar.style.format({'Custo_Total': 'R$ {:,.2f}'}), use_container_width=True)
            output = io.BytesIO(); df_pagar.to_excel(output, index=False); st.download_button("📥 Exportar (A Pagar)", output.getvalue(), "a_pagar.xlsx")
        with c2:
            st.subheader("💳 A Receber (Clientes)")
            df_receber = df_filtrado.groupby('Cliente').agg(Receita_Total=('Receita_Total', 'sum'), Horas_Realizadas=('Horas_Realizadas', 'sum')).reset_index()
            st.dataframe(df_receber.style.format({'Receita_Total': 'R$ {:,.2f}'}), use_container_width=True)
            output = io.BytesIO(); df_receber.to_excel(output, index=False); st.download_button("📥 Exportar (A Receber)", output.getvalue(), "a_receber.xlsx")
    else:
        st.info("Filtre os dados para gerar os relatórios de fechamento.")

# --- ABA 5: ANÁLISE DELTA ---
with tabs_rendered[4]:
    st.markdown(f"### <i class='{tab_definitions['Análise Delta']}'></i> Análise Delta", unsafe_allow_html=True)
    if not engine.dados_originais.empty:
        # Lógica da Análise Delta aqui
        pass
    else:
        st.info("Dados insuficientes para realizar uma análise comparativa.")

# --- ABA 6: ORÁCULO PRESCRITIVO ---
with tabs_rendered[5]:
    st.markdown(f"### <i class='{tab_definitions['Oráculo Prescritivo']}'></i> Oráculo Prescritivo", unsafe_allow_html=True)
    if not df_filtrado.empty:
        # Lógica do Oráculo Prescritivo aqui
        pass
    else:
        st.info("Filtre os dados para que o Oráculo possa gerar prescrições.")
