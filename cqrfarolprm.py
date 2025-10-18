# -*- coding: utf-8 -*-
# MAESTRO QUÂNTICO v8.1 - Versão Corrigida

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
import io
import time
import re
from datetime import datetime, timedelta
import json
from io import BytesIO

try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False

warnings.filterwarnings('ignore')

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="MAESTRO QUÂNTICO | Diagnóstico Dinâmico", 
    page_icon="🌌", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- ESTILO CSS SIMPLIFICADO ---
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0c0c2e 0%, #1a1a3e 50%, #0c0c2e 100%);
        color: #ffffff;
    }
    
    .header-glow {
        background: linear-gradient(90deg, #0066ff 0%, #00ccff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1.5rem;
        font-size: 2.8rem;
    }
    
    .quantum-card {
        background: rgba(20, 25, 60, 0.7);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(0, 204, 255, 0.2);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-card {
        background: rgba(15, 20, 45, 0.8);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(0, 204, 255, 0.1);
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00ccff, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #a0a0c0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# --- NÚCLEO QUÂNTICO SIMPLIFICADO ---
class QuantumAnalysisEngine:
    def __init__(self):
        self.dados_originais = self._carregar_dados_reais()
        self.dados_filtrados = self.dados_originais.copy()
        
    def _carregar_dados_reais(self):
        """Carrega dados do arquivo Excel fornecido"""
        try:
            df = pd.read_excel('dados_maestro_extraidos.xlsx', sheet_name='DadosMaestro')
            return self._processar_dados_avancado(df)
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return self._criar_dados_demonstracao()
    
    def _processar_dados_avancado(self, df):
        """Processamento avançado dos dados"""
        numeric_cols = ['Horas_Previstas', 'Horas_Realizadas', 'Receita_Total', 'Custo_Total', 'Margem_Percentual']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Métricas avançadas
        df['Lucro_Total'] = df['Receita_Total'] - df['Custo_Total']
        df['Eficiencia_Horas'] = np.where(
            df['Horas_Previstas'] > 0, 
            df['Horas_Realizadas'] / df['Horas_Previstas'], 
            1
        )
        df['Ticket_Medio_Hora'] = np.where(
            df['Horas_Realizadas'] > 0,
            df['Receita_Total'] / df['Horas_Realizadas'],
            0
        )
        
        # Preencher valores ausentes
        for col in ['Nivel_Consultor', 'Negocio_Projeto', 'Status_Projeto', 'Consultor']:
            df[col] = df[col].fillna('Não Definido')
            
        return df
    
    def _criar_dados_demonstracao(self):
        """Cria dados de demonstração"""
        st.warning("🔬 Modo de Demonstração Ativo")
        meses = list(range(1, 13))
        data = []
        
        for mes in meses:
            for _ in range(15):
                data.append({
                    'Mes': mes, 'Ano': 2024,
                    'Consultor': np.random.choice(['ADRIANO AFONSO', 'ALYNE CAMPOS', 'AUGUSTO KREJCI', 'CLEBER NEVES']),
                    'Nivel_Consultor': np.random.choice(['SENIOR', 'ESPECIALISTA']),
                    'Cliente': 'TOTVS IP',
                    'Projeto': 'ALOCAÇÃO DE RECURSOS',
                    'Negocio_Projeto': 'OUTSOURCING - LOCAÇÃO',
                    'Status_Projeto': 'EM ABERTO',
                    'Horas_Previstas': abs(np.random.normal(120, 30)),
                    'Horas_Realizadas': abs(np.random.normal(125, 35)),
                    'Receita_Total': abs(np.random.normal(15000, 4000)),
                    'Custo_Total': abs(np.random.normal(9000, 2000)),
                    'Margem_Percentual': np.random.normal(0.35, 0.1)
                })
        
        df = pd.DataFrame(data)
        df['Lucro_Total'] = df['Receita_Total'] - df['Custo_Total']
        return df
    
    def aplicar_filtros(self, filters):
        """Aplica filtros aos dados"""
        df = self.dados_originais.copy()
        
        for key, value in filters.items():
            if value and value != "TODOS" and value != ["TODOS"]:
                if isinstance(value, list):
                    df = df[df[key].isin(value)]
                else:
                    df = df[df[key] == value]
        
        self.dados_filtrados = df
        return df
    
    def executar_diagnostico_quantico(self, df):
        """Executa diagnóstico quântico completo"""
        diagnosticos = []
        alertas = []
        
        if df.empty:
            return diagnosticos, alertas
        
        # ANÁLISE DE MARGENS
        margens_negativas = df[df['Margem_Percentual'] < 0]
        if not margens_negativas.empty:
            perda_total = margens_negativas['Lucro_Total'].sum()
            alertas.append({
                'nivel': 'CRITICO',
                'titulo': 'MARGENS NEGATIVAS DETECTADAS',
                'descricao': f'{len(margens_negativas)} projetos com margem negativa',
                'impacto': f'Perda: R$ {abs(perda_total):,.0f}',
                'acao_imediata': 'Revisar custos e renegociar contratos'
            })
        
        # ANÁLISE DE CONCENTRAÇÃO
        top_cliente_receita = df.groupby('Cliente')['Receita_Total'].sum().nlargest(1)
        concentracao = top_cliente_receita.iloc[0] / df['Receita_Total'].sum()
        
        if concentracao > 0.4:
            alertas.append({
                'nivel': 'ALTO',
                'titulo': 'CONCENTRAÇÃO DE RISCO',
                'descricao': f'{top_cliente_receita.index[0]} representa {concentracao:.1%} da receita',
                'impacto': 'Risco operacional elevado',
                'acao_imediata': 'Diversificar portfólio de clientes'
            })
        
        # ANÁLISE DE EFICIÊNCIA
        eficiencia_media = df['Eficiencia_Horas'].mean()
        if eficiencia_media > 1.2:
            diagnosticos.append({
                'tipo': 'OPERACIONAL',
                'titulo': 'SUPERALOCAÇÃO DE HORAS',
                'descricao': f'Eficiência média de {eficiencia_media:.2f}x - horas realizadas excedem as previstas',
                'prescricao': 'Implementar controle rigoroso de escopo'
            })
        elif eficiencia_media < 0.8:
            diagnosticos.append({
                'tipo': 'OPERACIONAL', 
                'titulo': 'SUBUTILIZAÇÃO DE RECURSOS',
                'descricao': f'Eficiência média de {eficiencia_media:.2f}x - capacidade ociosa detectada',
                'prescricao': 'Otimizar alocação e buscar novos projetos'
            })
        
        return diagnosticos, alertas
    
    def _calcular_metricas_chave(self, df):
        """Calcula métricas-chave para dashboard"""
        return {
            'receita_total': df['Receita_Total'].sum(),
            'lucro_total': df['Lucro_Total'].sum(),
            'margem_media': df['Margem_Percentual'].mean(),
            'eficiencia_media': df['Eficiencia_Horas'].mean(),
            'ticket_medio': df['Ticket_Medio_Hora'].mean(),
            'projetos_ativos': len(df),
            'clientes_ativos': df['Cliente'].nunique()
        }

# --- SISTEMA DE COMANDO SIMPLIFICADO ---
class VoiceCommandSystem:
    def __init__(self):
        self.commands = {
            'lançar horas': self.lancar_horas,
            'novo projeto': self.novo_projeto,
            'status geral': self.status_geral
        }
    
    def processar_comando(self, comando):
        comando = comando.lower()
        for cmd, funcao in self.commands.items():
            if cmd in comando:
                return funcao(comando)
        return "Comando não reconhecido"
    
    def lancar_horas(self, comando):
        return "Sistema de lançamento de horas ativado"
    
    def novo_projeto(self, comando):
        return "Criando novo projeto..."
    
    def status_geral(self, comando):
        return "Gerando relatório de status geral..."

# --- INICIALIZAÇÃO DO SISTEMA ---
@st.cache_resource
def init_quantum_engine():
    return QuantumAnalysisEngine()

@st.cache_resource
def init_voice_system():
    return VoiceCommandSystem()

engine = init_quantum_engine()
voice_system = init_voice_system()

# --- INTERFACE PRINCIPAL ---
st.markdown("<h1 class='header-glow'>MAESTRO QUÂNTICO v8.1</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0a0c0;'>Sistema de Diagnóstico Empresarial</p>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🎛️ Controles")
    
    dados = engine.dados_originais
    filters = {
        'Ano': st.selectbox("**Ano**", ["TODOS"] + sorted(dados['Ano'].unique())),
        'Mes': st.selectbox("**Mês**", ["TODOS"] + sorted(dados['Mes'].unique())),
        'Nivel_Consultor': st.multiselect("**Nível**", 
                                         ["TODOS"] + sorted(dados['Nivel_Consultor'].unique()),
                                         default=["TODOS"]),
        'Negocio_Projeto': st.multiselect("**Negócio**", 
                                         ["TODOS"] + sorted(dados['Negocio_Projeto'].unique()),
                                         default=["TODOS"])
    }
    
    df_filtrado = engine.aplicar_filtros(filters)
    
    st.markdown("---")
    st.markdown("### 📊 Resumo")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Projetos", len(df_filtrado))
        st.metric("Receita", f"R$ {df_filtrado['Receita_Total'].sum():,.0f}")
    with col2:
        st.metric("Margem", f"{df_filtrado['Margem_Percentual'].mean():.1%}")
        st.metric("Eficiência", f"{df_filtrado['Eficiencia_Horas'].mean():.2f}x")

# --- EXECUTAR DIAGNÓSTICO ---
diagnosticos, alertas = engine.executar_diagnostico_quantico(df_filtrado)

# --- ABAS PRINCIPAIS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Painel", "🔍 Diagnóstico", "💰 Fechamento", "🎤 Comandos"])

with tab1:
    st.markdown("### 📊 Painel de Controle")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    metricas = engine._calcular_metricas_chave(df_filtrado)
    
    with col1:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>RECEITA TOTAL</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>R$ {metricas['receita_total']:,.0f}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>LUCRO TOTAL</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>R$ {metricas['lucro_total']:,.0f}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>MARGEM MÉDIA</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>{metricas['margem_media']:.1%}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='kpi-card'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>PROJETOS ATIVOS</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>{metricas['projetos_ativos']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
        st.markdown("**📈 Evolução Mensal**")
        evolucao_mensal = df_filtrado.groupby('Mes').agg({
            'Receita_Total': 'sum',
            'Lucro_Total': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=evolucao_mensal['Mes'], y=evolucao_mensal['Receita_Total'], 
                               name='Receita', line=dict(color='#00ccff', width=3)))
        fig.add_trace(go.Scatter(x=evolucao_mensal['Mes'], y=evolucao_mensal['Lucro_Total'], 
                               name='Lucro', line=dict(color='#00ff88', width=3)))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
        st.markdown("**🎯 Performance por Nível**")
        perf_nivel = df_filtrado.groupby('Nivel_Consultor').agg({
            'Margem_Percentual': 'mean',
            'Ticket_Medio_Hora': 'mean'
        }).reset_index()
        
        fig = px.bar(perf_nivel, x='Nivel_Consultor', y='Margem_Percentual', 
                    color='Ticket_Medio_Hora', color_continuous_scale='viridis')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 🔍 Diagnóstico Detalhado")
    
    if alertas:
        st.markdown("#### ⚠️ Alertas Críticos")
        for alerta in alertas:
            st.markdown(f"<div class='quantum-card'>", unsafe_allow_html=True)
            st.markdown(f"**{alerta['titulo']}** · 🔴 **{alerta['nivel']}**")
            st.markdown(f"{alerta['descricao']}")
            st.markdown(f"**Impacto:** {alerta['impacto']}")
            st.markdown(f"**Ação Imediata:** {alerta['acao_imediata']}")
            st.markdown("</div>", unsafe_allow_html=True)
    
    if diagnosticos:
        st.markdown("#### 📋 Diagnósticos")
        for diagnostico in diagnosticos:
            st.markdown(f"<div class='quantum-card'>", unsafe_allow_html=True)
            st.markdown(f"**{diagnostico['titulo']}**")
            st.markdown(f"{diagnostico['descricao']}")
            st.markdown(f"**Prescrição:** {diagnostico['prescricao']}")
            st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("### 💰 Fechamento Financeiro")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
        st.markdown("**💰 A Pagar (Consultores)**")
        df_pagar = df_filtrado.groupby(['Consultor', 'Nivel_Consultor']).agg({
            'Custo_Total': 'sum',
            'Horas_Realizadas': 'sum'
        }).round(2).reset_index()
        
        st.dataframe(
            df_pagar.style.format({
                'Custo_Total': 'R$ {:.2f}'
            }),
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
        st.markdown("**💳 A Receber (Clientes)**")
        df_receber = df_filtrado.groupby('Cliente').agg({
            'Receita_Total': 'sum',
            'Horas_Realizadas': 'sum'
        }).round(2).reset_index()
        
        st.dataframe(
            df_receber.style.format({
                'Receita_Total': 'R$ {:.2f}'
            }),
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown("### 🎤 Sistema de Comandos")
    
    st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
    st.markdown("**💬 Comandos Disponíveis:**")
    st.markdown("- `lançar horas` - Iniciar lançamento de horas")
    st.markdown("- `novo projeto` - Criar novo projeto")
    st.markdown("- `status geral` - Ver status geral")
    
    comando = st.text_input("Digite seu comando:", placeholder="Ex: 'lançar horas'")
    
    if st.button("Executar Comando", width='stretch'):
        if comando:
            resultado = voice_system.processar_comando(comando)
            st.success(f"**Resultado:** {resultado}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>MAESTRO QUÂNTICO v8.1 · Sistema Corrigido</div>", unsafe_allow_html=True)