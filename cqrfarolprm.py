# -*- coding: utf-8 -*-
# MAESTRO QUÂNTICO v6.2 - A Sinfonia Completa e Unificada

# --- Importações Essenciais ---
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
import io
import time
import re

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
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
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
    .data-hologram { background: rgba(10, 8, 24, 0.8); border-radius: 20px; padding: 30px; border: 1px solid rgba(0, 191, 255, 0.2); margin-bottom: 25px; box-shadow: 0 0 25px rgba(0, 191, 255, 0.1); }
    .narrative-box, .insight-card, .alert-card, .success-card { background: rgba(28, 28, 40, 0.7); border-radius: 15px; padding: 25px; border: 1px solid rgba(0, 191, 255, 0.2); margin-bottom: 15px; }
    .narrative-box { border-left: 5px solid #8A2BE2; }
    .insight-card { border-left: 5px solid #FFD700; }
    .alert-card { border-left: 5px solid #FF4500; }
    .success-card { border-left: 5px solid #39FF14; }
    .entity-box { background-color: rgba(0, 191, 255, 0.1); border: 1px solid #00BFFF; border-radius: 8px; padding: 10px; margin: 5px; text-align: center; }
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
            insights.append({'tipo': 'alerta', 'texto': f"**Análise de Consequência (Biópsia):** O projeto **'{anomalia_critica['Projeto']}'** tem uma margem atipicamente baixa. **Diagnóstico:** A alocação de um consultor de nível **'{anomalia_critica['Nivel_Consultor']}'** neste tipo de contrato pode estar gerando um **custo oculto de subutilização estratégica**. **Ação Imediata:** Revisar a política de alocação para projetos de baixo valor."})
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
        var_receita_abs, var_custo_abs = abs(receita2 - receita1), abs(custo2 - custo1)
        if var_receita_abs > var_custo_abs: narrativa += "A principal causa foi o **comportamento da receita**. "
        else: narrativa += "A principal causa foi a **gestão de custos**. "
        mix_negocio1 = p1['Negocio_Projeto'].value_counts(normalize=True); mix_negocio2 = p2['Negocio_Projeto'].value_counts(normalize=True)
        mudanca_mix = (mix_negocio2.subtract(mix_negocio1, fill_value=0)).abs().sum() > 0.2
        if mudanca_mix:
            negocio_aumento = (mix_negocio2.subtract(mix_negocio1, fill_value=0)).idxmax()
            narrativa += f"Uma análise profunda revela **mudança no mix de negócios**, com aumento em projetos **'{negocio_aumento}'**. "
        narrativa += f"**Prescrição:** Recomenda-se investigar os projetos de '{negocio_aumento if mudanca_mix else p2['Negocio_Projeto'].mode()[0]}' para replicar sucessos ou mitigar riscos."
        return narrativa

# --- Classe para Processamento da O.S. POR VOZ ---
class OSProcessor:
    def __init__(self, data_engine):
        self.consultores = sorted([''] + data_engine.dados_originais['Consultor'].unique().tolist())
        self.clientes = sorted([''] + data_engine.dados_originais['Cliente'].unique().tolist())
    
    def parse_command(self, command):
        command = command.lower()
        parsed_data = {'consultor': None, 'cliente': None, 'horas': None, 'projeto': 'Não especificado'}
        
        horas_match = re.search(r'(\d+[\.,]?\d*)\s*h(oras)?', command)
        if horas_match: parsed_data['horas'] = float(horas_match.group(1).replace(',', '.'))
        
        for consultor in self.consultores:
            if consultor and consultor.lower() in command: parsed_data['consultor'] = consultor; break
        
        for cliente in self.clientes:
            if cliente and cliente.lower() in command: parsed_data['cliente'] = cliente; break
        
        projeto_match = re.search(r'projeto (.+?)( para| do| com| na| cliente)', command)
        if not projeto_match: projeto_match = re.search(r'projeto (.+)', command)
        if projeto_match: parsed_data['projeto'] = projeto_match.group(1).strip().upper()
            
        return parsed_data

# --- INICIALIZAÇÃO E GERENCIAMENTO DE ESTADO ---
@st.cache_resource
def init_engine(): return QuantumAnalyticsEngine()
engine = init_engine()
os_processor = OSProcessor(engine)

if 'spinner_text' not in st.session_state: st.session_state['spinner_text'] = "Processando Ressonância..."

# --- UI PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>MAESTRO QUÂNTICO</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🌌 Controles da Orquestra")
    dados_disponiveis = engine.dados_originais
    filters = {'Ano': st.selectbox("Ano", ["TODOS"] + sorted(dados_disponiveis['Ano'].unique())),
               'Mes': st.selectbox("Mês", ["TODOS"] + sorted(dados_disponiveis['Mes'].unique())),
               'Nivel_Consultor': st.multiselect("Nível", ["TODOS"] + sorted(dados_disponiveis['Nivel_Consultor'].unique()), default=["TODOS"]),
               'Negocio_Projeto': st.multiselect("Negócio", ["TODOS"] + sorted(dados_disponiveis['Negocio_Projeto'].unique()), default=["TODOS"]),
               'Consultor': st.multiselect("Consultor", ["TODOS"] + sorted(dados_disponiveis['Consultor'].unique()), default=["TODOS"])}
df_filtrado = engine.aplicar_filtros(filters)

tab_names = ["Visão Geral", "Análise Dimensional", "Consultores & Projetos", "Fechamento", "Comparativo", "Lançar O.S.", "Assistente IA"]
tabs = st.tabs([f"**{name}**" for name in tab_names])

with tabs[0]: # VISÃO HOLOGRÁFICA
    st.markdown("### <i class='bi bi-infinity'></i> A Visão Consolidada", unsafe_allow_html=True)
    if df_filtrado.empty: st.warning("Nenhum dado para exibir com os filtros atuais.")
    else:
        with st.container():
            st.markdown('<div class="data-hologram">', unsafe_allow_html=True)
            kpis = {'receita': df_filtrado['Receita_Total'].sum(), 'lucro': df_filtrado['Lucro_Total'].sum(),
                    'margem': df_filtrado[df_filtrado['Margem_Percentual'] > 0]['Margem_Percentual'].mean(),
                    'horas_r': df_filtrado['Horas_Realizadas'].sum(), 'horas_p': df_filtrado['Horas_Previstas'].sum()}
            kpis['delta_h'] = kpis['horas_r'] - kpis['horas_p']
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Receita Total", f"R$ {kpis['receita']:,.0f}"); c2.metric("Lucro Total", f"R$ {kpis['lucro']:,.0f}")
            c3.metric("Margem Média", f"{kpis['margem']:.1f}%")
            c4.metric("Horas Realizadas", f"{kpis['horas_r']:.0f}h", f"{kpis['delta_h']:.0f}h vs. Orçado")
            st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]: # ANÁLISE DIMENSIONAL
    st.markdown("### <i class='bi bi-arrows-angle-expand'></i> Mapa de Calor de Performance", unsafe_allow_html=True)
    if not df_filtrado.empty and len(df_filtrado) > 1:
        heatmap_data = df_filtrado.pivot_table(index='Nivel_Consultor', columns='Negocio_Projeto', values='Margem_Percentual', aggfunc='mean').fillna(0)
        if not heatmap_data.empty: st.plotly_chart(px.imshow(heatmap_data, text_auto='.1f', aspect="auto"), use_container_width=True)

with tabs[2]: # CONSULTORES E PROJETOS
    st.markdown("### <i class='bi bi-people-fill'></i> Observatório de Performance", unsafe_allow_html=True)
    if not df_filtrado.empty:
        st.dataframe(df_filtrado[['Consultor', 'Nivel_Consultor', 'Projeto', 'Cliente', 'Receita_Total', 'Lucro_Total', 'Margem_Percentual']].style.format(formatter={'Receita_Total': 'R$ {:,.2f}', 'Lucro_Total': 'R$ {:,.2f}', 'Margem_Percentual': '{:.1f}%'}), use_container_width=True)

with tabs[3]: # FECHAMENTO
    st.markdown("### <i class='bi bi-calculator-fill'></i> Fechamento Financeiro", unsafe_allow_html=True)
    if not df_filtrado.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("💰 A Pagar (Consultores)"); df_pagar = df_filtrado.groupby(['Consultor', 'Nivel_Consultor'])[['Custo_Total', 'Horas_Previstas', 'Horas_Realizadas']].sum().reset_index()
            st.dataframe(df_pagar.style.format(formatter={'Custo_Total': 'R$ {:,.2f}'}), use_container_width=True)
            output = io.BytesIO(); df_pagar.to_excel(output, index=False); st.download_button("📥 Exportar (A Pagar)", output.getvalue(), "a_pagar.xlsx")
        with c2:
            st.subheader("💳 A Receber (Clientes)"); df_receber = df_filtrado.groupby('Cliente')[['Receita_Total', 'Horas_Previstas', 'Horas_Realizadas']].sum().reset_index()
            st.dataframe(df_receber.style.format(formatter={'Receita_Total': 'R$ {:,.2f}'}), use_container_width=True)
            output = io.BytesIO(); df_receber.to_excel(output, index=False); st.download_button("📥 Exportar (A Receber)", output.getvalue(), "a_receber.xlsx")

with tabs[4]: # COMPARATIVO
    st.markdown("### <i class='bi bi-subtract'></i> Análise Comparativa com Diagnóstico IA", unsafe_allow_html=True)
    anos = sorted(engine.dados_originais['Ano'].unique()); meses = sorted(engine.dados_originais['Mes'].unique())
    c1, c2 = st.columns(2)
    with c1: st.subheader("Período 1"); ano1 = st.selectbox("Ano 1", anos, key="ano1"); mes1 = st.selectbox("Mês 1", meses, key="mes1")
    with c2: st.subheader("Período 2"); ano2 = st.selectbox("Ano 2", anos, index=0, key="ano2"); mes2 = st.selectbox("Mês 2", meses, index=min(1, len(meses)-1), key="mes2")
    if st.button("🔍 Calcular Ressonância", use_container_width=True):
        p1 = engine.dados_originais[(engine.dados_originais['Ano']==ano1) & (engine.dados_originais['Mes']==mes1)]
        p2 = engine.dados_originais[(engine.dados_originais['Ano']==ano2) & (engine.dados_originais['Mes']==mes2)]
        if not p1.empty and not p2.empty:
            st.markdown('<div class="narrative-box">', unsafe_allow_html=True)
            st.subheader("A História dos Dados (Análise do Maestro)")
            with st.spinner("O Maestro está realizando a biópsia dos dados..."):
                time.sleep(1.5) # Efeito dramático
                st.write(engine.diagnosticar_e_narrar_variacao(p1, p2, f"{mes1}/{ano1}", f"{mes2}/{ano2}"))
            st.markdown('</div>', unsafe_allow_html=True)
        else: st.warning("Um dos períodos selecionados não contém dados.")

with tabs[5]: # LANÇAR O.S.
    st.markdown("### <i class='bi bi-mic-fill'></i> O Ouvido do Maestro: Lançamento de O.S.", unsafe_allow_html=True)
    st.write("Digite o comando como se estivesse falando. A IA irá extrair as informações-chave.")
    
    comando = st.text_input("Sua Intenção:", placeholder="Ex: Lançar 80 horas para Rafael Oliveira no projeto de PMO do cliente Autozone")
    
    if comando:
        parsed = os_processor.parse_command(comando)
        st.write("#### O Maestro entendeu:")
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='entity-box'><b>Consultor:</b><br>{parsed['consultor'] or 'Não encontrado'}</div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='entity-box'><b>Cliente:</b><br>{parsed['cliente'] or 'Não encontrado'}</div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='entity-box'><b>Horas:</b><br>{parsed['horas'] or 'Não encontrado'}</div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='entity-box'><b>Projeto:</b><br>{parsed['projeto']}</div>", unsafe_allow_html=True)
        
        if all(parsed.values()):
            if st.button("🚀 Confirmar e Lançar O.S.", use_container_width=True, type="primary"):
                st.success(f"O.S. de {parsed['horas']}h para {parsed['consultor']} no projeto {parsed['projeto']} do cliente {parsed['cliente']} lançada com sucesso!")
                st.balloons()

with tabs[6]: # ASSISTENTE IA
    st.markdown("### <i class='bi bi-stars'></i> O Oráculo Preditivo", unsafe_allow_html=True)
    st.markdown('<div class="narrative-box">', unsafe_allow_html=True)
    st.subheader("💡 Feed de Prescrições Vivas")
    st.markdown(f"*Insights gerados a partir de **{len(df_filtrado)}** registros ressonantes...*")
    insights = engine.gerar_insights_prescritivos(df_filtrado)
    for insight in insights:
        st.markdown(f'<div class="{insight["tipo"]}-card">{insight["texto"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)