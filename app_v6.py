import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import random
import io
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

warnings.filterwarnings('ignore')

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Maestro Farol - Quantum Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PREMIUM ---
st.markdown("""
<style>
/* ... (Base CSS mantida e refinada) ... */
.stApp {
    background-color: #0a0e1a;
}

/* ESTILO DO HEADER PREMIUM */
.header-premium {
    background: linear-gradient(135deg, #1e2a52 0%, #3b1d5a 100%);
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 25px;
    border: 1px solid rgba(79, 195, 247, 0.3);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}
.logo-maestro {
    font-size: 2.5em;
    font-weight: bold;
    color: #ffffff;
    text-shadow: 0 0 10px rgba(79, 195, 247, 0.7);
}
.tagline {
    color: #b0c4de;
    font-style: italic;
    font-size: 1.1em;
}

/* ESTILO PARA O PAINEL EXECUTIVO (CEO Dashboard) */
.ceo-dashboard {
    background: rgba(10, 14, 26, 0.8);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 20px;
    border: 1px solid rgba(79, 195, 247, 0.2);
    box-shadow: 0 8px 32px rgba(79, 195, 247, 0.1);
}

/* NOVO: ÍNDICE DE SAÚDE QUÂNTICA */
.quantum-health-card {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 50%;
    width: 200px;
    height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: 2px solid;
    margin: auto;
    transition: all 0.5s ease;
}
.quantum-health-score {
    font-size: 3.5em;
    font-weight: bold;
    color: white;
    text-shadow: 0 0 15px;
}
.quantum-health-title {
    color: #b0c4de;
    font-weight: bold;
}
.status-saudavel { border-color: #4CAF50; box-shadow: 0 0 20px #4CAF50; }
.status-atencao { border-color: #FFD700; box-shadow: 0 0 20px #FFD700; }
.status-critico { border-color: #FF4500; box-shadow: 0 0 20px #FF4500; }
.quantum-health-score.status-saudavel { color: #4CAF50; text-shadow: 0 0 15px #4CAF50; }
.quantum-health-score.status-atencao { color: #FFD700; text-shadow: 0 0 15px #FFD700; }
.quantum-health-score.status-critico { color: #FF4500; text-shadow: 0 0 15px #FF4500; }


/* ESTILO PARA CARDS DE PRESCRIÇÃO (REFINADO) */
.prescription-card {
    background: rgba(255, 255, 255, 0.05);
    border-left: 5px solid;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}
.prescription-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}
.prescription-card.CRÍTICA { border-left-color: #FF4500; }
.prescription-card.ALTA { border-left-color: #FFA500; }
.prescription-card.MÉDIA { border-left-color: #4FC3F7; }
.prescription-card.BAIXA { border-left-color: #4CAF50; }
.prescription-title { color: #ffffff; margin: 10px 0 5px 0; font-weight: bold; }
.prescription-icon { font-size: 1.5em; margin-right: 10px; }


/* ESTILO PARA O SIMULADOR QUÂNTICO */
.simulator-section {
    background: rgba(0, 0, 0, 0.2);
    padding: 25px;
    border-radius: 15px;
    border: 1px solid rgba(79, 195, 247, 0.2);
}
.simulator-results {
    background: rgba(10, 14, 26, 0.9);
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)


# --- DADOS E VARIÁVEIS GLOBAIS (AMPLIADO) ---
consultores = ['RAFAEL OLIVEIRA', 'CLEBER NEVES', 'ADRIANO AFONSO','LEANDRO GONCALVES', 'VALDINER APARECIDO', 'THIAGO MILANÊS']
clientes = ['AUTOZONE', 'TOTVS NOROESTE', 'HYDAC', 'TBC','TOTVS IP', 'TOTVS PAULISTA', 'Investimento']
tipos_proj = ['Implantação ERP', 'Desenvolvimento Customizado', 'Suporte Contínuo', 'Consultoria Estratégica']
niveis = {'RAFAEL OLIVEIRA': 'SÊNIOR', 'CLEBER NEVES': 'PLENO','ADRIANO AFONSO': 'ESPECIALISTA', 'LEANDRO GONCALVES': 'PLENO','VALDINER APARECIDO': 'PLENO', 'THIAGO MILANÊS': 'SÊNIOR'}
complexidades = ['Baixa', 'Média', 'Alta', 'Crítica']
senioridade_exigida = ['JÚNIOR', 'PLENO', 'SÊNIOR', 'ESPECIALISTA']


# --- NÚCLEO DE RACIOCÍNIO QUÂNTICO (CRQ) - VERSÃO PREMIUM ---
class CoreQuantumReasoning:
    def __init__(self):
        self.dados_universo = pd.DataFrame()
        self.estado_quantum = pd.DataFrame()

    def carregar_universo_dados(self):
        # SIMULAÇÃO DE DADOS RICOS (BASEADO NA PLANILHA)
        np.random.seed(42)
        num_registros = 150
        hoje = datetime.now()
        
        df = pd.DataFrame({
            'Consultor': np.random.choice(consultores, num_registros),
            'Cliente': np.random.choice(clientes, num_registros),
            'Projeto': [f'PROJ_{1000+i}' for i in range(num_registros)],
            'TipoProj': np.random.choice(tipos_proj, num_registros),
            'Dt_Inicio_Proj': [hoje - timedelta(days=random.randint(30, 365)) for _ in range(num_registros)],
            'Complexidade': np.random.choice(complexidades, num_registros, p=[0.2, 0.4, 0.3, 0.1]),
            'Senioridade_Exigida': np.random.choice(senioridade_exigida, num_registros, p=[0.1, 0.4, 0.4, 0.1]),
        })

        # Engenharia de Features Avançada
        df['Nivel_Consultor'] = df['Consultor'].map(niveis)
        df['Duracao_Prev_Dias'] = [random.randint(30, 120) for _ in range(num_registros)]
        df['Dt_Fim_Prev'] = df.apply(lambda row: row['Dt_Inicio_Proj'] + timedelta(days=row['Duracao_Prev_Dias']), axis=1)
        
        # Simular Atrasos e Desempenho
        atraso_real = np.random.normal(5, 20, num_registros).clip(-15, 60)
        df['Atraso_Dias'] = atraso_real.astype(int)
        df['Dt_Fim_Real'] = df.apply(lambda row: row['Dt_Fim_Prev'] + timedelta(days=row['Atraso_Dias']), axis=1)

        df['Hrs_Prev'] = df['Duracao_Prev_Dias'] * np.random.uniform(4, 6, num_registros)
        df['Hrs_Real'] = df['Hrs_Prev'] + (df['Atraso_Dias'] * np.random.uniform(4, 6, num_registros))
        
        df['VH_Venda_Base'] = df['Complexidade'].map({'Baixa': 100, 'Média': 130, 'Alta': 160, 'Crítica': 200})
        df['VH_Venda'] = df['VH_Venda_Base'] * np.random.uniform(0.95, 1.1, num_registros)
        df['VH_Custo_Base'] = df['Nivel_Consultor'].map({'PLENO': 70, 'SÊNIOR': 90, 'ESPECIALISTA': 120})
        df['VH_Custo'] = df['VH_Custo_Base'] * np.random.uniform(0.98, 1.05, num_registros)

        df['Receita'] = df['Hrs_Real'] * df['VH_Venda']
        df['Custo'] = df['Hrs_Real'] * df['VH_Custo']
        df['Lucro'] = df['Receita'] - df['Custo']
        df['Margem'] = np.where(df['Receita'] > 0, (df['Lucro'] / df['Receita']) * 100, 0)
        
        df['Data'] = df['Dt_Fim_Real']
        df['Ano'] = df['Data'].dt.year
        df['Mes'] = df['Data'].dt.month

        # Métricas de Performance (Refinadas)
        df['Eficiencia'] = np.where(df['Hrs_Prev'] > 0, (df['Hrs_Real'] / df['Hrs_Prev']) * 100, 100)
        df['ROI_Hora'] = np.where(df['Hrs_Real'] > 0, (df['Receita'] - df['Custo']) / df['Hrs_Real'], 0)

        # Mismatch de Senioridade (Novo)
        map_senioridade = {'JÚNIOR': 1, 'PLENO': 2, 'SÊNIOR': 3, 'ESPECIALISTA': 4}
        df['Num_Senioridade_Exigida'] = df['Senioridade_Exigida'].map(map_senioridade)
        df['Num_Nivel_Consultor'] = df['Nivel_Consultor'].map(map_senioridade)
        df['Mismatch_Senioridade'] = df['Num_Nivel_Consultor'] - df['Num_Senioridade_Exigida']
        
        # Score de Performance (Refinado com novas variáveis)
        df['Score_Risco'] = (
            (np.clip(df['Atraso_Dias'], 0, 60) / 60 * 0.5) +
            (np.clip(-df['Mismatch_Senioridade'], 0, 3) / 3 * 0.5)
        ) * 100
        
        df['Score_Performance'] = (
            (np.clip(df['Margem'], 0, 100) / 100 * 0.4) +
            (np.clip(100 - abs(df['Eficiencia'] - 100), 0, 100) / 100 * 0.2) +
            (np.clip(df['ROI_Hora'] / (df['VH_Venda'] - df['VH_Custo']).mean(), 0, 1.5) / 1.5 * 0.2) +
            ((100 - df['Score_Risco']) / 100 * 0.2)
        ) * 100
        
        self.dados_universo = df.fillna(0)

    def aplicar_colapso_quantico(self, filtros):
        # O "Colapso" é a nossa filtragem, definindo o estado atual para análise
        df = self.dados_universo.copy()
        if filtros.get('consultores') and 'TODOS' not in filtros['consultores']:
            df = df[df['Consultor'].isin(filtros['consultores'])]
        if filtros.get('clientes') and 'TODOS' not in filtros['clientes']:
            df = df[df['Cliente'].isin(filtros['clientes'])]
        if filtros.get('tipos') and 'TODOS' not in filtros['tipos']:
            df = df[df['TipoProj'].isin(filtros['tipos'])]
        if filtros.get('mes') and 'TODOS' not in filtros['mes']:
            df = df[df['Mes'] == filtros['mes']]
        if filtros.get('ano') and 'TODOS' not in filtros['ano']:
            df = df[df['Ano'] == filtros['ano']]
        self.estado_quantum = df
        return df

    # --- NOVAS FUNÇÕES PREMIUM ---
    def calcular_indice_saude_quantica(self):
        df = self.estado_quantum
        if df.empty:
            return 0, "INDETERMINADO", "Sem dados para análise."

        # Ponderação de Fatores Críticos
        margem_media = df['Margem'].mean()
        eficiencia_media = df['Eficiencia'].mean()
        atraso_medio = df['Atraso_Dias'].mean()
        mismatch_medio = df['Mismatch_Senioridade'].mean()

        # Normalização dos scores
        score_margem = np.clip(margem_media / 35, 0, 1.5) # Alvo de margem: 35%
        score_eficiencia = np.clip(1 - abs(eficiencia_media - 100) / 50, 0, 1) # Tolera até 50% de desvio
        score_prazo = np.clip(1 - atraso_medio / 30, 0, 1) # Tolera até 30 dias de atraso médio
        score_alocacao = np.clip(1 - abs(mismatch_medio) / 1.5, 0, 1) # Tolera 1.5 níveis de mismatch
        
        # Pesos da Sinfonia
        peso_margem = 0.4
        peso_eficiencia = 0.2
        peso_prazo = 0.25
        peso_alocacao = 0.15

        indice_final = (score_margem * peso_margem + 
                        score_eficiencia * peso_eficiencia + 
                        score_prazo * peso_prazo + 
                        score_alocacao * peso_alocacao) * 100
        
        indice_final = np.clip(indice_final, 0, 100)

        if indice_final >= 75:
            status = "SAUDÁVEL"
            descricao = "Ressonância positiva. Operação harmônica e lucrativa."
        elif indice_final >= 50:
            status = "ATENÇÃO"
            descricao = "Dissonância moderada. Pontos de melhoria detectados."
        else:
            status = "CRÍTICO"
            descricao = "Risco de colapso. Ações corretivas urgentes são necessárias."

        return int(indice_final), status, descricao

    def gerar_mapa_entrelacamento(self):
        # Visualiza as "ações fantasmagóricas" entre as métricas
        df = self.estado_quantum
        if df.empty or len(df) < 2:
            return None
        
        cols_interesse = ['Margem', 'Atraso_Dias', 'Eficiencia', 'Mismatch_Senioridade', 'ROI_Hora']
        corr_matrix = df[cols_interesse].corr()
        
        fig = go.Figure(data=go.Heatmap(
                   z=corr_matrix,
                   x=corr_matrix.columns,
                   y=corr_matrix.columns,
                   hoverongaps = False,
                   colorscale='RdBu_r',
                   zmin=-1, zmax=1))
        fig.update_layout(
            title='Mapa de Entrelaçamentos (Correlações)',
            template='plotly_dark'
        )
        return fig

    def simular_cenario(self, df_base, alteracoes):
        # O nosso "Simulador de Realidades"
        df_simulado = df_base.copy()
        
        if alteracoes['tipo'] == 'alocacao':
            consultor_alvo = alteracoes['consultor']
            novo_nivel = alteracoes['novo_nivel']
            map_senioridade_rev = {1: 'JÚNIOR', 2: 'PLENO', 3: 'SÊNIOR', 4: 'ESPECIALISTA'}
            
            # Impacto simulado
            df_simulado.loc[df_simulado['Consultor'] == consultor_alvo, 'Nivel_Consultor'] = novo_nivel
            df_simulado['Num_Nivel_Consultor'] = df_simulado['Nivel_Consultor'].map(niveis)
            df_simulado['Mismatch_Senioridade'] = df_simulado['Num_Nivel_Consultor'] - df_simulado['Num_Senioridade_Exigida']
            
            # Simula que um melhor alinhamento reduz o atraso e melhora eficiência
            df_simulado['Atraso_Dias'] -= df_simulado['Mismatch_Senioridade'] * 5 # Cada nível de melhora reduz 5 dias de atraso
            df_simulado['Hrs_Real'] = df_simulado['Hrs_Prev'] + (df_simulado['Atraso_Dias'] * np.random.uniform(4, 6, len(df_simulado)))
            
        elif alteracoes['tipo'] == 'custo':
            variacao = alteracoes['variacao'] / 100
            df_simulado['VH_Custo'] *= (1 + variacao)

        # Recalcula as métricas chave
        df_simulado['Custo'] = df_simulado['Hrs_Real'] * df_simulado['VH_Custo']
        df_simulado['Lucro'] = df_simulado['Receita'] - df_simulado['Custo']
        df_simulado['Margem'] = np.where(df_simulado['Receita'] > 0, (df_simulado['Lucro'] / df_simulado['Receita']) * 100, 0)

        return df_simulado


    def gerar_prescricoes_quantum_premium(self):
        # O "Maestro" que rege a "Interferência Construtiva"
        df = self.estado_quantum
        if df.empty:
            return []
        
        prescricoes = []

        # PRESCRIÇÃO 1: Dissonância de Alocação (Mismatch de Senioridade)
        projetos_mismatch = df[df['Mismatch_Senioridade'] < -1] # Consultor 2+ níveis abaixo do exigido
        if not projetos_mismatch.empty:
            proj_critico = projetos_mismatch.loc[projetos_mismatch['Score_Risco'].idxmax()]
            prescricoes.append({
                'icone': '👥', 'tipo': 'ALOCAÇÃO', 'prioridade': 'CRÍTICA',
                'titulo': 'Dissonância Crítica de Alocação',
                'analise': f"O consultor **{proj_critico['Consultor']} ({proj_critico['Nivel_Consultor']})** está em um projeto de alta complexidade ('{proj_critico['Projeto']}') que exige nível **{proj_critico['Senioridade_Exigida']}**. Este desalinhamento gera um risco sistêmico de atraso ({proj_critico['Atraso_Dias']:.0f} dias) e compromete a margem.",
                'prescricao': "1. **Ação Imediata:** Realocar um consultor Sênior/Especialista para este projeto. \n2. **Ação Estratégica:** Revisar o processo de alocação para cruzar 'Complexidade do Projeto' com 'Nível do Consultor'. \n3. Use o **Simulador Quântico** para prever o impacto da realocação.",
            })

        # PRESCRIÇÃO 2: Projetos em Zona de Colapso (Margem Negativa + Atraso)
        projetos_colapso = df[(df['Margem'] < 15) & (df['Atraso_Dias'] > 20)]
        if not projetos_colapso.empty:
            receita_em_risco = projetos_colapso['Receita'].sum()
            prescricoes.append({
                'icone': '💥', 'tipo': 'RENTABILIDADE', 'prioridade': 'CRÍTICA',
                'titulo': 'Projetos em Rota de Colapso Financeiro',
                'analise': f"Detectamos **{len(projetos_colapso)} projetos** operando com margem crítica (abaixo de 15%) e atrasos significativos (>20 dias). Isso representa **R$ {receita_em_risco:,.2f}** em receita que está destruindo valor.",
                'prescricao': "1. **Comitê de Crise:** Analisar individualmente cada um desses projetos. \n2. **Renegociação:** Iniciar renegociação de escopo/prazo com os clientes envolvidos. \n3. **Controle de Danos:** Avaliar a viabilidade de pausar ou encerrar projetos irrecuperáveis.",
            })

        # PRESCRIÇÃO 3: Oportunidade de Ouro (Mix de Serviços)
        rentabilidade_tipo = df.groupby('TipoProj').agg({'ROI_Hora': 'mean', 'Hrs_Real': 'sum'}).reset_index()
        if len(rentabilidade_tipo) > 1:
            melhor_tipo = rentabilidade_tipo.loc[rentabilidade_tipo['ROI_Hora'].idxmax()]
            pior_tipo = rentabilidade_tipo.loc[rentabilidade_tipo['ROI_Hora'].idxmin()]
            if (melhor_tipo['ROI_Hora'] / pior_tipo['ROI_Hora']) > 2:
                prescricoes.append({
                    'icone': '💎', 'tipo': 'ESTRATÉGIA', 'prioridade': 'ALTA',
                    'titulo': 'Oportunidade de Ouro: Otimização do Mix de Serviços',
                    'analise': f"O serviço de **'{melhor_tipo['TipoProj']}'** gera um ROI/Hora de **R$ {melhor_tipo['ROI_Hora']:.2f}**, sendo 2x mais lucrativo que **'{pior_tipo['TipoProj']}'** (R$ {pior_tipo['ROI_Hora']:.2f}). Atualmente, **{(pior_tipo['Hrs_Real']/df['Hrs_Real'].sum()*100):.0f}%** das horas estão alocadas no serviço menos rentável.",
                    'prescricao': "1. **Foco Comercial:** Direcionar a força de vendas para priorizar contratos de '{melhor_tipo['TipoProj']}'. \n2. **Repricing:** Revisar a precificação dos serviços de '{pior_tipo['TipoProj']}' para aumentar a margem ou desencorajar a venda. \n3. **Upselling:** Criar pacotes que incentivem clientes atuais a migrarem para serviços de maior valor.",
                })

        # PRESCRIÇÃO 4: Risco de Burnout
        carga_consultor = df.groupby('Consultor').agg({'Hrs_Real': 'sum'}).reset_index()
        consultores_sobrecarregados = carga_consultor[carga_consultor['Hrs_Real'] > 180] # Acima de 180h/mês
        if not consultores_sobrecarregados.empty:
            cons_critico = consultores_sobrecarregados.loc[consultores_sobrecarregados['Hrs_Real'].idxmax()]
            prescricoes.append({
                'icone': '🔥', 'tipo': 'PESSOAL', 'prioridade': 'ALTA',
                'titulo': 'Alerta de Burnout: Superposição de Carga de Trabalho',
                'analise': f"O consultor **{cons_critico['Consultor']}** registrou **{cons_critico['Hrs_Real']:.0f} horas**, um volume insustentável que eleva o risco de burnout, queda de qualidade e turnover.",
                'prescricao': "1. **Revisão de Alocação:** Redistribuir projetos ou tarefas de {cons_critico['Consultor']}. \n2. **Contratação:** Avaliar a necessidade de contratação para aliviar a sobrecarga sistêmica. \n3. **Banco de Horas:** Implementar uma política clara de compensação de horas extras.",
            })

        # PRESCRIÇÃO 5: Excelência Operacional
        if not prescricoes:
             prescricoes.append({
                'icone': '✅', 'tipo': 'SUCESSO', 'prioridade': 'BAIXA',
                'titulo': 'Sinfonia em Harmonia: Excelência Operacional',
                'analise': "Nossa análise quântica não detectou dissonâncias ou riscos críticos nos dados atuais. Todos os indicadores sistêmicos estão em ressonância positiva, indicando uma operação saudável, eficiente e lucrativa.",
                'prescricao': "1. **Documentar Boas Práticas:** Identificar os padrões dos projetos de sucesso e transformá-los em metodologia. \n2. **Reconhecimento:** Celebrar os resultados com a equipe para manter o moral elevado. \n3. **Expansão Consciente:** Usar a estabilidade atual como base para explorar novos mercados ou clientes com segurança.",
            })

        return prescricoes

    # Funções auxiliares (mantidas e otimizadas)
    def calcular_metricas_consolidadas(self):
        df = self.estado_quantum
        if df.empty:
            return {'receita': 0, 'custo': 0, 'lucro': 0, 'margem': 0, 'projetos': 0, 'consultores': 0, 'atraso_medio': 0}
        return {
            'receita': df['Receita'].sum(), 'custo': df['Custo'].sum(), 'lucro': df['Lucro'].sum(),
            'margem': df['Margem'].mean(), 'projetos': df['Projeto'].nunique(), 'consultores': df['Consultor'].nunique(),
            'atraso_medio': df['Atraso_Dias'].mean()
        }


# --- INTERFACE STREAMLIT (VERSÃO PREMIUM) ---

# Instância do CRQ
if 'crq' not in st.session_state:
    st.session_state.crq = CoreQuantumReasoning()
    st.session_state.crq.carregar_universo_dados()

crq = st.session_state.crq

# Header
st.markdown('<div class="header-premium"><div class="logo-maestro">🔮 MAESTRO FAROL</div><div class="tagline">A Orquestra de Realidades para a Gestão de Negócios</div></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🧭 Colapso Quântico (Filtros)")
    mes_sel = st.selectbox("📅 Mês", ["TODOS"] + list(range(1, 13)), index=0)
    ano_sel = st.selectbox("📆 Ano", ["TODOS"] + sorted(crq.dados_universo['Ano'].unique().astype(int)), index=0)
    cons_sel = st.multiselect("👥 Consultores", ["TODOS"] + consultores, default=["TODOS"])
    cli_sel = st.multiselect("🏢 Clientes", ["TODOS"] + clientes, default=["TODOS"])
    tipo_sel = st.multiselect("🎯 Tipo de Serviço", ["TODOS"] + tipos_proj, default=["TODOS"])
    
    if st.button("🔄 Reger a Sinfonia (Analisar)", type="primary", use_container_width=True):
        pass # Apenas para forçar o rerun

# Aplicação dos filtros
filtros = {'consultores': cons_sel, 'clientes': cli_sel, 'tipos': tipo_sel, 'mes': mes_sel, 'ano': ano_sel}
df_filtrado = crq.aplicar_colapso_quantico(filtros)
metricas = crq.calcular_metricas_consolidadas()
indice_saude, status_saude, desc_saude = crq.calcular_indice_saude_quantica()
prescricoes = crq.gerar_prescricoes_quantum_premium()

# Abas Principais
tab_executiva, tab_prescritiva, tab_simulador, tab_fechamento, tab_comparativo = st.tabs([
    "🎯 Visão Executiva", 
    "🧠 IA Prescritiva", 
    "🔮 Simulador Quântico",
    "💰 Fechamento",
    "⚖️ Comparativo"
])

# --- ABA 1: VISÃO EXECUTIVA ---
with tab_executiva:
    st.markdown('<div class="ceo-dashboard">', unsafe_allow_html=True)
    
    col_saude, col_kpis = st.columns([1, 2])
    
    with col_saude:
        status_class = f"status-{status_saude.lower()}"
        st.markdown(f"""
        <div class="quantum-health-card {status_class}">
            <div class="quantum-health-title">Saúde Quântica</div>
            <div class="quantum-health-score {status_class}">{indice_saude}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; margin-top: 10px;'><b>{status_saude}</b>: {desc_saude}</p>", unsafe_allow_html=True)

    with col_kpis:
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("💰 Receita Total", f"R$ {metricas['receita']:,.0f}")
        kpi2.metric("📈 Lucro Total", f"R$ {metricas['lucro']:,.0f}")
        kpi3.metric("📊 Margem Média", f"{metricas['margem']:.1f}%")

        kpi4, kpi5, kpi6 = st.columns(3)
        kpi4.metric("📁 Projetos Ativos", f"{metricas['projetos']}")
        kpi5.metric("👥 Consultores Ativos", f"{metricas['consultores']}")
        kpi6.metric("⏳ Atraso Médio (dias)", f"{metricas['atraso_medio']:.1f}")

    st.markdown("---")
    
    col_mapa, col_receita = st.columns(2)

    with col_mapa:
        st.markdown("#### 🌍 Mapa de Entrelaçamentos")
        mapa_fig = crq.gerar_mapa_entrelacamento()
        if mapa_fig:
            st.plotly_chart(mapa_fig, use_container_width=True)
        else:
            st.info("Dados insuficientes para gerar o mapa de entrelaçamentos.")

    with col_receita:
        st.markdown("#### 💰 Receita por Cliente")
        if not df_filtrado.empty:
            fig_rec = px.bar(df_filtrado, x='Cliente', y='Receita', title='', color='TipoProj', template='plotly_dark')
            fig_rec.update_layout(showlegend=False)
            st.plotly_chart(fig_rec, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- ABA 2: IA PRESCRITIVA ---
with tab_prescritiva:
    st.markdown("## 🧠 Oráculo Quântico: Prescrições e Alertas")
    st.info("O Maestro regeu a sinfonia dos dados e estas são as ressonâncias que emergiram. Cada card é uma rota para um futuro ótimo.")
    
    if prescricoes:
        for p in prescricoes:
            st.markdown(f"""
            <div class="prescription-card {p['prioridade']}">
                <h4 class="prescription-title"><span class="prescription-icon">{p['icone']}</span> {p['titulo']}</h4>
                <p><strong>Análise do Maestro:</strong> {p['analise']}</p>
                <p><strong>Prescrição para Ressonância:</strong><br>{p['prescricao']}</p>
                <span style="font-size: 0.8em; color: #aaa; float: right;">TIPO: {p['tipo']} | PRIORIDADE: {p['prioridade']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ Nenhuma dissonância crítica encontrada. A operação está em harmonia.")

# --- ABA 3: SIMULADOR QUÂNTICO ---
with tab_simulador:
    st.markdown("## 🔮 Simulador de Realidades")
    st.markdown('<div class="simulator-section">', unsafe_allow_html=True)
    
    st.write("Aqui, você não prevê o futuro. Você o projeta. Altere as variáveis (os 'qubits') e observe o colapso da função de onda em um novo resultado.")

    sim_tipo = st.radio("Escolha o tipo de simulação:", ('Alocação de Pessoal', 'Variação de Custo'), horizontal=True, label_visibility="collapsed")
    
    alteracoes_sim = {}
    if sim_tipo == 'Alocação de Pessoal':
        col_sim1, col_sim2 = st.columns(2)
        with col_sim1:
            consultor_sim = st.selectbox("Selecione o Consultor", consultores)
        with col_sim2:
            novo_nivel_sim = st.selectbox("Promover/Alterar para Nível", senioridade_exigida, index=2)
        alteracoes_sim = {'tipo': 'alocacao', 'consultor': consultor_sim, 'novo_nivel': novo_nivel_sim}
    
    if sim_tipo == 'Variação de Custo':
        variacao_custo = st.slider("Variação % no Custo/Hora de todos os consultores", -20.0, 20.0, 0.0, 0.5)
        alteracoes_sim = {'tipo': 'custo', 'variacao': variacao_custo}

    if st.button("▶️ Simular Interferência", type="primary", use_container_width=True):
        if df_filtrado.empty:
            st.error("Selecione dados na sidebar antes de simular.")
        else:
            df_simulado = crq.simular_cenario(df_filtrado, alteracoes_sim)
            
            # Métricas Originais
            lucro_orig = df_filtrado['Lucro'].sum()
            margem_orig = df_filtrado['Margem'].mean()
            atraso_orig = df_filtrado['Atraso_Dias'].mean()

            # Métricas Simuladas
            lucro_sim = df_simulado['Lucro'].sum()
            margem_sim = df_simulado['Margem'].mean()
            atraso_sim = df_simulado['Atraso_Dias'].mean()
            
            st.markdown('<div class="simulator-results">', unsafe_allow_html=True)
            st.markdown("<h5>Resultados do Colapso da Simulação:</h5>", unsafe_allow_html=True)
            
            res1, res2, res3 = st.columns(3)
            with res1:
                st.metric("Lucro Total", f"R$ {lucro_sim:,.0f}", f"R$ {lucro_sim - lucro_orig:,.0f}")
            with res2:
                st.metric("Margem Média", f"{margem_sim:.1f}%", f"{margem_sim - margem_orig:.1f} pp")
            with res3:
                st.metric("Atraso Médio", f"{atraso_sim:.1f} dias", f"{atraso_sim - atraso_orig:.1f} d")
            st.markdown('</div>', unsafe_allow_html=True)


    st.markdown('</div>', unsafe_allow_html=True)

# --- ABA 4: FECHAMENTO (Mantida e Refinada) ---
with tab_fechamento:
    # O código desta aba foi mantido, pois a estrutura já era sólida.
    # Pequenos ajustes visuais podem ser feitos se necessário.
    st.markdown("## 💰 Fechamento Operacional")
    if not df_filtrado.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 👥 Por Consultor")
            fech_consultor = df_filtrado.groupby('Consultor').agg(
                Horas_Realizadas=('Hrs_Real', 'sum'),
                Custo_Total=('Custo', 'sum'),
                Receita_Gerada=('Receita', 'sum'),
                Margem_Media=('Margem', 'mean')
            ).reset_index()
            st.dataframe(fech_consultor.style.format({
                'Horas_Realizadas': '{:.0f}h',
                'Custo_Total': 'R$ {:,.2f}',
                'Receita_Gerada': 'R$ {:,.2f}',
                'Margem_Media': '{:.1f}%'
            }), use_container_width=True)

        with col2:
            st.markdown("### 🏢 Por Cliente")
            fech_cliente = df_filtrado.groupby('Cliente').agg(
                Horas_Consumidas=('Hrs_Real', 'sum'),
                Custo_Total=('Custo', 'sum'),
                Receita_Total=('Receita', 'sum'),
                Margem_Media=('Margem', 'mean')
            ).reset_index()
            st.dataframe(fech_cliente.style.format({
                'Horas_Consumidas': '{:.0f}h',
                'Custo_Total': 'R$ {:,.2f}',
                'Receita_Total': 'R$ {:,.2f}',
                'Margem_Media': '{:.1f}%'
            }), use_container_width=True)
    else:
        st.warning("Nenhum dado para o fechamento com os filtros atuais.")


# --- ABA 5: COMPARATIVO (Mantida e Refinada) ---
with tab_comparativo:
    # O código desta aba também foi mantido pela sua utilidade.
    st.markdown("## ⚖️ Comparativo de Realidades (Períodos)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Realidade 1")
        ano1 = st.selectbox("Ano 1", sorted(crq.dados_universo['Ano'].unique().astype(int)), key='ano1')
        mes1 = st.selectbox("Mês 1", list(range(1, 13)), key='mes1')
    with col2:
        st.markdown("##### Realidade 2")
        ano2 = st.selectbox("Ano 2", sorted(crq.dados_universo['Ano'].unique().astype(int)), key='ano2', index=len(sorted(crq.dados_universo['Ano'].unique()))-1)
        mes2 = st.selectbox("Mês 2", list(range(1, 13)), key='mes2', index=datetime.now().month-2)
        
    if st.button("Comparar Realidades", use_container_width=True):
        df1 = crq.dados_universo[(crq.dados_universo['Ano'] == ano1) & (crq.dados_universo['Mes'] == mes1)]
        df2 = crq.dados_universo[(crq.dados_universo['Ano'] == ano2) & (crq.dados_universo['Mes'] == mes2)]
        
        if df1.empty or df2.empty:
            st.error("Um ou ambos os períodos não contêm dados.")
        else:
            m1 = {'receita': df1['Receita'].sum(), 'lucro': df1['Lucro'].sum(), 'margem': df1['Margem'].mean()}
            m2 = {'receita': df2['Receita'].sum(), 'lucro': df2['Lucro'].sum(), 'margem': df2['Margem'].mean()}
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Receita", f"R$ {m2['receita']:,.0f}", f"R$ {m2['receita'] - m1['receita']:,.0f}")
            c2.metric("Lucro", f"R$ {m2['lucro']:,.0f}", f"R$ {m2['lucro'] - m1['lucro']:,.0f}")
            c3.metric("Margem", f"{m2['margem']:.1f}%", f"{m2['margem'] - m1['margem']:.1f} pp")
