import streamlit as st
from shared import init_idioma, t, aplicar_estilo, cabecalho

st.set_page_config(page_title="Painel Combe", page_icon="📊", layout="wide")

init_idioma()
aplicar_estilo()
cabecalho(titulo_chave="titulo_home", subtitulo_chave="subtitulo_home")

st.markdown("<div style='height:4px; background: linear-gradient(90deg,#7C3AED,#3B82F6,#10B981); border-radius:4px; margin: 8px 0 32px;'></div>", unsafe_allow_html=True)

# CSS para estilizar o st.page_link como card
st.markdown("""
<style>
[data-testid="stPageLink"] {
    background: linear-gradient(145deg,#FFFFFF,#F8FAFC) !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 0 !important;
    box-shadow: 0 4px 16px rgba(15,23,42,0.06) !important;
    width: 100% !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
[data-testid="stPageLink"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 24px rgba(15,23,42,0.10) !important;
}
[data-testid="stPageLink"] p {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)


def card_modulo(titulo, descricao, pagina, icone, cor, disponivel=True):
    disponivel_html = ""
    if not disponivel:
        disponivel_html = f"<span style='background:rgba(148,163,184,0.15); color:#94A3B8; font-size:10px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; padding:4px 10px; border-radius:6px; margin-left:8px;'>{t('em_breve')}</span>"

    st.markdown(
        f"<div style='background: linear-gradient(145deg,#FFFFFF,#F8FAFC); border:1px solid #E2E8F0; "
        f"border-top: 3px solid {cor}; border-radius:14px; padding:28px 24px; "
        f"box-shadow:0 4px 16px rgba(15,23,42,0.06); min-height:180px; "
        f"transition: transform 0.15s ease, box-shadow 0.15s ease; cursor:{'pointer' if disponivel else 'default'};'>"
        f"<span style='display:block; font-size:32px; margin-bottom:12px;'>{icone}</span>"
        f"<span style='display:block; font-family:Space Grotesk,sans-serif; font-size:20px; font-weight:800; color:#0F172A; margin-bottom:8px;'>{titulo}{disponivel_html}</span>"
        f"<span style='display:block; font-size:13px; color:#64748B; line-height:1.5;'>{descricao}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
    if disponivel:
        st.page_link(pagina, label=titulo, use_container_width=True)


col1, col2, col3 = st.columns(3)
with col1:
    card_modulo(t("card_marketplaces_titulo"), t("card_marketplaces_desc"), "pages/1_Marketplaces.py", "🛒", "#7C3AED")
with col2:
    card_modulo(t("card_forecast_titulo"), t("card_forecast_desc"), "pages/2_Forecast.py", "📈", "#3B82F6")
with col3:
    card_modulo(t("card_cobertura_titulo"), t("card_cobertura_desc"), "pages/3_Cobertura.py", "📦", "#10B981")