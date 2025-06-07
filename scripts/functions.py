import streamlit as st
import plotly.express as px
import pandas as pd

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

    departs_df = df['product_department'].value_counts().sort_values(ascending=False)

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

    # Obter lista de lojas únicas (ordenadas)
    lojas = sorted(df["store_id"].unique())

    # SelectBox para escolher a loja
    loja_selecionada = st.selectbox("Seleciona uma loja:", ["Todas"] + lojas, index=1)

    # Filtrar o DataFrame consoante a loja selecionada
    if loja_selecionada != "Todas":
        df = df[df["store_id"] == loja_selecionada]
    
    sales_by_day_store = (
        df.groupby([df['transaction_timestamp'].dt.date, 'store_id'])
        .size()
        .reset_index(name='num_sales')
    )

    fig = px.line(
        sales_by_day_store,
        x='transaction_timestamp',
        y='num_sales',
        color='store_id',
        markers=True,
        title=' ',
        color_discrete_sequence=px.colors.qualitative.Plotly
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

def top_product_categories(df):
#Gráfico de barras com as categorias de produto mais vendidas
    st.subheader("Top Categorias de Produto Mais Vendidas")

    # Obter listas únicas e ordenadas
    lojas = sorted(df["store_id"].unique())
    departamentos = sorted(df["product_department"].unique())

    # SelectBoxes para filtrar
    col1, col2 = st.columns(2)
    with col1:
        loja_selecionada = st.selectbox("Seleciona uma loja:", ["Todas"] + lojas)
    with col2:
        departamento_selecionado = st.selectbox("Seleciona um departamento:", ["Todos"] + departamentos, index=3)

    # Aplicar filtros
    if loja_selecionada != "Todas":
        df = df[df["store_id"] == loja_selecionada]

    if departamento_selecionado != "Todos":
        df = df[df["product_department"] == departamento_selecionado]
    
    category_sales = (
        df.groupby(['product_department', 'product_category'])
        .size()
        .reset_index(name='num_sales')
        .sort_values('num_sales', ascending=False)
    )

    fig = px.bar(
        category_sales,
        x='product_category',
        y='num_sales',
        color='product_department',
        title=' ',
        labels={'num_sales': 'Número de Vendas', 'product_category': 'Categoria'},
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)


def top_selling_store(df):
#Gráfico de Barras com as lojas com mais venda
    st.subheader("Loja com Mais Vendas")

    # Converter store_id para string e adicionar prefixo "Loja"
    df["store_id"] = df["store_id"].astype(str)
    df["store_id"] = "Loja " + df["store_id"]

    # Definir ordenação por nome
    ordem_lojas = sorted(df["store_id"].unique(), key=lambda x: int(x.split(" ")[1]))  # Loja 1, Loja 2, Loja 3
    df["store_id"] = pd.Categorical(df["store_id"], categories=ordem_lojas, ordered=True)

    # Selectbox de filtro de departamento
    departamentos = sorted(df["product_department"].unique())
    departamento_selecionado = st.selectbox("Seleciona um departamento:", ["Todos"] + departamentos)

    if departamento_selecionado != "Todos":
        df = df[df["product_department"] == departamento_selecionado]

    # Contagem de vendas por loja (sem reordenar)
    store_sales = (
        df.groupby("store_id")
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
    st.subheader("Top Categorias de Vendas por Departamento")

    # Selectbox para escolher o departamento
    departamentos = sorted(df["product_department"].unique())
    departamento_selecionado = st.selectbox("Seleciona um departamento:", departamentos)

    # Filtrar dados
    df_filtrado = df[df["product_department"] == departamento_selecionado]

    # Agrupar e contar vendas por categoria
    category_sales = (
        df_filtrado.groupby("product_category")
        .size()
        .reset_index(name="num_sales")
        .sort_values("num_sales", ascending=False)
    )

    # Manter apenas Top 10 (ou ajustar para outro valor)
    top_n = 10
    outros_total = category_sales["num_sales"][top_n:].sum()

    top_categories = category_sales.head(top_n).copy()

    # Gráfico de barras horizontal
    fig = px.bar(
        top_categories.sort_values("num_sales", ascending=True),  # ordem crescente para eixo Y
        x="num_sales",
        y="product_category",
        orientation="h",
        text="num_sales",
        color="product_category",
        color_discrete_sequence=px.colors.qualitative.Set3,
        labels={"num_sales": "Número de Vendas", "product_category": "Categoria"},
        title=f"Top {top_n} Categorias de Vendas no Departamento '{departamento_selecionado}'"
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

    # Garantir que estamos a trabalhar com a loja 1 (numérico)
    df_loja1 = df[df["store_id"] == 1].copy()

    # Extrair apenas a data (sem horas) do timestamp
    df_loja1["date"] = pd.to_datetime(df_loja1["transaction_timestamp"]).dt.date

    # Agrupar por data e se é promo ou não
    vendas_diarias = (
        df_loja1.groupby(["date", "is_promo_day"])["sales_value"]
        .sum()
        .reset_index()
    )

    # Mapear valores booleanos para nomes legíveis
    vendas_diarias["Tipo de Dia"] = vendas_diarias["is_promo_day"].map({
        True: "Com Promoção",
        False: "Sem Promoção"
    })

    fig = px.box(
        vendas_diarias,
        x="Tipo de Dia",
        y="sales_value",
        color="Tipo de Dia",
        title="Distribuição Diária das Vendas - Loja 1",
        color_discrete_sequence=["#00838F", "#F25C54"],
        points="all"  # mostra os pontos individuais
    )

    fig.update_layout(
        yaxis_title="Vendas Diárias (€)",
        xaxis_title="Tipo de Dia",
        template="plotly_white",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
