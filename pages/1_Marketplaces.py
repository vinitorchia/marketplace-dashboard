import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import ssl
import os
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from shared import init_idioma, t, aplicar_estilo, cabecalho

DATABASE_URL = "postgresql+pg8000://postgres.bcygxizqoamfzuzyiyfh:V1ni.tfs2006%40@aws-1-sa-east-1.pooler.supabase.com:6543/postgres"
STATUS_EXCLUIDOS = ["Cancelado", "Cancelado pelo comprador", "Cancelado pelo vendedor"]

DE_PARA_FG = {"1012":"FG104338","GF":"FG104338","FG104338":"FG104338","1050":"FG104304","TOG":"FG104304","FG104304":"FG104304","1111":"FG104311","OF.CC":"FG104311","FG104311":"FG104311","1112":"FG104319","OF.CA":"FG104319","FG104319":"FG104319","1113":"FG104306","OF.CE":"FG104306","FG104306":"FG104306","1114":"FG104312","OF.PR":"FG104312","FG104312":"FG104312","1116":"FG104317","OF.CME":"FG104317","FG104317":"FG104317","1413":"FG104328","VAG.LUB":"FG104328","FG104328":"FG104328","1418":"FG104295","WSH.OB":"FG104295","FG104295":"FG104295","1419":"FG104301","WSH.PH":"FG104301","FG104301":"FG104301","1420":"FG104315","DEO,OB":"FG104315","FG104315":"FG104315","1421":"FG104336","DEO.PH":"FG104336","FG104336":"FG104336","1424":"FG104401","WSH.FP.200":"FG104401","FG104401":"FG104401","1425":"FG104412","WSH.JB.200":"FG104412","FG104412":"FG104412","1426":"FG104320","DEO.JB":"FG104320","FG104320":"FG104320","1427":"FG104323","DEO.FP":"FG104323","FG104323":"FG104323","3130":"FG104314","MB.CC":"FG104314","FG104314":"FG104314","3131":"FG104310","MB.CA":"FG104310","FG104310":"FG104310","3132":"FG104300","MB.CE":"FG104300","FG104300":"FG104300","3133":"FG104308","MB.PR":"FG104308","FG104308":"FG104308","4001":"4001","CGX.OLD":"4001","4002":"FG104298","CGX.REG":"FG104298","FG104298":"FG104298","4004":"FG104347","VAG.PACK":"FG104347","FG104347":"FG104347","4005":"4005","4006":"4006","4007":"FG104342","WSH.UP.300":"FG104342","FG104342":"FG104342","4008":"FG104369","CREAM.UP":"FG104369","FG104369":"FG104369","4009":"FG104339","CGX.MB":"FG104339","FG104339":"FG104339","1012K3":"FG104552","K3.GF":"FG104552","FG104552":"FG104552","1050K3":"FG104553","K3.TOG":"FG104553","FG104553":"FG104553","1111K3":"FG104554","K3.OF.CC":"FG104554","FG104554":"FG104554","1112K3":"FG104555","K3.OF.CA":"FG104555","FG104555":"FG104555","1113K3":"FG104556","K3.OF.CE":"FG104556","FG104556":"FG104556","1114K3":"FG104557","K3.OF.PR":"FG104557","FG104557":"FG104557","1116K3":"FG104558","K3.OF.CME":"FG104558","FG104558":"FG104558","3130K3":"FG104559","K3.MB.CC":"FG104559","FG104559":"FG104559","3131K3":"FG104560","K3.MB.CA":"FG104560","FG104560":"FG104560","3132K3":"FG104561","K3.MB.CE":"FG104561","FG104561":"FG104561","3133K3":"FG104562","K3.MB.PR":"FG104562","FG104562":"FG104562","4002K3":"FG104563","K3.CGX.REG":"FG104563","FG104563":"FG104563","4009K3":"FG104564","K3.CGX.MB":"FG104564","FG104564":"FG104564","1436":"FG104483","WSH.PH.354":"FG104483","FG104483":"FG104483","1435":"FG104476","WSH.PS.354":"FG104476","FG104476":"FG104476","1437":"FG104466","WSH.OB.354":"FG104466","FG104466":"FG104466","1434":"FG104524","WSH.CAM.354":"FG104524","FG104524":"FG104524","4003":"FG105044","CGX.2IN1":"FG105044","FG105044":"FG105044","4010":"FG105220","BBC.CE":"FG105220","FG100815":"FG100815","4011":"FG105221","BBC.PR":"FG105221","FG100816":"FG100816","1480":"FG105126","AST.VIO.50":"FG105126","FG105126":"FG105126","1481":"FG105127","AST.VIO.100":"FG105127","FG105127":"FG105127","1483":"FG105128","AST.LIQ.74":"FG105128","FG105128":"FG105128","4012":"FG105309","CGX.ECOMM":"FG105309","FG105309":"FG105309","FG104827":"FG104827","DEO.CAM":"FG104827","FG104828":"FG104828","DEO.PS":"FG104828","FG104826":"FG104826","DEO.OB":"FG104826","FG105220":"FG105220","FG105221":"FG105221"}
DE_PARA_NOME = {"FG104338":"GRECIN 2000 HOMEM LOCAO","FG104304":"GRECIN TONS DE GRISALHO","FG104311":"GRECIN 5 CAST. CLARO","FG104319":"GRECIN 5 CAST.","FG104306":"GRECIN 5 CAST. ESCURO","FG104312":"GRECIN 5 PRETO","FG104317":"GRECIN 5 CASTANHO MEDIO ESCURO","FG104328":"VAGISIL GEL LUBRIFICANTE 100GR","FG104295":"SAB INT VAGISIL GEL OB 200G+100G GRATIS","FG104301":"SAB INT VAGISIL GEL PP 200G+100G GRATIS","FG104315":"VAGISIL DESOD. INTIMO 60 ML","FG104336":"VAGISIL DESODORANTE PH 75 ML","FG104401":"SAB INT VAGISIL 200ML JB","FG104412":"SAB INT VAGISIL 200ML FP","FG104320":"VAGISIL DESODORANTE JB","FG104323":"VAGISIL DESODORANTE FP","FG104314":"GRECIN 5 PG CAST. CLARO","FG104310":"GRECIN 5 PG CAST.","FG104300":"GRECIN 5 PG CAST. ESCURO","FG104308":"GRECIN 5 PG PRETO","4001":"GRECIN CONTROL GX SH RED GRIS","FG104298":"GRECIN CONTROL GX SH RED GRIS","FG104347":"PACK VAGISIL PH + DEO PH","4005":"PACK ESSENCIAS DELICADAS JASMIM BRANCO","4006":"PACK ESSENCIAS DELICADAS FLOR DE PESSEGUEIRO","FG104342":"SAB INT VAGISIL GEL UP 200G+100G GRATIS","FG104369":"VAGISIL CREME URIN PROTECT","FG104339":"GRECIN CONTROL GX BARBA E BIGODE","FG104552":"GRECIN 2000 HOMEM LOCAO 3X","FG104553":"GRECIN TONS DE GRISALHO 3X","FG104554":"GRECIN 5 CAST. CLARO 3X","FG104555":"GRECIN 5 CAST. 3X","FG104556":"GRECIN 5 CAST. ESCURO 3X","FG104557":"GRECIN 5 PRETO 3X","FG104558":"GRECIN 5 CASTANHO MEDIO ESCURO 3X","FG104559":"GRECIN 5 PG CAST. CLARO 3X","FG104560":"GRECIN 5 PG CAST. 3X","FG104561":"GRECIN 5 PG CAST. ESCURO 3X","FG104562":"GRECIN 5 PG PRETO 3X","FG104563":"GRECIN CONTROL GX SH RED GRIS 3X","FG104564":"GRECIN CONTROL GX BARBA E BIGODE 3X","FG104483":"VAGISIL CUIDADO PH 354ML","FG104476":"VAGISIL PELE SENSIVEL 354ML","FG104466":"VAGISIL ODOR BLOCK 354ML","FG104524":"VAGISIL CAMOMILA 354ML","FG105044":"GRECIN CONTROL GX 2 EM 1 118ML","FG100815":"GRECIN RETOCADOR BARBA CAST. ESCURO","FG100816":"GRECIN RETOCADOR BARBA PRETO","FG105126":"ASTROGLIDE GEL 50ML","FG105127":"ASTROGLIDE GEL 100ML","FG105128":"ASTROGLIDE LIQUIDO 74ML","FG105309":"GRECIN CONTROL GX SHAMPOO 177ML","FG104827":"VAGISIL DESOD. CHAMOMILA 75ML","FG104828":"VAGISIL DESOD. PELE SENSIVEL 75ML","FG104826":"VAGISIL DESOD. ODOR BLOCK 75ML","FG105220":"GRECIN RETOCADOR BARBA CAST. ESCURO","FG105221":"GRECIN RETOCADOR BARBA PRETO"}

