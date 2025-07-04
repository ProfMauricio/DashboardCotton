import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar o layout da página
st.set_page_config(layout="wide")

# Carregar os dados do arquivo "vendas.csv" (certifique-se de que o arquivo está no mesmo diretório)
df = pd.read_csv("dados.csv", sep=";", decimal=",")
df_vendas = pd.read_csv("compras.csv", sep=",", encoding="utf-8")

# Converter a coluna "Date" para o formato de data
df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
df = df.sort_values("Data")




# Converter a coluna "Date" para o formato de data
df_vendas["data_compra"] = pd.to_datetime(df_vendas["data_compra"])
df_vendas = df_vendas.sort_values("data_compra")

# Criar uma nova coluna "Month" que contém o ano e o mês
df["Month"] = df["Data"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Criar uma seleção de meses na barra lateral do dashboard
month = st.sidebar.selectbox("Mês", df["Month"].unique())
df_filtered = df[df["Month"] == month]

# Criar uma seleção dos tipos de compras
tipos = st.sidebar.multiselect("Tipos", df_vendas['tipo'].unique())
df_vendas_filtrado = df_vendas[df_vendas['tipo'].isin(tipos)]

col1, col2 = st.columns(2) # Primeira linha com duas colunas
col3, col4 = st.columns(2) # Segunda linha com três colunas

# Criar o gráfico de faturamento por dia
fig_date = px.bar(df_filtered, x="Data", y="Valores", color="Produto", title="Faturamento por dia")

# Exibir o gráfico na primeira coluna
col1.plotly_chart(fig_date, use_container_width=True)

# Criar o gráfico de faturamento por tipo de produto
fig_prod = px.bar(df_filtered, x="Data", y="Tipo de Produto",
                  color="Produto", title="Faturamento por tipo de produto",
                  orientation="h")

# Exibir o gráfico na segunda coluna
col2.plotly_chart(fig_prod, use_container_width=True)

# Exibir o DataFrame
st.write(df_filtered)


# Criar o gráfico de pizza para exibir o faturamento por tipo de pagamento
fig_kind = px.pie(df_vendas_filtrado, values="valor", names="tipo",
                   title="Compras por tipo de pagamento")

# Exibir o gráfico na quarta coluna
col3.plotly_chart(fig_kind, use_container_width=True)


