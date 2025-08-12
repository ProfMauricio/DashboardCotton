import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.colors import ListedColormap
import numpy as np
from dados_fazenda import DadosFazenda

import folium
from streamlit_folium import st_folium
import geopandas as gpd

# ======================================================================================================================
# ======================================================================================================================

def espacar_linhas( col1, col2, col3, linhas:int = 2 ):
    for i in range(linhas):
        col1.text("\n")
        col2.text("\n")
        col3.text("\n")


# ======================================================================================================================
# ======================================================================================================================

def numft(x, pos):
    s = f'{x / 1000:,.0f}'
    return s

# ======================================================================================================================
# ======================================================================================================================

@st.cache_resource
def obter_maps():
    df_shp =  gpd.read_file('./Shapefile-Grid/grid.shp')
    return df_shp.to_json()

# ======================================================================================================================
# ======================================================================================================================


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

# ======================================================================================================================
# ======================================================================================================================


# ======================================================================================================================
# ======================================================================================================================


def obter_dados_gli() -> pd.DataFrame:
    """
    Função para obter os dados de GLI
    :return: Retorna um dataframe com os dados de GLI
    """

# ======================================================================================================================
# ======================================================================================================================

def dividir_coluna():
    st.markdown(
        """
        <style>
        .st-emotion-cache-1c5c404 { /* Target Streamlit's column container class */
            border-right: 1px solid #ccc; /* Add a right border to columns */
            padding-right: 20px; /* Add some padding for spacing */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def dividir_linha(col1, col2, col3):
    col1.divider()
    col2.divider()
    col3.divider()

# ======================================================================================================================
# ======================================================================================================================


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
        if i < 2 :
            resposta = True
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

    # lendo shapefile de grids
    shape_file_name = r'./Shapefile-Grid/grid.shp'
    shape_file = gpd.read_file(shape_file_name)
    # alterando dados para mesclagem com mapas
    dados_voo = dados_gestao_agro.rename(columns={'bloco': 'FID'})
    dados_shape_mesclados = shape_file.merge(dados_voo, on='FID', how='inner')

    # proporção entre as colunas do dashboard
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1],  gap="medium",vertical_alignment="top")

    indice_filtro_ndvi={'Etapa 1': 0.1,
                        'Etapa 2': 0.6,
                        'Etapa 3': 0.6,
                        'voo4': 0.6}
    dados_gestao_agro['ndvi_cores'] = dados_gestao_agro['ndvi'].map(lambda x: 'red' if x < indice_filtro_ndvi[etapa_selecionada] else 'green')

    ## altura dos gráficos
    alturaPadrao = 530

    # ==================================================================================================================
    # TRATANDO DADOS DE NDVI
    # ==================================================================================================================
    fig_ndvi_shp, ax_ndvi_shp = plt.subplots(1, 1, figsize=(10, 10))
    dados_shape_mesclados.plot(ax=ax_ndvi_shp,
                               column='gli',
                               cmap='RdYlGn',
                               legend=True,
                               legend_kwds={'label': 'Valores de GLI', 'orientation': 'vertical'},
                               linewidth=0.9,
                               edgecolor='gray',
                               vmin=0,
                               vmax=1,
                               )

    #ax_ndvi_shp.set_title(label=f"NDVI na {etapa_selecionada} ")

    # gráficos de barras de NDVI
    fig_ndvi = px.bar(dados_gestao_agro, y='ndvi', x="bloco", height=alturaPadrao,
                      color='ndvi_cores', color_discrete_map="identity",
                      labels={'bloco':'Bloco', 'ndvi':'Valor médio de NVDI por bloco'},
                      #title=f"Valores médios de NDVI por bloco no voo ({etapa_selecionada})",
                      range_y=[0,1],
                      )


    # setor de exibição de gráficos da primeira coluna (NDVI)
    col1.text(f"NVDI por bloco - {etapa_selecionada}")
    col1.pyplot(fig_ndvi_shp, use_container_width=True)
    col1.plotly_chart(fig_ndvi) #,use_container_width=True)
    col1.write(dados_gestao_agro[['bloco','ndvi']], unsafe_allow_html=True)
    # dividir_linha(col1,col2,col3)
    dividir_coluna()

    # dando espaço entre as linhas
    #espacar_linhas(col1,col2,col3, linhas=3)


    # ==================================================================================================================
    # TRATANDO DADOS DE GLI
    # ==================================================================================================================

    #df_ndvi_filtro =

    # gráficos de GLI

    fig_gli = px.bar(dados_gestao_agro, y='gli', x="bloco", height=alturaPadrao,
                     labels={'bloco': 'Bloco', 'gli': 'Valor médio de GLI por bloco'},
                     text_auto=True,
                     #title=f"Valores médios de GLI por bloco na \netapa ({etapa_selecionada})",
                     range_y=[0, 1],
                     )

    fig_gli.update_xaxes(
        type="category",
    )


    # ajustando exibição do mapa com dados de GLI
    custom_colors = ['red', 'orange', 'yellow', 'blue', 'green']
    custom_cmap = ListedColormap(custom_colors)
    fig_gli_shp, ax_gli = plt.subplots(1, 1, figsize=(10, 10))
    dados_shape_mesclados.plot(ax=ax_gli,
                               column='gli',
                               cmap='RdYlGn', #cmap=custom_cmap,
                               legend=True,
                               legend_kwds={'label': 'Valores de GLI', 'orientation': 'vertical'},
                               linewidth=0.9,
                               edgecolor='gray',
                               vmin=0,
                               vmax=1
                               )
    #ax_gli.set_title(label=f"GLI na {etapa_selecionada} ")

    #col1, col2, col3 = st.columns([4, 4, 2])


    col2.text(f"GLI por bloco - {etapa_selecionada}")
    #col2.text("")
    col2.pyplot(fig_gli_shp,use_container_width=True)
    col2.plotly_chart(fig_gli,use_container_width=True)
    col2.write(dados_gestao_agro[['bloco', 'gli']])

    # alinhar gráficos
    #dividir_linha(col1, col2, col3)
    # dando espaço entre as linhas
    #espacar_linhas(col1,col2,col3, linhas=3)

    # ==================================================================================================================
    # TRATANDO DADOS DE SAVI
    # ==================================================================================================================

    # gráficos de SAVI
    fig_savi_shp, ax_savi = plt.subplots(1, 1, figsize=(10, 10))
    dados_shape_mesclados.plot(ax=ax_savi,
                               column='savi',
                               cmap='RdYlGn',
                               legend=True,
                               legend_kwds={'label': 'Valores de SAVI', 'orientation': 'vertical'},
                               linewidth=0.9,
                               edgecolor='gray',
                               vmin=0,
                               vmax=1,
                               )
    #ax_savi.set_title(label=f"SAVI na {etapa_selecionada} ")

    fig_savi = px.bar(dados_gestao_agro,
                      y='savi',
                      x="bloco",
                      height=alturaPadrao,
                      labels={'bloco': 'Bloco', 'savi': 'Valor médio de SAVI por bloco'},
                      #title=f"Valores médios de SAVI por bloco no voo ({etapa_selecionada})",
                      range_y=[0,1],)

    col3.text(f"Índice SAVI por bloco - {etapa_selecionada}")
    col3.pyplot(fig_savi_shp,use_container_width=True)
    col3.plotly_chart(fig_savi,use_container_width=True)
    col3.write(dados_gestao_agro[['bloco', 'savi']])

    # alinhar gráficos
    #dividir_linha(col1, col2, col3)
    # dando espaço entre as linhas
    #espacar_linhas(col1,col2,col3, linhas=3)

    # ==================================================================================================================
    # TRATANDO DADOS DE STATUS TERM
    # ==================================================================================================================



    # graficos de Termal/Produtividade
    #fig_status_termal = px.bar(dados_gestao_agro, y='status_term', x="bloco",
    #                           labels={'bloco': 'Bloco', 'status_term': 'Valor  médios de taxa de ocupação por bloco'},
    #                           title=f"Valores de status termal por bloco na etapa ({etapa_selecionada})",
    #                           color_discrete_map={
    #                               "baixa": "red",
    #                               "media": "orange",
    #                               "alta": "green",
    #                               },)

    dados_gestao_agro_termal = dados_gestao_agro
    # transformando categoria para valor
    dados_gestao_agro_termal.loc[dados_gestao_agro_termal['status_term'] == 'baixa', 'status_term_valor'] = 10
    dados_gestao_agro_termal.loc[dados_gestao_agro_termal['status_term'] == 'media', 'status_term_valor'] = 20
    dados_gestao_agro_termal.loc[dados_gestao_agro_termal['status_term'] == 'alta', 'status_term_valor'] = 30




    #st.write(dados_gestao_agro_termal)

    tipos_status_term = dados_gestao_agro_termal['status_term'].value_counts()
    tipos_status_term = tipos_status_term.reset_index()
    # colocando cores nas estatisticas
    #tipos_status_term['cores_status_term'] = tipos_status_term['status_term'].apply(lambda x: 'green' if x == 'baixa'  else 'yellow' if x == 'media' else 'red')

    custom_colors_termal = []

    if tipos_status_term['status_term'].value_counts().get('baixa', 0) > 0:
        custom_colors_termal.append('green')

    if tipos_status_term['status_term'].value_counts().get('media', 0) > 0:
        custom_colors_termal.append('yellow')

    if tipos_status_term['status_term'].value_counts().get('alta', 0) > 0:
        custom_colors_termal.append('red')

    custom_cmap_termal = ListedColormap(custom_colors_termal)



    #fig_status_termal = px.pie(dados_gestao_agro_termal, values='status_term_valor',
    #                           names='status_term',
    #                           title=f"Valores de status termal por bloco na etapa ({etapa_selecionada})",
    #                           )

    fig_status_termal = px.bar(tipos_status_term,
                               x='status_term',
                               y='count',
                               color='status_term',
                               color_discrete_sequence=custom_colors_termal)
    #

    fig_status_term_shp, ax_status_term = plt.subplots(1, 1, figsize=(10, 10))
    dados_shape_mesclados.plot(ax=ax_status_term,
                               column='status_term',
                               cmap=custom_cmap_termal,
                               legend=True,
                               #legend_kwds={'label': 'Valores de status termal', 'orientation': 'vertical'},
                               linewidth=0.9,
                               edgecolor='gray',)

    #ax_status_term.set_title(label=f"Status termal na {etapa_selecionada} ")
    col4.text(f"Status termal por bloco - {etapa_selecionada}")
    col4.pyplot(fig_status_term_shp, use_container_width=True)
    col4.plotly_chart(fig_status_termal, use_container_width=True)
    col4.write(tipos_status_term)

    #camada_adicionada = obter_maps()


    #with st.form(key='mymap'):
    #    m = folium.Map(location=camada_adicionada, zoom_start=12)
    #    folium.GeoJson(camada_adicionada, name="Minha camada", style_function=lambda feature: {"fillColor": "yellow", "color": "black", "weight": 0.5, "fillOpacity": 0.4}).add_to(m)
    #    st_folium(m, height=800, width=800, use_container_width=True, key='Map')
    #'''