DE_PARA_BRAND = {"FG104338":"GRECIN", "FG104304":"GRECIN", "FG104311":"GRECIN", "FG104319":"GRECIN", "FG104306":"GRECIN", "FG104312":"GRECIN", "FG104317":"GRECIN", "FG104328":"VAGISIL", "FG104295":"VAGISIL", "FG104301":"VAGISIL", "FG104315":"VAGISIL", "FG104336":"VAGISIL", "FG104401":"VAGISIL", "FG104412":"VAGISIL", "FG104320":"VAGISIL", "FG104323":"VAGISIL", "FG104314":"GRECIN", "FG104310":"GRECIN", "FG104300":"GRECIN", "FG104308":"GRECIN", "4001":"GRECIN", "FG104298":"GRECIN", "FG104347":"VAGISIL", "4005":"VAGISIL", "4006":"VAGISIL", "FG104342":"VAGISIL", "FG104369":"VAGISIL", "FG104339":"GRECIN", "FG104552":"GRECIN", "FG104553":"GRECIN", "FG104554":"GRECIN", "FG104555":"GRECIN", "FG104556":"GRECIN", "FG104557":"GRECIN", "FG104558":"GRECIN", "FG104559":"GRECIN", "FG104560":"GRECIN", "FG104561":"GRECIN", "FG104562":"GRECIN", "FG104563":"GRECIN", "FG104564":"GRECIN", "FG104483":"VAGISIL", "FG104476":"VAGISIL", "FG104466":"VAGISIL", "FG104524":"VAGISIL", "FG105044":"GRECIN", "FG100815":"GRECIN", "FG100816":"GRECIN", "FG105126":"ASTROGLIDE", "FG105127":"ASTROGLIDE", "FG105128":"ASTROGLIDE", "FG105309":"GRECIN", "FG104827":"VAGISIL", "FG104828":"VAGISIL", "FG104826":"VAGISIL", "FG105220":"GRECIN", "FG105221":"GRECIN"}

