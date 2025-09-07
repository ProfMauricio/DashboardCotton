import streamlit as st
#import pandas as pd
import plotly.express as px
from leitura_planilhas import *


if __name__ == '__main__':
    # dados originais 
    #dados_fazenda, dados_talhoes = ler_dados_fazenda('./dadosPlanilha/planilha_saida.xlsx')
    info_fazenda, local_custo_geral, local_custo_hectare, talhoes_custo_geral = carregar_dados_custo(pasta_destino='./dadosPlanilha')

    ################
    # Manipulação dos dashboards
    #################
    # Configurar o layout da página
    st.set_page_config(layout="wide")
    st.image('./logo_embrapa.png', width=200)
    st.subheader(f'Custo de produção - Fazenda {info_fazenda["NomeFazenda"]}')


    #col1, col2  = st.columns([7,3])

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











