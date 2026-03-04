import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ---------------------------------------------------------
# 1. CONFIGURAÇÃO UI/UX E LOGIN
# ---------------------------------------------------------
st.set_page_config(page_title="Megalink - BI Operacional", layout="wide")

def verificar_senha():
    def senha_inserida():
        if st.session_state["password"] == "megalink2024":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<h1 style='text-align: center; color: #00d1ff; font-family: Orbitron;'>ACESSO RESTRITO</h1>", unsafe_allow_html=True)
        st.text_input("Digite a senha de acesso", type="password", on_change=senha_inserida, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Senha incorreta. Tente novamente", type="password", on_change=senha_inserida, key="password")
        st.error("😕 Acesso negado.")
        return False
    return True

def aplicar_design_premium():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
        .block-container { padding-top: 1.5rem !important; }
        .stApp { background: radial-gradient(circle at top right, #0d1117, #010409); color: #e6edf3; font-family: 'Inter', sans-serif; }
        .neon-title { font-family: 'Orbitron', sans-serif; color: #00d1ff; text-shadow: 0 0 15px rgba(0, 209, 255, 0.6); font-size: 1.8rem; margin-bottom: 20px; }
        .glass-card { background: rgba(22, 27, 34, 0.7); backdrop-filter: blur(10px); border-radius: 15px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; }
        .metric-card { background: rgba(0, 209, 255, 0.05); border: 1px solid rgba(0, 209, 255, 0.3); border-radius: 12px; padding: 20px; text-align: center; }
        .stButton>button { width: 100%; border-radius: 10px; background-color: rgba(0, 209, 255, 0.1); color: #00d1ff; border: 1px solid #00d1ff; transition: 0.3s; }
        .stButton>button:hover { background-color: #00d1ff; color: #000; box-shadow: 0 0 20px rgba(0, 209, 255, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. CARREGAMENTO DE DADOS
# ---------------------------------------------------------
@st.cache_data(ttl=600)
def carregar_dados_mestre():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRhakH8eejohlExEaPwdEc3juvNyv7oK21XS8jLoPqRxFfgHJjERxG-SkE2Ugy5B95677gh7nj0Wet/pub?gid=1830501183&single=true&output=csv"
    df = pd.read_csv(url)
    cols = df.columns.tolist()
    df = df.rename(columns={cols[0]: 'CÓDIGO', cols[1]: 'DATA', cols[2]: 'COLABORADOR', cols[3]: 'CARGO', cols[4]: 'SUPERVISOR'})
    df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True, errors='coerce')
    df = df.replace(r'^\s*$', np.nan, regex=True).replace('None', np.nan)
    return df, cols

def obter_nomes_itens(cod_ini, colunas_reais):
    if cod_ini == 1: return [colunas_reais[50]]
    elif cod_ini == 1001: return colunas_reais[6:19]
    elif cod_ini == 2001: return colunas_reais[19:40]
    elif cod_ini == 3001: return colunas_reais[40:50]
    return []

# ---------------------------------------------------------
# 3. ABA: RELATÓRIO GERAL (CONSOLIDADO)
# ---------------------------------------------------------
def renderizar_relatorio_geral(df_base, colunas_reais):
    st.markdown("<h2 class='neon-title'>RELATÓRIO GERAL DE OPERAÇÕES</h2>", unsafe_allow_html=True)
    
    categorias = {
        "Fardamento": obter_nomes_itens(1, colunas_reais),
        "Equipamentos": obter_nomes_itens(1001, colunas_reais),
        "Ferramentas": obter_nomes_itens(2001, colunas_reais),
        "EPI": obter_nomes_itens(3001, colunas_reais)
    }
    
    all_rows = []
    for cat, itens in categorias.items():
        temp_df = df_base.melt(id_vars=['DATA', 'SUPERVISOR', 'COLABORADOR'], value_vars=itens, var_name='Item', value_name='Status')
        temp_df['Categoria'] = cat
        all_rows.append(temp_df)
    
    df_global = pd.concat(all_rows)
    df_global['Status'] = df_global['Status'].fillna('Preservado')
    df_global['Conforme'] = df_global['Status'].apply(lambda x: 1 if str(x).lower() == 'preservado' else 0)

    # KPIs Exigidos
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='metric-card'><h5>Índice de Preservação Global</h5><h2 style='color:#00FF7F;'>{int(df_global['Conforme'].mean()*100)}%</h2></div>", unsafe_allow_html=True)
    with m2:
        total_avarias = len(df_global[df_global['Conforme'] == 0])
        st.markdown(f"<div class='metric-card'><h5>Avarias Totais</h5><h2 style='color:#FF3131;'>{total_avarias}</h2></div>", unsafe_allow_html=True)
    with m3:
        melhor_sup = df_global.groupby('SUPERVISOR')['Conforme'].mean().idxmax()
        st.markdown(f"<div class='metric-card'><h5>Líder em Conservação</h5><h2 style='color:#00d1ff;'>{melhor_sup}</h2></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([6, 4])
    with c1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        df_cat = df_global.groupby(['Categoria', 'Conforme']).size().reset_index(name='Qtd')
        df_cat['Situação'] = df_cat['Conforme'].map({1: 'OK', 0: 'Avaria'})
        fig = px.bar(df_cat, x='Categoria', y='Qtd', color='Situação', barmode='group',
                     color_discrete_map={'OK':'#00FF7F','Avaria':'#FF3131'}, template="plotly_dark", title="PANORAMA POR CATEGORIA")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        df_rad = df_global.groupby('SUPERVISOR')['Conforme'].mean().reset_index()
        fig_r = go.Figure(go.Scatterpolar(r=df_rad['Conforme']*100, theta=df_rad['SUPERVISOR'], fill='toself', line=dict(color='#00d1ff')))
        fig_r.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), template="plotly_dark", title="SCORE GERAL DE LIDERANÇA")
        st.plotly_chart(fig_r, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. EXECUÇÃO PRINCIPAL
# ---------------------------------------------------------
if verificar_senha():
    aplicar_design_premium()
    
    with st.sidebar:
        st.image("https://logodownload.org/wp-content/uploads/2020/02/megalink-logo.png", width=150)
        st.markdown("---")
        if st.button("🔄 ATUALIZAR DADOS"):
            st.cache_data.clear()
            st.toast("Dados atualizados!", icon="✅")
            st.rerun()
        st.info("Senha de acesso: megalink2024")

    df_base, colunas_reais = carregar_dados_mestre()

    st.markdown("<h1 class='neon-title'>MEGALINK BI OPERACIONAL</h1>", unsafe_allow_html=True)
    abas = st.tabs(["📊 Relatório Geral", "👕 Fardamento", "🛠️ Equipamentos", "🔧 Ferramentas", "🛡️ EPI"])
    
    with abas[0]:
        renderizar_relatorio_geral(df_base, colunas_reais)

    modulos = [
        {"nome": "Fardamento", "ini": 1, "aba": abas[1]},
        {"nome": "Equipamentos", "ini": 1001, "aba": abas[2]},
        {"nome": "Ferramentas", "ini": 2001, "aba": abas[3]},
        {"nome": "EPI", "ini": 3001, "aba": abas[4]}
    ]

    for mod in modulos:
        with mod["aba"]:
            ini = mod["ini"]
            df_s = df_base[(df_base['CÓDIGO'].astype(float) >= ini) & (df_base['CÓDIGO'].astype(float) <= ini+999)]
            nomes_itens = obter_nomes_itens(ini, colunas_reais)
            
            # Filtros Superior
            f1, f2 = st.columns(2)
            with f1: f_col = st.selectbox(f"Colaborador ({mod['nome']})", ["Todos"] + sorted(df_s['COLABORADOR'].dropna().unique().tolist()), key=f"c_{ini}")
            with f2: f_sup = st.selectbox(f"Supervisor ({mod['nome']})", ["Todos"] + sorted(df_s['SUPERVISOR'].dropna().unique().tolist()), key=f"s_{ini}")
            
            df_f = df_s.copy()
            if f_col != "Todos": df_f = df_f[df_f['COLABORADOR'] == f_col]
            if f_sup != "Todos": df_f = df_f[df_f['SUPERVISOR'] == f_sup]

            # GRAFICOS ORIGINAIS RESTAURADOS
            df_long = df_f.melt(id_vars=['DATA', 'COLABORADOR', 'SUPERVISOR'], value_vars=nomes_itens, var_name='Item', value_name='Obs').fillna('Preservado')
            df_long['Conforme'] = df_long['Obs'].apply(lambda x: 1 if str(x).lower() == 'preservado' else 0)

            c_graf1, c_graf2 = st.columns([6, 4])
            with c_graf1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                fig_bar = px.bar(df_long.groupby(['Item', 'Conforme']).size().reset_index(name='Qtd'), 
                                x='Item', y='Qtd', color=df_long.groupby(['Item', 'Conforme']).size().reset_index(name='Qtd')['Conforme'].map({1:'OK', 0:'Avaria'}),
                                title=f"Estado de Prontidão: {mod['nome']}", color_discrete_map={'OK': '#00FF7F', 'Avaria': '#FF3131'}, template="plotly_dark")
                st.plotly_chart(fig_bar, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with c_graf2:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                df_rad_a = df_long.groupby('SUPERVISOR')['Conforme'].mean().reset_index()
                fig_rad_a = go.Figure(go.Scatterpolar(r=df_rad_a['Conforme']*100, theta=df_rad_a['SUPERVISOR'], fill='toself', line=dict(color='#00d1ff')))
                fig_rad_a.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), template="plotly_dark", title=f"Score de Cuidado: {mod['nome']}")
                st.plotly_chart(fig_rad_a, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # TABELAS RESTAURADAS
            st.markdown(f"### 🚨 Itens para Reposição: {mod['nome']}")
            df_rep = df_long[df_long['Conforme'] == 0]
            st.dataframe(df_rep[['DATA', 'COLABORADOR', 'SUPERVISOR', 'Item', 'Obs']], use_container_width=True, hide_index=True)
            
            st.markdown(f"### 📋 Histórico Detalhado: {mod['nome']}")
            st.dataframe(df_f[['DATA', 'COLABORADOR', 'SUPERVISOR'] + nomes_itens].fillna("Preservado"), use_container_width=True, hide_index=True)