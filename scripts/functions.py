import streamlit as st
import plotly.express as px
import pandas as pd

import plotly.graph_objects as go
import numpy as np

# PERFIL DOS CLIENTES

def client_age_hist(df):
    # Histograma com a distribuição da idade dos clientes
    st.subheader("Distribuição da Idade dos Clientes")
    
    unique_clients = df.drop_duplicates(subset="client_id")

    fig_age = px.histogram(
        unique_clients,
        x="client_age",
        nbins=30,
        color_discrete_sequence=["#00838F"],
        title=" "
    )
    mean_age = unique_clients["client_age"].mean()
    fig_age.add_vline(
        x=mean_age,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Média = {mean_age:.1f}",
        annotation_position="top"
    )
    fig_age.update_layout(
        xaxis_title="Idade",
        yaxis_title="Número de Clientes",
        template="plotly_white",
        title_font_size=20
    )
    fig_age.update_traces(
        hovertemplate="Idade: %{x}<br>Número de Clientes: %{y}",
        marker_line_width=1,
        marker_line_color="black"
    )
    st.plotly_chart(fig_age, use_container_width=True)

def client_fam_num_bar(df):
    # Gráfico de barras com o número de clientes por tamanho do agregado familiar
    st.subheader("Número de Clientes por Tamanho do Agregado Familiar")

    unique_clients = df.drop_duplicates(subset="client_id")
    
    agg_df = unique_clients["client_household_size"].value_counts().sort_index().reset_index()
    agg_df.columns = ["client_household_size", "count"]

    fig_fam_num = px.bar(
        agg_df,
        x="client_household_size",
        y="count",
        color_discrete_sequence=["#00838F"],
        title=" "
    )
    fig_fam_num.update_layout(
        xaxis_title="Tamanho do Agregado Familiar",
        yaxis_title="Número de Clientes",
        template="plotly_white",
        title_font_size=20
    )
    fig_fam_num.update_traces(
        hovertemplate="Tamanho do Agregado: %{x}<br>Número de Clientes: %{y}",
        marker_line_width=1,
        marker_line_color="black"
    )
    st.plotly_chart(fig_fam_num)

def client_with_kids_or_not_pie(df):
    # Pie Chart com a proporção de clientes com filhos e sem filhos
    st.subheader("Clientes com Filhos vs. sem Filhos")
    
    unique_clients = df.drop_duplicates(subset="client_id")
    
    unique_clients["client_has_kids"] = df["client_has_kids"].map({False: "Não tem filho", True: "Tem filho"})
    names = unique_clients['client_has_kids'].value_counts().index
    values = (unique_clients["client_has_kids"].value_counts()).values
    
    fig = px.pie(
        names=names,
        values=values,
        color_discrete_sequence=["#E0E0E0", "#00838F"],
        title=" "
    )
    fig.update_layout(
        template="plotly_white",
        title_font_size=20
    )
    fig.update_traces(
        hovertemplate="%{label}<br>Número de Clientes: %{value}<br>Percentagem: %{percent}",
        marker_line_width=1,
        marker_line_color="black"
    )

    st.plotly_chart(fig, use_container_width=True)


def client_salary_hist(df):
    # Histograma com a distribuição do salário dos clientes
    st.subheader("Distribuição do Salário dos Clientes")

    unique_clients = df.drop_duplicates(subset="client_id")
    
    fig_sal_hist = px.histogram(
        unique_clients,
        x="client_salary",
        nbins=50,
        color_discrete_sequence=["#00838F"],
        title=" "
    )
    mean_salary = df["client_salary"].mean()
    fig_sal_hist.add_vline(
        x=mean_salary,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Média = {mean_salary:.1f}k",
        annotation_position="top"
    )
    fig_sal_hist.update_layout(
        xaxis_title="Salário",
        yaxis_title="Número de Clientes",
        template="plotly_white",
        title_font_size=20
    )
    fig_sal_hist.update_traces(
        hovertemplate="Salário: %{x}<br>Número de Clientes: %{y}",
        marker_line_width=1,
        marker_line_color="black"
    )
    st.plotly_chart(fig_sal_hist, use_container_width=True)

