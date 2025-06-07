import streamlit as st
import pandas as pd
from scripts.functions import (
    depart_sales_num_bar,
    sales_evolution_by_store,
    top_product_categories,
    top_selling_store,
    product_share_by_category,
    vendas_boxplot_promocao,
)

st.set_page_config(page_title="Padrões de Compra", layout="wide")

st.title("🛒 Padrões de Compra")

df_full = pd.read_csv("data/dataset.csv")
df = df_full.copy()

df['transaction_timestamp'] = pd.to_datetime(df['transaction_timestamp'])
promo_days_df = df[df['is_promo_day'] == 1]
total_promo_days = promo_days_df['transaction_timestamp'].dt.date.nunique()

st.markdown(
    f"""
    <div style='
        display: flex;
        justify-content: space-around;
        background-color: #00838F;
        color: white;
        padding: 15px 0;
        font-size: 20px;
        font-weight: bold;
        border-radius: 8px;
        margin-bottom: 20px;
    '>
        <div>Total de Vendas: {df['basket_id'].nunique()}</div>
        <div>Total de Produtos Vendidos: {df['quantity'].sum()}</div>
        <div>Dias com Promoção: {total_promo_days}</div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.container():
    depart_sales_num_bar(df_full)

st.markdown("---")

with st.container():
    sales_evolution_by_store(df)

with st.container():
    top_product_categories(df)

with st.container():
    top_selling_store(df)

with st.container():
    product_share_by_category(df)

with st.container():
    vendas_boxplot_promocao(df)
