import streamlit as st
import pandas as pd
import plotly.express as px

from dados_fazenda import DadosFazenda

import folium
from streamlit_folium import st_folium
import geopandas as gpd


@st.cache_resource
def obter_maps():
    df_shp =  gpd.read_file('./Shapefile-Grid/grid.shp')
    return df_shp.to_json()


def obter_dados_voos( dados : dict) -> list :
    """
    rotina que lê uma planilha
    :param dados: estrutura com as fases, nomes dos arquivos e dados
    :return:
    """
    global dados_agricolas_voos
    for i, nome_arq in enumerate(dados['nomes_arquivos']):
        if dados['status'][i] == True:
            dados_voo = pd.read_csv(nome_arq)
            id_voo = f'Etapa {i + 1}'
            temp_dict = {id_voo: dados_voo}
            dados_agricolas_voos.append(dados_voo)
    return dados_agricolas_voos

# =========================================================================================================

def obter_dados_ndvi() -> pd.DataFrame:
    """
    Função para obter os dados de NDVI
    :return: Retorna um dataframe com os dados de NDVI
    """



def obter_dados_gli() -> pd.DataFrame:
    """
    Função para obter os dados de GLI
    :return: Retorna um dataframe com os dados de GLI
    """

if __name__ == '__main__':
    # carregando os dados da base (planilhas)
    dados_agricolas_voos = []
    dados_fazenda = {
        'etapas' : ['Etapa 1', 'Etapa 2', 'Etapa 3'],
        'etapas_voos': ['etapa1', 'etapa2', 'etapa3'],
        'nomes_arquivos': ['./dadosPlanilha/voos/relatorio_manejo_agricola_etapa1.csv',
                  './dadosPlanilha/voos/relatorio_manejo_agricola_etapa2.csv',
                  './dadosPlanilha/voos/relatorio_manejo_agricola_etapa3.csv'],
        'status': [False, False, False],
    }

    # carregando os arquivos na memoria
    leitura_dados = DadosFazenda()
    # buscando os arquivos
    for i,etapa in enumerate(dados_fazenda['etapas_voos']):
        resposta = leitura_dados.obter_voo(etapa, dados_fazenda['nomes_arquivos'][i])
        dados_fazenda['status'][i] = resposta
        if resposta :
            print('Voo obtido com sucesso')

    dados_agricolas_voos = obter_dados_voos(dados_fazenda)
    lista_filtro_etapas = [dados_fazenda['etapas'][i] for i in range(len(dados_fazenda['etapas'])) if dados_fazenda['status'][i] ]

    # ajustando o site para  gestão agrícola
    st.set_page_config(layout="wide")
    st.title("Gestão agrícola e recomendações para suporte a decisão")
    # filtro dos voos realizados
    etapa_selecionada = st.sidebar.selectbox("Dados de qual etapa",
                                             lista_filtro_etapas)

    lista_etapa_indice = {f'Etapa{i+1}':i for i in range(len(dados_fazenda['etapas']))}

    # obtendo os dados do voo selecionado
    dados_gestao_agro =  dados_agricolas_voos[dados_fazenda['etapas'].index(etapa_selecionada)]

    indice_filtro_ndvi={'Etapa 1': 0.1,
                        'Etapa 2': 0.6,
                        'Etapa 3': 0.6,
                        'voo4': 0.6}
    dados_gestao_agro['ndvi_cores'] = dados_gestao_agro['ndvi'].map(lambda x: 'red' if x < indice_filtro_ndvi[etapa_selecionada] else 'green')
    # gráficos de NDVI
    fig_ndvi  = px.bar(dados_gestao_agro, y='ndvi', x="bloco",
                       color='ndvi_cores', color_discrete_map="identity",
                       labels={'bloco':'Bloco', 'ndvi_avg':'Valor médio de NVDI por bloco'},
                       title=f"Valores médios de NDVI por bloco no voo ({etapa_selecionada})")

    col1, col2, col3 = st.columns([4, 1, 1])
    col1.plotly_chart(fig_ndvi)

    #df_ndvi_filtro =

    # gráficos de GLI
    fig_gli = px.bar(dados_gestao_agro, y='gli', x="bloco",
                     labels={'bloco': 'Bloco', 'gli': 'Valor médio de GLI por bloco'},
                     text_auto=True,
                     title=f"Valores médios de GLI por bloco no voo ({etapa_selecionada})")

    fig_gli.update_xaxes(
        type="category",
    )

    col1, col2, col3 = st.columns([4, 1, 1])
    col1.plotly_chart(fig_gli)


    # gráficos de SAVI
    fig_savi = px.bar(dados_gestao_agro, y='savi', x="bloco",
                      labels={'bloco': 'Bloco', 'savi': 'Valor médio de SAVI por bloco'},
                      title=f"Valores médios de SAVI por bloco no voo ({etapa_selecionada})")


    col1.plotly_chart(fig_savi)


    # graficos de Termal/Produtividade
    fig_tx_ocupacao = px.bar(dados_gestao_agro, y='tx_ocupacao', x="bloco",
                      labels={'bloco': 'Bloco', 'tx_ocupacao': 'Valor  médios de taxa de ocupação por bloco'},
                      title=f"Valores médios de taxa de ocupação por bloco no voo ({etapa_selecionada})")

    col1.plotly_chart(fig_tx_ocupacao)

    camada_adicionada = obter_maps()

    with st.form(key='mymap'):
        m = folium.Map(location=camada_adicionada, zoom_start=12)
        folium.GeoJson(camada_adicionada, name="Minha camada", style_function=lambda feature: {"fillColor": "yellow", "color": "black", "weight": 0.5, "fillOpacity": 0.4}).add_to(m)
        st_folium(m, height=800, width=800, use_container_width=True, key='Map')
        m












