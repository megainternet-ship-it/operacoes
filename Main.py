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
    
    col1, col2, col3 = st.columns()
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
    col_data = df.columns
    df[col_data] = pd.to_datetime(df[col_data], dayfirst=True, errors='coerce')
    df = df.dropna(subset=[col_data])
    df['Mes_Ano_Ref'] = df[col_data].dt.strftime('%m/%Y')
    meses_disponiveis = sorted(df['Mes_Ano_Ref'].unique(), reverse=True)
    c1, c2 = st.columns()
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
    "📅 ESCALA DE TRABALHO"
])


# =========================================================
# GUIA 01 — EPI
# =========================================================

with abas:
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
            id_vars=[df_f_epi.columns],
            value_vars=cols_itens_epi,
            value_name='Status'
        )
        df_perf = df_perf[df_perf['Status']=='PRESERVADO']
        df_perf = df_perf.groupby(
            df_f_epi.columns
        ).size().reset_index(name='Qtd OK')
        st.plotly_chart(
            px.pie(
                df_perf,
                names=df_perf.columns,
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

with abas:
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
            df_f_eq.columns
        ).size().reset_index(name='Total OK')
        st.plotly_chart(
            px.pie(
                df_p_eq,
                names=df_p_eq.columns,
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

with abas:
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
            df_f_fe.columns
        ).size().reset_index(name='Total OK')
        st.plotly_chart(
            px.pie(
                df_p_fe,
                names=df_p_fe.columns,
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

with abas:
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
    df_chart_fard = df_f_fard[df_f_fard.columns].value_counts().reset_index()
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

with abas:
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
            data_col = temp.columns
            for _,linha in temp.iterrows():
                data = linha[data_col]
                colab = linha.iloc
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
        f_rep_colab = fr1.multiselect("Colaborador", sorted(df_rep["Colaborador"].unique()), key="f_rep_colab_aba4")
        # --- NOVO FILTRO DE CATEGORIA ---
        f_rep_cat = fr2.multiselect("Categoria", sorted(df_rep["Categoria"].unique()), key="f_rep_cat_aba4")
        
        if f_rep_colab:
            df_rep = df_rep[df_rep["Colaborador"].isin(f_rep_colab)]
        if f_rep_cat:
            df_rep = df_rep[df_rep["Categoria"].isin(f_rep_cat)]
        
        st.table(df_rep)
    else:
        st.warning("Sem itens pendentes.")


# =========================================================
# GUIA 06 — INTELIGÊNCIA OPERACIONAL
# =========================================================

with abas:
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
# 📅 GUIA 07 — ESCALA DE TRABALHO (VERSÃO ORIGINAL v62)
# =========================================================

with abas:
    st.markdown("### 📅 Central de Edição: Escala Backbone")
    
    # 1. Obter lista de técnicos da base (Apenas nomes da coluna 1 do CSV)
    nomes_base = sorted(BASE_CONTATOS.iloc[:,1].dropna().unique().tolist()) if not BASE_CONTATOS.empty else []
    lista_colab_limpa = [n for n in nomes_base if not any(char.isdigit() for char in str(n)[:2])]

    # 2. Legenda Visual
    st.markdown("""
    <div class="legenda-box">
        <div class="legenda-grid">
            <div class="legenda-item" style="background-color:#FF0000; color:white;"><b>F:</b> FERIADO</div>
            <div class="legenda-item" style="background-color:#9966FF; color:white;"><b>AT:</b> LICENÇA/ATESTADO</div>
            <div class="legenda-item" style="background-color:#FF9900; color:black;"><b>BK:</b> EQUIPE BACKUP</div>
            <div class="legenda-item" style="background-color:#2E7D32; color:white;"><b>FO:</b> FOLGA</div>
            <div class="legenda-item" style="background-color:#FFFF00; color:black;"><b>SB:</b> SOBREAVISO</div>
            <div class="legenda-item" style="background-color:#1976D2; color:white;"><b>T:</b> H COMERCIAL</div>
            <div class="legenda-item" style="background-color:#F06292; color:black;"><b>V:</b> VIAJAR EM DEMANDA</div>
            <div class="legenda-item" style="background-color:#00E5FF; color:black;"><b>FE:</b> FÉRIAS</div>
            <div class="legenda-item" style="background-color:#795548; color:white;"><b>DF:</b> DAY OFF</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Inicializar dados da sessão (Persistência de 26 linhas)
    if "df_escala_editavel" not in st.session_state:
        data_inicial = [
            {"Regiao": "SOBREAVISO", "Tecnico": "INTERNO", "Auxiliar": "-", "Seg": "LUIS", "Ter": "VINICIUS", "Qua": "MARCIA", "Qui": "DANILO", "Sex": "REGINALDO", "Sab": "DANILO", "Dom": "LUIS"},
            {"Regiao": "FLORIANO", "Tecnico": "-", "Auxiliar": "-", "Seg": "T", "Ter": "SB", "Qua": "T", "Qui": "SB", "Sex": "FO", "Sab": "T", "Dom": "SB"},
            {"Regiao": "TERESINA", "Tecnico": "-", "Auxiliar": "-", "Seg": "T", "Ter": "T", "Qua": "SB", "Qui": "T", "Sex": "FO", "Sab": "FO", "Dom": "-"},
        ]
        while len(data_inicial) < 26:
            data_inicial.append({"Regiao": "-", "Tecnico": "-", "Auxiliar": "-", "Seg": "-", "Ter": "-", "Qua": "-", "Qui": "-", "Sex": "-", "Sab": "-", "Dom": "-"})
        st.session_state["df_escala_editavel"] = pd.DataFrame(data_inicial)

    # 4. CONFIGURAÇÃO DE COLUNAS
    config_colunas = {
        "Regiao": st.column_config.SelectboxColumn("Região", options=["FLORIANO", "TERESINA", "AMARANTE", "PICOS", "PARNAÍBA", "PARAIBANO", "PERITORÓ", "SÃO LUÍS", "MATÕES-MA", "SOBREAVISO", "-"]),
        "Tecnico": st.column_config.SelectboxColumn("Técnico", options=["-"] + lista_colab_limpa),
        "Auxiliar": st.column_config.SelectboxColumn("Auxiliar", options=["-"] + lista_colab_limpa),
        "Seg": st.column_config.TextColumn("Seg"),
        "Ter": st.column_config.TextColumn("Ter"),
        "Qua": st.column_config.TextColumn("Qua"),
        "Qui": st.column_config.TextColumn("Qui"),
        "Sex": st.column_config.TextColumn("Sex"),
        "Sab": st.column_config.TextColumn("Sáb"),
        "Dom": st.column_config.TextColumn("Dom"),
    }

    # 5. Editor de Dados Principal
    df_atualizado = st.data_editor(
        st.session_state["df_escala_editavel"],
        column_config=config_colunas,
        num_rows="dynamic",
        use_container_width=True,
        height=700,
        key="editor_escala_final"
    )
    st.session_state["df_escala_editavel"] = df_atualizado

    # 6. Lógica do Informativo Automático
    st.markdown("---")
    st.markdown("### 📝 Informativo de Sobreaviso Automático")

    hoje = datetime.now()
    dias_semana_map = {0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira", 3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"}
    cols_semana_map = {0: "Seg", 1: "Ter", 2: "Qua", 3: "Qui", 4: "Sex", 5: "Sab", 6: "Dom"}
    
    dia_txt = dias_semana_map[hoje.weekday()]
    col_dia = cols_semana_map[hoje.weekday()]

    def get_tel(nome):
        if not nome or nome == "-" or nome in ["T", "SB", "FO", "F", "AT", "BK", "V", "FE", "DF"]: return ""
        try:
            match = BASE_CONTATOS[BASE_CONTATOS.iloc[:,1].str.contains(str(nome), case=False, na=False)]
            if not match.empty:
                val = str(match.iloc)
                return f"({val})" if len(val) > 5 else ""
            return ""
        except: return ""

    def extrair_equipe_dia(regiao):
        res = []
        df_tecnicos = df_atualizado.iloc[1:] # Pula a linha de supervisor
        subset = df_tecnicos[(df_tecnicos['Regiao'] == regiao) & (df_tecnicos[col_dia].str.upper() == "SB")]
        for _, r in subset.iterrows():
            if r['Tecnico'] != "-":
                res.append(f"{r['Tecnico']} {get_tel(r['Tecnico'])}".strip())
            if r['Auxiliar'] != "-":
                res.append(f"{r['Auxiliar']} {get_tel(r['Auxiliar'])}".strip())
        return " / ".join(res) if res else "-"

    supervisor_hoje = df_atualizado.iloc[col_dia]
    
    texto_informativo = f"""INFORMATIVO – Sobreaviso interno
{dia_txt}, {hoje.strftime('%d/%m/%Y')} | 08:00h - 23:59h

Responsável pelo Sobreaviso Interno:
→ {supervisor_hoje} {get_tel(supervisor_hoje)}

EQUIPE TÉCNICA EM SOBREAVISO:

TERESINA: {extrair_equipe_dia('TERESINA')}
PARNAÍBA: {extrair_equipe_dia('PARNAÍBA')}
PERITORÓ: Francisco Carneiro 99 9 9194-6616
          Francinaldo 99 9 9120-7148
SÃO LUÍS: Washington JRnet +55 98 8714-5950
PARAIBANO: {extrair_equipe_dia('PARAIBANO')}
FLORIANO: {extrair_equipe_dia('FLORIANO')}
AMARANTE: {extrair_equipe_dia('AMARANTE')}
PICOS: {extrair_equipe_dia('PICOS')}

Após horário de expediente do sobreaviso interno as tratativas de demandas serão feitas pelo suporte interno N1/TX/Suporte.
"""
    st.text_area("Copiável (Baseado na escala de hoje):", value=texto_informativo, height=450)