def client_num_per_city_bar(df):
    # Gráfico de Barras com o número de clientes por cidade
    st.subheader("Número de Clientes por Cidade")
    
    unique_clients = df.drop_duplicates(subset="client_id")
    top_cities = unique_clients["client_city"].value_counts().nlargest(10)

    fig_city_bar = px.bar(
        x=top_cities.index,
        y=top_cities.values,
        color_discrete_sequence=["#00838F"],
        title=" "
    )
    fig_city_bar.update_layout(
        xaxis_title="Cidade",
        yaxis_title="Número de Clientes",
        template="plotly_white",
        title_font_size=20
    )
    fig_city_bar.update_traces(
        hovertemplate="Cidade: %{x}<br>Número de Clientes: %{y}",
        marker_line_width=1,
        marker_line_color="black"
    )
    st.plotly_chart(fig_city_bar, use_container_width=True)

# PADRÕES DE COMPRA

def depart_sales_num_bar(df):
    # Gráfico de Barras com o número de vendas por cada departamento
    st.subheader("Número de Vendas por Departamento")

    # Selectbox para escolher a loja
    lojas = sorted(df["store_id"].astype(str).unique())
    loja_selecionada = st.selectbox("Seleciona uma loja:", ["Todas"] + lojas)

    # Aplicar filtro à loja, se necessário
    if loja_selecionada != "Todas":
        df = df[df["store_id"].astype(str) == loja_selecionada]

    # Contar número de vendas por departamento
    departs_df = df['product_department'].value_counts().sort_values(ascending=False)
    
    # Criar gráfico
    fig_depart = px.bar(
        x=departs_df.index,
        y=departs_df.values,
        text=departs_df.values,
        color_discrete_sequence=["#00838F"],
        title=" "
    )

    fig_depart.update_layout(
        xaxis_title="Departamento",
        yaxis_title="Número de faturas",
        template="plotly_white",
        title_font_size=20
    )

    fig_depart.update_traces(
        hovertemplate="Departamento: %{x}<br>Quantidade: %{y}",
        marker_line_width=1,
        marker_line_color="black"
    )

    st.plotly_chart(fig_depart, use_container_width=True)

def sales_evolution_by_store(df):
    #Gráfico de Linha com a evolução das vendas ao longo do tempo por loja
    st.subheader("Evolução das Vendas ao Longo do Tempo por Loja")

    df['transaction_timestamp'] = pd.to_datetime(df['transaction_timestamp'])

    lojas = sorted(df["store_id"].unique())

    loja_selecionada = st.selectbox("Seleciona uma loja:", ["Todas"] + lojas, index=1)

    if loja_selecionada != "Todas":
        df = df[df["store_id"] == loja_selecionada]

    # Agrupar por dia e loja
    sales_by_day_store = (
        df.groupby([df['transaction_timestamp'].dt.date, 'store_id'])
        .size()
        .reset_index(name='num_sales')
        .rename(columns={'transaction_timestamp': 'date'})
    )

    # Definir cores: se for loja única, usar azul. Se forem todas, deixar o Plotly escolher.
    if loja_selecionada == "Todas":
        color_sequence = px.colors.qualitative.Set2  # várias cores
    else:
        color_sequence = ["#00838F"]  # só uma cor

    fig = px.line(
        sales_by_day_store,
        x='date',
        y='num_sales',
        color='store_id',
        markers=True,
        title=' ',
        color_discrete_sequence=color_sequence
    )

    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Número de Vendas",
        template="plotly_white",
        title_font_size=20
    )

    fig.update_traces(
        hovertemplate="Data: %{x}<br>Loja: %{fullData.name}<br>Vendas: %{y}"
    )

    st.plotly_chart(fig, use_container_width=True)


def top_selling_store(df):
    # Gráfico de Barras com as lojas com mais venda
    st.subheader("Loja com Mais Vendas")

    # Criar cópia auxiliar do DataFrame
    df_aux = df.copy()

    # Converter store_id para string e adicionar prefixo "Loja"
    df_aux["store_id"] = df_aux["store_id"].astype(str)
    df_aux["store_id"] = "Loja " + df_aux["store_id"]

    # Definir ordenação por nome
    ordem_lojas = sorted(df_aux["store_id"].unique(), key=lambda x: int(x.split(" ")[1]))
    df_aux["store_id"] = pd.Categorical(df_aux["store_id"], categories=ordem_lojas, ordered=True)

    # Selectbox de filtro de departamento
    departamentos = sorted(df_aux["product_department"].unique())
    departamento_selecionado = st.selectbox("Seleciona um departamento:", ["Todos"] + departamentos)

    if departamento_selecionado != "Todos":
        df_aux = df_aux[df_aux["product_department"] == departamento_selecionado]

    # Contagem de vendas por loja
    store_sales = (
        df_aux.groupby("store_id")
        .size()
        .reset_index(name="num_sales")
    )

    # Gráfico
    fig = px.bar(
        store_sales,
        x="store_id",
        y="num_sales",
        text="num_sales",
        color_discrete_sequence=["#00838F"],
        labels={"store_id": "Loja", "num_sales": "Número de Vendas"},
        title=" "
    )

    fig.update_layout(
        template="plotly_white",
        title_font_size=20
    )

    fig.update_traces(
        hovertemplate="Loja: %{x}<br>Vendas: %{y}",
        marker_line_width=1,
        marker_line_color="black"
    )

    st.plotly_chart(fig, use_container_width=True)

