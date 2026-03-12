import streamlit as st 
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import io

st.set_page_config(page_title="Operacional Backbone", layout="wide")

# ================================
# CORREÇÃO VISUAL E ESTILO LOGIN (CSS CUSTOMIZADO)
# ================================
st.markdown("""
<style>
/* Reset e Variáveis do seu CSS */
:root {
  --primary: #00D9FF;
  --primary-foreground: #0A0E27;
  --background: #0A0E27;
  --foreground: #E0F7FF;
  --card: #0F1535;
  --card-foreground: #E0F7FF;
  --radius: 0.5rem;
  --border: #003D66;
}

/* Esconder Header Padrão */
header {visibility: hidden;}
[data-testid="stHeader"] {visibility: hidden;}
[data-testid="stToolbar"] {right: 2rem;}

/* Animações e Efeitos do Login */
@keyframes scan-lines {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}

.stForm {
    background-color: var(--card) !important;
    border: 2px solid var(--primary) !important;
    border-radius: var(--radius) !important;
    padding: 2rem !important;
    box-shadow: 0 0 15px rgba(0, 217, 255, 0.2) !important;
}

.glow-title {
    color: #FFFFFF !important;
    text-align: center;
    font-family: 'Poppins', sans-serif;
    text-shadow: none !important;
    font-weight: 700;
}

/* Efeito de scan no fundo da tela de login */
.login-bg {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: repeating-linear-gradient(0deg, rgba(0, 217, 255, 0.03) 0px, transparent 1px, transparent 2px);
    pointer-events: none;
    animation: scan-lines 10s linear infinite;
    z-index: 0;
}

/* Blocos de Região para a Nova Escala */
.region-header {
    background-color: #003D66;
    color: white;
    padding: 10px;
    border-radius: 5px;
    margin-top: 25px;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    border-left: 5px solid #00D9FF;
}

/* Estilo da Legenda */
.legenda-box {
    background-color: rgba(0, 217, 255, 0.05);
    border: 1px solid #00D9FF;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 15px;
}

.legenda-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 8px;
}

.legenda-item {
    font-size: 0.75rem;
    padding: 3px 6px;
    border-radius: 4px;
}

/* AJUSTE DE FONTE E TABELA PARA 26 LINHAS - COMPACIDADE MÁXIMA */
[data-testid="stDataEditor"] {
    font-size: 10.5px !important;
}

[data-testid="stDataEditor"] div {
    font-size: 10.5px !important;
}

/* Reduzir padding das células */
div[data-testid="stDataEditor"] div[role="gridcell"] {
    padding-top: 0px !important;
    padding-bottom: 0px !important;
}

/* LÓGICA DE CORES VIA CSS PARA O EDITOR */
div[data-testid="stDataEditor"] div[role="gridcell"]:has(div:contains("F")) { background-color: #FF0000 !important; color: white !important; }
div[data-testid="stDataEditor"] div[role="gridcell"]:has(div:contains("AT")) { background-color: #9966FF !important; color: white !important; }
div[data-testid="stDataEditor"] div[role="gridcell"]:has(div:contains("BK")) { background-color: #FF9900 !important; color: black !important; }
div[data-testid="stDataEditor"] div[role="gridcell"]:has(div:contains("FO")) { background-color: #2E7D32 !important; color: white !important; }
div[data-testid="stDataEditor"] div[role="gridcell"]:has(div:contains("SB")) { background-color: #FFFF00 !important; color: black !important; }
div[data-testid="stDataEditor"] div[role="gridcell"]:has(div:contains("T")) { background-color: #1976D2 !important; color: white !important; }
div[data-testid="stDataEditor"] div[role="gridcell"]:has(div:contains("V")) { background-color: #F06292 !important; color: black !important; }
div[data-testid="stDataEditor"] div[role="gridcell"]:has(div:contains("FE")) { background-color: #00E5FF !important; color: black !important; }
div[data-testid="stDataEditor"] div[role="gridcell"]:has(div:contains("DF")) { background-color: #795548 !important; color: white !important; }

/* Destaque para a linha de Supervisor Interno */
div[data-testid="stDataEditor"] div[role="row"]:nth-child(2) div[role="gridcell"] {
    font-weight: bold !important;
    border-bottom: 2px solid var(--primary) !important;
    background-color: rgba(0, 217, 255, 0.05) !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CACHE DE LEITURA DAS PLANILHAS (MANTIDO INTEGRAL)
# =========================================================

@st.cache_data(ttl=300)
def carregar_csv(url):
    try:
        return pd.read_csv(url, on_bad_lines='skip', low_memory=False)
    except Exception as e:
        st.error(f"Erro ao conectar com a base de dados: {e}")
        return pd.DataFrame()


# =========================================================
# 1. ACESSO E CONFIGURAÇÃO
# =========================================================
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False


def tela_login():
    st.markdown('<div class="login-bg"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<h1 class="glow-title">🔒 OPERACIONAL BACKBONE</h1>', unsafe_allow_html=True)
        st.write("") 

        with st.form("login_form"):
            st.markdown('<p style="color:#00D9FF; text-align:center;">SISTEMA DE GESTÃO OPERACIONAL</p>', unsafe_allow_html=True)
            senha = st.text_input("Credencial de Acesso", type="password")
            submit = st.form_submit_button("DESBLOQUEAR ACESSO")

            if submit:
                if senha == "megalink2024":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Acesso Negado: Credencial Inválida")


if not st.session_state["autenticado"]:
    tela_login()
    st.stop()


# =========================================================
# 2. BASES DE DADOS
# =========================================================

URL_EPI = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRhakH8eejohlExEaPwdEc3juvNyv7oK21XS8jLoPqRxFfgHJjERxG-SkE2Ugy5B95677gh7nj0Wet/pub?gid=304420373&single=true&output=csv"
URL_EQUIP = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRhakH8eejohlExEaPwdEc3juvNyv7oK21XS8jLoPqRxFfgHJjERxG-SkE2Ugy5B95677gh7nj0Wet/pub?gid=932732884&single=true&output=csv"
URL_FERRA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRhakH8eejohlExEaPwdEc3juvNyv7oK21XS8jLoPqRxFfgHJjERxG-SkE2Ugy5B95677gh7nj0Wet/pub?gid=907191989&single=true&output=csv"
URL_FARD = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRhakH8eejohlExEaPwdEc3juvNyv7oK21XS8jLoPqRxFfgHJjERxG-SkE2Ugy5B95677gh7nj0Wet/pub?gid=353539867&single=true&output=csv"

# Base de contatos para Dropdowns e Informativo
BASE_CONTATOS = carregar_csv(URL_EPI)

# =========================================================
# 3. FUNÇÕES ORIGINAIS
# =========================================================

def limpar_media(df):
    termos = [
        'FOTO','MIDIA','MÍDIA','ANEXO',
        'URL','LINK','IMAGEM',
        'CIENTE','DECLARAÇÃO','ASSINATURA'
    ]
    cols_drop = [
        c for c in df.columns
        if any(t in str(c).upper() for t in termos)
        or df[c].astype(str).str.contains('http', na=False).any()
    ]
    return df.drop(columns=cols_drop)


def padronizar_status(df, colunas):
    for col in colunas:
        df[col] = df[col].astype(str).str.strip().str.lower()
        df[col] = df[col].replace(
            ['nan','null','0','0.0','preservado','preservada'],
            'PRESERVADO'
        )
        df[col] = df[col].str.upper()
    return df


def gerenciar_filtros(df, key_suffix):
    col_data = df.columns[0]
    df[col_data] = pd.to_datetime(df[col_data], dayfirst=True, errors='coerce')
    df = df.dropna(subset=[col_data])
    df['Mes_Ano_Ref'] = df[col_data].dt.strftime('%m/%Y')
    meses_disponiveis = sorted(df['Mes_Ano_Ref'].unique(), reverse=True)
    c1, c2 = st.columns([3,1])
    with c2:
        btn_limpar = st.button("🧹 Limpar filtro", key=f"btn_limpar_{key_suffix}")
    if btn_limpar:
        st.session_state[f"sel_{key_suffix}"] = "Todos"
        st.rerun()
    with c1:
        mes_sel = st.selectbox(
            "Filtrar por Mês",
            ["Todos"] + meses_disponiveis,
            key=f"sel_{key_suffix}"
        )
    if mes_sel != "Todos":
        df = df[df['Mes_Ano_Ref'] == mes_sel]
    return df.drop(columns=['Mes_Ano_Ref'])


# =========================================================
# 4. TÍTULO E ABAS
# =========================================================

st.markdown(
    "<h1 style='color:#FFFFFF;'>Operacional Backbone</h1>",
    unsafe_allow_html=True
)

abas = st.tabs([
    "🛡️ EPI",
    "🛠️ EQUIPAMENTOS",
    "🔧 FERRAMENTAS",
    "👕 FARDAMENTO",
    "📦 REPOSIÇÃO",
    "📊 INTELIGÊNCIA OPERACIONAL",
    "📝 GERÊNCIA DE OS"
])


# =========================================================
# GUIA 01 — EPI
# =========================================================

with abas[0]:
    df_epi = carregar_csv(URL_EPI).iloc[:,1:]
    df_epi = limpar_media(df_epi)
    df_epi = gerenciar_filtros(df_epi,"epi")
    cols_itens_epi = [c for c in df_epi.columns[5:]]
    df_epi = padronizar_status(df_epi,cols_itens_epi)
    f1,f2 = st.columns(2)
    c_epi = f1.multiselect(
        "Colaborador",
        sorted(df_epi.iloc[:,1].unique()),
        key="f_epi_colab_aba0"
    )
    s_epi = f2.multiselect(
        "Supervisor",
        sorted(df_epi.iloc[:,3].fillna("N/I").unique()),
        key="f_epi_super_aba0"
    )
    df_f_epi = df_epi.copy()
    if c_epi:
        df_f_epi = df_f_epi[df_f_epi.iloc[:,1].isin(c_epi)]
    if s_epi:
        df_f_epi = df_f_epi[df_f_epi.iloc[:,3].isin(s_epi)]
    cg1,cg2 = st.columns(2)
    with cg1:
        df_chart = df_f_epi.melt(
            value_vars=cols_itens_epi
        )['value'].value_counts().reset_index()
        df_chart.columns = ['Status','Quantidade']
        st.plotly_chart(
            px.bar(
                df_chart,
                x='Status',
                y='Quantidade',
                title="Panorama Geral EPI",
                template="plotly_dark",
                color='Status'
            ),
            use_container_width=True
        )
    with cg2:
        df_perf = df_f_epi.melt(
            id_vars=[df_f_epi.columns[3]],
            value_vars=cols_itens_epi,
            value_name='Status'
        )
        df_perf = df_perf[df_perf['Status']=='PRESERVADO']
        df_perf = df_perf.groupby(
            df_f_epi.columns[3]
        ).size().reset_index(name='Qtd OK')
        st.plotly_chart(
            px.pie(
                df_perf,
                names=df_perf.columns[0],
                values='Qtd OK',
                title="Performance Supervisor",
                hole=0.4,
                template="plotly_dark"
            ),
            use_container_width=True
        )
    st.dataframe(df_f_epi,use_container_width=True)


# =========================================================
# GUIA 02 — EQUIPAMENTOS
# =========================================================

with abas[1]:
    df_equip = carregar_csv(URL_EQUIP).iloc[:,1:]
    df_equip = limpar_media(df_equip)
    df_equip = gerenciar_filtros(df_equip,"eq")
    cols_itens_eq = [c for c in df_equip.columns[6:]]
    df_equip = padronizar_status(df_equip,cols_itens_eq)
    f1,f2 = st.columns(2)
    sel_c_eq = f1.multiselect(
        "Colaborador",
        sorted(df_equip.iloc[:,1].unique()),
        key="c_eq_aba1"
    )
    sel_s_eq = f2.multiselect(
        "Supervisor",
        sorted(df_equip.iloc[:,4].unique()),
        key="s_eq_aba1"
    )
    df_f_eq = df_equip.copy()
    if sel_c_eq:
        df_f_eq = df_f_eq[df_f_eq.iloc[:,1].isin(sel_c_eq)]
    if sel_s_eq:
        df_f_eq = df_f_eq[df_f_eq.iloc[:,4].isin(sel_s_eq)]
    g1_eq, g2_eq = st.columns(2)
    with g1_eq:
        df_m_eq = df_f_eq.melt(
            id_vars=df_f_eq.columns[:5],
            value_vars=cols_itens_eq,
            var_name='Item',
            value_name='Status'
        )
        df_chart_eq = df_m_eq.groupby(
            ['Item','Status']
        ).size().reset_index(name='Qtd')
        st.plotly_chart(
            px.bar(
                df_chart_eq,
                x='Item',
                y='Qtd',
                color='Status',
                barmode='group',
                template="plotly_dark"
            ),
            use_container_width=True
        )
    with g2_eq:
        df_p_eq = df_m_eq[df_m_eq['Status']=='PRESERVADO']
        df_p_eq = df_p_eq.groupby(
            df_f_eq.columns[4]
        ).size().reset_index(name='Total OK')
        st.plotly_chart(
            px.pie(
                df_p_eq,
                names=df_p_eq.columns[0],
                values='Total OK',
                title="Performance Supervisor",
                hole=0.4,
                template="plotly_dark"
            ),
            use_container_width=True
        )
    st.dataframe(df_f_eq,use_container_width=True)


# =========================================================
# GUIA 03 — FERRAMENTAS
# =========================================================

with abas[2]:
    df_ferra = carregar_csv(URL_FERRA).iloc[:,1:]
    df_ferra = limpar_media(df_ferra)
    df_ferra = gerenciar_filtros(df_ferra,"fe")
    cols_itens_fe = [c for c in df_ferra.columns[6:]]
    df_ferra = padronizar_status(df_ferra,cols_itens_fe)
    f1_fe, f2_fe = st.columns(2)
    sel_c_fe = f1_fe.multiselect(
        "Colaborador",
        sorted(df_ferra.iloc[:,1].unique()),
        key="c_fe_aba2"
    )
    sel_s_fe = f2_fe.multiselect(
        "Supervisor",
        sorted(df_ferra.iloc[:,4].unique()),
        key="s_fe_aba2"
    )
    df_f_fe = df_ferra.copy()
    if sel_c_fe:
        df_f_fe = df_f_fe[df_f_fe.iloc[:,1].isin(sel_c_fe)]
    if sel_s_fe:
        df_f_fe = df_f_fe[df_f_fe.iloc[:,4].isin(sel_s_fe)]
    g1_fe, g2_fe = st.columns(2)
    with g1_fe:
        df_m_fe = df_f_fe.melt(
            id_vars=df_f_fe.columns[:5],
            value_vars=cols_itens_fe,
            var_name='Item',
            value_name='Status'
        )
        df_chart_fe = df_m_fe.groupby(
            ['Item','Status']
        ).size().reset_index(name='Qtd')
        st.plotly_chart(
            px.bar(
                df_chart_fe,
                x='Item',
                y='Qtd',
                color='Status',
                barmode='group',
                template="plotly_dark"
            ),
            use_container_width=True
        )
    with g2_fe:
        df_p_fe = df_m_fe[df_m_fe['Status']=='PRESERVADO']
        df_p_fe = df_p_fe.groupby(
            df_f_fe.columns[4]
        ).size().reset_index(name='Total OK')
        st.plotly_chart(
            px.pie(
                df_p_fe,
                names=df_p_fe.columns[0],
                values='Total OK',
                title="Performance Supervisor",
                hole=0.4,
                template="plotly_dark"
            ),
            use_container_width=True
        )
    st.dataframe(df_f_fe,use_container_width=True)


# =========================================================
# GUIA 04 — FARDAMENTO
# =========================================================

with abas[3]:
    df_fard = carregar_csv(URL_FARD).iloc[:,1:]
    df_fard = limpar_media(df_fard)
    df_fard = gerenciar_filtros(df_fard,"fard")
    f_fard_colab = st.multiselect(
        "Filtrar Colaborador",
        sorted(df_fard.iloc[:,1].unique()),
        key="f_fard_colab_aba3"
    )
    df_f_fard = df_fard.copy()
    if f_fard_colab:
        df_f_fard = df_f_fard[df_f_fard.iloc[:,1].isin(f_fard_colab)]
    df_chart_fard = df_f_fard[df_f_fard.columns[5]].value_counts().reset_index()
    df_chart_fard.columns = ['Tempo','Quantidade']
    st.plotly_chart(
        px.bar(
            df_chart_fard,
            x='Tempo',
            y='Quantidade',
            title="Tempo de Uso",
            template="plotly_dark",
            color='Tempo'
        ),
        use_container_width=True
    )
    st.dataframe(df_f_fard,use_container_width=True)


# =========================================================
# GUIA 05 — REPOSIÇÃO
# =========================================================

with abas[4]:
    st.markdown("### 📦 Central de Reposição")
    
    lista_reposicao = []
    
    gatilhos = ['danificado','perdi','ruim','nao tenho','não tenho','pela metade']
    
    def normalizar(txt):
        txt = str(txt).lower().strip()
        txt = (
            txt.replace("ã","a")
               .replace("õ","o")
               .replace("á","a")
               .replace("é","e")
               .replace("í","i")
               .replace("ó","o")
               .replace("ú","u")
        )
        return txt

    def buscar(url,categoria,idx_inicio):
        try:
            temp = carregar_csv(url).iloc[:,1:]
            temp = limpar_media(temp)
            data_col = temp.columns[0]

            for _,linha in temp.iterrows():
                data = linha[data_col]
                colab = linha.iloc[1]
                itens = temp.columns[idx_inicio:]

                for it in itens:
                    stt = normalizar(linha[it])

                    if any(g in stt for g in gatilhos):
                        lista_reposicao.append(
                        {
                            'Data':data,
                            'Colaborador':colab,
                            'Categoria':categoria,
                            'Item':it,
                            'Status':stt.upper()
                        })

        except:
            pass


    buscar(URL_EPI,"EPI",5)
    buscar(URL_EQUIP,"EQUIPAMENTO",6)
    buscar(URL_FERRA,"FERRAMENTA",6)

    df_rep_total = pd.DataFrame(lista_reposicao)

    if not df_rep_total.empty:

        df_rep = gerenciar_filtros(df_rep_total,"reposicao")

        fr1, fr2 = st.columns(2)

        f_rep_colab = fr1.multiselect(
            "Colaborador",
            sorted(df_rep["Colaborador"].unique()),
            key="f_rep_colab_aba4"
        )

        f_rep_categoria = fr2.multiselect(
            "Categoria",
            sorted(df_rep["Categoria"].unique()),
            key="f_rep_categoria_aba4"
        )

        if f_rep_colab:
            df_rep = df_rep[df_rep["Colaborador"].isin(f_rep_colab)]

        if f_rep_categoria:
            df_rep = df_rep[df_rep["Categoria"].isin(f_rep_categoria)]

        st.table(df_rep)

    else:
        st.warning("Sem itens pendentes.")


# =========================================================
# GUIA 06 — INTELIGÊNCIA OPERACIONAL
# =========================================================

with abas[5]:
    st.markdown("## 📊 Dashboard Estratégico")
    if not df_rep_total.empty:
        df_intel = df_rep_total.copy()
        df_intel = gerenciar_filtros(df_intel, "intel_geral")
        fi1, fi2 = st.columns(2)
        f_intel_colab = fi1.multiselect("Colaborador", sorted(df_intel["Colaborador"].unique()), key="f_intel_colab_aba5")
        if f_intel_colab:
            df_intel = df_intel[df_intel["Colaborador"].isin(f_intel_colab)]
        col1,col2,col3 = st.columns(3)
        total = len(df_intel)
        colaboradores = df_intel["Colaborador"].nunique()
        itens = df_intel["Item"].nunique()
        col1.metric("Ocorrências", total)
        col2.metric("Colaboradores Impactados", colaboradores)
        col3.metric("Itens Diferentes", itens)
        st.divider()
        ranking_itens = (
            df_intel.groupby("Item")
            .size()
            .reset_index(name="Ocorrencias")
            .sort_values("Ocorrencias",ascending=False)
        )
        st.subheader("Ranking — Itens que mais quebram")
        st.plotly_chart(
            px.bar(
                ranking_itens,
                x="Item",
                y="Ocorrencias",
                color="Ocorrencias",
                template="plotly_dark"
            ),
            use_container_width=True
        )
        ranking_colab = (
            df_intel.groupby("Colaborador")
            .size()
            .reset_index(name="Ocorrencias")
            .sort_values("Ocorrencias",ascending=False)
        )
        st.subheader("Ranking — Colaboradores")
        st.plotly_chart(
            px.bar(
                ranking_colab.head(10),
                x="Colaborador",
                y="Ocorrencias",
                color="Ocorrencias",
                template="plotly_dark"
            ),
            use_container_width=True
        )
        st.subheader("Indicador de Risco Operacional")
        risco = round((total/(colaboradores+1))*10,2)
        st.metric("Índice de risco", risco)
        st.subheader("Previsão automática de reposição")
        previsao = ranking_itens.copy()
        previsao["Reposição Próximo Mês"] = (previsao["Ocorrencias"]*1.25).astype(int)
        st.dataframe(previsao,use_container_width=True)
    else:
        st.warning("Ainda não há dados suficientes para análise estratégica.")

# =========================================================
# GUIA 07 — GERÊNCIA DE OS (ESTRUTURA SAAS DASHBOARD)
# =========================================================

with abas[6]:
    # --- 1. ESTILO ESPECÍFICO PARA OS CARDS ---
    st.markdown("""
        <style>
        .metric-card {
            background-color: #0F1535;
            border: 1px solid #1E293B;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #00D9FF;
        }
        .metric-value { font-size: 28px; font-weight: bold; color: white; }
        .metric-label { font-size: 12px; color: #94A3B8; text-transform: uppercase; }
        </style>
    """, unsafe_allow_html=True)

    # Inicialização de variáveis de estado
    if "db_os" not in st.session_state:
        st.session_state["db_os"] = pd.DataFrame(columns=[
            "Número OS", "Trecho / Cliente", "Descrição", "Líder Responsável", 
            "Previsão", "Status", "Última Atualização", "Intervalo Alerta"
        ])

    # --- 2. CABEÇALHO E BOTÕES DE AÇÃO ---
    c_tit, c_btns = st.columns([1, 1.5])
    with c_tit:
        st.markdown("### Gerência de Ordens de Serviço")
    
    with c_btns:
        col_b1, col_b2, col_b3 = st.columns(3)
        btn_nova_os = col_b1.button("➕ Nova OS", use_container_width=True, type="primary")
        btn_relatorio = col_b2.button("📑 Relatório de Plantão", use_container_width=True)
        if col_b3.button("🗑️ Zerar Relatório", use_container_width=True):
            st.session_state["db_os"] = pd.DataFrame(columns=st.session_state["db_os"].columns)
            st.rerun()

    # --- 3. CARDS DE INDICADORES ---
    df_indicadores = st.session_state["db_os"]
    total_ativas = len(df_indicadores[df_indicadores["Status"] != "Concluída"])
    concluidas = len(df_indicadores[df_indicadores["Status"] == "Concluída"])
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.markdown(f'<div class="metric-card"><p class="metric-label">OS ATIVAS</p><p class="metric-value">{total_ativas}</p></div>', unsafe_allow_html=True)
    kpi2.markdown(f'<div class="metric-card" style="border-left-color: #EF4444;"><p class="metric-label">OS ATRASADAS</p><p class="metric-value">0</p></div>', unsafe_allow_html=True)
    kpi3.markdown(f'<div class="metric-card" style="border-left-color: #10B981;"><p class="metric-label">CONCLUÍDAS HOJE</p><p class="metric-value">{concluidas}</p></div>', unsafe_allow_html=True)
    kpi4.markdown(f'<div class="metric-card" style="border-left-color: #F59E0B;"><p class="metric-label">SEM ATUALIZAÇÃO +24H</p><p class="metric-value">0</p></div>', unsafe_allow_html=True)

    st.write("")

    # --- 4. ÁREA DE FILTROS ---
    with st.container():
        f_col1, f_col2, f_col3, f_col4 = st.columns([1, 1, 1, 2])
        filtro_st = f_col1.selectbox("Status:", ["Todos", "Aberta", "Em andamento", "Aguardando", "Concluída"])
        filtro_li = f_col2.selectbox("Líder:", ["Todos", "Danilo Italiano", "Luis Fernandes", "Marcia Jordana", "Reginaldo Lopes", "Vinicius Araújo"])
        f_col3.write("") # Espaçador
        check_att = f_col3.checkbox("Sem atualização +24h")

    # --- 5. MODAL DE CADASTRO (SIMULADO COM CALENDÁRIO) ---
    if btn_nova_os:
        st.session_state["modal_aberto"] = True

    if st.session_state.get("modal_aberto", False):
        with st.expander("📝 Formulário: Nova Ordem de Serviço", expanded=True):
            with st.form("nova_os_form"):
                c1, c2 = st.columns(2)
                num = c1.text_input("Número da OS", placeholder="Ex: OS-001")
                trecho_c = c2.text_input("Trecho / Cliente", placeholder="Ex: Rua A - Cliente X")
                
                obs = st.text_area("Descrição / Observações", placeholder="Descreva o trabalho a ser realizado")
                
                c3, c4 = st.columns(2)
                lider_os = c3.selectbox("Líder Responsável", ["Selecione um líder", "Danilo Italiano", "Luis Fernandes", "Marcia Jordana", "Reginaldo Lopes", "Vinicius Araújo"])
                status_os = c4.selectbox("Status", ["Aberta", "Em andamento", "Aguardando", "Concluída"])
                
                c5, c6 = st.columns(2)
                alerta = c5.number_input("⏰ Intervalo de Alerta (minutos)", value=30)
                # CALENDÁRIO PARA PREVISÃO
                previsao_dt = c6.date_input("Previsão de Atendimento (Data)", value=datetime.now())
                previsao_hr = c6.time_input("Previsão de Atendimento (Hora)")
                
                # CALENDÁRIO PARA HORÁRIO DA SITUAÇÃO (Como na imagem)
                c7, c8 = st.columns([2, 1])
                data_sit = c7.date_input("Horário da Situação", value=datetime.now())
                hora_sit = c7.time_input("Hora da Situação", label_visibility="collapsed")
                # Botão "Usar Agora" é simulado pelo valor padrão do datetime.now()
                
                st.markdown("---")
                f_btn1, f_btn2 = st.columns([1, 5])
                with f_btn1:
                    cancelar = st.form_submit_button("Cancelar")
                with f_btn2:
                    salvar = st.form_submit_button("Salvar OS", type="primary")

                if salvar:
                    if num and trecho_c and lider_os != "Selecione um líder":
                        # Junta data e hora para salvar na tabela
                        dt_previsao = f"{previsao_dt.strftime('%d/%m/%Y')} {previsao_hr.strftime('%H:%M')}"
                        dt_situacao = f"{data_sit.strftime('%d/%m/%Y')} {hora_sit.strftime('%H:%M')}"
                        
                        nova_linha = {
                            "Número OS": num, 
                            "Trecho / Cliente": trecho_c, 
                            "Descrição": obs,
                            "Líder Responsável": lider_os, 
                            "Previsão": dt_previsao, 
                            "Status": status_os,
                            "Última Atualização": dt_situacao, 
                            "Intervalo Alerta": alerta
                        }
                        st.session_state["db_os"] = pd.concat([st.session_state["db_os"], pd.DataFrame([nova_linha])], ignore_index=True)
                        st.session_state["modal_aberto"] = False
                        st.toast("OS Salva com Sucesso!", icon="✅")
                        st.rerun()
                    else:
                        st.error("Por favor, preencha os campos obrigatórios (Número, Trecho e Líder).")
                
                if cancelar:
                    st.session_state["modal_aberto"] = False
                    st.rerun()

    # --- 6. RELATÓRIO TEXTUAL (ESTRUTURA SOLICITADA) ---
    if btn_relatorio:
        st.markdown("#### 📋 Relatório para Cópia")
        data_h = datetime.now().strftime("%d/%m/%Y")
        data_a = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        
        rel_texto = f"Bom dia!\n\nSeguem os dados do plantão / sobreaviso {data_h} a {data_a}\n"
        rel_texto += "="*80 + "\n"
        
        if st.session_state["db_os"].empty:
            rel_texto += "\nNenhuma OS registrada neste período.\n"
        else:
            for _, r in st.session_state["db_os"].iterrows():
                rel_texto += f"\n📦 OS: {r['Número OS']} | {r['Trecho / Cliente']}\n"
                rel_texto += f"   Status: {r['Status']} | Líder: {r['Líder Responsável']}\n"
                rel_texto += f"   Descrição: {r['Descrição']}\n"
        
        rel_texto += "\n" + "="*80
        st.code(rel_texto, language="text")

    # --- 7. TABELA DE DADOS (DATA EDITOR) ---
    df_view = st.session_state["db_os"].copy()
    if filtro_st != "Todos": df_view = df_view[df_view["Status"] == filtro_st]
    if filtro_li != "Todos": df_view = df_view[df_view["Líder Responsável"] == filtro_li]

    st.data_editor(
        df_view,
        column_config={
            "Status": st.column_config.SelectboxColumn(options=["Aberta", "Em andamento", "Aguardando", "Concluída"]),
            "Líder Responsável": st.column_config.SelectboxColumn(options=["Danilo Italiano", "Luis Fernandes", "Marcia Jordana", "Reginaldo Lopes", "Vinicius Araújo"])
        },
        use_container_width=True,
        hide_index=True,
        key="editor_gerencia_final"
    )







