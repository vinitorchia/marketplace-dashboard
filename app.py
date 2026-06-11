import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import ssl
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

DATABASE_URL = "postgresql+pg8000://postgres.bcygxizqoamfzuzyiyfh:V1ni.tfs2006%40@aws-1-sa-east-1.pooler.supabase.com:6543/postgres"
STATUS_EXCLUIDOS = ["Cancelado", "Cancelado pelo comprador", "Cancelado pelo vendedor"]

DE_PARA_FG = {"1012":"FG104338","GF":"FG104338","FG104338":"FG104338","1050":"FG104304","TOG":"FG104304","FG104304":"FG104304","1111":"FG104311","OF.CC":"FG104311","FG104311":"FG104311","1112":"FG104319","OF.CA":"FG104319","FG104319":"FG104319","1113":"FG104306","OF.CE":"FG104306","FG104306":"FG104306","1114":"FG104312","OF.PR":"FG104312","FG104312":"FG104312","1116":"FG104317","OF.CME":"FG104317","FG104317":"FG104317","1413":"FG104328","VAG.LUB":"FG104328","FG104328":"FG104328","1418":"FG104295","WSH.OB":"FG104295","FG104295":"FG104295","1419":"FG104301","WSH.PH":"FG104301","FG104301":"FG104301","1420":"FG104315","DEO,OB":"FG104315","FG104315":"FG104315","1421":"FG104336","DEO.PH":"FG104336","FG104336":"FG104336","1424":"FG104401","WSH.FP.200":"FG104401","FG104401":"FG104401","1425":"FG104412","WSH.JB.200":"FG104412","FG104412":"FG104412","1426":"FG104320","DEO.JB":"FG104320","FG104320":"FG104320","1427":"FG104323","DEO.FP":"FG104323","FG104323":"FG104323","3130":"FG104314","MB.CC":"FG104314","FG104314":"FG104314","3131":"FG104310","MB.CA":"FG104310","FG104310":"FG104310","3132":"FG104300","MB.CE":"FG104300","FG104300":"FG104300","3133":"FG104308","MB.PR":"FG104308","FG104308":"FG104308","4001":"4001","CGX.OLD":"4001","4002":"FG104298","CGX.REG":"FG104298","FG104298":"FG104298","4004":"FG104347","VAG.PACK":"FG104347","FG104347":"FG104347","4005":"4005","4006":"4006","4007":"FG104342","WSH.UP.300":"FG104342","FG104342":"FG104342","4008":"FG104369","CREAM.UP":"FG104369","FG104369":"FG104369","4009":"FG104339","CGX.MB":"FG104339","FG104339":"FG104339","1012K3":"FG104552","K3.GF":"FG104552","FG104552":"FG104552","1050K3":"FG104553","K3.TOG":"FG104553","FG104553":"FG104553","1111K3":"FG104554","K3.OF.CC":"FG104554","FG104554":"FG104554","1112K3":"FG104555","K3.OF.CA":"FG104555","FG104555":"FG104555","1113K3":"FG104556","K3.OF.CE":"FG104556","FG104556":"FG104556","1114K3":"FG104557","K3.OF.PR":"FG104557","FG104557":"FG104557","1116K3":"FG104558","K3.OF.CME":"FG104558","FG104558":"FG104558","3130K3":"FG104559","K3.MB.CC":"FG104559","FG104559":"FG104559","3131K3":"FG104560","K3.MB.CA":"FG104560","FG104560":"FG104560","3132K3":"FG104561","K3.MB.CE":"FG104561","FG104561":"FG104561","3133K3":"FG104562","K3.MB.PR":"FG104562","FG104562":"FG104562","4002K3":"FG104563","K3.CGX.REG":"FG104563","FG104563":"FG104563","4009K3":"FG104564","K3.CGX.MB":"FG104564","FG104564":"FG104564","1436":"FG104483","WSH.PH.354":"FG104483","FG104483":"FG104483","1435":"FG104476","WSH.PS.354":"FG104476","FG104476":"FG104476","1437":"FG104466","WSH.OB.354":"FG104466","FG104466":"FG104466","1434":"FG104524","WSH.CAM.354":"FG104524","FG104524":"FG104524","4003":"FG105044","CGX.2IN1":"FG105044","FG105044":"FG105044","4010":"FG105220","BBC.CE":"FG105220","FG100815":"FG100815","4011":"FG105221","BBC.PR":"FG105221","FG100816":"FG100816","1480":"FG105126","AST.VIO.50":"FG105126","FG105126":"FG105126","1481":"FG105127","AST.VIO.100":"FG105127","FG105127":"FG105127","1483":"FG105128","AST.LIQ.74":"FG105128","FG105128":"FG105128","4012":"FG105309","CGX.ECOMM":"FG105309","FG105309":"FG105309","FG104827":"FG104827","DEO.CAM":"FG104827","FG104828":"FG104828","DEO.PS":"FG104828","FG104826":"FG104826","DEO.OB":"FG104826","FG105220":"FG105220","FG105221":"FG105221"}
DE_PARA_NOME = {"FG104338":"GRECIN 2000 HOMEM LOCAO","FG104304":"GRECIN TONS DE GRISALHO","FG104311":"GRECIN 5 CAST. CLARO","FG104319":"GRECIN 5 CAST.","FG104306":"GRECIN 5 CAST. ESCURO","FG104312":"GRECIN 5 PRETO","FG104317":"GRECIN 5 CASTANHO MEDIO ESCURO","FG104328":"VAGISIL GEL LUBRIFICANTE 100GR","FG104295":"SAB INT VAGISIL GEL OB 200G+100G GRATIS","FG104301":"SAB INT VAGISIL GEL PP 200G+100G GRATIS","FG104315":"VAGISIL DESOD. INTIMO 60 ML","FG104336":"VAGISIL DESODORANTE PH 75 ML","FG104401":"SAB INT VAGISIL 200ML JB","FG104412":"SAB INT VAGISIL 200ML FP","FG104320":"VAGISIL DESODORANTE JB","FG104323":"VAGISIL DESODORANTE FP","FG104314":"GRECIN 5 PG CAST. CLARO","FG104310":"GRECIN 5 PG CAST.","FG104300":"GRECIN 5 PG CAST. ESCURO","FG104308":"GRECIN 5 PG PRETO","4001":"GRECIN CONTROL GX SH RED GRIS","FG104298":"GRECIN CONTROL GX SH RED GRIS","FG104347":"PACK VAGISIL PH + DEO PH","4005":"PACK ESSENCIAS DELICADAS JASMIM BRANCO","4006":"PACK ESSENCIAS DELICADAS FLOR DE PESSEGUEIRO","FG104342":"SAB INT VAGISIL GEL UP 200G+100G GRATIS","FG104369":"VAGISIL CREME URIN PROTECT","FG104339":"GRECIN CONTROL GX BARBA E BIGODE","FG104552":"GRECIN 2000 HOMEM LOCAO 3X","FG104553":"GRECIN TONS DE GRISALHO 3X","FG104554":"GRECIN 5 CAST. CLARO 3X","FG104555":"GRECIN 5 CAST. 3X","FG104556":"GRECIN 5 CAST. ESCURO 3X","FG104557":"GRECIN 5 PRETO 3X","FG104558":"GRECIN 5 CASTANHO MEDIO ESCURO 3X","FG104559":"GRECIN 5 PG CAST. CLARO 3X","FG104560":"GRECIN 5 PG CAST. 3X","FG104561":"GRECIN 5 PG CAST. ESCURO 3X","FG104562":"GRECIN 5 PG PRETO 3X","FG104563":"GRECIN CONTROL GX SH RED GRIS 3X","FG104564":"GRECIN CONTROL GX BARBA E BIGODE 3X","FG104483":"VAGISIL CUIDADO PH 354ML","FG104476":"VAGISIL PELE SENSIVEL 354ML","FG104466":"VAGISIL ODOR BLOCK 354ML","FG104524":"VAGISIL CAMOMILA 354ML","FG105044":"GRECIN CONTROL GX 2 EM 1 118ML","FG100815":"GRECIN RETOCADOR BARBA CAST. ESCURO","FG100816":"GRECIN RETOCADOR BARBA PRETO","FG105126":"ASTROGLIDE GEL 50ML","FG105127":"ASTROGLIDE GEL 100ML","FG105128":"ASTROGLIDE LIQUIDO 74ML","FG105309":"GRECIN CONTROL GX SHAMPOO 177ML","FG104827":"VAGISIL DESOD. CHAMOMILA 75ML","FG104828":"VAGISIL DESOD. PELE SENSIVEL 75ML","FG104826":"VAGISIL DESOD. ODOR BLOCK 75ML","FG105220":"GRECIN RETOCADOR BARBA CAST. ESCURO","FG105221":"GRECIN RETOCADOR BARBA PRETO"}