DE_PARA_SUBBRAND = {"FG104338":"GF", "FG104304":"TOG", "FG104311":"OF", "FG104319":"OF", "FG104306":"OF", "FG104312":"OF", "FG104317":"OF", "FG104328":"LUB", "FG104295":"WASH", "FG104301":"WASH", "FG104315":"DEO", "FG104336":"DEO", "FG104401":"WASH", "FG104412":"WASH", "FG104320":"DEO", "FG104323":"DEO", "FG104314":"MB", "FG104310":"MB", "FG104300":"MB", "FG104308":"MB", "4001":"CGX", "FG104298":"CGX", "FG104347":"WASH", "4005":"DESCONTINUADO", "4006":"DESCONTINUADO", "FG104342":"WASH", "FG104369":"CREAM", "FG104339":"MBX", "FG104552":"GF", "FG104553":"TOG", "FG104554":"OF", "FG104555":"OF", "FG104556":"OF", "FG104557":"OF", "FG104558":"OF", "FG104559":"MB", "FG104560":"MB", "FG104561":"MB", "FG104562":"MB", "FG104563":"CGX", "FG104564":"MBX", "FG104483":"WASH", "FG104476":"WASH", "FG104466":"WASH", "FG104524":"WASH", "FG105044":"CGX", "FG100815":"BBC", "FG100816":"BBC", "FG105126":"ASTROGLIDE", "FG105127":"ASTROGLIDE", "FG105128":"ASTROGLIDE", "FG105309":"CGX", "FG104827":"DEO", "FG104828":"DEO", "FG104826":"DEO", "FG105220":"BBC", "FG105221":"BBC"}

