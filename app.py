import streamlit as st
from shared import init_idioma, t, aplicar_estilo, cabecalho

st.set_page_config(page_title="Painel Combe", page_icon="📊", layout="wide")

init_idioma()
aplicar_estilo()
cabecalho(titulo_chave="titulo_home", subtitulo_chave="subtitulo_home")

st.markdown("<div style='height:4px; background: linear-gradient(90deg,#7C3AED,#3B82F6,#10B981); border-radius:4px; margin: 8px 0 32px;'></div>", unsafe_allow_html=True)


def card_modulo(titulo, descricao, pagina, icone, cor, disponivel=True):
    st.markdown(
        f"<div style='background:linear-gradient(145deg,#FFFFFF,#F8FAFC); border:1px solid #E2E8F0; "
        f"border-top:3px solid {cor}; border-radius:14px; padding:28px 24px; "
        f"box-shadow:0 4px 16px rgba(15,23,42,0.06); min-height:160px;'>"
        f"<span style='display:block; font-size:32px; margin-bottom:12px;'>{icone}</span>"
        f"<span style='display:block; font-family:Space Grotesk,sans-serif; font-size:20px; font-weight:800; color:#0F172A; margin-bottom:8px;'>{titulo}</span>"
        f"<span style='display:block; font-size:13px; color:#64748B; line-height:1.5;'>{descricao}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
    if disponivel:
        st.page_link(pagina, label=f"Acessar {titulo} →", use_container_width=True)
    else:
        st.markdown(f"<div style='text-align:center; color:#94A3B8; font-size:12px; padding:8px;'>Em breve</div>", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)
with col1:
    card_modulo(t("card_marketplaces_titulo"), t("card_marketplaces_desc"), "pages/1_Marketplaces.py", "🛒", "#7C3AED")
with col2:
    card_modulo(t("card_forecast_titulo"), t("card_forecast_desc"), "pages/2_Forecast.py", "📈", "#3B82F6")
with col3:
    card_modulo(t("card_cobertura_titulo"), t("card_cobertura_desc"), "pages/3_Cobertura.py", "📦", "#10B981")