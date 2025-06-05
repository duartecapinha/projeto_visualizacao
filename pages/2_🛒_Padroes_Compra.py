import streamlit as st
import pandas as pd
from scripts.functions import (
    depart_sales_num_bar
)

st.set_page_config(page_title="Padrões de Compra", layout="wide")

st.title("🛒 Padrões de Compra")

df = pd.read_csv("data/dataset.csv")

total_sales = df['basket_id'].nunique()
total_products_sold = df['quantity'].sum()
total_promo_days = df['is_promo_day'].sum()

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
        <div>Total de Vendas: {total_sales}</div>
        <div>Total de Produtos Vendidos: {total_products_sold}</div>
        <div>Dias com Promoção: {total_promo_days}TEMOS DE MUDAR ISTO TUDO DEPOIS DA ANÁLISE</div>
    </div>
    """,
    unsafe_allow_html=True
)

depart_sales_num_bar(df)