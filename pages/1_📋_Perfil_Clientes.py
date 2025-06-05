import streamlit as st
import pandas as pd
from scripts.functions import (
    client_age_hist,
    client_fam_num_bar,
    client_with_kids_or_not_pie,
    client_salary_hist,
    client_num_per_city_bar,
)

st.set_page_config(page_title="Perfil dos Clientes", layout="wide")

st.title("📋 Perfil dos Clientes")
df_full = pd.read_csv("data/dataset.csv")
df = df_full.copy()  # Remover duplicados para análises corretas

# Obter lista de cidades únicas (ordenadas)
cidades = sorted(df["client_city"].unique())

# SelectBox para escolher a cidade
cidade_selecionada = st.selectbox("Seleciona uma cidade:", ["Todas"] + cidades)
if cidade_selecionada != "Todas":
    df = df[df["client_city"] == cidade_selecionada]

total_clients = df['client_id'].nunique()
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
        <div>Total de Clientes: {total_clients}</div>
        <div>Idade Média: {df['client_age'].mean():.1f}</div>
        <div>Salário Médio: {df['client_salary'].mean():,.1f}k €</div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.container():
    client_num_per_city_bar(df_full)

with st.container():
    client_with_kids_or_not_pie(df)
    
with st.container():
    client_fam_num_bar(df)

col1, col2 = st.columns(2)
with col1:
    client_age_hist(df)
with col2:
    client_salary_hist(df)
