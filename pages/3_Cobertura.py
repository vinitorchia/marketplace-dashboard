import streamlit as st
from shared import init_idioma, t, aplicar_estilo, cabecalho

st.set_page_config(page_title="Cobertura", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

init_idioma()
aplicar_estilo()
cabecalho(titulo_chave="titulo_painel", subtitulo_chave="card_cobertura_titulo")

st.markdown("<div style='height:4px; background: linear-gradient(90deg,#7C3AED,#3B82F6,#10B981); border-radius:4px; margin: 8px 0 32px;'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div style='background: linear-gradient(145deg,#FFFFFF,#F8FAFC); border:1px solid #E2E8F0;
            border-top: 3px solid #10B981; border-radius:14px; padding:60px 40px;
            box-shadow:0 4px 16px rgba(15,23,42,0.06); text-align:center;'>
    <div style='font-size:48px; margin-bottom:16px;'>📦</div>
    <div style='font-family:Space Grotesk,sans-serif; font-size:22px; font-weight:800; color:#0F172A; margin-bottom:8px;'>{t("em_breve")}</div>
    <div style='font-size:14px; color:#64748B;'>{t("em_desenvolvimento_msg")}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
if st.button(t("voltar_home")):
    st.switch_page("app.py")