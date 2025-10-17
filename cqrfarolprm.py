# -*- coding: utf-8 -*-
# MAESTRO QUÂNTICO v3.0 - A Sinfonia Completa

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
st.set_page_config(
    page_title="MAESTRO QUÂNTICO - Inteligência Preditiva",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILO CSS AVANÇADO (COM PAINÉIS AMOLED) ---
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
        background: rgba(10, 8, 24, 0.8);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(0, 191, 255, 0.2);
        margin-bottom: 20px;
        box-shadow: 0 0 20px rgba(0, 191, 255, 0.1);
    }
    .insight-card, .alert-card, .success-card {
        background: rgba(28, 28, 40, 0.7); border-radius: 15px; padding: 25px;
        border: 1px solid rgba(0, 191, 255, 0.2); margin-bottom: 15px;
    }
    .insight-card { border-left: 5px solid #FFD700; }
    .alert-card { border-left: 5px solid #FF4500; }
    .success-card { border-left: 5px solid #39FF14; }
</style>
""", unsafe_allow_html=True)

# --- NÚCLEO DE CONEXÃO E EXTRAÇÃO DE DADOS ---
# (Mantido como na versão anterior, já validado)
class DataOrchestrator:
    # ... (código da classe DataOrchestrator permanece o mesmo) ...

# --- MOTOR DE ANÁLISE QUÂNTICO v3.0 (IA APRIMORADA) ---
class QuantumAnalyticsEngine:
    # ... (código do __init__, _load_data, _processar_dados, _create_mock_data, aplicar_filtros permanecem os mesmos) ...

    def gerar_insights_prescritivos(self):
        df = self.dados_filtrados
        if df.empty or len(df) < 3:
            return [{'tipo': 'info', 'texto': 'Dados insuficientes para gerar insights. Altere os filtros para uma análise mais ampla.'}]
        
        insights = []

        # Insight 1: Análise de Senioridade (Mantido)
        perf_nivel = df.groupby('Nivel_Consultor')['Margem_Percentual'].mean()
        if len(perf_nivel) > 1 and 'Não Definido' in perf_nivel: perf_nivel = perf_nivel.drop('Não Definido')
        if not perf_nivel.empty:
            nivel_max = perf_nivel.idxmax()
            margem_max = perf_nivel.max()
            insights.append({
                'tipo': 'sucesso',
                'texto': f"**Ressonância de Senioridade:** Consultores de nível **'{nivel_max}'** estão entregando a maior margem média (**{margem_max:.1f}%**). **Prescrição Estratégica:** Avalie o mix de projetos para maximizar a alocação deste nível nos contratos mais valiosos."
            })

        # Insight 2: Análise de Linha de Negócio (Mantido)
        perf_negocio = df.groupby('Negocio_Projeto')['Lucro_Total'].sum()
        if len(perf_negocio) > 1 and 'Não Definido' in perf_negocio: perf_negocio = perf_negocio.drop('Não Definido')
        if not perf_negocio.empty:
            negocio_max = perf_negocio.idxmax()
            lucro_max = perf_negocio.max()
            insights.append({
                'tipo': 'oportunidade',
                'texto': f"**Foco de Lucratividade:** A linha de negócio **'{negocio_max}'** é a mais lucrativa, gerando **R$ {lucro_max:,.2f}** de lucro total. **Prescrição Comercial:** Direcione os esforços de vendas para expandir a carteira nesta área."
            })

        # Insight 3 (NOVO): Detecção de Anomalia (Outlier) na Margem
        if 'Margem_Percentual' in df.columns and len(df) > 5:
            q1 = df['Margem_Percentual'].quantile(0.25)
            q3 = df['Margem_Percentual'].quantile(0.75)
            iqr = q3 - q1
            limite_inferior = q1 - 1.5 * iqr
            
            anomalias = df[df['Margem_Percentual'] < limite_inferior]
            if not anomalias.empty:
                anomalia_critica = anomalias.sort_values('Margem_Percentual').iloc[0]
                insights.append({
                    'tipo': 'alerta',
                    'texto': f"**Interferência Destrutiva:** O projeto **'{anomalia_critica['Projeto']}'** com o consultor **'{anomalia_critica['Consultor']}'** apresenta uma margem de **{anomalia_critica['Margem_Percentual']:.1f}%**, um valor significativamente abaixo do padrão. **Ação Imediata:** Revisar os custos, escopo e alocação deste projeto."
                })
        
        return insights if insights else [{'tipo': 'info', 'texto': 'A orquestra está em harmonia. Nenhuma anomalia crítica detectada nos filtros atuais.'}]

# (O resto do código base, como a inicialização do engine, é mantido)
# ...

# --- INICIALIZAÇÃO ---
@st.cache_resource
def init_engine():
    # Esta função agora precisa ser definida, pois o código de exemplo não a continha.
    class QuantumAnalyticsEngine:
        # ... (Definição completa da classe como acima) ...
        pass
    
    class DataOrchestrator:
        # ... (Definição completa da classe como acima) ...
        pass

    return QuantumAnalyticsEngine()

engine = init_engine()

# --- INTERFACE PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>MAESTRO QUÂNTICO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8A8A8A; margin-top: -10px;'>A Sinfonia Estratégica da Sua Consultoria</p>", unsafe_allow_html=True)

# --- SIDEBAR DE CONTROLES ---
# (O código da sidebar permanece o mesmo)
# ...

df_filtrado = engine.aplicar_filtros(filters) if 'filters' in locals() else engine.dados_filtrados

# --- ESTRUTURA DE ABAS COMPLETA ---
tab_names = ["Visão Geral", "Análise Dimensional", "Consultores & Projetos", "Fechamento", "Comparativo", "Simulador", "Apontamento", "Assistente IA"]
tabs = st.tabs([f"**{name}**" for name in tab_names])

# Tab 1: Visão Geral (com KPIs aprimorados e novos gráficos)
with tabs[0]:
    if df_filtrado.empty: st.warning("Nenhum dado para exibir com os filtros atuais.")
    else:
        st.markdown('<div class="data-panel">', unsafe_allow_html=True)
        
        # KPIs aprimorados
        kpis = {
            'receita_total': df_filtrado['Receita_Total'].sum(),
            'lucro_total': df_filtrado['Lucro_Total'].sum(),
            'margem_media': df_filtrado['Margem_Percentual'][df_filtrado['Margem_Percentual'] > 0].mean(),
            'horas_realizadas': df_filtrado['Horas_Realizadas'].sum(),
            'horas_previstas': df_filtrado['Horas_Previstas'].sum(),
        }
        kpis['delta_horas'] = kpis['horas_realizadas'] - kpis['horas_previstas']
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Receita Total", f"R$ {kpis['receita_total']:,.0f}")
        c2.metric("Lucro Total", f"R$ {kpis['lucro_total']:,.0f}")
        c3.metric("Margem Média", f"{kpis['margem_media']:.1f}%")
        
        delta_icon = "▲" if kpis['delta_horas'] >= 0 else "▼"
        delta_color = "normal" if kpis['delta_horas'] >= 0 else "inverse" # Verde para mais horas, vermelho para menos
        c4.metric("Horas Realizadas", f"{kpis['horas_realizadas']:.0f}h", f"{delta_icon} {kpis['delta_horas']:.0f}h vs. Orçado", delta_color=delta_color)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Faturamento por Cliente")
            receita_cliente = df_filtrado.groupby('Cliente')['Receita_Total'].sum().nlargest(7)
            fig = px.pie(receita_cliente, values='Receita_Total', names=receita_cliente.index, hole=0.5)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', legend_title_text='Clientes')
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("### Horas: Orçado vs. Realizado")
            horas_agg = df_filtrado.groupby('Negocio_Projeto')[['Horas_Previstas', 'Horas_Realizadas']].sum()
            fig = go.Figure(data=[
                go.Bar(name='Orçado', x=horas_agg.index, y=horas_agg['Horas_Previstas']),
                go.Bar(name='Realizado', x=horas_agg.index, y=horas_agg['Horas_Realizadas'])
            ])
            fig.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)

# Tab 2: Análise Dimensional (Mantida)
with tabs[1]:
    # ... (código da aba Análise Dimensional) ...

# Tab 3: Consultores & Projetos (Mantida)
with tabs[2]:
    # ... (código da aba Consultores & Projetos) ...

# Tab 4: Fechamento (NOVA)
with tabs[3]:
    st.header("Fechamento Financeiro")
    if not df_filtrado.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("💰 A Pagar (Consultores)")
            df_pagar = df_filtrado.groupby(['Consultor', 'Nivel_Consultor']).agg(
                Custo_Total=('Custo_Total', 'sum'),
                Horas_Trabalhadas=('Horas_Realizadas', 'sum')
            ).reset_index().sort_values('Custo_Total', ascending=False)
            st.dataframe(df_pagar.style.format({"Custo_Total": "R$ {:,.2f}"}), use_container_width=True)
            
            # Exportar para Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_pagar.to_excel(writer, index=False, sheet_name='A_Pagar')
            st.download_button("📥 Exportar (A Pagar)", output.getvalue(), "a_pagar.xlsx")

        with c2:
            st.subheader("💳 A Receber (Clientes)")
            df_receber = df_filtrado.groupby('Cliente').agg(
                Receita_Total=('Receita_Total', 'sum'),
                Horas_Faturadas=('Horas_Realizadas', 'sum')
            ).reset_index().sort_values('Receita_Total', ascending=False)
            st.dataframe(df_receber.style.format({"Receita_Total": "R$ {:,.2f}"}), use_container_width=True)
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_receber.to_excel(writer, index=False, sheet_name='A_Receber')
            st.download_button("📥 Exportar (A Receber)", output.getvalue(), "a_receber.xlsx")
    else:
        st.warning("Nenhum dado para exibir.")

# Tab 5: Comparativo (NOVA)
with tabs[4]:
    st.header("Análise Comparativa Entre Períodos")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Período 1 (Referência)")
        ano1 = st.selectbox("Ano 1", sorted(engine.dados_originais['Ano'].unique()), key="ano1")
        mes1 = st.selectbox("Mês 1", sorted(engine.dados_originais['Mes'].unique()), key="mes1")
    with c2:
        st.subheader("Período 2 (Comparação)")
        ano2 = st.selectbox("Ano 2", sorted(engine.dados_originais['Ano'].unique()), index=1 if len(engine.dados_originais['Mes'].unique()) > 1 else 0, key="ano2")
        mes2 = st.selectbox("Mês 2", sorted(engine.dados_originais['Mes'].unique()), index=1 if len(engine.dados_originais['Mes'].unique()) > 1 else 0, key="mes2")

    p1 = engine.dados_originais[(engine.dados_originais['Ano']==ano1) & (engine.dados_originais['Mes']==mes1)]
    p2 = engine.dados_originais[(engine.dados_originais['Ano']==ano2) & (engine.dados_originais['Mes']==mes2)]

    if p1.empty or p2.empty:
        st.warning("Um dos períodos selecionados não contém dados.")
    else:
        receita1, receita2 = p1['Receita_Total'].sum(), p2['Receita_Total'].sum()
        lucro1, lucro2 = p1['Lucro_Total'].sum(), p2['Lucro_Total'].sum()
        
        st.markdown("---")
        st.subheader("Resultados da Comparação")
        c1, c2 = st.columns(2)
        c1.metric(f"Receita Período 2 ({mes2}/{ano2})", f"R$ {receita2:,.0f}", f"{((receita2-receita1)/receita1)*100 if receita1 else 0:.1f}% vs. Período 1")
        c2.metric(f"Lucro Período 2 ({mes2}/{ano2})", f"R$ {lucro2:,.0f}", f"{((lucro2-lucro1)/lucro1)*100 if lucro1 else 0:.1f}% vs. Período 1")

# Tab 6: Simulador (NOVA)
with tabs[5]:
    st.header("Simulador de Realidades")
    # ... (Lógica do simulador pode ser adicionada aqui) ...
    st.info("Funcionalidade em desenvolvimento.")

# Tab 7: Apontamento (NOVA)
with tabs[6]:
    st.header("Apontamento Simplificado por Voz (Protótipo)")
    # ... (Lógica do apontamento por voz pode ser adicionada aqui) ...
    st.info("Funcionalidade em desenvolvimento.")

# Tab 8: Assistente IA (Melhorada)
with tabs[7]:
    # ... (código da aba Assistente IA com a nova função de insights) ...