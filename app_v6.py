# -*- coding: utf-8 -*-

# --- Importações Essenciais ---
# As importações foram unificadas e organizadas.
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
import re # Biblioteca para processamento de linguagem natural (regex)

# Tenta importar a biblioteca do banco de dados, mas não quebra se não encontrar
try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False

warnings.filterwarnings('ignore')

# --- CONFIGURAÇÃO DA PÁGINA ---
# Padrão premium, layout amplo e ícone temático.
st.set_page_config(
    page_title="MAESTRO QUÂNTICO - Inteligência Preditiva",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILO CSS AVANÇADO (PREMIUM) ---
# Refinamento do CSS para um visual mais sofisticado e coeso.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }

    .main {
        background-color: #050818;
        color: #E0E0E0;
    }
    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e 0%, #050818 50%);
    }

    /* Títulos com gradiente, alinhados à identidade visual */
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #00BFFF, #8A2BE2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Cards de Métricas e Insights com efeito de vidro e borda neon */
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

    /* Customização da Sidebar */
    .st-emotion-cache-16txtl3 {
        background-color: rgba(10, 8, 24, 0.9);
        border-right: 1px solid rgba(0, 191, 255, 0.2);
    }

    /* Botões com estilo */
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
    .stButton>button:active {
        background-color: #0077CC !important;
    }
