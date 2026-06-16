import streamlit as st
from shared import init_idioma, t, aplicar_estilo, cabecalho

st.set_page_config(page_title="Painel Combe", page_icon="📊", layout="wide")

init_idioma()
aplicar_estilo()
cabecalho(titulo_chave="titulo_home", subtitulo_chave="subtitulo_home")

st.markdown("<div style='height:4px; background: linear-gradient(90deg,#7C3AED,#3B82F6,#10B981); border-radius:4px; margin: 8px 0 32px;'></div>", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="stButton"] button {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    opacity: 0;
    cursor: pointer;
    z-index: 10;
}
.card-wrapper {
    position: relative;
}
</style>
""", unsafe_allow_html=True)


def card_modulo(titulo, descricao, pagina, icone, cor, key, disponivel=True):
    disponivel_html = ""
    if not disponivel:
        disponivel_html = f"<span style='background:rgba(148,163,184,0.15); color:#94A3B8; font-size:10px; font-weight:700; text-transform:uppercase; padding:4px 10px; border-radius:6px; margin-left:8px;'>{t('em_breve')}</span>"

    st.markdown(
        f"<div class='card-wrapper' style='position:relative; background:linear-gradient(145deg,#FFFFFF,#F8FAFC); border:1px solid #E2E8F0; "
        f"border-top:3px solid {cor}; border-radius:14px; padding:28px 24px; "
        f"box-shadow:0 4px 16px rgba(15,23,42,0.06); min-height:180px;'>"
        f"<span style='display:block; font-size:32px; margin-bottom:12px;'>{icone}</span>"
        f"<span style='display:block; font-family:Space Grotesk,sans-serif; font-size:20px; font-weight:800; color:#0F172A; margin-bottom:8px;'>{titulo}{disponivel_html}</span>"
        f"<span style='display:block; font-size:13px; color:#64748B; line-height:1.5;'>{descricao}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
    if disponivel:
        if st.button(titulo, key=key, use_container_width=True):
            st.switch_page(pagina)


col1, col2, col3 = st.columns(3)
with col1:
    card_modulo(t("card_marketplaces_titulo"), t("card_marketplaces_desc"), "pages/1_Marketplaces.py", "🛒", "#7C3AED", key="btn_mkt")
with col2:
    card_modulo(t("card_forecast_titulo"), t("card_forecast_desc"), "pages/2_Forecast.py", "📈", "#3B82F6", key="btn_fct")
with col3:
    card_modulo(t("card_cobertura_titulo"), t("card_cobertura_desc"), "pages/3_Cobertura.py", "📦", "#10B981", key="btn_cob")