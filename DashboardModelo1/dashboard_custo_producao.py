

import streamlit as st
import pandas as pd
import plotly.express as px
#from leitura_planilhas import *
from sqlalchemy import create_engine



import locale

df_fazenda = None
df_custo = None
df_custo_por_talhao_guarda_chuva =None
df_detalhes_custo_producao = None
df_custos_producao = None
df_talhoes = None


# =====================================================================================================================
# =====================================================================================================================

#@st.cache_data()
def load_data_from_db():
    # carregando os dados de gestão agricola

    DB_USER = st.secrets["database"]['user']
    DB_PASSWORD = st.secrets["database"]['pass']
    DB_HOST = st.secrets["database"]['host']
    DB_PORT = st.secrets["database"]['port']
    DB_DATABASE = st.secrets["database"]['database']

    url_conexao = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
    db_schema = "dashboard"
    connect_args = {'options': f'-c search_path={db_schema}'}
    engine = create_engine(url_conexao, connect_args=connect_args)
    sessao = engine.connect()
    # dados de sensoriamento do solo
    rdf_fazenda = pd.read_sql_query("select * from dashboard.fazendas where nome like 'São José'", sessao)
    id = rdf_fazenda.iloc[0]['id']
    rdf_custo_producao_guarda_chuva = pd.read_sql_query("select * from dashboard.v_gestao_guarda_chuva_fazenda", sessao)
    rdf_custo_por_talhao_guarda_chuva = pd.read_sql_query("select * from dashboard.v_gestao_guarda_chuva_por_talhao", sessao)
    rdf_detalhes_custo_producao = pd.read_sql_query("select * from dashboard.detalhes_tipos_custos_producao", sessao)
    rdf_custos_producao = pd.read_sql_query("select * from dashboard.tipos_custos_producao", sessao)
    rdf_talhoes = pd.read_sql_query("select * from dashboard.talhoes ", sessao)
    rdf_tipos_despesas_guarda_chuva = pd.read_sql_query("select * from dashboard.tipos_despesas_guarda_chuva", sessao)
    sessao.close()
    engine.dispose()
    return rdf_fazenda, rdf_custo_producao_guarda_chuva, rdf_custo_por_talhao_guarda_chuva, rdf_detalhes_custo_producao, rdf_custos_producao, rdf_talhoes, rdf_tipos_despesas_guarda_chuva



def ajuste_moeda(valor):
    return f'{locale.currency(valor, grouping=True, symbol=True)}'

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    # dados originais
    (df_fazenda,
     df_custo_producao_guarda_chuva,
     df_custo_por_talhao_guarda_chuva,
     df_detalhes_custo_producao,
     df_custos_producao, df_talhoes, df_tipos_despesas_guarda_chuva) = load_data_from_db()
    #dados_fazenda, dados_talhoes = ler_dados_fazenda('./dadosPlanilha/planilha_saida.xlsx')
    #info_fazenda, local_custo_geral, local_custo_hectare, talhoes_custo_geral = carregar_dados_custo(pasta_destino='./dadosPlanilha')

    ################
    # Manipulação dos dashboards
    #################
    # Configurar o layout da página
    st.set_page_config(layout="wide")
    st.image('./logo_embrapa.png', width=200)
    dados = df_fazenda.iloc[0]
    talhao_selecionado = st.sidebar.selectbox(f"Talhões da fazenda {dados['nome']}", df_talhoes['nome'].unique())

    # Trecho de análise e preparação de dataframes e análises

    ### Etapa das coluna 1
    valores_somados_por_tipo_custo = df_custo_producao_guarda_chuva.groupby('Tipo_Custo')['valor'].sum()
    # formatando dados para apresentação
    df_valores_somados_por_tipo_custo = pd.DataFrame(valores_somados_por_tipo_custo)
    styled_df_valores_somados_por_tipo_custo = df_valores_somados_por_tipo_custo.style.format(ajuste_moeda)
    styled_df_valores_somados_por_tipo_custo = styled_df_valores_somados_por_tipo_custo.set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'left')]}]
    )

    fig_guarda_chuva_geral = px.bar(valores_somados_por_tipo_custo,
                                    labels={'Tipo_Custo': 'Despesas', 'value': 'Valores em R$'},
                                    title="Custos gerais de produção")


    st.subheader(f'Fazenda {dados["nome"]} -- Custo de produção ')

    ### Etapa das coluna 2

    df_custo_talhao = df_custo_por_talhao_guarda_chuva[
        df_custo_por_talhao_guarda_chuva['nome_talhao'] == talhao_selecionado]
    valores_somados_por_tipo_custo_por_talhao = df_custo_talhao.groupby('tipo_despesa')['valor'].sum()
    fig_guarda_chuva_geral_por_talhao = px.bar(valores_somados_por_tipo_custo_por_talhao,
                                               labels={'Tipo_Custo': 'Despesas', 'value': 'Valores em R$'},
                                               title=f"Custos gerais de produção no {talhao_selecionado}")

    # formatando dados para apresentação
    df_valores_somados_por_tipo_custo_por_talhao = pd.DataFrame(valores_somados_por_tipo_custo_por_talhao)
    styled_df_valores_somados_por_tipo_custo_por_talhao = df_valores_somados_por_tipo_custo_por_talhao.style.format(
        ajuste_moeda)
    styled_df_valores_somados_por_tipo_custo_por_talhao = styled_df_valores_somados_por_tipo_custo_por_talhao.set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'left')]}])


    ################################
    ##  INICIANDO APRESENTAÇÃO DE GRÁFICOS
    st.metric(label="Soma de custos gerais", value=locale.currency(valores_somados_por_tipo_custo.sum(),symbol=True,
                                                                   grouping=True),
              delta=None,
              delta_color="normal")

    st.divider()

    col1, col2  = st.columns([6,6])

    col1.subheader("Custo geral por tipo de despesa")
    col1.plotly_chart(fig_guarda_chuva_geral)

    col1.divider()
    col1.write(styled_df_valores_somados_por_tipo_custo, use_container_width=True)
    col1.divider()

    ### tratando os dados de custo por hectare
    col2.subheader("Custos gerais por tipo de despesa por talhão")
    col2.plotly_chart(fig_guarda_chuva_geral_por_talhao)
    col2.divider()
    #st.subheader("Gráficos e estatísticas de Custos por hectare")
    col2.write(styled_df_valores_somados_por_tipo_custo_por_talhao)
    col2.divider()
    st.divider()
    col1.subheader("Detalhes dos custos por hectare")
    col2.subheader('Detalhamentos dos custos')
    detalhes_tipos_despesas_guarda_chuva = col1.selectbox("Tipo de Despesa Guarda Chuva", df_tipos_despesas_guarda_chuva.nome.unique())
    detalhes_tipos_despesas_producao = col2.selectbox("Tipo de Despesa de Custo de Produção", df_custos_producao.nome.unique())
    # filtrando os dados de cada tipo
    df_filtro_despesas_guarda_chuva = df_custo_producao_guarda_chuva[df_custo_producao_guarda_chuva['Tipo_Custo'] == detalhes_tipos_despesas_guarda_chuva]
    df_filtro_despesas_producao_por_talhao = df_custo_por_talhao_guarda_chuva[df_custo_por_talhao_guarda_chuva['tipo_despesa'] == detalhes_tipos_despesas_producao]
    df_filtro_despesas_producao_por_talhao = df_filtro_despesas_producao_por_talhao[df_custo_por_talhao_guarda_chuva['nome_talhao'] == talhao_selecionado]

    col1.write(detalhes_tipos_despesas_guarda_chuva)
    temp1 = pd.DataFrame(df_filtro_despesas_guarda_chuva[['Id', 'Detalhe_Custo', 'valor']])
    styled_df_temp1 = temp1.style.format(ajuste_moeda, subset=['valor'])
    styled_df_temp1 = styled_df_temp1.set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'left')]}]
    )


    temp2 = pd.DataFrame(df_filtro_despesas_producao_por_talhao[['id', 'detalhe_tipo_despesa', 'valor']] )
    st.write(temp2)
    styled_df_temp2 = temp2.style.format(ajuste_moeda, subset=['valor'])
    styled_df_temp2 = styled_df_temp2.set_table_styles( [{'selector': 'th', 'props': [('text-align', 'left')]}] )

    col1.write(styled_df_temp1, use_container_width=True)
    col2.write(styled_df_temp2,use_container_width=True)






