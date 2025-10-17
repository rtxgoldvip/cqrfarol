# -*- coding: utf-8 -*-
# MAESTRO QUÂNTICO v4.0 - O Maestro Narrador

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
        box-shadow: 0 0 20px rgba(0, 191, 255, 0.1);
    }
    .narrative-box {
        background: rgba(28, 28, 40, 0.7); border-radius: 15px; padding: 25px;
        border-left: 5px solid #8A2BE2; margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- NÚCLEO DE CONEXÃO E EXTRAÇÃO DE DADOS (VALIDADO) ---
class DataOrchestrator:
    def __init__(self):
        self.conn_str = self._get_conn_str()

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
        # A Super Query validada
        if not PYODBC_AVAILABLE or not self.conn_str: return None
        super_query = """
        SELECT ... (A query completa que já validamos) ...
        """
        try:
            with pyodbc.connect(self.conn_str, timeout=10) as cnxn:
                df = pd.read_sql(super_query, cnxn)
            return df
        except Exception: return None

# --- MOTOR DE ANÁLISE QUÂNTICO v4.0 (COM IA NARRATIVA) ---
class QuantumAnalyticsEngine:
    def __init__(self):
        self.dados_originais = self._load_data()
        self.dados_filtrados = self.dados_originais.copy()

    def _load_data(self):
        # ... (código do _load_data, usando o mock enriquecido se a conexão falhar)
        # CORREÇÃO: Removendo o erro de indentação.
        pass

    def _processar_dados(self, df):
        # ... (código de processamento de dados)
        pass

    def _create_mock_data(self):
        # ... (código do mock de dados enriquecido)
        pass

    def aplicar_filtros(self, filters):
        # ... (código para aplicar filtros)
        pass
        
    def gerar_insights_prescritivos(self, df):
        # ... (código da IA prescritiva da v3.0)
        pass

    def diagnosticar_e_narrar_variacao(self, p1, p2, periodo1_nome, periodo2_nome):
        if p1.empty or p2.empty:
            return "Dados insuficientes para um dos períodos para gerar uma narrativa."

        lucro1, lucro2 = p1['Lucro_Total'].sum(), p2['Lucro_Total'].sum()
        variacao_lucro = ((lucro2 - lucro1) / lucro1) * 100 if lucro1 != 0 else float('inf')

        if abs(variacao_lucro) < 2:
            return f"A performance de lucro entre {periodo1_nome} e {periodo2_nome} manteve-se estável, com uma variação mínima de {variacao_lucro:.1f}%. A estratégia atual demonstra consistência."

        direcao = "aumento" if variacao_lucro > 0 else "redução"
        narrativa = f"Observou-se um(a) **{direcao} de {abs(variacao_lucro):.1f}% no lucro** em {periodo2_nome} em comparação com {periodo1_nome}. "
        
        # Diagnóstico Causa-Raiz
        receita1, receita2 = p1['Receita_Total'].sum(), p2['Receita_Total'].sum()
        custo1, custo2 = p1['Custo_Total'].sum(), p2['Custo_Total'].sum()

        if abs((receita2 - receita1) / receita1 if receita1 else 0) > abs((custo2 - custo1) / custo1 if custo1 else 0):
            narrativa += "O principal motor dessa variação foi o **comportamento da receita**. "
        else:
            narrativa += "O principal motor dessa variação foi a **gestão de custos**. "
        
        # Análise de Mix de Negócio
        mix_negocio1 = p1['Negocio_Projeto'].value_counts(normalize=True)
        mix_negocio2 = p2['Negocio_Projeto'].value_counts(normalize=True)
        mudanca_mix = (mix_negocio2 - mix_negocio1).abs().sum() > 0.1 # Mudança de mais de 10%
        
        if mudanca_mix:
            negocio_aumento = (mix_negocio2 - mix_negocio1).idxmax()
            narrativa += f"Uma análise mais profunda revela uma **mudança no mix de negócios**, com um aumento significativo em projetos do tipo **'{negocio_aumento}'**. "

        narrativa += f"**Prescrição:** Recomenda-se investigar os projetos dentro de '{negocio_aumento}' para replicar os sucessos (se o lucro aumentou) ou mitigar os riscos (se o lucro caiu)."
        return narrativa

# --- INICIALIZAÇÃO ---
@st.cache_resource
def init_engine():
    return QuantumAnalyticsEngine()

engine = init_engine()

# --- INTERFACE PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>MAESTRO QUÂNTICO</h1>", unsafe_allow_html=True)

# ... (Código da Sidebar para filtros) ...

df_filtrado = engine.aplicar_filtros(filters)

# --- ESTRUTURA DE ABAS COMPLETA ---
tab_names = ["Visão Geral", "Análise Dimensional", "Consultores & Projetos", "Fechamento", "Comparativo", "Simulador", "Assistente IA"]
tabs = st.tabs([f"**{name}**" for name in tab_names])

# ... (Código das abas Visão Geral, Análise Dimensional, Consultores, Fechamento) ...

# Tab 5: Comparativo (COM IA NARRATIVA)
with tabs[4]:
    st.header("Análise Comparativa com Diagnóstico IA")
    c1, c2 = st.columns(2)
    # ... (Seleção dos períodos 1 e 2) ...

    p1 = engine.dados_originais[(engine.dados_originais['Ano']==ano1) & (engine.dados_originais['Mes']==mes1)]
    p2 = engine.dados_originais[(engine.dados_originais['Ano']==ano2) & (engine.dados_originais['Mes']==mes2)]

    if p1.empty or p2.empty:
        st.warning("Um dos períodos selecionados não contém dados.")
    else:
        # Métricas visuais
        # ... (código dos st.metric) ...
        
        # A Nova IA em Ação
        st.markdown('<div class="narrative-box">', unsafe_allow_html=True)
        st.subheader("A História dos Dados (Análise do Maestro)")
        with st.spinner("O Maestro está analisando a partitura dos períodos..."):
            narrativa_gerada = engine.diagnosticar_e_narrar_variacao(p1, p2, f"{mes1}/{ano1}", f"{mes2}/{ano2}")
            st.write(narrativa_gerada)
        st.markdown('</div>', unsafe_allow_html=True)

# ... (Código das abas Simulador e Assistente IA) ...
# ... (Removi o Apontamento por Voz para focar nas funcionalidades principais, podemos reativar depois) ...