"""
Módulo compartilhado: traduções, estilo (CSS) e cabeçalho/logo
usado em todas as páginas do dashboard.
"""
import streamlit as st
import os

TRADUCOES = {
    "titulo_painel": {"PT": "Painel de Inteligência Comercial", "EN": "Commercial Intelligence Dashboard", "ES": "Panel de Inteligencia Comercial"},
    "titulo_principal": {"PT": "Comparativo de Vendas por Marketplace", "EN": "Sales Comparison by Marketplace", "ES": "Comparativo de Ventas por Marketplace"},
    "titulo_home": {"PT": "Painel de Inteligência Comercial", "EN": "Commercial Intelligence Dashboard", "ES": "Panel de Inteligencia Comercial"},
    "subtitulo_home": {"PT": "Módulos", "EN": "Modules", "ES": "Módulos"},
    "card_marketplaces_titulo": {"PT": "Marketplaces", "EN": "Marketplaces", "ES": "Marketplaces"},
    "card_marketplaces_desc": {"PT": "Comparativo de vendas, faturamento e quantidade por marketplace, brand e subbrand.", "EN": "Sales, revenue and units comparison by marketplace, brand and subbrand.", "ES": "Comparativo de ventas, facturación y cantidad por marketplace, marca y submarca."},
    "card_forecast_titulo": {"PT": "Forecast", "EN": "Forecast", "ES": "Forecast"},
    "card_forecast_desc": {"PT": "Projeções de vendas e tendências futuras.", "EN": "Sales projections and future trends.", "ES": "Proyecciones de ventas y tendencias futuras."},
    "card_cobertura_titulo": {"PT": "Cobertura", "EN": "Coverage", "ES": "Cobertura"},
    "card_cobertura_desc": {"PT": "Análise de cobertura de estoque e disponibilidade.", "EN": "Stock coverage and availability analysis.", "ES": "Análisis de cobertura de stock y disponibilidad."},
    "acessar": {"PT": "Acessar →", "EN": "Open →", "ES": "Acceder →"},
    "em_breve": {"PT": "Em breve", "EN": "Coming soon", "ES": "Próximamente"},
    "em_desenvolvimento_msg": {"PT": "Este módulo está em desenvolvimento e estará disponível em breve.", "EN": "This module is under development and will be available soon.", "ES": "Este módulo está en desarrollo y estará disponible próximamente."},
    "voltar_home": {"PT": "← Voltar para Home", "EN": "← Back to Home", "ES": "← Volver al Inicio"},
    "erro_conexao": {"PT": "Erro ao conectar no banco", "EN": "Error connecting to database", "ES": "Error al conectar con la base de datos"},
    "nenhum_dado": {"PT": "Nenhum dado encontrado.", "EN": "No data found.", "ES": "No se encontraron datos."},
    "periodo_rapido": {"PT": "Período rápido", "EN": "Quick period", "ES": "Período rápido"},
    "personalizado": {"PT": "Personalizado", "EN": "Custom", "ES": "Personalizado"},
    "ultima_semana": {"PT": "Última semana", "EN": "Last week", "ES": "Última semana"},
    "ultimo_mes": {"PT": "Último mês", "EN": "Last month", "ES": "Último mes"},
    "ultimos_6_meses": {"PT": "Últimos 6 meses", "EN": "Last 6 months", "ES": "Últimos 6 meses"},
    "ultimo_ano": {"PT": "Último ano", "EN": "Last year", "ES": "Último año"},
    "marketplace": {"PT": "Marketplace", "EN": "Marketplace", "ES": "Marketplace"},
    "todos": {"PT": "Todos", "EN": "All", "ES": "Todos"},
    "produto_fg": {"PT": "Produto (FG)", "EN": "Product (FG)", "ES": "Producto (FG)"},
    "brand": {"PT": "Brand", "EN": "Brand", "ES": "Marca"},
    "subbrand": {"PT": "Subbrand", "EN": "Subbrand", "ES": "Submarca"},
    "datas": {"PT": "Datas", "EN": "Dates", "ES": "Fechas"},
    "visao_geral": {"PT": "Visão Geral do Período Selecionado", "EN": "Overview of Selected Period", "ES": "Visión General del Período Seleccionado"},
    "faturamento_liquido": {"PT": "Faturamento Líquido", "EN": "Net Revenue", "ES": "Facturación Neta"},
    "pedidos_validos": {"PT": "Pedidos Válidos", "EN": "Valid Orders", "ES": "Pedidos Válidos"},
    "ticket_medio": {"PT": "Ticket Médio", "EN": "Average Ticket", "ES": "Ticket Promedio"},
    "mom_titulo": {"PT": "MoM — Meses Fechados", "EN": "MoM — Closed Months", "ES": "MoM — Meses Cerrados"},
    "mom_comparando": {"PT": "Comparando {a} com {b} e {c}", "EN": "Comparing {a} with {b} and {c}", "ES": "Comparando {a} con {b} y {c}"},
    "ultimo_mes_fechado": {"PT": "{m} — Último Mês Fechado", "EN": "{m} — Last Closed Month", "ES": "{m} — Último Mes Cerrado"},
    "vs_mes_anterior": {"PT": "vs {m} (Mês Anterior)", "EN": "vs {m} (Previous Month)", "ES": "vs {m} (Mes Anterior)"},
    "vs_mesmo_mes_ly": {"PT": "vs {m} (Mesmo Mês LY)", "EN": "vs {m} (Same Month LY)", "ES": "vs {m} (Mismo Mes LY)"},
    "ytd_titulo": {"PT": "YTD — Acumulado do Ano", "EN": "YTD — Year to Date", "ES": "YTD — Acumulado del Año"},
    "ytd_periodo": {"PT": "Jan/{ano} até {m} vs mesmo período {ano_ly}", "EN": "Jan/{ano} to {m} vs same period {ano_ly}", "ES": "Ene/{ano} hasta {m} vs mismo período {ano_ly}"},
    "ytd_ano": {"PT": "YTD {ano}", "EN": "YTD {ano}", "ES": "YTD {ano}"},
    "crescimento_ytd": {"PT": "Crescimento YTD {ano} vs {ano_ly}", "EN": "YTD Growth {ano} vs {ano_ly}", "ES": "Crecimiento YTD {ano} vs {ano_ly}"},
    "visualizar_marketplace_por": {"PT": "Visualizar marketplace por:", "EN": "View marketplace by:", "ES": "Visualizar marketplace por:"},
    "faturamento_rs": {"PT": "Faturamento (R$)", "EN": "Revenue ($)", "ES": "Facturación ($)"},
    "quantidade_vendida": {"PT": "Quantidade vendida", "EN": "Units sold", "ES": "Cantidad vendida"},
    "faturamento_liquido_por_mp": {"PT": "Faturamento Líquido por Marketplace", "EN": "Net Revenue by Marketplace", "ES": "Facturación Neta por Marketplace"},
    "quantidade_por_mp": {"PT": "Quantidade Vendida por Marketplace", "EN": "Units Sold by Marketplace", "ES": "Cantidad Vendida por Marketplace"},
    "participacao_pct": {"PT": "Participação %", "EN": "Share %", "ES": "Participación %"},
    "fat_qtd_brand_subbrand": {"PT": "Faturamento e Quantidade por Brand / Subbrand", "EN": "Revenue and Units by Brand / Subbrand", "ES": "Facturación y Cantidad por Marca / Submarca"},
    "visualizar_brand_por": {"PT": "Visualizar brand/subbrand por:", "EN": "View brand/subbrand by:", "ES": "Visualizar marca/submarca por:"},
    "por_brand": {"PT": "Por Brand", "EN": "By Brand", "ES": "Por Marca"},
    "por_subbrand": {"PT": "Por Subbrand", "EN": "By Subbrand", "ES": "Por Submarca"},
    "evolucao_diaria": {"PT": "Evolução Diária por Marketplace", "EN": "Daily Trend by Marketplace", "ES": "Evolución Diaria por Marketplace"},
    "top10_titulo": {"PT": "Top 10 Produtos (FG Consolidado)", "EN": "Top 10 Products (Consolidated FG)", "ES": "Top 10 Productos (FG Consolidado)"},
    "visualizar_por": {"PT": "Visualizar por:", "EN": "View by:", "ES": "Visualizar por:"},
    "pedidos_validos_tab": {"PT": "Pedidos Válidos", "EN": "Valid Orders", "ES": "Pedidos Válidos"},
    "cancelados": {"PT": "Cancelados", "EN": "Cancelled", "ES": "Cancelados"},
    "nenhum_cancelamento": {"PT": "Nenhum cancelamento no período.", "EN": "No cancellations in this period.", "ES": "No hay cancelaciones en el período."},
    "footer": {"PT": "Atualizado a cada 5 min · {n} pedidos válidos · Última data: {data}", "EN": "Updated every 5 min · {n} valid orders · Last date: {data}", "ES": "Actualizado cada 5 min · {n} pedidos válidos · Última fecha: {data}"},
    "idioma": {"PT": "Idioma", "EN": "Language", "ES": "Idioma"},
}


