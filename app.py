import streamlit as st
from shared import init_idioma, t, aplicar_estilo, cabecalho

st.set_page_config(page_title="Painel Combe", page_icon="📊", layout="wide")

init_idioma()
aplicar_estilo()
cabecalho(titulo_chave="titulo_home", subtitulo_chave="subtitulo_home")

st.markdown("<div style='height:4px; background: linear-gradient(90deg,#7C3AED,#3B82F6,#10B981); border-radius:4px; margin: 8px 0 32px;'></div>", unsafe_allow_html=True)

# Obtém a base URL do app para montar os links
base = st.context.url if hasattr(st, 'context') and hasattr(st.context, 'url') else ""

MODULOS = [
    {"titulo": t("card_marketplaces_titulo"), "desc": t("card_marketplaces_desc"), "slug": "Marketplaces", "icone": "🛒", "cor": "#7C3AED"},
    {"titulo": t("card_forecast_titulo"),     "desc": t("card_forecast_desc"),     "slug": "Forecast",     "icone": "📈", "cor": "#3B82F6"},
    {"titulo": t("card_cobertura_titulo"),    "desc": t("card_cobertura_desc"),    "slug": "Cobertura",    "icone": "📦", "cor": "#10B981"},
]

cols = st.columns(3)
for col, mod in zip(cols, MODULOS):
    with col:
        st.markdown(
            f"<a href='/{mod['slug']}' target='_self' style='display:block; text-decoration:none;'>"
            f"<div style='background:linear-gradient(145deg,#FFFFFF,#F8FAFC); border:1px solid #E2E8F0; "
            f"border-top:3px solid {mod['cor']}; border-radius:14px; padding:28px 24px; "
            f"box-shadow:0 4px 16px rgba(15,23,42,0.06); min-height:180px; cursor:pointer;'>"
            f"<span style='display:block; font-size:32px; margin-bottom:12px;'>{mod['icone']}</span>"
            f"<span style='display:block; font-family:Space Grotesk,sans-serif; font-size:20px; font-weight:800; color:#0F172A; margin-bottom:8px;'>{mod['titulo']}</span>"
            f"<span style='display:block; font-size:13px; color:#64748B; line-height:1.5;'>{mod['desc']}</span>"
            f"</div></a>",
            unsafe_allow_html=True
        )

st.markdown("<br><div style='text-align:center; color:#94A3B8; font-size:12px;'>Ou use o menu lateral para navegar entre módulos</div>", unsafe_allow_html=True)