def product_share_by_category(df):
    # Gráfico de Barras Horizontal com as categorias de vendas por departamento
    st.subheader("Top Categorias de Vendas por Departamento")

    # Criar duas colunas lado a lado
    col1, col2 = st.columns(2)

    # Selectbox para loja na primeira coluna (com opção "Todas")
    with col1:
        lojas = sorted(df["store_id"].unique())
        loja_selecionada = st.selectbox("Seleciona uma loja:", ["Todas"] + lojas)

    # Selectbox para departamento na segunda coluna
    with col2:
        departamentos = sorted(df["product_department"].unique())
        departamento_selecionado = st.selectbox("Seleciona um departamento:", departamentos)

    # Filtrar dados por departamento (e por loja se necessário)
    df_filtrado = df[df["product_department"] == departamento_selecionado]
    if loja_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado["store_id"] == loja_selecionada]

    # Agrupar e contar vendas por categoria
    category_sales = (
        df_filtrado.groupby("product_category")
        .size()
        .reset_index(name="num_sales")
        .sort_values("num_sales", ascending=False)
    )

    # Manter apenas Top 10
    top_n = 10
    top_categories = category_sales.head(top_n).copy()

    # Gráfico de barras horizontal
    fig = px.bar(
        top_categories.sort_values("num_sales", ascending=True),
        x="num_sales",
        y="product_category",
        orientation="h",
        text="num_sales",
        color="product_category",
        color_discrete_sequence=["#00838F"],
        labels={"num_sales": "Número de Vendas", "product_category": "Categoria"},
        title=f"Top {top_n} Categorias de Vendas | {'Todas as Lojas' if loja_selecionada == 'Todas' else f'Loja {loja_selecionada}'} · Departamento '{departamento_selecionado}'"
    )

    fig.update_traces(
        textposition='outside',
        marker_line_color="black",
        marker_line_width=0.5
    )

    fig.update_layout(
        template="plotly_white",
        yaxis=dict(title=""),
        xaxis=dict(title="Número de Vendas"),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

def vendas_boxplot_promocao(df):
    st.subheader("Distribuição Diária das Vendas com e sem Promoções (Loja 1)")

    # Criar cópia auxiliar para preservar df original
    df_aux = df.copy()

    # Garantir tipos corretos
    df_aux["store_id"] = pd.to_numeric(df_aux["store_id"], errors="coerce")
    df_aux["is_promo_day"] = df_aux["is_promo_day"].map({1: True, 0: False, "True": True, "False": False}).astype(bool)
    df_aux["transaction_timestamp"] = pd.to_datetime(df_aux["transaction_timestamp"], errors="coerce")

    # Filtrar Loja 1
    df_loja1 = df_aux[df_aux["store_id"] == 1].copy()
    if df_loja1.empty:
        return  # Não mostra nada se não houver dados

    # Extrair data
    df_loja1["date"] = df_loja1["transaction_timestamp"].dt.date

    # Agrupar por data e tipo de dia
    vendas_diarias = (
        df_loja1.groupby(["date", "is_promo_day"])["sales_value"]
        .sum()
        .reset_index()
    )
    if vendas_diarias.empty:
        return  # Não mostra gráfico se não houver agregações

    # Mapeamento para nomes legíveis
    vendas_diarias["Tipo de Dia"] = vendas_diarias["is_promo_day"].map({
        True: "Com Promoção",
        False: "Sem Promoção"
    })

    # Gráfico boxplot
    fig = px.box(
        vendas_diarias,
        x="Tipo de Dia",
        y="sales_value",
        color="Tipo de Dia",
        title=" ",
        color_discrete_sequence=["#00838F", "#F25C54"],
        points="all"
    )

    fig.update_layout(
        yaxis_title="Vendas Diárias (€)",
        xaxis_title="Tipo de Dia",
        template="plotly_white",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)



def salary_vs_avg_spent(df):
    """
    Scatter plot de Salário vs Preço Médio Gasto por Cliente,
    com marcadores semi-transparentes e linha de tendência opaca.
    """
    st.subheader("Salário vs Preço Médio Gasto por Cliente")

    # 1) Agrupa por cliente
    client_stats = (
        df
        .groupby("client_id")
        .agg(
            client_salary=("client_salary", "first"),
            total_spent=("sales_value", "sum"),
            baskets=("basket_id", "nunique")
        )
        .reset_index()
    )
    client_stats["avg_spent"] = client_stats["total_spent"] / client_stats["baskets"]

    # 2) Scatter com opacidade nos marcadores
    fig = px.scatter(
        client_stats,
        x="client_salary",
        y="avg_spent",
        opacity=0.6,  # marcadores semi-transparentes
        labels={
            "client_salary": "Salário (€k)",
            "avg_spent": "Preço Médio Gasto (€)"
        },
        title=" "
    )
    fig.update_traces(
        hovertemplate="Salário: %{x}k<br>Preço Médio: €%{y:.2f}"
    )

    # 3) Ajuste linear com numpy.polyfit
    x = client_stats["client_salary"].to_numpy()
    y = client_stats["avg_spent"].to_numpy()
    if len(x) > 1:
        m, b = np.polyfit(x, y, 1)
        x_line = np.array([x.min(), x.max()])
        y_line = m * x_line + b
        fig.add_trace(
            go.Scatter(
                x=x_line,
                y=y_line,
                mode="lines",
                line=dict(dash="dash", color="red"),
                opacity=0.8,  # linha de tendência leve transparente
                name="Tendência"
            )
        )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Salário",
        yaxis_title="Preço Médio Gasto por Cesta",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    st.plotly_chart(fig, use_container_width=True)


def produtos_com_mais_cupons(df, top_n: int = 10):
    """
    Mostra os produtos onde se aplicam mais 'cupões',
    usando como proxy qualquer desconto (discount_value > 0),
    e permite filtrar por departamento.
    """
    st.subheader("Top Produtos com Mais Cupões Aplicados")

    # ——— 1) Filtro por departamento ———
    departamentos = sorted(df["product_department"].astype(str).unique())
    departamento_selecionado = st.selectbox("Seleciona um Departamento:", ["Todos"] + departamentos)
    if departamento_selecionado != "Todos":
        df = df[df["product_department"].astype(str) == departamento_selecionado]

    # ——— 2) Detecta coluna de cupões ou usa discount_value ———
    possíveis = [c for c in df.columns if any(x in c.lower() for x in ("coupon", "voucher"))]
    if possíveis:
        cupao_col = possíveis[0]
        df_cupons = df[df[cupao_col].notna()].copy()
    elif "discount_value" in df.columns:
        cupao_col = "discount_value"
        df_cupons = df[df["discount_value"] > 0].copy()
        st.info("ℹ️ A usar `discount_value > 0` como proxy para cupões.")
    else:
        st.error("❌ Não encontrei colunas de cupões nem de desconto no dataset.")
        return

    if df_cupons.empty:
        st.info("ℹ️ Não existem registos com cupões/descontos aplicados para este departamento.")
        return

    # ——— 3) Conta quantas aplicações por categoria de produto ———
    cupons_por_produto = (
        df_cupons
        .groupby("product_category")
        .size()
        .reset_index(name="num_cupons")
    )

    # ——— 4) Junta nomes de produto se existirem ———
    if "product_name" in df_cupons.columns:
        nomes = df_cupons[["product_category", "product_name"]].drop_duplicates()
        cupons_por_produto = cupons_por_produto.merge(nomes, on="product_category", how="left")
        label = "product_name"
    else:
        cupons_por_produto["product_name"] = cupons_por_produto["product_category"].astype(str)
        label = "product_name"

    # ——— 5) Top N e gráfico ———
    top = cupons_por_produto.sort_values("num_cupons", ascending=False).head(top_n)
    fig = px.bar(
        top.sort_values("num_cupons", ascending=True),
        x="num_cupons",
        y=label,
        orientation="h",
        text="num_cupons",
        color_discrete_sequence=["#00838F"],
        labels={"num_cupons": "Número de Cupões", label: "Produto"},
        title=f"Top {top_n} Produtos com Mais Cupões"
    )
    fig.update_traces(textposition="outside", marker_line_color="black", marker_line_width=0.5)
    fig.update_layout(template="plotly_white", xaxis_title="Número de Cupões", yaxis_title="")

    st.plotly_chart(fig, use_container_width=True)