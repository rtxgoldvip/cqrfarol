# -*- coding: utf-8 -*-
# MAESTRO QUÂNTICO v8.0 - Sistema de Diagnóstico Empresarial Dinâmico

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
from scipy import stats
import speech_recognition as sr
from io import BytesIO

try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False

warnings.filterwarnings('ignore')

# --- CONFIGURAÇÃO DA PÁGINA PREMIUM ---
st.set_page_config(
    page_title="MAESTRO QUÂNTICO | Diagnóstico Dinâmico", 
    page_icon="🌌", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- ESTILO CSS PREMIUM AVANÇADO ---
st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0c0c2e 0%, #1a1a3e 50%, #0c0c2e 100%);
        color: #ffffff;
    }
    
    .stApp {
        background: radial-gradient(ellipse at top right, #1a1a3e 0%, #0c0c2e 70%);
        animation: cosmicPulse 20s ease-in-out infinite;
    }
    
    @keyframes cosmicPulse {
        0%, 100% { background-size: 100% 100%; }
        50% { background-size: 120% 120%; }
    }
    
    .header-glow {
        background: linear-gradient(90deg, #0066ff 0%, #00ccff 50%, #0066ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1.5rem;
        font-size: 2.8rem;
        animation: textGlow 3s ease-in-out infinite;
    }
    
    @keyframes textGlow {
        0%, 100% { filter: drop-shadow(0 0 10px rgba(0, 102, 255, 0.5)); }
        50% { filter: drop-shadow(0 0 20px rgba(0, 204, 255, 0.8)); }
    }
    
    .quantum-card {
        background: rgba(20, 25, 60, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(0, 204, 255, 0.3);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
    }
    
    .quantum-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 204, 255, 0.1), transparent);
        transition: left 0.6s;
    }
    
    .quantum-card:hover::before {
        left: 100%;
    }
    
    .quantum-card:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: rgba(0, 204, 255, 0.6);
        box-shadow: 0 15px 40px rgba(0, 102, 255, 0.3);
    }
    
    .pulse-alert {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 68, 0, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(255, 68, 0, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 68, 0, 0); }
    }
    
    .floating-kpi {
        background: linear-gradient(135deg, rgba(0, 102, 255, 0.2), rgba(0, 204, 255, 0.1));
        border: 1px solid rgba(0, 204, 255, 0.3);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .floating-kpi:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 102, 255, 0.2);
    }
    
    .voice-command {
        background: linear-gradient(135deg, rgba(0, 200, 100, 0.2), rgba(0, 255, 150, 0.1));
        border: 2px dashed rgba(0, 255, 150, 0.4);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .voice-command:hover {
        background: linear-gradient(135deg, rgba(0, 200, 100, 0.3), rgba(0, 255, 150, 0.2));
        border-color: rgba(0, 255, 150, 0.6);
    }
    
    .scenario-simulator {
        background: linear-gradient(135deg, rgba(150, 0, 255, 0.2), rgba(200, 0, 255, 0.1));
        border: 1px solid rgba(200, 0, 255, 0.3);
        border-radius: 15px;
        padding: 25px;
    }
</style>
""", unsafe_allow_html=True)

# --- NÚCLEO QUÂNTICO - MOTOR DE ANÁLISE DINÂMICA ---
class QuantumAnalysisEngine:
    def __init__(self):
        self.dados_originais = self._carregar_dados_reais()
        self.dados_filtrados = self.dados_originais.copy()
        self.historico_analises = []
        self.ultimo_diagnostico = None
        
    def _carregar_dados_reais(self):
        """Carrega dados do arquivo Excel fornecido"""
        try:
            df = pd.read_excel('dados_maestro_extraidos.xlsx', sheet_name='DadosMaestro')
            return self._processar_dados_avancado(df)
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return self._criar_dados_demonstracao()
    
    def _processar_dados_avancado(self, df):
        """Processamento avançado dos dados para análise quântica"""
        # Conversão e limpeza
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
        df['ROI_Projeto'] = np.where(
            df['Custo_Total'] > 0,
            df['Lucro_Total'] / df['Custo_Total'],
            0
        )
        
        # Análise de desvio padrão para detectar anomalias
        df['Desvio_Margem'] = (df['Margem_Percentual'] - df['Margem_Percentual'].mean()) / df['Margem_Percentual'].std()
        
        # Preencher valores ausentes
        for col in ['Nivel_Consultor', 'Negocio_Projeto', 'Status_Projeto', 'Consultor']:
            df[col] = df[col].fillna('Não Definido')
            
        return df
    
    def _criar_dados_demonstracao(self):
        """Cria dados de demonstração baseados na estrutura real"""
        st.warning("🔬 Modo de Demonstração Ativo - Usando dados sintéticos")
        # Dados mais realistas baseados no arquivo fornecido
        meses = list(range(1, 13))
        data = []
        
        for mes in meses:
            # Projetos TOTVS IP (maioria)
            for _ in range(15):
                data.append({
                    'Mes': mes, 'Ano': 2024,
                    'Consultor': np.random.choice(['ADRIANO AFONSO', 'ALYNE CAMPOS', 'AUGUSTO KREJCI', 'CLEBER NEVES']),
                    'Nivel_Consultor': np.random.choice(['SENIOR', 'ESPECIALISTA'], p=[0.6, 0.4]),
                    'Cliente': 'TOTVS IP',
                    'Projeto': 'ALOCAÇÃO DE RECURSOS',
                    'Negocio_Projeto': 'OUTSOURCING - LOCAÇÃO',
                    'Status_Projeto': 'EM ABERTO',
                    'Horas_Previstas': np.random.normal(120, 30),
                    'Horas_Realizadas': np.random.normal(125, 35),
                    'Receita_Total': np.random.normal(15000, 4000),
                    'Custo_Total': np.random.normal(9000, 2000),
                    'Margem_Percentual': np.random.normal(0.35, 0.1)
                })
            
            # Projetos outros clientes
            for cliente in ['SOL FÁCIL - INOVE', 'TOTVS MATRIZ', 'ASH BRASIL']:
                data.append({
                    'Mes': mes, 'Ano': 2024,
                    'Consultor': np.random.choice(['DIOGO MELO', 'SILVINO MARTINS', 'VITOR NUCCI']),
                    'Nivel_Consultor': np.random.choice(['SENIOR', 'ESPECIALISTA', 'PLENO']),
                    'Cliente': cliente,
                    'Projeto': np.random.choice(['HRS FECHADAS', 'EMPRÉSTIMO DE RECURSO', 'PROJETO FECHADO']),
                    'Negocio_Projeto': np.random.choice(['PROJETOS', 'OUTSOURCING - LOCAÇÃO']),
                    'Status_Projeto': 'EM ABERTO',
                    'Horas_Previstas': np.random.normal(80, 20),
                    'Horas_Realizadas': np.random.normal(85, 25),
                    'Receita_Total': np.random.normal(8000, 2000),
                    'Custo_Total': np.random.normal(5000, 1500),
                    'Margem_Percentual': np.random.normal(0.25, 0.15)
                })
        
        df = pd.DataFrame(data)
        # Garantir valores positivos
        for col in ['Horas_Previstas', 'Horas_Realizadas', 'Receita_Total', 'Custo_Total']:
            df[col] = df[col].abs()
        
        df['Lucro_Total'] = df['Receita_Total'] - df['Custo_Total']
        return df
    
    def analisar_variacao_receita(self, mes_atual, mes_anterior):
        """Análise quântica da variação de receita entre meses"""
        dados_mes_atual = self.dados_filtrados[self.dados_filtrados['Mes'] == mes_atual]
        dados_mes_anterior = self.dados_filtrados[self.dados_filtrados['Mes'] == mes_anterior]
        
        if dados_mes_atual.empty or dados_mes_anterior.empty:
            return {"erro": "Dados insuficientes para análise"}
        
        receita_atual = dados_mes_atual['Receita_Total'].sum()
        receita_anterior = dados_mes_anterior['Receita_Total'].sum()
        variacao_absoluta = receita_atual - receita_anterior
        variacao_percentual = (variacao_absoluta / receita_anterior) * 100 if receita_anterior != 0 else 0
        
        # Análise multidimensional dos fatores
        fatores = self._identificar_fatores_variacao(dados_mes_atual, dados_mes_anterior)
        
        return {
            'variacao_absoluta': variacao_absoluta,
            'variacao_percentual': variacao_percentual,
            'fatores_principais': fatores,
            'prescricoes': self._gerar_prescricoes_variacao(fatores, variacao_percentual)
        }
    
    def _identificar_fatores_variacao(self, atual, anterior):
        """Identifica os fatores que causaram a variação"""
        fatores = []
        
        # Fator 1: Volume de Horas
        horas_atual = atual['Horas_Realizadas'].sum()
        horas_anterior = anterior['Horas_Realizadas'].sum()
        variacao_horas = horas_atual - horas_anterior
        if abs(variacao_horas) > horas_anterior * 0.05:  # Variação > 5%
            fatores.append({
                'fator': 'VOLUME_HORAS',
                'impacto': variacao_horas / horas_anterior * 100,
                'descricao': f'Variação de {variacao_horas:.0f} horas realizadas'
            })
        
        # Fator 2: Mix de Clientes
        mix_atual = atual.groupby('Cliente')['Receita_Total'].sum()
        mix_anterior = anterior.groupby('Cliente')['Receita_Total'].sum()
        
        for cliente in mix_atual.index:
            if cliente in mix_anterior.index:
                variacao = mix_atual[cliente] - mix_anterior[cliente]
                if abs(variacao) > mix_anterior[cliente] * 0.1:  # Variação > 10%
                    fatores.append({
                        'fator': 'MIX_CLIENTES',
                        'impacto': variacao / mix_anterior.sum() * 100,
                        'descricao': f'Variação no cliente {cliente}: R$ {variacao:,.0f}',
                        'cliente': cliente
                    })
        
        # Fator 3: Eficiência Operacional
        eficiencia_atual = atual['Ticket_Medio_Hora'].mean()
        eficiencia_anterior = anterior['Ticket_Medio_Hora'].mean()
        variacao_eficiencia = eficiencia_atual - eficiencia_anterior
        
        if abs(variacao_eficiencia) > eficiencia_anterior * 0.05:
            fatores.append({
                'fator': 'EFICIENCIA_OPERACIONAL',
                'impacto': variacao_eficiencia / eficiencia_anterior * 100,
                'descricao': f'Variação no ticket médio: R$ {variacao_eficiencia:.2f}/hora'
            })
        
        # Ordenar por impacto absoluto
        fatores.sort(key=lambda x: abs(x['impacto']), reverse=True)
        return fatores[:5]  # Top 5 fatores
    
    def _gerar_prescricoes_variacao(self, fatores, variacao_percentual):
        """Gera prescrições específicas baseadas nos fatores identificados"""
        prescricoes = []
        
        for fator in fatores:
            if fator['fator'] == 'VOLUME_HORAS':
                if fator['impacto'] > 0:
                    prescricoes.append({
                        'prioridade': 'ALTA',
                        'acao': 'AUMENTAR_CAPACIDADE',
                        'descricao': 'Expandir capacidade produtiva para sustentar crescimento',
                        'detalhes': f'Horas aumentaram {fator["impacto"]:.1f}% - considerar contratações'
                    })
                else:
                    prescricoes.append({
                        'prioridade': 'CRITICA',
                        'acao': 'OTIMIZAR_ALOCACAO',
                        'descricao': 'Recuperar capacidade ociosa através de novos projetos',
                        'detalhes': f'Horas reduziram {abs(fator["impacto"]):.1f}% - buscar novos negócios'
                    })
            
            elif fator['fator'] == 'MIX_CLIENTES':
                cliente = fator.get('cliente', '')
                if fator['impacto'] > 0:
                    prescricoes.append({
                        'prioridade': 'MEDIA',
                        'acao': 'CONSOLIDAR_RELACIONAMENTO',
                        'descricao': f'Fortalecer parceria com {cliente}',
                        'detalhes': f'Cliente cresceu {fator["impacto"]:.1f}% - oportunidade de expansão'
                    })
                else:
                    prescricoes.append({
                        'prioridade': 'ALTA',
                        'acao': 'RECUPERAR_CLIENTE',
                        'descricao': f'Recuperar volume com {cliente}',
                        'detalhes': f'Cliente reduziu {abs(fator["impacto"]):.1f}% - analisar causas'
                    })
        
        return prescricoes
    
    def executar_diagnostico_quantico(self, df):
        """Executa diagnóstico quântico completo"""
        diagnosticos = []
        alertas = []
        
        if df.empty:
            return diagnosticos, alertas
        
        # ANÁLISE DE SUPERPOSIÇÃO - Todas as possibilidades
        diagnosticos.extend(self._analise_superposicao(df))
        
        # ANÁLISE DE ENTRELAÇAMENTO - Interdependências
        diagnosticos.extend(self._analise_entrelacamento(df))
        
        # ANÁLISE DE INTERFERÊNCIA - Padrões ocultos
        diagnosticos.extend(self._analise_interferencia(df))
        
        # ALERTAS CRÍTICOS
        alertas.extend(self._gerar_alertas_criticos(df))
        
        self.ultimo_diagnostico = {
            'timestamp': datetime.now(),
            'diagnosticos': diagnosticos,
            'alertas': alertas,
            'metricas_chave': self._calcular_metricas_chave(df)
        }
        
        return diagnosticos, alertas
    
    def _analise_superposicao(self, df):
        """Análise de todas as possibilidades simultâneas"""
        diagnosticos = []
        
        # Potencial de Otimização
        margem_ideal = df['Margem_Percentual'].quantile(0.75)  # Top 25%
        projetos_abaixo_ideal = df[df['Margem_Percentual'] < margem_ideal]
        
        if len(projetos_abaixo_ideal) > len(df) * 0.3:  # 30% abaixo do ideal
            potencial_otimizacao = (margem_ideal - projetos_abaixo_ideal['Margem_Percentual'].mean()) * projetos_abaixo_ideal['Receita_Total'].sum()
            
            diagnosticos.append({
                'tipo': 'SUPERPOSICAO',
                'titulo': 'POTENCIAL DE OTIMIZAÇÃO IDENTIFICADO',
                'descricao': f'{len(projetos_abaixo_ideal)} projetos podem atingir margem ideal',
                'potencial': f'R$ {potencial_otimizacao:,.0f}',
                'prescricao': 'Implementar melhores práticas dos projetos top 25%'
            })
        
        return diagnosticos
    
    def _analise_entrelacamento(self, df):
        """Análise das interdependências entre variáveis"""
        diagnosticos = []
        
        # Correlação entre nível do consultor e margem
        correlacao_nivel_margem = df.groupby('Nivel_Consultor')['Margem_Percentual'].mean()
        if len(correlacao_nivel_margem) > 1:
            variacao = correlacao_nivel_margem.max() - correlacao_nivel_margem.min()
            if variacao > 0.15:  # 15% de variação
                diagnosticos.append({
                    'tipo': 'ENTRELAÇAMENTO',
                    'titulo': 'SENIORIDADE IMPACTA MARGEM',
                    'descricao': f'Variação de {variacao:.1%} na margem entre níveis',
                    'prescricao': 'Otimizar mix de senioridade por tipo de projeto'
                })
        
        return diagnosticos
    
    def _analise_interferencia(self, df):
        """Análise de padrões através de interferência quântica"""
        diagnosticos = []
        
        # Padrão de sazonalidade
        if len(df['Mes'].unique()) >= 6:
            receita_mensal = df.groupby('Mes')['Receita_Total'].sum()
            coef_variacao = receita_mensal.std() / receita_mensal.mean()
            
            if coef_variacao > 0.25:
                diagnosticos.append({
                    'tipo': 'INTERFERENCIA',
                    'titulo': 'PADRÃO SAZONAL DETECTADO',
                    'descricao': f'Alta variação mensal ({coef_variacao:.1%})',
                    'prescricao': 'Criar estratégia para suavizar receita ao longo do ano'
                })
        
        return diagnosticos
    
    def _gerar_alertas_criticos(self, df):
        """Gera alertas críticos em tempo real"""
        alertas = []
        
        # Projetos com margem negativa
        margens_negativas = df[df['Margem_Percentual'] < 0]
        if not margens_negativas.empty:
            perda_total = margens_negativas['Lucro_Total'].sum()
            alertas.append({
                'nivel': 'CRITICO',
                'titulo': 'SANGRIA FINANCEIRA DETECTADA',
                'descricao': f'{len(margens_negativas)} projetos com margem negativa',
                'impacto': f'Perda: R$ {abs(perda_total):,.0f}',
                'acao_imediata': 'Revisar custos e renegociar contratos'
            })
        
        # Excessiva dependência de um cliente
        top_cliente_receita = df.groupby('Cliente')['Receita_Total'].sum().nlargest(1)
        concentracao = top_cliente_receita.iloc[0] / df['Receita_Total'].sum()
        
        if concentracao > 0.4:  # 40% de concentração
            alertas.append({
                'nivel': 'ALTO',
                'titulo': 'CONCENTRAÇÃO DE RISCO',
                'descricao': f'{top_cliente_receita.index[0]} representa {concentracao:.1%} da receita',
                'impacto': 'Risco operacional elevado',
                'acao_imediata': 'Diversificar portfólio de clientes'
            })
        
        return alertas
    
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

# --- SISTEMA DE COMANDO POR VOZ ---
class VoiceCommandSystem:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.commands = {
            'lançar horas': self.lancar_horas,
            'novo projeto': self.novo_projeto,
            'status geral': self.status_geral,
            'alertas críticos': self.alertas_criticos
        }
    
    def processar_comando(self, comando):
        comando = comando.lower()
        for cmd, funcao in self.commands.items():
            if cmd in comando:
                return funcao(comando)
        return "Comando não reconhecido. Tente: 'lançar horas', 'novo projeto', 'status geral'"
    
    def lancar_horas(self, comando):
        return "Sistema de lançamento de horas ativado. Use o formulário na aba 'Comando de Voz'"
    
    def novo_projeto(self, comando):
        return "Criando novo projeto... Preencha os detalhes no formulário abaixo"
    
    def status_geral(self, comando):
        return "Gerando relatório de status geral..."
    
    def alertas_criticos(self, comando):
        return "Buscando alertas críticos..."

# --- SIMULADOR DE CENÁRIOS ---
class SimuladorCenarios:
    def __init__(self, engine):
        self.engine = engine
    
    def simular_cenario_otimo(self, dados_base):
        """Simula o cenário ótimo baseado nas melhores práticas"""
        # Usa os top 25% de projetos como benchmark
        benchmark = dados_base[dados_base['Margem_Percentual'] >= dados_base['Margem_Percentual'].quantile(0.75)]
        
        cenario_otimo = dados_base.copy()
        
        # Aplica melhorias baseadas no benchmark
        cenario_otimo['Margem_Percentual'] = benchmark['Margem_Percentual'].mean()
        cenario_otimo['Eficiencia_Horas'] = benchmark['Eficiencia_Horas'].mean()
        cenario_otimo['Ticket_Medio_Hora'] = benchmark['Ticket_Medio_Hora'].mean()
        
        # Recalcula métricas
        cenario_otimo['Receita_Total'] = cenario_otimo['Horas_Realizadas'] * cenario_otimo['Ticket_Medio_Hora']
        cenario_otimo['Lucro_Total'] = cenario_otimo['Receita_Total'] * cenario_otimo['Margem_Percentual']
        cenario_otimo['Custo_Total'] = cenario_otimo['Receita_Total'] - cenario_otimo['Lucro_Total']
        
        return cenario_otimo
    
    def comparar_cenarios(self, atual, otimo):
        """Compara cenário atual vs ótimo"""
        comparacao = {
            'receita_atual': atual['Receita_Total'].sum(),
            'receita_otimo': otimo['Receita_Total'].sum(),
            'lucro_atual': atual['Lucro_Total'].sum(),
            'lucro_otimo': otimo['Lucro_Total'].sum(),
            'margem_atual': atual['Margem_Percentual'].mean(),
            'margem_otimo': otimo['Margem_Percentual'].mean(),
            'eficiencia_atual': atual['Eficiencia_Horas'].mean(),
            'eficiencia_otimo': otimo['Eficiencia_Horas'].mean()
        }
        
        comparacao['potencial_receita'] = comparacao['receita_otimo'] - comparacao['receita_atual']
        comparacao['potencial_lucro'] = comparacao['lucro_otimo'] - comparacao['lucro_atual']
        
        return comparacao

# --- INICIALIZAÇÃO DO SISTEMA ---
@st.cache_resource
def init_quantum_engine():
    return QuantumAnalysisEngine()

@st.cache_resource
def init_voice_system():
    return VoiceCommandSystem()

engine = init_quantum_engine()
voice_system = init_voice_system()
simulador = SimuladorCenarios(engine)

# --- INTERFACE PRINCIPAL ---
st.markdown("<h1 class='header-glow'>MAESTRO QUÂNTICO v8.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0a0c0; font-size: 1.2rem;'>Sistema de Diagnóstico Empresarial Dinâmico</p>", unsafe_allow_html=True)

# --- SIDEBAR AVANÇADO ---
with st.sidebar:
    st.markdown("### 🎛️ Controles Quânticos")
    
    dados = engine.dados_originais
    filters = {
        'Ano': st.selectbox("**Ano**", ["TODOS"] + sorted(dados['Ano'].unique())),
        'Mes': st.selectbox("**Mês**", ["TODOS"] + sorted(dados['Mes'].unique())),
        'Nivel_Consultor': st.multiselect("**Nível**", 
                                         ["TODOS"] + sorted(dados['Nivel_Consultor'].unique()),
                                         default=["TODOS"]),
        'Negocio_Projeto': st.multiselect("**Negócio**", 
                                         ["TODOS"] + sorted(dados['Negocio_Projeto'].unique()),
                                         default=["TODOS"]),
        'Consultor': st.multiselect("**Consultor**", 
                                   ["TODOS"] + sorted(dados['Consultor'].unique()),
                                   default=["TODOS"]),
        'Cliente': st.multiselect("**Cliente**",
                                 ["TODOS"] + sorted(dados['Cliente'].unique()),
                                 default=["TODOS"])
    }
    
    # Aplicar filtros
    df_filtrado = engine.aplicar_filtros(filters)
    
    # Estatísticas em tempo real
    st.markdown("---")
    st.markdown("### 📊 Ressonância Atual")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Projetos", len(df_filtrado))
        st.metric("Receita", f"R$ {df_filtrado['Receita_Total'].sum():,.0f}")
    with col2:
        st.metric("Margem", f"{df_filtrado['Margem_Percentual'].mean():.1%}")
        st.metric("Eficiência", f"{df_filtrado['Eficiencia_Horas'].mean():.2f}x")

# --- EXECUTAR DIAGNÓSTICO QUÂNTICO ---
diagnosticos, alertas = engine.executar_diagnostico_quantico(df_filtrado)

# --- ABAS QUÂNTICAS ---
tab_icons = ["bi-cpu", "bi-heart-pulse", "bi-graph-up-arrow", "bi-cash-stack", "bi-people", "bi-lightbulb", "bi-mic", "bi-sliders"]
tab_names = ["Painel Quântico", "Diagnóstico", "Comparativo", "Fechamento", "Recursos", "Simulador", "Comando Voz", "Configurações"]
tabs = st.tabs([f"<i class='bi {icon}'></i> {name}" for icon, name in zip(tab_icons, tab_names)])

with tabs[0]:  # PAINEL QUÂNTICO
    st.markdown("<div class='section-title'><i class='bi bi-cpu'></i> PAINEL DE CONTROLE QUÂNTICO</div>", unsafe_allow_html=True)
    
    # KPIs DINÂMICOS
    col1, col2, col3, col4 = st.columns(4)
    
    metricas = engine._calcular_metricas_chave(df_filtrado) if engine.ultimo_diagnostico else {
        'receita_total': df_filtrado['Receita_Total'].sum(),
        'lucro_total': df_filtrado['Lucro_Total'].sum(),
        'margem_media': df_filtrado['Margem_Percentual'].mean(),
        'eficiencia_media': df_filtrado['Eficiencia_Horas'].mean()
    }
    
    with col1:
        st.markdown("<div class='floating-kpi'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>RECEITA QUÂNTICA</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>R$ {metricas['receita_total']:,.0f}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='floating-kpi'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>LUCRO RESSONANTE</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>R$ {metricas['lucro_total']:,.0f}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='floating-kpi'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>EFICIÊNCIA</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>{metricas['eficiencia_media']:.2f}x</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='floating-kpi'>", unsafe_allow_html=True)
        st.markdown("<div class='kpi-label'>PROJETOS ATIVOS</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='kpi-value'>{metricas['projetos_ativos']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ALERTAS EM TEMPO REAL
    if alertas:
        st.markdown("<div class='section-title'><i class='bi bi-exclamation-triangle'></i> ALERTAS QUÂNTICOS</div>", unsafe_allow_html=True)
        for alerta in alertas:
            card_class = "pulse-alert" if alerta['nivel'] == 'CRITICO' else ""
            st.markdown(f"<div class='quantum-card {card_class}'>", unsafe_allow_html=True)
            st.markdown(f"**{alerta['titulo']}** · 🔴 **{alerta['nivel']}**", unsafe_allow_html=True)
            st.markdown(f"{alerta['descricao']}")
            st.markdown(f"**Impacto:** {alerta['impacto']}")
            st.markdown(f"**Ação Imediata:** {alerta['acao_imediata']}")
            st.markdown("</div>", unsafe_allow_html=True)
    
    # GRÁFICOS QUÂNTICOS
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
        st.markdown("**📈 Evolução da Ressonância Mensal**")
        evolucao_mensal = df_filtrado.groupby('Mes').agg({
            'Receita_Total': 'sum',
            'Lucro_Total': 'sum',
            'Margem_Percentual': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=evolucao_mensal['Mes'], y=evolucao_mensal['Receita_Total'], 
                               name='Receita', line=dict(color='#00ccff', width=3)))
        fig.add_trace(go.Scatter(x=evolucao_mensal['Mes'], y=evolucao_mensal['Lucro_Total'], 
                               name='Lucro', line=dict(color='#00ff88', width=3)))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
        st.markdown("**🎯 Matriz de Performance Quântica**")
        
        performance_matrix = df_filtrado.groupby('Nivel_Consultor').agg({
            'Margem_Percentual': 'mean',
            'Eficiencia_Horas': 'mean',
            'Ticket_Medio_Hora': 'mean'
        }).reset_index()
        
        fig = px.scatter(performance_matrix, x='Eficiencia_Horas', y='Margem_Percentual',
                        size='Ticket_Medio_Hora', color='Nivel_Consultor',
                        hover_name='Nivel_Consultor', size_max=50)
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tabs[1]:  # DIAGNÓSTICO
    st.markdown("<div class='section-title'><i class='bi bi-heart-pulse'></i> DIAGNÓSTICO QUÂNTICO DINÂMICO</div>", unsafe_allow_html=True)
    
    if diagnosticos:
        for diagnostico in diagnosticos:
            st.markdown(f"<div class='quantum-card'>", unsafe_allow_html=True)
            st.markdown(f"**🎭 {diagnostico['tipo']}** · {diagnostico['titulo']}", unsafe_allow_html=True)
            st.markdown(f"{diagnostico['descricao']}")
            if 'potencial' in diagnostico:
                st.markdown(f"**Potencial Identificado:** {diagnostico['potencial']}")
            st.markdown(f"**Prescrição Quântica:** {diagnostico['prescricao']}")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
        st.markdown("**✅ RESSONÂNCIA HARMÔNICA**")
        st.markdown("O sistema opera em estado de equilíbrio quântico. Nenhuma interferência negativa detectada.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ANÁLISE DE VARIAÇÃO ENTRE MESES
    st.markdown("<div class='section-title'><i class='bi bi-arrow-left-right'></i> ANÁLISE DE VARIAÇÃO ENTRE MESES</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        mes_atual = st.selectbox("Mês Atual", sorted(df_filtrado['Mes'].unique()), key='mes_atual')
    with col2:
        mes_anterior = st.selectbox("Mês Anterior", sorted(df_filtrado['Mes'].unique()), key='mes_anterior')
    
    if st.button("🔍 Analisar Variação Quântica", type="primary"):
        with st.spinner("Executando análise de interferência..."):
            analise = engine.analisar_variacao_receita(mes_atual, mes_anterior)
            
            if 'erro' not in analise:
                st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
                st.markdown(f"**📊 Variação: {analise['variacao_percentual']:+.1f}%**")
                st.markdown(f"**Valor:** R$ {analise['variacao_absoluta']:,.0f}")
                
                st.markdown("**🎯 Fatores Principais:**")
                for fator in analise['fatores_principais']:
                    st.markdown(f"- {fator['descricao']} (Impacto: {fator['impacto']:+.1f}%)")
                
                st.markdown("**💡 Prescrições:**")
                for prescricao in analise['prescricoes']:
                    st.markdown(f"- **{prescricao['prioridade']}:** {prescricao['descricao']}")
                
                st.markdown("</div>", unsafe_allow_html=True)

with tabs[2]:  # COMPARATIVO
    st.markdown("<div class='section-title'><i class='bi bi-graph-up-arrow'></i> ANÁLISE COMPARATIVA AVANÇADA</div>", unsafe_allow_html=True)
    
    # Comparação entre períodos
    col1, col2, col3 = st.columns(3)
    with col1:
        periodo1_ano = st.selectbox("Ano Período 1", [2024], key='p1_ano')
        periodo1_mes = st.selectbox("Mês Período 1", sorted(df_filtrado['Mes'].unique()), key='p1_mes')
    with col2:
        periodo2_ano = st.selectbox("Ano Período 2", [2024], key='p2_ano')
        periodo2_mes = st.selectbox("Mês Período 2", sorted(df_filtrado['Mes'].unique()), key='p2_mes')
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Comparar Períodos", use_container_width=True):
            p1 = df_filtrado[(df_filtrado['Ano'] == periodo1_ano) & (df_filtrado['Mes'] == periodo1_mes)]
            p2 = df_filtrado[(df_filtrado['Ano'] == periodo2_ano) & (df_filtrado['Mes'] == periodo2_mes)]
            
            if not p1.empty and not p2.empty:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
                    st.markdown(f"**Período 1 ({periodo1_mes}/{periodo1_ano})**")
                    st.metric("Receita", f"R$ {p1['Receita_Total'].sum():,.0f}")
                    st.metric("Lucro", f"R$ {p1['Lucro_Total'].sum():,.0f}")
                    st.metric("Margem", f"{p1['Margem_Percentual'].mean():.1%}")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
                    st.markdown(f"**Período 2 ({periodo2_mes}/{periodo2_ano})**")
                    st.metric("Receita", f"R$ {p2['Receita_Total'].sum():,.0f}", 
                             f"{(p2['Receita_Total'].sum() - p1['Receita_Total'].sum()):,.0f}")
                    st.metric("Lucro", f"R$ {p2['Lucro_Total'].sum():,.0f}",
                             f"{(p2['Lucro_Total'].sum() - p1['Lucro_Total'].sum()):,.0f}")
                    st.metric("Margem", f"{p2['Margem_Percentual'].mean():.1%}",
                             f"{(p2['Margem_Percentual'].mean() - p1['Margem_Percentual'].mean()):.1%}")
                    st.markdown("</div>", unsafe_allow_html=True)

with tabs[3]:  # FECHAMENTO
    st.markdown("<div class='section-title'><i class='bi bi-cash-stack'></i> FECHAMENTO FINANCEIRO DINÂMICO</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
        st.markdown("**💰 A Pagar (Consultores)**")
        df_pagar = df_filtrado.groupby(['Consultor', 'Nivel_Consultor']).agg({
            'Custo_Total': 'sum',
            'Horas_Previstas': 'sum',
            'Horas_Realizadas': 'sum',
            'Margem_Percentual': 'mean'
        }).round(2).reset_index()
        
        st.dataframe(
            df_pagar.style.format({
                'Custo_Total': 'R$ {:.2f}',
                'Margem_Percentual': '{:.1%}'
            }),
            use_container_width=True,
            height=400
        )
        
        # Exportar
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_pagar.to_excel(writer, sheet_name='A_Pagar', index=False)
        st.download_button(
            "📥 Exportar A Pagar",
            output.getvalue(),
            "a_pagar.xlsx",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='quantum-card'>", unsafe_allow_html=True)
        st.markdown("**💳 A Receber (Clientes)**")
        df_receber = df_filtrado.groupby('Cliente').agg({
            'Receita_Total': 'sum',
            'Horas_Previstas': 'sum',
            'Horas_Realizadas': 'sum',
            'Projeto': 'count'
        }).round(2).reset_index()
        
        st.dataframe(
            df_receber.style.format({
                'Receita_Total': 'R$ {:.2f}'
            }),
            use_container_width=True,
            height=400
        )
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_receber.to_excel(writer, sheet_name='A_Receber', index=False)
        st.download_button(
            "📥 Exportar A Receber",
            output.getvalue(),
            "a_receber.xlsx",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

with tabs[5]:  # SIMULADOR
    st.markdown("<div class='section-title'><i class='bi bi-lightbulb'></i> SIMULADOR DE CENÁRIOS QUÂNTICOS</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='scenario-simulator'>", unsafe_allow_html=True)
    st.markdown("**🎯 Simulação do Futuro Ótimo**")
    
    if st.button("🚀 Simular Cenário Ótimo", use_container_width=True, type="primary"):
        with st.spinner("Calculando interferência construtiva..."):
            cenario_otimo = simulador.simular_cenario_otimo(df_filtrado)
            comparacao = simulador.comparar_cenarios(df_filtrado, cenario_otimo)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Receita Atual", f"R$ {comparacao['receita_atual']:,.0f}",
                         f"+R$ {comparacao['potencial_receita']:,.0f}")
            
            with col2:
                st.metric("Lucro Atual", f"R$ {comparacao['lucro_atual']:,.0f}",
                         f"+R$ {comparacao['potencial_lucro']:,.0f}")
            
            with col3:
                st.metric("Margem Atual", f"{comparacao['margem_atual']:.1%}",
                         f"+{comparacao['margem_otimo'] - comparacao['margem_atual']:.1%}")
            
            st.markdown("**📈 Prescrições para o Cenário Ótimo:**")
            st.markdown("""
            1. **Alocar projetos de alto valor para consultores sênior**
            2. **Negociar aumento no ticket médio baseado no benchmark**
            3. **Otimizar eficiência operacional através das melhores práticas**
            4. **Reduzir custos em projetos abaixo da margem ideal**
            """)
    
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[6]:  # COMANDO DE VOZ
    st.markdown("<div class='section-title'><i class='bi bi-mic'></i> COMANDO DE VOZ QUÂNTICO</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='voice-command'>", unsafe_allow_html=True)
    st.markdown("**🎤 Sistema de Reconhecimento de Voz**")
    st.markdown("Clique no microfone e dite seu comando:")
    
    comando = st.text_input("Ou digite seu comando aqui:", placeholder="Ex: 'lançar horas', 'novo projeto', 'status geral'")
    
    if st.button("🎤 Processar Comando", use_container_width=True) and comando:
        resultado = voice_system.processar_comando(comando)
        st.success(f"**Comando Processado:** {resultado}")
    
    # Formulário de lançamento rápido
    st.markdown("---")
    st.markdown("**📝 Lançamento Rápido de Horas**")
    
    with st.form("lancamento_horas"):
        col1, col2, col3 = st.columns(3)
        with col1:
            consultor = st.selectbox("Consultor", df_filtrado['Consultor'].unique())
        with col2:
            projeto = st.selectbox("Projeto", df_filtrado['Projeto'].unique())
        with col3:
            horas = st.number_input("Horas Realizadas", min_value=0.0, step=0.5)
        
        if st.form_submit_button("💾 Lançar Horas", use_container_width=True):
            st.success(f"Horas lançadas para {consultor} no projeto {projeto}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- RODAPÉ QUÂNTICO ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666; font-size: 0.8rem;'>", unsafe_allow_html=True)
st.markdown("MAESTRO QUÂNTICO v8.0 · Sistema de Diagnóstico Empresarial Dinâmico · Baseado nos Princípios da Computação Quântica")
st.markdown("</div>", unsafe_allow_html=True)