def init_idioma():
    if "idioma" not in st.session_state:
        st.session_state["idioma"] = "PT"
    qp_lang = st.query_params.get("lang")
    if qp_lang in ("PT", "EN", "ES") and qp_lang != st.session_state["idioma"]:
        st.session_state["idioma"] = qp_lang


def t(chave, **kwargs):
    texto = TRADUCOES.get(chave, {}).get(st.session_state.get("idioma", "PT"), chave)
    if kwargs:
        return texto.format(**kwargs)
    return texto


def aplicar_estilo():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F4F6FB; color: #1E293B; }
    .stApp { background: linear-gradient(135deg, #F4F6FB 0%, #EBEFF7 100%); }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: #0F172A !important; }
    [data-testid="metric-container"] { background: linear-gradient(145deg, #FFFFFF, #F8FAFC); border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px 24px; box-shadow: 0 4px 16px rgba(15,23,42,0.06); }
    [data-testid="metric-container"] p { color: #64748B !important; font-size: 12px !important; font-weight: 600 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }
    [data-testid="stMetricValue"] > div { color: #0F172A !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 28px !important; font-weight: 800 !important; }
    [data-testid="stDateInput"] input { background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important; color: #1E293B !important; border-radius: 8px !important; }
    [data-testid="stDateInput"] > div > div { background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important; border-radius: 8px !important; color: #1E293B !important; }
    [data-testid="stSelectbox"] > div > div { background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important; color: #1E293B !important; border-radius: 8px !important; }
    [data-testid="stTabs"] [data-baseweb="tab"] { background: transparent; color: #64748B; font-weight: 500; }
    [data-testid="stTabs"] [aria-selected="true"] { color: #7C3AED !important; border-bottom: 2px solid #7C3AED !important; }
    [data-testid="stDataFrame"] { border: 1px solid #E2E8F0; border-radius: 12px; overflow: hidden; }
    hr { border-color: #E2E8F0 !important; }
    .section-title { font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 600; color: #64748B; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 20px; }
    .kpi-section-label { font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; padding: 6px 14px; border-radius: 6px; display: inline-block; margin-bottom: 12px; }
    .kpi-main  { background: rgba(124,58,237,0.10); color: #7C3AED; border: 1px solid rgba(124,58,237,0.25); }
    .kpi-mom   { background: rgba(59,130,246,0.10); color: #2563EB; border: 1px solid rgba(59,130,246,0.25); }
    .kpi-ytd   { background: rgba(16,185,129,0.10); color: #059669; border: 1px solid rgba(16,185,129,0.25); }
    [data-testid="StyledFullScreenButton"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    #MainMenu { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    .stSpinner { display: none !important; }
    [data-testid="stSidebar"] { display: block !important; visibility: visible !important; }
    [data-testid="stBottomBlockContainer"] { display: none !important; }
    ._profileContainer_1yi6l_53 { display: none !important; }
    .viewerBadge_container__r5tak { display: none !important; }
    #stDecoration { display: none !important; }
    [data-testid="stActionButtonIcon"] { display: none !important; }
    .stDeployButton { display: none !important; }
    [kind="deployButton"] { display: none !important; }
    footer { display: none !important; }
    footer:after { display: none !important; }
    [data-testid="manage-app-button"] { display: none !important; }
    div[class*="profileContainer"] { display: none !important; }
    div[class*="viewerBadge"] { display: none !important; }
    div[class*="styles_viewerBadge"] { display: none !important; }
    div[class*="streamlitAppDeployButton"] { display: none !important; }
    button[title="View fullscreen"] { display: none !important; }
    button[title="Fullscreen"] { display: none !important; }
    [data-testid="stImage"] button { display: none !important; }
    [data-testid="stElementToolbar"] { display: none !important; }
    .js-plotly-plot, .plot-container { width: 100% !important; max-width: 100% !important; overflow: hidden !important; }
    [data-testid="stHorizontalBlock"] { overflow: visible; }
    [data-testid="column"] { min-width: 0 !important; overflow: hidden; }
    [data-testid="stAppViewContainer"] > .main .block-container { padding-top: 0.5rem !important; }
    [data-testid="stSidebarNav"] { padding-top: 3rem !important; }
    [data-testid="stSidebarContent"] { padding-top: 3rem !important; }
    .card-modulo { display:block !important; text-decoration:none !important; color:inherit !important; transition: transform 0.15s ease, box-shadow 0.15s ease; }
    .card-modulo:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(15,23,42,0.10) !important; text-decoration:none !important; }
    .card-modulo * { text-decoration:none !important; }
    </style>
    """, unsafe_allow_html=True)


def seletor_idioma_html():
    """Retorna o HTML dos links PT · EN · ES."""
    idioma_atual = st.session_state["idioma"]
    opcoes = ["PT", "EN", "ES"]
    links = []
    for lng in opcoes:
        if lng == idioma_atual:
            links.append(f"<span style='color:#7C3AED; font-weight:700;'>{lng}</span>")
        else:
            links.append(f"<a href='?lang={lng}' target='_self' style='color:#94A3B8; font-weight:600; text-decoration:none;'>{lng}</a>")
    return " <span style='color:#CBD5E1;'>·</span> ".join(links)


def cabecalho(titulo_chave="titulo_painel", subtitulo_chave="titulo_principal", mostrar_logo=True):
    """Renderiza o cabeçalho padrão com seletor de idioma e logo."""
    col_titulo, col_logo = st.columns([5, 1], vertical_alignment="center")
    with col_titulo:
        lang_html = seletor_idioma_html()
        st.markdown(f"""
        <div style='padding: 0 0 24px 0;'>
            <div style='display:flex; align-items:center; gap:10px; margin-bottom:8px;'>
                <div style='font-family: Space Grotesk, sans-serif; font-size: 11px; font-weight: 600; letter-spacing: 0.15em; color: #7C3AED; text-transform: uppercase;'>{t(titulo_chave)}</div>
                <div style='font-family: Space Grotesk, sans-serif; font-size: 11px; letter-spacing: 0.05em;'>{lang_html}</div>
            </div>
            <h1 style='font-size: 32px; font-weight: 700; margin: 0; color: #0F172A;'>{t(subtitulo_chave)}</h1>
        </div>
        """, unsafe_allow_html=True)
    with col_logo:
        if mostrar_logo:
            logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_combe.png")
            if os.path.exists(logo_path):
                st.image(logo_path, width=200)