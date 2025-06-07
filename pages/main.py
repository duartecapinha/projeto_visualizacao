import streamlit as st
import pandas as pd
from scripts.functions import (
    # CLIENTES
    client_age_hist,
    client_fam_num_bar,
    client_with_kids_or_not_pie,
    client_salary_hist,
    client_num_per_city_bar,

    # PADRÕES DE COMPRA
    depart_sales_num_bar,
    sales_evolution_by_store,
    top_product_categories,
    top_selling_store,
    product_share_by_category,
    vendas_boxplot_promocao,
)

# Configuração da página
st.set_page_config(page_title="Dashboard Consolidado", layout="wide")
df = pd.read_csv("data/dataset.csv")
df["transaction_timestamp"] = pd.to_datetime(df["transaction_timestamp"])

# KPIs de vendas
total_faturas = f"{df['basket_id'].nunique():,}"
total_produtos = f"{df['quantity'].sum():,}"
total_promo = df[df["is_promo_day"] == 1]["transaction_timestamp"].dt.date.nunique()

# CSS dos botões
st.markdown("""
    <style>
        .menu-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 0px;
            margin-bottom: 20px;
        }
        .menu-button {
            padding: 10px 30px;
            border: none;
            border-radius: 8px;
            background: linear-gradient(135deg, #1e1e80, #6a1b9a);
            font-weight: bold;
            font-size: 22px;
            cursor: pointer;
            color: white;
            box-shadow: 0 0 10px rgba(106, 27, 154, 0.3);
            transition: all 0.3s ease-in-out;
        }
        .menu-button:hover {
            transform: scale(1.03);
            box-shadow: 0 0 15px rgba(106, 27, 154, 0.5);
        }

    </style>
""", unsafe_allow_html=True)

# Botões do topo
col1, col2 = st.columns(2)
with col1:
    if st.button("👥 Perfil Clientes"):
        st.session_state["tab"] = "clientes"
with col2:
    if st.button("🛒 Padrões de Compra"):
        st.session_state["tab"] = "compras"

# Estado inicial
if "tab" not in st.session_state:
    st.session_state["tab"] = "clientes"

# ============================
# === Perfil dos Clientes ===
# ============================
if st.session_state["tab"] == "clientes":
    st.markdown("<h4>👥 Perfil dos Clientes</h4>", unsafe_allow_html=True)

    # Botões e gráfico lado a lado
    col_graph, col_menu = st.columns([5, 2], gap="large")
    with col_menu:
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        selected = st.radio("", [
            "Clientes por Cidade",
            "Distribuição por Idade",
            "Distribuição por Salário",
            "Com/sem Filhos",
            "Nº Elementos por Família"
        ], format_func=lambda x: f"📊 {x}", label_visibility="collapsed")

    with col_graph:
        df_clientes = df.copy()
        cidades = sorted(df_clientes["client_city"].unique())
        cidade_selecionada = st.selectbox("Seleciona uma cidade:", ["Todas"] + cidades)

        if cidade_selecionada != "Todas":
            df_clientes = df_clientes[df_clientes["client_city"] == cidade_selecionada]

        if selected == "Clientes por Cidade":
            client_num_per_city_bar(df_clientes)
        elif selected == "Distribuição por Idade":
            client_age_hist(df_clientes)
        elif selected == "Distribuição por Salário":
            client_salary_hist(df_clientes)
        elif selected == "Com/sem Filhos":
            client_with_kids_or_not_pie(df_clientes)
        elif selected == "Nº Elementos por Família":
            client_fam_num_bar(df_clientes)

    # KPIs abaixo
    st.markdown("""<hr style='margin-top: 10px; margin-bottom: 5px;'>""", unsafe_allow_html=True)

    st.markdown(f"""
        <style>
            .kpi-container {{
                display: flex;
                justify-content: space-between;
                margin-top: -10px;
                margin-bottom: -10px;
            }}
            .kpi-box {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                padding: 10px;
                flex: 1;
                border-radius: 8px;
            }}
            .kpi-label {{
                font-size: 16px;
                font-weight: 500;
                color: #ccc;
                white-space: nowrap;
            }}
            .kpi-value {{
                font-size: 26px;
                font-weight: bold;
                color: white;
            }}
        </style>
        <div class="kpi-container">
            <div class="kpi-box">
                <div class="kpi-label">👥 Total de Clientes</div>
                <div class="kpi-value">{df['client_id'].nunique()}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label">🎂 Idade Média</div>
                <div class="kpi-value">{df['client_age'].mean():.1f}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label">💰 Salário Médio</div>
                <div class="kpi-value">{df['client_salary'].mean():,.1f}k €</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ============================
# === Padrões de Compra =====
# ============================
elif st.session_state["tab"] == "compras":
    st.markdown("<h4>🛒 Padrões de Compra</h4>", unsafe_allow_html=True)

    col_graph, col_menu = st.columns([5, 2], gap="large")
    with col_menu:
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        selected = st.radio("", [
            "Evolução de Vendas",
            "Vendas por Departamento",
            "Loja com Mais Vendas",
            "Top Categorias Vendidas",
            "Top por Departamento",
            "Promoções: Loja 1"
        ], format_func=lambda x: f"📊 {x}", label_visibility="collapsed")

    with col_graph:
        if selected == "Evolução de Vendas":
            sales_evolution_by_store(df)
        elif selected == "Vendas por Departamento":
            depart_sales_num_bar(df)
        elif selected == "Loja com Mais Vendas":
            top_selling_store(df)
        elif selected == "Top Categorias Vendidas":
            top_product_categories(df)
        elif selected == "Top por Departamento":
            product_share_by_category(df)
        elif selected == "Promoções: Loja 1":
            vendas_boxplot_promocao(df)

    st.markdown("""<hr style='margin-top: 10px; margin-bottom: 5px;'>""", unsafe_allow_html=True)

    st.markdown(f"""
        <style>
            .kpi-container {{
                display: flex;
                justify-content: space-between;
                margin-top: -10px;
                margin-bottom: -10px;
            }}
            .kpi-box {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                padding: 10px;
                flex: 1;
                border-radius: 8px;
            }}
            .kpi-label {{
                font-size: 16px;
                font-weight: 500;
                color: #ccc;
                white-space: nowrap;
            }}
            .kpi-value {{
                font-size: 26px;
                font-weight: bold;
                color: white;
            }}
        </style>
        <div class="kpi-container">
            <div class="kpi-box">
                <div class="kpi-label">📋 Total de Faturas</div>
                <div class="kpi-value">{total_faturas}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label">📦 Produtos Vendidos</div>
                <div class="kpi-value">{total_produtos}</div>
            </div>
            <div class="kpi-box">
                <div class="kpi-label">🔥 Dias com Promoção</div>
                <div class="kpi-value">{total_promo}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


