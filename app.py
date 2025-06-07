import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="Dashboard de Clientes", page_icon="📊", layout="wide")

col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("<div style='padding-bottom: 30px;'>", unsafe_allow_html=True)
    st.image("image/logo.png")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.title("Dashboard de Análise de Clientes")
    st.markdown("#### Bem-vindo! Explora os dados dos clientes e os seus hábitos de compra.")

st.markdown("---")

st.markdown("#### 📌 O que podes analisar neste dashboard?")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    🔹 **Perfil dos Clientes**
    - Idade dos Clientes
    - Salário dos Clientes
    """)

with col2:
    st.markdown("""
    🔸 **Padrões de Compra**
    - Produtos mais comprados
    - Categorias por departamento
    """)

st.markdown("---")

if st.button("👉 Começar a Explorar"):
    st.switch_page("pages/main.py")

st.markdown("""
<div style='text-align: center; color: grey; font-size: 12px; margin-top: 50px;'>
Desenvolvido por Duarte Capinha, Dionisio e Pedro • Projeto de Visualização de Dados
</div>
""", unsafe_allow_html=True)