def mapear_sku(sku):
    return DE_PARA_FG.get(str(sku).strip(), str(sku).strip())

def nome_fg(fg):
    return DE_PARA_NOME.get(str(fg).strip(), str(fg))

def delta_pct(atual, anterior):
    if anterior == 0:
        return None
    return ((atual - anterior) / anterior) * 100

def fmt_delta(pct):
    if pct is None:
        return "N/D"
    sinal = "▲" if pct >= 0 else "▼"
    return f"{sinal} {abs(pct):.1f}%"

def mes_completo_ini(ref):
    return ref.replace(day=1)

def mes_completo_fim(ref):
    return (ref.replace(day=1) + relativedelta(months=1)) - timedelta(days=1)

def fat_periodo(df, ini, fim, vc):
    mask = (df["data"].dt.date >= ini) & (df["data"].dt.date <= fim)
    return df[mask][vc].sum()

st.set_page_config(page_title="Vendas por Marketplace", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0D0F14; color: #E2E8F0; }
.stApp { background: linear-gradient(135deg, #0D0F14 0%, #111827 100%); }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: #F8FAFC !important; }
[data-testid="metric-container"] { background: linear-gradient(145deg, #1A1F2E, #161B27); border: 1px solid #2D3748; border-radius: 12px; padding: 20px 24px; box-shadow: 0 4px 24px rgba(0,0,0,0.4); }
[data-testid="metric-container"] p { color: #CBD5E1 !important; font-size: 12px !important; font-weight: 600 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] > div { color: #FFFFFF !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 28px !important; font-weight: 800 !important; }
[data-testid="stDateInput"] input { background-color: #1A1F2E !important; border: 1px solid #2D3748 !important; color: #E2E8F0 !important; border-radius: 8px !important; }
[data-testid="stDateInput"] > div > div { background-color: #1A1F2E !important; border: 1px solid #2D3748 !important; border-radius: 8px !important; color: #E2E8F0 !important; }
[data-testid="stSelectbox"] > div > div { background-color: #1A1F2E !important; border: 1px solid #2D3748 !important; color: #E2E8F0 !important; border-radius: 8px !important; }
[data-testid="stTabs"] [data-baseweb="tab"] { background: transparent; color: #94A3B8; font-weight: 500; }
[data-testid="stTabs"] [aria-selected="true"] { color: #7C3AED !important; border-bottom: 2px solid #7C3AED !important; }
[data-testid="stDataFrame"] { border: 1px solid #2D3748; border-radius: 12px; overflow: hidden; }
hr { border-color: #1E2535 !important; }
.section-title { font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 600; color: #94A3B8; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px; }
.kpi-section-label { font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; padding: 6px 14px; border-radius: 6px; display: inline-block; margin-bottom: 12px; }
.kpi-main  { background: rgba(124,58,237,0.15); color: #A78BFA; border: 1px solid rgba(124,58,237,0.3); }
.kpi-mom   { background: rgba(59,130,246,0.15); color: #60A5FA; border: 1px solid rgba(59,130,246,0.3); }
.kpi-ytd   { background: rgba(16,185,129,0.15); color: #34D399; border: 1px solid rgba(16,185,129,0.3); }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)
def carregar_dados():
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        engine = create_engine(DATABASE_URL, connect_args={"ssl_context": ssl_context})
        df = pd.read_sql("SELECT * FROM vendas ORDER BY data DESC", engine)
        return df
    except Exception as e:
        st.error(f"Erro ao conectar no banco: {e}")
        return pd.DataFrame()

st.markdown("""
<div style='padding: 8px 0 24px 0;'>
    <div style='font-family: Space Grotesk, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 0.15em; color: #7C3AED; text-transform: uppercase; margin-bottom: 8px;'>Painel de Inteligência Comercial</div>
    <h1 style='font-size: 32px; font-weight: 700; margin: 0; color: #F8FAFC;'>Comparativo de Vendas por Marketplace</h1>
</div>
""", unsafe_allow_html=True)

df_bruto = carregar_dados()
if df_bruto.empty:
    st.warning("Nenhum dado encontrado.")
    st.stop()

df_bruto["data"] = pd.to_datetime(df_bruto["data"])
df_bruto["fg"] = df_bruto["sku"].apply(mapear_sku)
df_bruto["nome_produto"] = df_bruto["fg"].apply(nome_fg)

df_valido = df_bruto[~df_bruto["status"].isin(STATUS_EXCLUIDOS)] if "status" in df_bruto.columns else df_bruto.copy()
df_cancelado = df_bruto[df_bruto["status"].isin(STATUS_EXCLUIDOS)] if "status" in df_bruto.columns else pd.DataFrame()

valor_col = "valor_total" if "valor_total" in df_valido.columns else "valor"
hoje = df_valido["data"].max().date()

# ── Períodos para MoM e YTD (sempre meses fechados) ───────
# Último mês completo
if hoje == mes_completo_fim(hoje):
    ult_mes_ini = mes_completo_ini(hoje)
    ult_mes_fim = mes_completo_fim(hoje)
else:
    ult_mes_ini = mes_completo_ini(hoje - relativedelta(months=1))
    ult_mes_fim = mes_completo_fim(hoje - relativedelta(months=1))

# Mês anterior ao último mês completo
mes_ant_ini = mes_completo_ini(ult_mes_ini - relativedelta(months=1))
mes_ant_fim = mes_completo_fim(ult_mes_ini - relativedelta(months=1))

# Mesmo mês do ano passado
mes_ly_ini = mes_completo_ini(ult_mes_ini - relativedelta(years=1))
mes_ly_fim = mes_completo_fim(ult_mes_ini - relativedelta(years=1))

# YTD: janeiro até último mês fechado
ytd_ini = date(hoje.year, 1, 1)
ytd_fim = ult_mes_fim
ytd_ly_ini = date(hoje.year - 1, 1, 1)
ytd_ly_fim = date(hoje.year - 1, ult_mes_ini.month, mes_completo_fim(mes_ly_ini).day)

fat_ult_mes = fat_periodo(df_valido, ult_mes_ini, ult_mes_fim, valor_col)
fat_mes_ant = fat_periodo(df_valido, mes_ant_ini, mes_ant_fim, valor_col)
fat_mes_ly  = fat_periodo(df_valido, mes_ly_ini, mes_ly_fim, valor_col)
fat_ytd     = fat_periodo(df_valido, ytd_ini, ytd_fim, valor_col)
fat_ytd_ly  = fat_periodo(df_valido, ytd_ly_ini, ytd_ly_fim, valor_col)

st.markdown("<div style='height:4px; background: linear-gradient(90deg,#7C3AED,#3B82F6,#10B981); border-radius:4px; margin-bottom:24px;'></div>", unsafe_allow_html=True)

# ── Filtros com atalhos de período ────────────────────────
col_f1, col_f2, col_f3, col_f4 = st.columns([2, 1, 1, 1])

with col_f1:
    atalho = st.selectbox("Período rápido", ["Personalizado", "Última semana", "Último mês", "Últimos 6 meses", "Último ano"])

with col_f2:
    marketplace_sel = st.selectbox("Marketplace", ["Todos"] + sorted(df_valido["marketplace"].unique().tolist()))

with col_f3:
    fgs_disponiveis = ["Todos"] + sorted([f"{fg} — {nome_fg(fg)}" for fg in df_valido["fg"].unique() if fg in DE_PARA_NOME])
    fg_sel = st.selectbox("Produto (FG)", fgs_disponiveis)

# Calcular período pelo atalho
data_max = df_valido["data"].max().date()
data_min_base = df_valido["data"].min().date()

if atalho == "Última semana":
    periodo = (data_max - timedelta(days=7), data_max)
elif atalho == "Último mês":
    periodo = (data_max - relativedelta(months=1), data_max)
elif atalho == "Últimos 6 meses":
    periodo = (data_max - relativedelta(months=6), data_max)
elif atalho == "Último ano":
    periodo = (data_max - relativedelta(years=1), data_max)
else:
    with col_f4:
        periodo = st.date_input("Datas", value=(data_min_base, data_max), min_value=data_min_base, max_value=data_max)

if atalho != "Personalizado":
    with col_f4:
        st.markdown(f"<div style='padding-top:28px; color:#94A3B8; font-size:12px;'>{periodo[0].strftime('%d/%m/%Y')} → {periodo[1].strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

# Aplicar filtros nos gráficos
df = df_valido.copy()
if len(periodo) == 2:
    df = df[(df["data"].dt.date >= periodo[0]) & (df["data"].dt.date <= periodo[1])]
if marketplace_sel != "Todos":
    df = df[df["marketplace"] == marketplace_sel]
if fg_sel != "Todos":
    df = df[df["fg"] == fg_sel.split(" — ")[0]]

df_canc = df_cancelado.copy()
if not df_canc.empty and len(periodo) == 2:
    df_canc = df_canc[(df_canc["data"].dt.date >= periodo[0]) & (df_canc["data"].dt.date <= periodo[1])]

total_liquido = df[valor_col].sum()
total_cancelado = df_canc[valor_col].sum() if not df_canc.empty else 0
ticket = total_liquido / len(df) if len(df) > 0 else 0

# ── KPIs Visão Geral ──────────────────────────────────────
def kpi_card(label, value, delta=None, delta_positive=None, border_color="#7C3AED"):
    delta_html = ""
    if delta is not None:
        cor = "#10B981" if delta_positive else "#EF4444"
        delta_html = f"<div style='font-size:13px; font-weight:600; color:{cor}; margin-top:6px;'>{delta}</div>"
    return f"""
    <div style='background: linear-gradient(145deg,#1A1F2E,#161B27); border:1px solid #2D3748;
                border-top: 3px solid {border_color}; border-radius:12px; padding:20px 24px;
                box-shadow:0 4px 24px rgba(0,0,0,0.4);'>
        <div style='font-family:Space Grotesk,sans-serif; font-size:11px; font-weight:700;
                    letter-spacing:0.1em; text-transform:uppercase; color:#94A3B8; margin-bottom:10px;'>{label}</div>
        <div style='font-family:Space Grotesk,sans-serif; font-size:28px; font-weight:800; color:#FFFFFF;'>{value}</div>
        {delta_html}
    </div>"""

# ── KPIs Visão Geral ──────────────────────────────────────
st.markdown("<div style='height:1px; background:#1E2535; margin: 20px 0 16px;'></div>", unsafe_allow_html=True)
st.markdown("<span class='kpi-section-label kpi-main'>Visão Geral do Período Selecionado</span>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(kpi_card("Faturamento Líquido", f"R$ {total_liquido:,.0f}", border_color="#7C3AED"), unsafe_allow_html=True)
with c2:
    st.markdown(kpi_card("Pedidos Válidos", f"{len(df):,}", border_color="#7C3AED"), unsafe_allow_html=True)
with c3:
    st.markdown(kpi_card("Ticket Médio", f"R$ {ticket:,.2f}", border_color="#7C3AED"), unsafe_allow_html=True)

# ── KPIs MoM ─────────────────────────────────────────────
st.markdown("<div style='height:1px; background:#1E2535; margin: 24px 0 16px;'></div>", unsafe_allow_html=True)
st.markdown("<span class='kpi-section-label kpi-mom'>MoM — Meses Fechados</span>", unsafe_allow_html=True)
st.markdown(f"<div style='color:#64748B; font-size:12px; margin-bottom:12px;'>Comparando {ult_mes_ini.strftime('%B/%Y')} com {mes_ant_ini.strftime('%B/%Y')} e {mes_ly_ini.strftime('%B/%Y')}</div>", unsafe_allow_html=True)

pct_ant = delta_pct(fat_ult_mes, fat_mes_ant)
pct_ly  = delta_pct(fat_ult_mes, fat_mes_ly)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(kpi_card(f"{ult_mes_ini.strftime('%B/%Y')} — Último Mês Fechado", f"R$ {fat_ult_mes:,.0f}", border_color="#3B82F6"), unsafe_allow_html=True)
with m2:
    st.markdown(kpi_card(f"vs {mes_ant_ini.strftime('%B/%Y')} (Mês Anterior)", f"R$ {fat_mes_ant:,.0f}", delta=fmt_delta(pct_ant), delta_positive=(pct_ant or 0) >= 0, border_color="#3B82F6"), unsafe_allow_html=True)
with m3:
    st.markdown(kpi_card(f"vs {mes_ly_ini.strftime('%B/%Y')} (Mesmo Mês LY)", f"R$ {fat_mes_ly:,.0f}", delta=fmt_delta(pct_ly), delta_positive=(pct_ly or 0) >= 0, border_color="#3B82F6"), unsafe_allow_html=True)

# ── KPIs YTD ─────────────────────────────────────────────
st.markdown("<div style='height:1px; background:#1E2535; margin: 24px 0 16px;'></div>", unsafe_allow_html=True)
st.markdown("<span class='kpi-section-label kpi-ytd'>YTD — Acumulado do Ano</span>", unsafe_allow_html=True)
st.markdown(f"<div style='color:#64748B; font-size:12px; margin-bottom:12px;'>Jan/{hoje.year} até {ult_mes_fim.strftime('%B/%Y')} vs mesmo período {hoje.year - 1}</div>", unsafe_allow_html=True)

pct_ytd = delta_pct(fat_ytd, fat_ytd_ly)

y1, y2, y3 = st.columns(3)
with y1:
    st.markdown(kpi_card(f"YTD {hoje.year}", f"R$ {fat_ytd:,.0f}", border_color="#10B981"), unsafe_allow_html=True)
with y2:
    st.markdown(kpi_card(f"YTD {hoje.year - 1}", f"R$ {fat_ytd_ly:,.0f}", border_color="#10B981"), unsafe_allow_html=True)
with y3:
    st.markdown(kpi_card(f"Crescimento YTD {hoje.year} vs {hoje.year-1}", fmt_delta(pct_ytd), delta=f"R$ {fat_ytd - fat_ytd_ly:+,.0f}", delta_positive=(pct_ytd or 0) >= 0, border_color="#10B981"), unsafe_allow_html=True)

# ── Gráficos ──────────────────────────────────────────────
CORES = ["#F59E0B","#10B981","#3B82F6","#7C3AED","#EF4444","#EC4899","#06B6D4"]
LAYOUT_BASE = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#94A3B8", family="Inter"), xaxis=dict(gridcolor="#1E2535", linecolor="#2D3748"), yaxis=dict(gridcolor="#1E2535", linecolor="#2D3748"), margin=dict(l=10, r=10, t=40, b=10))

st.markdown("<div style='height:1px; background:#1E2535; margin: 24px 0;'></div>", unsafe_allow_html=True)

col_a, col_b = st.columns([3, 2])
with col_a:
    st.markdown("<div class='section-title'>Faturamento Líquido por Marketplace</div>", unsafe_allow_html=True)
    por_mp = df.groupby("marketplace")[valor_col].sum().reset_index()
    por_mp.columns = ["Marketplace", "Faturamento"]
    por_mp = por_mp.sort_values("Faturamento", ascending=True)
    fig1 = go.Figure(go.Bar(x=por_mp["Faturamento"], y=por_mp["Marketplace"], orientation="h", marker=dict(color=CORES[:len(por_mp)], opacity=0.9), text=[f"R$ {v:,.0f}" for v in por_mp["Faturamento"]], textposition="outside", textfont=dict(color="#CBD5E1", size=11)))
    fig1.update_layout(**LAYOUT_BASE, height=320)
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.markdown("<div class='section-title'>Participação %</div>", unsafe_allow_html=True)
    fig2 = go.Figure(go.Pie(labels=por_mp["Marketplace"], values=por_mp["Faturamento"], hole=0.55, marker=dict(colors=CORES[:len(por_mp)]), textinfo="percent", textfont=dict(color="#E2E8F0", size=12)))
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#94A3B8"), legend=dict(font=dict(color="#CBD5E1")), margin=dict(l=0, r=0, t=40, b=0), height=320)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<div class='section-title'>Evolução Diária por Marketplace</div>", unsafe_allow_html=True)
evolucao = df.groupby(["data","marketplace"])[valor_col].sum().reset_index()
evolucao.columns = ["Data","Marketplace","Faturamento"]
fig3 = px.line(evolucao, x="Data", y="Faturamento", color="Marketplace", markers=False, color_discrete_sequence=CORES)
fig3.update_traces(line=dict(width=2))
fig3.update_layout(**LAYOUT_BASE, height=360, legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1")))
st.plotly_chart(fig3, use_container_width=True)

st.markdown("<div style='height:1px; background:#1E2535; margin: 24px 0;'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Top 10 Produtos (FG Consolidado)</div>", unsafe_allow_html=True)
metrica_sel = st.radio("Visualizar por:", ["Faturamento (R$)", "Quantidade vendida"], horizontal=True)

if metrica_sel == "Faturamento (R$)":
    top = df.groupby(["fg","nome_produto"])[valor_col].sum().reset_index()
    top.columns = ["FG","Produto","Valor"]
    top = top.sort_values("Valor", ascending=False).head(10).sort_values("Valor", ascending=True)
    top["Label"] = top["FG"] + " — " + top["Produto"].str[:35]
    fig_top = go.Figure(go.Bar(x=top["Valor"], y=top["Label"], orientation="h", marker=dict(color="#7C3AED", opacity=0.85), text=[f"R$ {v:,.0f}" for v in top["Valor"]], textposition="outside", textfont=dict(color="#CBD5E1", size=10)))
else:
    top = df.groupby(["fg","nome_produto"])["quantidade"].sum().reset_index()
    top.columns = ["FG","Produto","Valor"]
    top = top.sort_values("Valor", ascending=False).head(10).sort_values("Valor", ascending=True)
    top["Label"] = top["FG"] + " — " + top["Produto"].str[:35]
    fig_top = go.Figure(go.Bar(x=top["Valor"], y=top["Label"], orientation="h", marker=dict(color="#10B981", opacity=0.85), text=[f"{v:,.0f}" for v in top["Valor"]], textposition="outside", textfont=dict(color="#CBD5E1", size=10)))

fig_top.update_layout(**{k:v for k,v in LAYOUT_BASE.items() if k!='yaxis'}, height=460, yaxis={"categoryorder":"array","categoryarray":top["Label"].tolist(),"gridcolor":"#1E2535","tickfont":{"size":10,"color":"#CBD5E1"}})
st.plotly_chart(fig_top, use_container_width=True)

st.markdown("<div style='height:1px; background:#1E2535; margin: 24px 0;'></div>", unsafe_allow_html=True)
aba1, aba2 = st.tabs(["Pedidos Válidos", "Cancelados"])
colunas_exibir = ["data","fg","nome_produto","marketplace","valor","quantidade"]
if "status" in df.columns: colunas_exibir.append("status")
if "valor_total" in df.columns: colunas_exibir.append("valor_total")

with aba1:
    st.dataframe(df[colunas_exibir].sort_values("data", ascending=False), use_container_width=True, height=380)
with aba2:
    if not df_canc.empty:
        st.dataframe(df_canc[colunas_exibir].sort_values("data", ascending=False), use_container_width=True, height=380)
    else:
        st.info("Nenhum cancelamento no período.")

st.markdown(f"<div style='text-align:center; color:#4B5563; font-size:11px; padding: 24px 0 8px;'>Atualizado a cada 5 min · {len(df):,} pedidos válidos · Última data: {hoje}</div>", unsafe_allow_html=True)