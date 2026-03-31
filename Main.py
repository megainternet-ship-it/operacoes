import streamlit as st 
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Operacional Backbone", layout="wide")

# ================================
# CSS ORIGINAL E ESTILO
# ================================
st.markdown("""
<style>
:root {
  --primary: #00D9FF;
  --background: #0A0E27;
  --card: #0F1535;
}
header {visibility: hidden;}
[data-testid="stHeader"] {visibility: hidden;}

.stForm {
    background-color: var(--card) !important;
    border: 2px solid var(--primary) !important;
    border-radius: 0.5rem !important;
    padding: 2rem !important;
}

.glow-title {
    color: #FFFFFF !important;
    text-align: center;
    font-weight: 700;
}

[data-testid="stDataEditor"] { font-size: 10.5px !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# LÓGICA DE DADOS COM BOTÃO DE ATUALIZAÇÃO RESTRITO AO LINK
# =========================================================

# TTL de 0 para que o cache seja controlado manualmente ou expire rápido
@st.cache_data(ttl=600)
def carregar_csv(url):
    try:
        # Adicionando um parâmetro de tempo ao final da URL para evitar cache do servidor Google
        url_final = f"{url}&cache_bust={datetime.now().timestamp()}"
        return pd.read_csv(url_final, on_bad_lines='skip', low_memory=False)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

def limpar_media(df):
    termos = ['FOTO','MIDIA','MÍDIA','ANEXO','URL','LINK','IMAGEM','CIENTE','DECLARAÇÃO','ASSINATURA']
    cols_drop = [c for c in df.columns if any(t in str(c).upper() for t in termos) or df[c].astype(str).str.contains('http', na=False).any()]
    return df.drop(columns=cols_drop)

def padronizar_status(df, colunas):
    for col in colunas:
        df[col] = df[col].astype(str).str.strip().str.lower()
        df[col] = df[col].replace(['nan','null','0','0.0','preservado','preservada'], 'PRESERVADO')
        df[col] = df[col].str.upper()
    return df

def gerenciar_filtros(df, key_suffix):
    col_data = df.columns[0]
    df[col_data] = pd.to_datetime(df[col_data], dayfirst=True, errors='coerce')
    df = df.dropna(subset=[col_data])
    df['Mes_Ano_Ref'] = df[col_data].dt.strftime('%m/%Y')
    meses_disponiveis = sorted(df['Mes_Ano_Ref'].unique(), reverse=True)
    
    c1, c2 = st.columns([3,1])
    with c1:
        mes_sel = st.selectbox("Filtrar por Mês", ["Todos"] + meses_disponiveis, key=f"sel_{key_suffix}")
    with c2:
        if st.button("🧹 Limpar", key=f"btn_limpar_{key_suffix}"):
            st.rerun()
            
    if mes_sel != "Todos":
        df = df[df['Mes_Ano_Ref'] == mes_sel]
    return df.drop(columns=['Mes_Ano_Ref'])

# =========================================================
# HEADER E BOTÃO DE ATUALIZAÇÃO GLOBAL
# =========================================================
c_tit, c_upd = st.columns([4, 1])
with c_tit:
    st.markdown("<h1 style='color:#FFFFFF;'>Operacional Backbone</h1>", unsafe_allow_html=True)
with c_upd:
    st.write("") # Alinhamento
    if st.button("🔄 ATUALIZAR PLANILHA", use_container_width=True, type="primary"):
        st.cache_data.clear() # Limpa todo o cache para puxar dados novos do Sheets
        st.toast("Puxando dados atualizados do Google Sheets...", icon="📥")
        st.rerun()

# =========================================================
# BASES DE DADOS
# =========================================================
URL_EPI = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRhakH8eejohlExEaPwdEc3juvNyv7oK21XS8jLoPqRxFfgHJjERxG-SkE2Ugy5B95677gh7nj0Wet/pub?gid=304420373&single=true&output=csv"
URL_EQUIP = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRhakH8eejohlExEaPwdEc3juvNyv7oK21XS8jLoPqRxFfgHJjERxG-SkE2Ugy5B95677gh7nj0Wet/pub?gid=932732884&single=true&output=csv"
URL_FERRA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRRhakH8eejohlExEaPwdEc3juvNyv7oK21XS8jLoPqRxFfgHJjERxG-SkE2Ugy5B95677gh7nj0Wet/pub?gid=907191989&single=true&output=csv"

# =========================================================
# LOGIN
# =========================================================
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<h1 class="glow-title">🔒 ACESSO SISTEMA</h1>', unsafe_allow_html=True)
        with st.form("login_form"):
            senha = st.text_input("Credencial", type="password")
            if st.form_submit_button("ENTRAR"):
                if senha == "megalink2024":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else: st.error("Senha incorreta")
    st.stop()

# =========================================================
# ABAS DO SISTEMA
# =========================================================
abas = st.tabs(["🛡️ EPI", "📦 REPOSIÇÃO", "📊 INTELIGÊNCIA OPERACIONAL", "📝 GERÊNCIA DE OS"])

# --- ABA 01: EPI ---
with abas[0]:
    df_epi = carregar_csv(URL_EPI).iloc[:,1:]
    df_epi = limpar_media(df_epi)
    df_epi = gerenciar_filtros(df_epi,"epi_view")
    cols_itens_epi = [c for c in df_epi.columns[5:]]
    df_epi = padronizar_status(df_epi, cols_itens_epi)
    
    # Filtros de Dashboard
    f1, f2 = st.columns(2)
    c_sel = f1.multiselect("Colaborador", sorted(df_epi.iloc[:,1].unique()), key="f_col")
    s_sel = f2.multiselect("Supervisor", sorted(df_epi.iloc[:,3].fillna("N/I").unique()), key="f_sup")
    
    df_f = df_epi.copy()
    if c_sel: df_f = df_f[df_f.iloc[:,1].isin(c_sel)]
    if s_sel: df_f = df_f[df_f.iloc[:,3].isin(s_sel)]
    
    g1, g2 = st.columns(2)
    with g1:
        st.plotly_chart(px.bar(df_f.melt(value_vars=cols_itens_epi)['value'].value_counts().reset_index(), 
                               x='value', y='count', title="Status Geral EPI", color='value', template="plotly_dark"), use_container_width=True)
    with g2:
        df_p = df_f.melt(id_vars=[df_f.columns[3]], value_vars=cols_itens_epi, value_name='Status')
        df_p = df_p[df_p['Status']=='PRESERVADO'].groupby(df_f.columns[3]).size().reset_index(name='OK')
        st.plotly_chart(px.pie(df_p, names=df_p.columns[0], values='OK', title="Conformidade por Supervisor", hole=0.4, template="plotly_dark"), use_container_width=True)
    
    st.dataframe(df_f, use_container_width=True)

# --- ABA 02: REPOSIÇÃO (TODOS OS ITENS) ---
with abas[1]:
    st.subheader("📦 Necessidade de Reposição")
    lista_rep = []
    gatilhos = ['danificado','perdi','ruim','nao tenho','não tenho']
    
    def check_rep(url, cat, start_idx):
        df = carregar_csv(url).iloc[:,1:]
        for _, row in df.iterrows():
            for col in df.columns[start_idx:]:
                status = str(row[col]).lower()
                if any(g in status for g in gatilhos):
                    lista_rep.append({'Data': row[0], 'Colaborador': row[1], 'Categoria': cat, 'Item': col, 'Status': status.upper()})

    check_rep(URL_EPI, "EPI", 5)
    check_rep(URL_EQUIP, "EQUIPAMENTO", 6)
    check_rep(URL_FERRA, "FERRAMENTA", 6)
    
    if lista_rep:
        st.table(pd.DataFrame(lista_rep))
    else: st.info("Tudo em conformidade.")

# --- ABA 03: INTELIGÊNCIA OPERACIONAL (FOCADO EM EPI) ---
with abas[2]:
    st.subheader("📊 Inteligência Estratégica (Foco EPI)")
    # Considera apenas o que foi coletado da URL_EPI para a inteligência
    lista_epi_rep = [x for x in lista_rep if x['Categoria'] == "EPI"]
    
    if lista_epi_rep:
        df_intel = pd.DataFrame(lista_epi_rep)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Trocas de EPI Pendentes", len(df_intel))
        m2.metric("Colaboradores em Alerta", df_intel["Colaborador"].nunique())
        m3.metric("Item mais Crítico", df_intel["Item"].mode()[0])
        
        st.divider()
        st.markdown("### Ranking de Desgaste por Item de EPI")
        rank = df_intel.groupby("Item").size().reset_index(name="Qtd").sort_values("Qtd", ascending=False)
        st.plotly_chart(px.bar(rank, x="Item", y="Qtd", color="Qtd", template="plotly_dark"), use_container_width=True)
        
        st.markdown("### Previsão de Compra/Estoque (EPI)")
        previsao = rank.copy()
        previsao["Sugerido Estoque (+25%)"] = (previsao["Qtd"] * 1.25).astype(int)
        st.dataframe(previsao, use_container_width=True)
    else:
        st.success("Nenhum desvio de EPI detectado para análise.")

# --- ABA 04: GERÊNCIA DE OS ---
with abas[3]:
    if "db_os" not in st.session_state:
        st.session_state["db_os"] = pd.DataFrame(columns=["OS", "Cliente", "Líder", "Status", "Atualização"])

    col_btn, _ = st.columns([1, 4])
    if col_btn.button("➕ Nova OS", type="primary"): st.session_state["os_modal"] = True

    if st.session_state.get("os_modal", False):
        with st.form("form_os"):
            n = st.text_input("OS"); c = st.text_input("Trecho"); l = st.selectbox("Líder", ["Danilo Italiano", "Luis Fernandes", "Marcia Jordana", "Reginaldo Lopes", "Vinicius Araújo"])
            s = st.selectbox("Status", ["Aberta", "Em andamento", "Concluída"])
            if st.form_submit_button("Salvar"):
                nova = pd.DataFrame([{"OS":n, "Cliente":c, "Líder":l, "Status":s, "Atualização":datetime.now().strftime("%d/%m %H:%M")}])
                st.session_state["db_os"] = pd.concat([st.session_state["db_os"], nova], ignore_index=True)
                st.session_state["os_modal"] = False
                st.rerun()

    st.data_editor(st.session_state["db_os"], use_container_width=True, hide_index=True)