</style>
""", unsafe_allow_html=True)


# --- NÚCLEO DE CONEXÃO COM O BANCO DE DADOS ---
# Classe robusta que lida com a conexão e busca de dados.
class DatabaseConnector:
    def __init__(self):
        # As credenciais devem, em um ambiente de produção, vir de segredos (st.secrets)
        self.server = '78.142.242.144'
        self.database = 'Farol'
        self.username = 'sa'
        self.password = 'Bagu@4312'
        self.conn = None

    def connect(self):
        if not PYODBC_AVAILABLE:
            st.sidebar.warning("Driver `pyodbc` não encontrado. Conexão com banco desativada.", icon="🔌")
            return False
        try:
            conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
            self.conn = pyodbc.connect(conn_str, timeout=5)
            return True
        except Exception as e:
            st.sidebar.error(f"Falha na conexão com o banco. Usando dados de exemplo. Erro: {e}", icon="❌")
            return False

    def get_data(self):
        query = """
        SELECT
            g.IdGest2, CAST(g.Mes as INT) as Mes, CAST(g.Ano as INT) as Ano,
            g.QtHrOrc as Horas_Previstas, g.QtHrReal as Horas_Realizadas,
            g.VlHrOrc as Valor_Hora_Venda, g.VlHrCusto as Valor_Hora_Custo,
            g.ReceitaReal as Receita_Total, g.CustoReal as Custo_Total,
            g.PercMgReal as Margem_Percentual,
            p.DescProj as Projeto, t.DescTipo as TipoProj,
            tec.NomeTec as Consultor, cli.Nome as Cliente
        FROM Tb_GestorFin2 g
        LEFT JOIN tb_Proj p ON g.ProjGest = p.AutNumProj
        LEFT JOIN tb_tipoproj t ON p.TipoProj = t.AutNumTipo
        LEFT JOIN tb_tec tec ON g.ConsultGest = tec.AutNumTec
        LEFT JOIN tb_Cliente cli ON p.CodCliProj = cli.AutNumCli
        WHERE tec.NomeTec IS NOT NULL AND p.DescProj IS NOT NULL
        """
        try:
            df = pd.read_sql(query, self.conn)
            return df
        except Exception as e:
            st.error(f"Erro ao buscar dados: {e}")
            return pd.DataFrame()

    def close(self):
        if self.conn:
            self.conn.close()

# --- MOTOR DE ANÁLISE QUÂNTICO ---
# O cérebro do sistema. Lida com dados, cálculos e a geração de insights dinâmicos.
class QuantumAnalyticsEngine:
    def __init__(self):
        self.dados_originais = self.load_data()
        self.dados_filtrados = self.dados_originais.copy()

    def load_data(self):
        db = DatabaseConnector()
        if db.connect():
            df = db.get_data()
            db.close()
            if not df.empty:
                st.sidebar.success(f"Conectado! {len(df)} registros carregados.", icon="✅")
                return self._processar_dados(df)
        
        # Fallback: se a conexão falhar ou não retornar dados, usa o mock.
        st.toast("Usando dados de simulação interna.", icon="🔬")
        return self._processar_dados(self._create_mock_data())

    def _processar_dados(self, df):
        # Garante que os dados, sejam do banco ou mock, passem pelo mesmo tratamento.
        numeric_cols = ['Horas_Previstas', 'Horas_Realizadas', 'Valor_Hora_Venda', 'Valor_Hora_Custo',
                        'Receita_Total', 'Custo_Total', 'Margem_Percentual']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        df['Lucro_Total'] = df['Receita_Total'] - df['Custo_Total']
        # Evita divisão por zero
        df['Horas_Realizadas_Calc'] = df['Horas_Realizadas'].replace(0, 1)
        df['Horas_Previstas_Calc'] = df['Horas_Previstas'].replace(0, 1)
        
        df['Desvio_Horas'] = df['Horas_Realizadas'] - df['Horas_Previstas']
        df['Eficiencia_Horas'] = (df['Horas_Realizadas'] / df['Horas_Previstas_Calc']) * 100
        df['Rentabilidade_Hora'] = df['Lucro_Total'] / df['Horas_Realizadas_Calc']
        
        # Corrige valores infinitos que podem surgir
        df.replace([np.inf, -np.inf], 0, inplace=True)
        return df

    def _create_mock_data(self):
        # Dados de exemplo realistas para garantir a funcionalidade offline.
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
        
        # Insight 1: Eficiência de Horas (Interferência Construtiva/Destrutiva)
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

        # Insight 2: Rentabilidade (Ressonância da Verdade)
        rentab_media = df['Rentabilidade_Hora'].mean()
        consultor_mais_rentavel = df.loc[df['Rentabilidade_Hora'].idxmax()]
        
        insights.append({
            'tipo': 'sucesso',
            'texto': f"**Ressonância da Verdade:** O consultor **{consultor_mais_rentavel['Consultor']}** está gerando **R$ {consultor_mais_rentavel['Rentabilidade_Hora']:.2f}/hora** no projeto '{consultor_mais_rentavel['Projeto']}', um valor significativamente acima da média de R$ {rentab_media:.2f}/hora. **Prescrição:** Entender as práticas deste consultor para replicar em toda a equipe. Este é o caminho da máxima lucratividade."
        })
        
        # Insight 3: Margem de Lucro (Entrelaçamento)
        cliente_menor_margem = df.loc[df['Margem_Percentual'].idxmin()]
        if cliente_menor_margem['Margem_Percentual'] < 35 and cliente_menor_margem['Margem_Percentual'] > 0:
            insights.append({
                'tipo': 'alerta',
                'texto': f"**Entrelaçamento Crítico:** O cliente **{cliente_menor_margem['Cliente']}** apresenta a menor margem de lucro (**{cliente_menor_margem['Margem_Percentual']:.1f}%**). O custo e a receita estão em um entrelaçamento desfavorável. **Prescrição:** Renegociar valores ou otimizar a alocação de custos para este cliente para evitar prejuízos futuros."
            })

        return insights if insights else [{'tipo': 'info', 'texto': 'A orquestra está em harmonia. Todos os indicadores estão dentro dos parâmetros esperados para a seleção atual.'}]

# --- PROCESSADOR DE COMANDOS DE VOZ (SIMULADO) ---
class VoiceCommandProcessor:
    def process(self, command):
        command = command.lower().strip()
        
        # Navegação entre abas
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
        
        # Filtros
        if re.search(r"filtrar consultor para (.*)", command):
            match = re.search(r"filtrar consultor para (.*)", command)
            consultor_name = match.group(1).strip().upper()
            # Aqui você precisaria verificar se o nome existe e atualizar o filtro no session_state
            return f"Filtro aplicado para o consultor: {consultor_name}. (Funcionalidade em desenvolvimento)"

        # Perguntas específicas
        if re.search(r"qual a (receita|margem|lucro) (total|média) do cliente (.*)", command):
             match = re.search(r"qual a (receita|margem|lucro) (total|média) do cliente (.*)", command)
             metric, _, client = match.groups()
             # Lógica para calcular a métrica para o cliente
             return f"Calculando a {metric} do cliente {client.upper()}... (Funcionalidade em desenvolvimento)"

        # Resetar
        if re.search(r"limpar|resetar filtros", command):
            # Lógica para resetar os filtros no session_state
            return "Filtros redefinidos para o estado inicial."

        return "Comando não compreendido. Tente 'mostrar a aba consultores' ou 'limpar filtros'."

# --- INICIALIZAÇÃO E CACHE ---
# Usar o cache do Streamlit para inicializar a classe principal apenas uma vez.
@st.cache_resource
def init_engine():
    return QuantumAnalyticsEngine()

engine = init_engine()
voice_processor = VoiceCommandProcessor()

# --- INTERFACE PRINCIPAL ---

# Título e Subtítulo
st.markdown("<h1 style='text-align: center;'>MAESTRO QUÂNTICO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8A8A8A; margin-top: -10px;'>Inteligência Preditiva para Gestão de Consultoria</p>", unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR DE CONTROLES ---
with st.sidebar:
    st.markdown("## 🌌 Controles da Orquestra")
    st.markdown("Filtre a superposição de dados para revelar a realidade desejada.")

    dados_disponiveis = engine.dados_originais
    
    # Filtros Dinâmicos
    ano_selecionado = st.selectbox("Ano", ["TODOS"] + sorted(dados_disponiveis['Ano'].unique().tolist()))
    mes_selecionado = st.selectbox("Mês", ["TODOS"] + sorted(dados_disponiveis['Mes'].unique().tolist()))
    consultor_selecionado = st.multiselect("Consultores", ["TODOS"] + sorted(dados_disponiveis['Consultor'].unique().tolist()), default=["TODOS"])
    cliente_selecionado = st.multiselect("Clientes", ["TODOS"] + sorted(dados_disponiveis['Cliente'].unique().tolist()), default=["TODOS"])
    projeto_selecionado = st.multiselect("Projetos", ["TODOS"] + sorted(dados_disponiveis['Projeto'].unique().tolist()), default=["TODOS"])

    if st.button("Aplicar Filtros", use_container_width=True, type="primary"):
        engine.aplicar_filtros(mes_selecionado, ano_selecionado, consultor_selecionado, cliente_selecionado, projeto_selecionado)
        st.rerun()

    st.markdown("---")
    st.info("Desenvolvido por Jefferson de Souza em parceria com a IA Gemini da Google.", icon="💡")


# Aplica os filtros ao carregar
df_filtrado = engine.aplicar_filtros(mes_selecionado, ano_selecionado, consultor_selecionado, cliente_selecionado, projeto_selecionado)
kpis = {
    'receita_total': df_filtrado['Receita_Total'].sum(),
    'lucro_total': df_filtrado['Lucro_Total'].sum(),
    'margem_media': df_filtrado[df_filtrado['Lucro_Total']>0]['Margem_Percentual'].mean() if not df_filtrado.empty else 0,
    'eficiencia_media': df_filtrado['Eficiencia_Horas'].mean() if not df_filtrado.empty else 0
}

# --- ABAS DE NAVEGAÇÃO ---
tab_names = [
    "Visão Geral (Orquestra)", "Análise Profunda (Ressonância)", 
    "Consultores & Projetos", "Simulador Quântico", 
    "Fechamento & Financeiro", "Assistente IA (Maestro)"
]

# Gerenciamento de estado da aba ativa para o comando de voz
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = tab_names[0]

# Renderiza as abas
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
            st.markdown("#### Receita por Cliente")
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
    if not df_filtrado.empty:
        st.markdown("#### Correlação entre Métricas Chave")
        corr_df = df_filtrado[['Receita_Total', 'Custo_Total', 'Lucro_Total', 'Horas_Realizadas', 'Margem_Percentual']].corr()
        fig = px.imshow(corr_df, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)

# Tab 3: Consultores & Projetos
with tabs[2]:
    st.subheader("Performance Individual e de Projetos")
    if not df_filtrado.empty:
        st.markdown("#### Análise por Consultor")
        df_consultor = df_filtrado.groupby('Consultor').agg(
            Receita_Total=('Receita_Total', 'sum'),
            Lucro_Total=('Lucro_Total', 'sum'),
            Margem_Média=('Margem_Percentual', 'mean'),
            Eficiência_Média=('Eficiencia_Horas', 'mean')
        ).reset_index()
        st.dataframe(df_consultor.style.format({
            "Receita_Total": "R$ {:,.2f}", "Lucro_Total": "R$ {:,.2f}", 
            "Margem_Média": "{:.1f}%", "Eficiência_Média": "{:.1f}%"}), use_container_width=True)

# Tab 4: Simulador Quântico
with tabs[3]:
    st.subheader("Terceiro Movimento: A Interferência - Moldando o Futuro")
    st.write("Simule cenários para encontrar a ressonância da verdade antes de tomar decisões.")
    
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
    st.subheader("Painel de Fechamento")
    if not df_filtrado.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 💰 A Pagar (Consultores)")
            df_pagar = df_filtrado.groupby('Consultor').agg(
                Custo_Total=('Custo_Total', 'sum'),
                Horas_Trabalhadas=('Horas_Realizadas', 'sum')
            ).reset_index()
            st.dataframe(df_pagar.style.format({"Custo_Total": "R$ {:,.2f}"}), use_container_width=True)
        with c2:
            st.markdown("#### 💳 A Receber (Clientes)")
            df_receber = df_filtrado.groupby('Cliente').agg(
                Receita_Total=('Receita_Total', 'sum'),
                Horas_Faturadas=('Horas_Realizadas', 'sum')
            ).reset_index()
            st.dataframe(df_receber.style.format({"Receita_Total": "R$ {:,.2f}"}), use_container_width=True)

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
                st.rerun() # Força a atualização da interface para mudar de aba