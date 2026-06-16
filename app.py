import streamlit as st
from shared import init_idioma, t, aplicar_estilo, cabecalho

st.set_page_config(page_title="Painel Combe", page_icon="📊", layout="wide")

init_idioma()
aplicar_estilo()
cabecalho(titulo_chave="titulo_home", subtitulo_chave="subtitulo_home")

st.markdown("<div style='height:4px; background: linear-gradient(90deg,#7C3AED,#3B82F6,#10B981); border-radius:4px; margin: 8px 0 32px;'></div>", unsafe_allow_html=True)


def card_modulo(titulo, descricao, pagina_slug, icone, cor, disponivel=True):
    disponivel_html = ""
    if not disponivel:
        disponivel_html = f"<span style='background:rgba(148,163,184,0.15); color:#94A3B8; font-size:10px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; padding:4px 10px; border-radius:6px; margin-left:8px;'>{t('em_breve')}</span>"

    conteudo = f"<span style='display:block; font-size:32px; margin-bottom:12px;'>{icone}</span><span style='display:block; font-family:Space Grotesk,sans-serif; font-size:20px; font-weight:800; color:#0F172A; margin-bottom:8px;'>{titulo}{disponivel_html}</span><span style='display:block; font-size:13px; color:#64748B; line-height:1.5;'>{descricao}</span>"

    estilo_card = f"display:block; background: linear-gradient(145deg,#FFFFFF,#F8FAFC); border:1px solid #E2E8F0; border-top: 3px solid {cor}; border-radius:14px; padding:28px 24px; box-shadow:0 4px 16px rgba(15,23,42,0.06); min-height:180px; text-decoration:none; color:inherit;"

    if disponivel:
        card_html = f"<a class='card-modulo' href='/{pagina_slug}' target='_self' style='{estilo_card}'>{conteudo}</a>"
    else:
        card_html = f"<span class='card-modulo' style='{estilo_card} cursor:default;'>{conteudo}</span>"

    st.markdown(card_html, unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)
with col1:
    card_modulo(
        t("card_marketplaces_titulo"),
        t("card_marketplaces_desc"),
        "Marketplaces",
        "🛒",
        "#7C3AED",
        disponivel=True,
    )
with col2:
    card_modulo(
        t("card_forecast_titulo"),
        t("card_forecast_desc"),
        "Forecast",
        "📈",
        "#3B82F6",
        disponivel=True,
    )
with col3:
    card_modulo(
        t("card_cobertura_titulo"),
        t("card_cobertura_desc"),
        "Cobertura",
        "📦",
        "#10B981",
        disponivel=True,
    )