def mapear_sku(sku):
    return DE_PARA_FG.get(str(sku).strip(), str(sku).strip())

def nome_fg(fg):
    return DE_PARA_NOME.get(str(fg).strip(), str(fg))

def brand_de_fg(fg):
    return DE_PARA_BRAND.get(str(fg).strip(), "Outros")

def subbrand_de_fg(fg):
    return DE_PARA_SUBBRAND.get(str(fg).strip(), "Outros")

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

init_idioma()
aplicar_estilo()

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
        st.error(f"{t('erro_conexao')}: {e}")
        return pd.DataFrame()

cabecalho()


df_bruto = carregar_dados()
if df_bruto.empty:
    st.warning(t("nenhum_dado"))
    st.stop()

df_bruto["data"] = pd.to_datetime(df_bruto["data"])
df_bruto["fg"] = df_bruto["sku"].apply(mapear_sku)
df_bruto["nome_produto"] = df_bruto["fg"].apply(nome_fg)
df_bruto["brand"] = df_bruto["fg"].apply(brand_de_fg)
df_bruto["subbrand"] = df_bruto["fg"].apply(subbrand_de_fg)

df_valido = df_bruto[~df_bruto["status"].isin(STATUS_EXCLUIDOS)] if "status" in df_bruto.columns else df_bruto.copy()
df_cancelado = df_bruto[df_bruto["status"].isin(STATUS_EXCLUIDOS)] if "status" in df_bruto.columns else pd.DataFrame()

valor_col = "valor_net" if "valor_net" in df_valido.columns else "valor_total" if "valor_total" in df_valido.columns else "valor"
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
mes_ant_ini = mes_completo_ini(hoje - relativedelta(months=1))
mes_ant_fim = mes_completo_fim(hoje - relativedelta(months=1))

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

OPCOES_ATALHO = ["personalizado", "ultima_semana", "ultimo_mes", "ultimos_6_meses", "ultimo_ano"]
CHAVE_ATALHO = {"personalizado": "personalizado", "ultima_semana": "ultima_semana", "ultimo_mes": "ultimo_mes", "ultimos_6_meses": "ultimos_6_meses", "ultimo_ano": "ultimo_ano"}

with col_f1:
    atalho_idx = st.selectbox(t("periodo_rapido"), range(len(OPCOES_ATALHO)), format_func=lambda i: t(OPCOES_ATALHO[i]))
    atalho = OPCOES_ATALHO[atalho_idx]

with col_f2:
    marketplace_sel = st.selectbox(t("marketplace"), [t("todos")] + sorted(df_valido["marketplace"].unique().tolist()))

with col_f3:
    fgs_disponiveis = [t("todos")] + sorted([f"{fg} — {nome_fg(fg)}" for fg in df_valido["fg"].unique() if fg in DE_PARA_NOME])
    fg_sel = st.selectbox(t("produto_fg"), fgs_disponiveis)

col_f5, col_f6 = st.columns([1, 1])
with col_f5:
    brand_sel = st.selectbox(t("brand"), [t("todos")] + sorted(df_valido["brand"].unique().tolist()))
with col_f6:
    if brand_sel != t("todos"):
        subbrands_disponiveis = sorted(df_valido[df_valido["brand"] == brand_sel]["subbrand"].unique().tolist())
    else:
        subbrands_disponiveis = sorted(df_valido["subbrand"].unique().tolist())
    subbrand_sel = st.selectbox(t("subbrand"), [t("todos")] + subbrands_disponiveis)

# Calcular período pelo atalho
data_max = df_valido["data"].max().date()
data_min_base = df_valido["data"].min().date()

if atalho == "ultima_semana":
    periodo = (data_max - timedelta(days=7), data_max)
elif atalho == "ultimo_mes":
    periodo = (data_max - relativedelta(months=1), data_max)
