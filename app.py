import streamlit as st
from shared import init_idioma, t, aplicar_estilo, cabecalho

st.set_page_config(page_title="Painel Combe", page_icon="📊", layout="wide")

init_idioma()
aplicar_estilo()
cabecalho(titulo_chave="titulo_home", subtitulo_chave="subtitulo_home")

st.markdown("<div style='height:4px; background: linear-gradient(90deg,#7C3AED,#3B82F6,#10B981); border-radius:4px; margin: 8px 0 32px;'></div>", unsafe_allow_html=True)

st.markdown("""
<style>
.card-btn button {
    background: linear-gradient(145deg,#FFFFFF,#F8FAFC) !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 28px 24px !important;
    box-shadow: 0 4px 16px rgba(15,23,42,0.06) !important;
    min-height: 200px !important;
    width: 100% !important;
    text-align: left !important;
    color: #0F172A !important;
    font-family: Space Grotesk, sans-serif !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    white-space: pre-line !important;
    line-height: 1.6 !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.card-btn button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 24px rgba(15,23,42,0.10) !important;
}
.card-mkt button { border-top: 3px solid #7C3AED !important; }
.card-fct button { border-top: 3px solid #3B82F6 !important; }
.card-cob button { border-top: 3px solid #10B981 !important; }
</style>
""", unsafe_allow_html=True)


def card_modulo(titulo, descricao, url, icone, cor_class, key, disponivel=True):
    label = f"{icone}\n\n**{titulo}**\n\n{descricao}"
    st.markdown(f"<div class='card-btn {cor_class}'>", unsafe_allow_html=True)
    if disponivel:
        if st.button(label, key=key, use_container_width=True):
            st.markdown(f"<meta http-equiv='refresh' content='0; url={url}'>", unsafe_allow_html=True)
    else:
        st.button(label, key=key, use_container_width=True, disabled=True)
    st.markdown("</div>", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)
with col1:
    card_modulo(t("card_marketplaces_titulo"), t("card_marketplaces_desc"), "/Marketplaces", "🛒", "card-mkt", "btn_mkt")
with col2:
    card_modulo(t("card_forecast_titulo"), t("card_forecast_desc"), "/Forecast", "📈", "card-fct", "btn_fct")
with col3:
    card_modulo(t("card_cobertura_titulo"), t("card_cobertura_desc"), "/Cobertura", "📦", "card-cob", "btn_cob")