def comentarios():
    # organizando os dados de custo geral num dataframe para exibir
    dict_custo = { 'Nomes': [ dado['item'] for dado in local_custo_geral ],
                   'Valores': [ dado['total'] for dado in local_custo_geral ],
                 }
    df_custogeral = pd.DataFrame.from_dict(dict_custo)
    fig_guarda_chuva_geral  = px.bar(df_custogeral, y='Valores', x="Nomes",
                                     labels={'Nomes':'Despesas', 'Valores':'Valores em R$'},
                                     title="Custos gerais de produção")
    st.plotly_chart(fig_guarda_chuva_geral)
    st.subheader("Custo geral por tipo de despesa")
    st.write(df_custogeral, use_container_width=True)

    ### tratando os dados de custo por hectare
    st.divider()

    st.subheader("Gráficos e estatísticas de Custos por hectare")


    #    #plot_bgcolor='white',x
    #    # paper_bgcolor='white',
    #    legend_title_text='Tipos de Custos'
    #)


    # gerando os custos por hectare
    dict_custos_por_hectare = { 'Nomes':  [ dado['item'] for dado in local_custo_hectare ],
                                'Valores': [ dado['total'] for dado in local_custo_hectare ],
                 }
    df_custos_por_hectare = pd.DataFrame.from_dict(dict_custos_por_hectare)

    fig_guarda_chuva_custos_hectare = px.bar(df_custos_por_hectare, y='Valores', x="Nomes",
                                            labels={'Nomes':'Despesas', 'Valores':'Valores em R$ por cada ha'},
                                            title="Custos de produção por hectare")

    st.plotly_chart(fig_guarda_chuva_custos_hectare)
    st.write(df_custos_por_hectare)
    st.divider()
    st.subheader("Detalhes dos custos por hectare")
    custo_selectionado = st.selectbox("Tipos de custos", dict_custo['Nomes'])
    # organiza um dataframe com os dados do tipo de custo selecionado
    lista = []
    for elem in local_custo_hectare:
        if elem['item'] == custo_selectionado:
            for x in elem['subitens']:
                lista.append(x)
            break
    dict_filtro_custo_detalhado = {'Nomes': [dado['Nome'] for dado in lista],
                               'Valores': [dado['Valor'] for dado in lista],
                               }

    df_filtro_custo_detalhado = pd.DataFrame.from_dict(dict_filtro_custo_detalhado)

    # st.subheader("Valores R$ por Hectare")
    fig_detalhe_custos_hectare = px.bar(dict_filtro_custo_detalhado, y='Valores', x="Nomes",)
    st.write(df_filtro_custo_detalhado)
    st.plotly_chart(fig_detalhe_custos_hectare, use_container_width=True)