elif atalho == "ultimos_6_meses":
    periodo = (data_max - relativedelta(months=6), data_max)
elif atalho == "ultimo_ano":
    periodo = (data_max - relativedelta(years=1), data_max)
else:
    with col_f4:
        periodo = st.date_input(
            t("datas"),
            value=(data_max - relativedelta(months=6), data_max),
            min_value=data_min_base,
            max_value=date(2030, 12, 31)
        )

if atalho != "personalizado":
    with col_f4:
        st.markdown(f"<div style='padding-top:28px; color:#64748B; font-size:12px;'>{periodo[0].strftime('%d/%m/%Y')} → {periodo[1].strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

# Aplicar filtros nos gráficos
df = df_valido.copy()
if len(periodo) == 2:
    df = df[(df["data"].dt.date >= periodo[0]) & (df["data"].dt.date <= periodo[1])]
if marketplace_sel != t("todos"):
    df = df[df["marketplace"] == marketplace_sel]
if fg_sel != t("todos"):
    df = df[df["fg"] == fg_sel.split(" — ")[0]]
if brand_sel != t("todos"):
    df = df[df["brand"] == brand_sel]
if subbrand_sel != t("todos"):
    df = df[df["subbrand"] == subbrand_sel]

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
        cor = "#059669" if delta_positive else "#DC2626"
        delta_html = f"<div style='font-size:13px; font-weight:600; color:{cor}; margin-top:6px;'>{delta}</div>"
    return f"""
    <div style='background: linear-gradient(145deg,#FFFFFF,#F8FAFC); border:1px solid #E2E8F0;
                border-top: 3px solid {border_color}; border-radius:12px; padding:20px 24px;
                box-shadow:0 4px 16px rgba(15,23,42,0.06);'>
        <div style='font-family:Space Grotesk,sans-serif; font-size:11px; font-weight:700;
                    letter-spacing:0.1em; text-transform:uppercase; color:#64748B; margin-bottom:10px;'>{label}</div>
        <div style='font-family:Space Grotesk,sans-serif; font-size:28px; font-weight:800; color:#0F172A;'>{value}</div>
        {delta_html}
    </div>"""

# ── KPIs Visão Geral ──────────────────────────────────────
st.markdown("<div style='height:1px; background:#E2E8F0; margin: 40px 0 24px;'></div>", unsafe_allow_html=True)
st.markdown(f"<span class='kpi-section-label kpi-main'>{t('visao_geral')}</span>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(kpi_card(t("faturamento_liquido"), f"R$ {total_liquido:,.0f}", border_color="#7C3AED"), unsafe_allow_html=True)
with c2:
    st.markdown(kpi_card(t("pedidos_validos"), f"{len(df):,}", border_color="#7C3AED"), unsafe_allow_html=True)
with c3:
    st.markdown(kpi_card(t("ticket_medio"), f"R$ {ticket:,.2f}", border_color="#7C3AED"), unsafe_allow_html=True)

# ── KPIs MoM ─────────────────────────────────────────────
st.markdown("<div style='height:1px; background:#E2E8F0; margin: 40px 0 24px;'></div>", unsafe_allow_html=True)
st.markdown(f"<span class='kpi-section-label kpi-mom'>{t('mom_titulo')}</span>", unsafe_allow_html=True)
st.markdown(f"<div style='color:#94A3B8; font-size:12px; margin-bottom:12px;'>{t('mom_comparando', a=ult_mes_ini.strftime('%B/%Y'), b=mes_ant_ini.strftime('%B/%Y'), c=mes_ly_ini.strftime('%B/%Y'))}</div>", unsafe_allow_html=True)

pct_ant = delta_pct(fat_ult_mes, fat_mes_ant)
pct_ly  = delta_pct(fat_ult_mes, fat_mes_ly)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(kpi_card(t("ultimo_mes_fechado", m=ult_mes_ini.strftime('%B/%Y')), f"R$ {fat_ult_mes:,.0f}", border_color="#3B82F6"), unsafe_allow_html=True)
with m2:
    st.markdown(kpi_card(t("vs_mes_anterior", m=mes_ant_ini.strftime('%B/%Y')), f"R$ {fat_mes_ant:,.0f}", delta=fmt_delta(pct_ant), delta_positive=(pct_ant or 0) >= 0, border_color="#3B82F6"), unsafe_allow_html=True)
with m3:
    st.markdown(kpi_card(t("vs_mesmo_mes_ly", m=mes_ly_ini.strftime('%B/%Y')), f"R$ {fat_mes_ly:,.0f}", delta=fmt_delta(pct_ly), delta_positive=(pct_ly or 0) >= 0, border_color="#3B82F6"), unsafe_allow_html=True)

# ── KPIs YTD ─────────────────────────────────────────────
st.markdown("<div style='height:1px; background:#E2E8F0; margin: 40px 0 24px;'></div>", unsafe_allow_html=True)
st.markdown(f"<span class='kpi-section-label kpi-ytd'>{t('ytd_titulo')}</span>", unsafe_allow_html=True)
st.markdown(f"<div style='color:#94A3B8; font-size:12px; margin-bottom:12px;'>{t('ytd_periodo', ano=hoje.year, m=ult_mes_fim.strftime('%B/%Y'), ano_ly=hoje.year - 1)}</div>", unsafe_allow_html=True)

pct_ytd = delta_pct(fat_ytd, fat_ytd_ly)

y1, y2, y3 = st.columns(3)
with y1:
    st.markdown(kpi_card(t("ytd_ano", ano=hoje.year), f"R$ {fat_ytd:,.0f}", border_color="#10B981"), unsafe_allow_html=True)
with y2:
    st.markdown(kpi_card(t("ytd_ano", ano=hoje.year - 1), f"R$ {fat_ytd_ly:,.0f}", border_color="#10B981"), unsafe_allow_html=True)
with y3:
    st.markdown(kpi_card(t("crescimento_ytd", ano=hoje.year, ano_ly=hoje.year-1), fmt_delta(pct_ytd), delta=f"R$ {fat_ytd - fat_ytd_ly:+,.0f}", delta_positive=(pct_ytd or 0) >= 0, border_color="#10B981"), unsafe_allow_html=True)

# ── Gráficos ──────────────────────────────────────────────
CORES = ["#F59E0B","#10B981","#3B82F6","#7C3AED","#EF4444","#EC4899","#06B6D4"]
LAYOUT_BASE = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#64748B", family="Inter"), xaxis=dict(gridcolor="#E2E8F0", linecolor="#CBD5E1"), yaxis=dict(gridcolor="#E2E8F0", linecolor="#CBD5E1"), margin=dict(l=10, r=10, t=40, b=10))

st.markdown("<div style='height:1px; background:#E2E8F0; margin: 40px 0;'></div>", unsafe_allow_html=True)

metrica_mp = st.radio(t("visualizar_marketplace_por"), [t("faturamento_rs"), t("quantidade_vendida")], horizontal=True, key="metrica_mp")

if metrica_mp == t("faturamento_rs"):
    por_mp = df.groupby("marketplace")[valor_col].sum().reset_index()
    por_mp.columns = ["Marketplace", "Valor"]
    por_mp = por_mp.sort_values("Valor", ascending=True)
    texto_mp = [f"R$ {v:,.0f}" for v in por_mp["Valor"]]
    titulo_mp = t("faturamento_liquido_por_mp")
else:
    por_mp = df.groupby("marketplace")["quantidade"].sum().reset_index()
    por_mp.columns = ["Marketplace", "Valor"]
    por_mp = por_mp.sort_values("Valor", ascending=True)
    texto_mp = [f"{v:,.0f}" for v in por_mp["Valor"]]
    titulo_mp = t("quantidade_por_mp")

col_a, col_b = st.columns([3, 2], gap="large")
with col_a:
    st.markdown(f"<div class='section-title'>{titulo_mp}</div>", unsafe_allow_html=True)
    fig1 = go.Figure(go.Bar(x=por_mp["Valor"], y=por_mp["Marketplace"], orientation="h", marker=dict(color=CORES[:len(por_mp)], opacity=0.9), text=texto_mp, textposition="inside", insidetextanchor="end", textfont=dict(color="#FFFFFF", size=11), cliponaxis=False))
    fig1_layout = {k: v for k, v in LAYOUT_BASE.items() if k != "xaxis"}
    fig1.update_layout(**fig1_layout, height=320, xaxis=dict(gridcolor="#E2E8F0", linecolor="#CBD5E1", range=[0, por_mp["Valor"].max() * 1.08]))
    st.plotly_chart(fig1, width='stretch', config={"displayModeBar": False})

with col_b:
    st.markdown(f"<div class='section-title'>{t('participacao_pct')}</div>", unsafe_allow_html=True)
    fig2 = go.Figure(go.Pie(labels=por_mp["Marketplace"], values=por_mp["Valor"], hole=0.55, marker=dict(colors=CORES[:len(por_mp)]), textinfo="percent", textfont=dict(color="#1E293B", size=12)))
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#64748B"), legend=dict(font=dict(color="#475569")), margin=dict(l=20, r=20, t=40, b=20), height=320)
    st.plotly_chart(fig2, width='stretch', config={"displayModeBar": False})


st.markdown("<div style='height:1px; background:#E2E8F0; margin: 40px 0;'></div>", unsafe_allow_html=True)

# ── Brand e Subbrand ──────────────────────────────────────
st.markdown(f"<div class='section-title'>{t('fat_qtd_brand_subbrand')}</div>", unsafe_allow_html=True)

metrica_brand = st.radio(t("visualizar_brand_por"), [t("faturamento_rs"), t("quantidade_vendida")], horizontal=True, key="metrica_brand")

if metrica_brand == t("faturamento_rs"):
    col_metrica_brand = valor_col
    fmt_brand = lambda v: f"R$ {v:,.0f}"
else:
    col_metrica_brand = "quantidade"
    fmt_brand = lambda v: f"{v:,.0f}"

por_brand = df.groupby("brand")[col_metrica_brand].sum().reset_index()
por_brand.columns = ["Brand", "Valor"]
por_brand = por_brand.sort_values("Valor", ascending=True)

por_subbrand = df.groupby(["brand","subbrand"])[col_metrica_brand].sum().reset_index()
por_subbrand.columns = ["Brand", "Subbrand", "Valor"]
por_subbrand = por_subbrand.sort_values("Valor", ascending=False)
por_subbrand["Label"] = por_subbrand["Brand"] + " — " + por_subbrand["Subbrand"]
por_subbrand = por_subbrand.sort_values("Valor", ascending=True)

col_c, col_d = st.columns([2, 3], gap="large")
with col_c:
    st.markdown(f"<div class='section-title'>{t('por_brand')}</div>", unsafe_allow_html=True)
    fig_brand = go.Figure(go.Bar(x=por_brand["Valor"], y=por_brand["Brand"], orientation="h", marker=dict(color=CORES[:len(por_brand)], opacity=0.9), text=[fmt_brand(v) for v in por_brand["Valor"]], textposition="outside", textfont=dict(color="#1E293B", size=11), cliponaxis=False))
    fig_brand_layout = {k: v for k, v in LAYOUT_BASE.items() if k != "xaxis"}
    fig_brand.update_layout(**fig_brand_layout, height=320, xaxis=dict(gridcolor="#E2E8F0", linecolor="#CBD5E1", range=[0, por_brand["Valor"].max() * 1.18]))
    st.plotly_chart(fig_brand, width='stretch', config={"displayModeBar": False})

with col_d:
    st.markdown(f"<div class='section-title'>{t('por_subbrand')}</div>", unsafe_allow_html=True)
    fig_subbrand = go.Figure(go.Bar(x=por_subbrand["Valor"], y=por_subbrand["Label"], orientation="h", marker=dict(color="#7C3AED", opacity=0.85), text=[fmt_brand(v) for v in por_subbrand["Valor"]], textposition="auto", textfont=dict(color="#1E293B", size=10), cliponaxis=False))
    fig_subbrand_layout = {k: v for k, v in LAYOUT_BASE.items() if k != "xaxis"}
    fig_subbrand.update_layout(**fig_subbrand_layout, height=max(320, 28 * len(por_subbrand)), xaxis=dict(gridcolor="#E2E8F0", linecolor="#CBD5E1", range=[0, por_subbrand["Valor"].max() * 1.18]))
    st.plotly_chart(fig_subbrand, width='stretch', config={"displayModeBar": False})


st.markdown("<div style='height:1px; background:#E2E8F0; margin: 40px 0;'></div>", unsafe_allow_html=True)
st.markdown(f"<div class='section-title'>{t('evolucao_diaria')}</div>", unsafe_allow_html=True)
evolucao = df.groupby(["data","marketplace"])[valor_col].sum().reset_index()
evolucao.columns = ["Data","Marketplace","Faturamento"]
fig3 = px.line(evolucao, x="Data", y="Faturamento", color="Marketplace", markers=False, color_discrete_sequence=CORES)
fig3.update_traces(line=dict(width=2))
fig3.update_layout(**LAYOUT_BASE, height=360, legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#475569")))
st.plotly_chart(fig3, width='stretch', config={"displayModeBar": False})

st.markdown("<div style='height:1px; background:#E2E8F0; margin: 40px 0;'></div>", unsafe_allow_html=True)
st.markdown(f"<div class='section-title'>{t('top10_titulo')}</div>", unsafe_allow_html=True)
metrica_sel = st.radio(t("visualizar_por"), [t("faturamento_rs"), t("quantidade_vendida")], horizontal=True)

if metrica_sel == t("faturamento_rs"):
    top = df.groupby(["fg","nome_produto"])[valor_col].sum().reset_index()
    top.columns = ["FG","Produto","Valor"]
    top = top.sort_values("Valor", ascending=False).head(10).sort_values("Valor", ascending=True)
    top["Label"] = top["FG"] + " — " + top["Produto"].str[:35]
    fig_top = go.Figure(go.Bar(x=top["Valor"], y=top["Label"], orientation="h", marker=dict(color="#7C3AED", opacity=0.85), text=[f"R$ {v:,.0f}" for v in top["Valor"]], textposition="outside", textfont=dict(color="#475569", size=10)))
else:
    top = df.groupby(["fg","nome_produto"])["quantidade"].sum().reset_index()
    top.columns = ["FG","Produto","Valor"]
    top = top.sort_values("Valor", ascending=False).head(10).sort_values("Valor", ascending=True)
    top["Label"] = top["FG"] + " — " + top["Produto"].str[:35]
    fig_top = go.Figure(go.Bar(x=top["Valor"], y=top["Label"], orientation="h", marker=dict(color="#10B981", opacity=0.85), text=[f"{v:,.0f}" for v in top["Valor"]], textposition="outside", textfont=dict(color="#475569", size=10)))

fig_top.update_layout(**{k:v for k,v in LAYOUT_BASE.items() if k!='yaxis'}, height=460, yaxis={"categoryorder":"array","categoryarray":top["Label"].tolist(),"gridcolor":"#E2E8F0","tickfont":{"size":10,"color":"#475569"}})
st.plotly_chart(fig_top, width='stretch', config={"displayModeBar": False})

st.markdown("<div style='height:1px; background:#E2E8F0; margin: 40px 0;'></div>", unsafe_allow_html=True)
aba1, aba2 = st.tabs([t("pedidos_validos_tab"), t("cancelados")])
colunas_exibir = ["data","fg","nome_produto","marketplace","valor","quantidade"]
if "status" in df.columns: colunas_exibir.append("status")
if "valor_total" in df.columns: colunas_exibir.append("valor_total")

with aba1:
    st.dataframe(df[colunas_exibir].sort_values("data", ascending=False), width='stretch', height=380)
with aba2:
    if not df_canc.empty:
        st.dataframe(df_canc[colunas_exibir].sort_values("data", ascending=False), width='stretch', height=380)
    else:
        st.info(t("nenhum_cancelamento"))

st.markdown(f"<div style='text-align:center; color:#94A3B8; font-size:11px; padding: 24px 0 8px;'>{t('footer', n=f'{len(df):,}', data=hoje)}</div>", unsafe_allow_html=True)