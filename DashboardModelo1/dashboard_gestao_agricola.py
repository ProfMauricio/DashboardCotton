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
    df_shp =  gpd.read_file('./Shapefile-Grid/grid_zoom.shp')
    df_shp =  gpd.read_file('./Shapefile-Grid/grid_zoom.shp')
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
    flag_leitura_dados_remoto = False
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
    if not flag_leitura_dados_remoto:
        leitura_dados = DadosFazenda()
        flag_leitura_dados_remoto = True
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
    col1, col2, col3, col4 = st.columns([1.15, 1.15, 1.15, 1],  gap="medium",vertical_alignment="top")

    indice_filtro_ndvi={'Etapa 1': 0.1,
                        'Etapa 2': 0.6,
                        'Etapa 3': 0.6,
                        'voo4': 0.6}
   

    ## altura dos gráficos
    alturaPadrao = 530

    # ==================================================================================================================
    # ==================================================================================================================
    #  SETOR DE MAPAS SHP
    # ==================================================================================================================
    # ==================================================================================================================

    # ========================
    # TRATANDO DADOS DE NDVI (coluna 1)
    # ========================

    # Criando gráfico do map de grid da primeira linha
    fig_ndvi_shp, ax_ndvi_shp = plt.subplots(1, 1, figsize=(10, 10))
    dados_shape_mesclados.plot(ax=ax_ndvi_shp,
                               column='ndvi',
                               cmap='RdYlGn',
                               legend=True,
                               legend_kwds={'label': 'Valores de GLI', 'orientation': 'vertical'},
                               linewidth=1,
                               edgecolor='lightgray',
                               vmin=0,
                               vmax=1,
                               )
    
    
    #ax_ndvi_shp.set_title(label=f"NDVI na {etapa_selecionada} ")

    # setor de exibição de gráficos da primeira coluna (NDVI)
    col1.markdown(f'<div style="text-align: center"><b>NVDI por bloco</b> ({etapa_selecionada})</div>', unsafe_allow_html=True)
    col1.pyplot(fig_ndvi_shp, use_container_width=True)


    # ========================
    # TRATANDO DADOS DE GLI ( coluna 2)
    # ========================


    # ajustando exibição do mapa com dados de GLI
    custom_colors = ['red', 'orange', 'yellow', 'blue', 'green', 'cyan', 'magenta', 'lightred']
    custom_cmap = ListedColormap(custom_colors)
    fig_gli_shp, ax_gli = plt.subplots(1, 1, figsize=(10, 10))
    dados_shape_mesclados.plot(ax=ax_gli,
                               column='gli',
                               cmap='RdYlGn', #cmap=custom_cmap,
                               legend=True,
                               legend_kwds={'label': 'Valores de GLI', 'orientation': 'vertical'},
                               linewidth=1,
                               edgecolor='lightgray',
                               vmin=0,
                               vmax=1
                               )
    col2.markdown(f'<div style="text-align: center"><b>GLI por bloco</b> ({etapa_selecionada})</div>',
                  unsafe_allow_html=True)
    col2.pyplot(fig_gli_shp,use_container_width=True)

    # ========================
    # TRATANDO DADOS DE SAVI (coluna 3)
    # ========================

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
    # ax_savi.set_title(label=f"SAVI na {etapa_selecionada} ")

    col3.markdown(f'<div style="text-align: center"><b>SAVI por bloco</b> ({etapa_selecionada})</div>',
                  unsafe_allow_html=True)
    col3.pyplot(fig_savi_shp, use_container_width=True)


    # ========================
    # TRATANDO DADOS DE STATUS TERM (coluna 4)
    # ========================

    dados_gestao_agro_termal = dados_gestao_agro
    # transformando categoria para valor
    dados_gestao_agro_termal.loc[dados_gestao_agro_termal['status_term'] == 'baixa', 'status_term_valor'] = 10
    dados_gestao_agro_termal.loc[dados_gestao_agro_termal['status_term'] == 'media', 'status_term_valor'] = 20
    dados_gestao_agro_termal.loc[dados_gestao_agro_termal['status_term'] == 'alta', 'status_term_valor'] = 30

    # st.write(dados_gestao_agro_termal)

    tipos_status_term = dados_gestao_agro_termal['status_term'].value_counts()
    tipos_status_term = tipos_status_term.reset_index()

    # colocando cores nas estatisticas
    # tipos_status_term['cores_status_term'] = tipos_status_term['status_term'].apply(lambda x: 'green' if x == 'baixa'  else 'yellow' if x == 'media' else 'red')

    custom_colors_termal = []

    if tipos_status_term['status_term'].value_counts().get('baixa', 0) > 0:
        custom_colors_termal.append('green')

    if tipos_status_term['status_term'].value_counts().get('media', 0) > 0:
        custom_colors_termal.append('yellow')

    if tipos_status_term['status_term'].value_counts().get('alta', 0) > 0:
        custom_colors_termal.append('red')

    custom_cmap_termal = ListedColormap(custom_colors_termal)
    col4.markdown(f'<div style="text-align: center"><b>Status termal por bloco</b> ({etapa_selecionada})</div>',
                  unsafe_allow_html=True)
    fig_status_term_shp, ax_status_term = plt.subplots(1, 1, figsize=(8.6, 8.6))
    dados_shape_mesclados.plot(ax=ax_status_term,
                               column='status_term',
                               cmap=custom_cmap_termal,
                               legend=True,
                               # legend_kwds={'label': 'Valores de status termal', 'orientation': 'vertical'},
                               linewidth=1,
                               edgecolor='gray', )

    col4.pyplot(fig_status_term_shp)


    # ==================================================================================================================
    # ==================================================================================================================
    # LINHA 2 -  GRÁFICOS DE BARRAS COM DISTRIBUIÇÕES DE CADA TIPO DA LINHA 1
    # ==================================================================================================================
    # ==================================================================================================================


    # ========================
    # TRATANDO DADOS DE NDVI (coluna 1)
    # ========================

    valor_filtro_ndvi = col1.slider("Filtro de valores NDVI ", min_value=0.0, max_value=1.0, step=0.01, value=0.0)
    # filtrando (destacando) os dados abaixo do limiar
    dados_gestao_agro['ndvi_cores'] = dados_gestao_agro['ndvi'].map(
        lambda x: 'red' if x < valor_filtro_ndvi else 'green')
    # gráficos de barras de NDVI
    fig_ndvi = px.bar(dados_gestao_agro, y='ndvi', x="bloco", height=alturaPadrao,
                      color='ndvi_cores', color_discrete_map="identity",
                      labels={'bloco': 'Bloco', 'ndvi': 'Valor médio de NVDI por bloco'},
                      # title=f"Valores médios de NDVI por bloco no voo ({etapa_selecionada})",
                      #range_y=[0, 1],
                      )
    # plotando gráfico de barras com dados filtrados
    col1.plotly_chart(fig_ndvi, use_container_width=True)
    # criando um conjunto dos valores abaixo do limiar definido
    dados_ndvi_filtrado = dados_gestao_agro[dados_gestao_agro['ndvi'] <= valor_filtro_ndvi]
    col1.markdown(f'<div style="text-align: center"><b>Blocos abaixo do limiar</b> ({etapa_selecionada})</div>', unsafe_allow_html=True)
    col1.write(dados_ndvi_filtrado[['bloco', 'ndvi']])

    # ========================
    # TRATANDO DADOS DE GLI (coluna 2)
    # ========================

    valor_filtro_gli = col2.slider("Filtro de valores GLI ", min_value=0.0, max_value=1.0, step=0.01, value=0.0)
    # filtrando (destacando) os dados abaixo do limiar
    dados_gestao_agro['gli_cores'] = dados_gestao_agro['gli'].map(
        lambda x: 'red' if x < valor_filtro_gli else 'blue')
    fig_gli = px.bar(dados_gestao_agro, y='gli', x="bloco", height=alturaPadrao,
                     labels={'bloco': 'Bloco', 'gli': 'Valor médio de GLI por bloco'},
                     text_auto=True,
                     color='gli_cores', color_discrete_map="identity",
                     # title=f"Valores médios de GLI por bloco na \netapa ({etapa_selecionada})",
                     # range_y=[0, 1],
                     )
    col2.plotly_chart(fig_gli, use_container_width=True)

    dados_gli_filtrado = dados_gestao_agro[dados_gestao_agro['gli'] <= valor_filtro_gli]
    col2.markdown(f'<div style="text-align: center"><b>Blocos abaixo do limiar</b> ({etapa_selecionada})</div>',
                  unsafe_allow_html=True)
    col2.write(dados_gli_filtrado[['bloco', 'gli']])

    # ========================
    # TRATANDO DADOS DE SAVI (COLUNA 3)
    # ========================

    valor_filtro_savi = col3.slider("Filtro de valores SAVI ", min_value=0.0, max_value=1.0, step=0.01, value=0.0)
    # filtrando (destacando) os dados abaixo do limiar
    dados_gestao_agro['savi_cores'] = dados_gestao_agro['savi'].map(
        lambda x: 'red' if x < valor_filtro_savi else 'lightgreen')

    fig_savi = px.bar(dados_gestao_agro,
                      y='savi',
                      x="bloco",
                      color='savi_cores', color_discrete_map="identity",
                      height=alturaPadrao,
                      labels={'bloco': 'Bloco', 'savi': 'Valor médio de SAVI por bloco'},
                      # title=f"Valores médios de SAVI por bloco no voo ({etapa_selecionada})",
                      # range_y=[0,1],
                      )
    dados_savi_filtrados = dados_gestao_agro[dados_gestao_agro['savi'] <= valor_filtro_savi]
    col3.plotly_chart(fig_savi, use_container_width=True)
    col3.markdown(f'<div style="text-align: center"><b>Blocos abaixo do limiar</b> ({etapa_selecionada})</div>',
                  unsafe_allow_html=True)
    col3.write(dados_savi_filtrados[['bloco', 'savi']])

    # ========================
    # TRATANDO DADOS DE STATUS TERM (COLUNA 4)
    # ========================
    col4.write(tipos_status_term)
    fig_status_termal = px.bar(
                               tipos_status_term,
                               x='status_term',
                               y='count',
                               # color='status_term',
                               # color_discrete_sequence=custom_colors_termal
                                labels={'status_term': 'Tipos de status termal', 'count': 'Quantidade de blocos'},
                               )

    col4.plotly_chart(fig_status_termal, figsize=(10, 10), use_container_width=True)


    # ==================================================================================================================
    # ==================================================================================================================
    # LINHA 3 -  GRÁFICOS VARIADOS
    # ==================================================================================================================
    # ==================================================================================================================



    # ==================================================================================================================
    # TRATANDO DADOS  (coluna 1)
    # ==================================================================================================================


    col1.markdown(f'<div style="text-align: center"><b>Uniformidade de cultura por sítio específico</b> ({etapa_selecionada})</div>',
                  unsafe_allow_html=True)


    # ==================================================================================================================
    # TRATANDO DADOS  COLUNA 2
    # ==================================================================================================================



    # mapa de estimativa de safra
    fig_esti_safra_shp, ax_esti_safra_shp = plt.subplots(1, 1, figsize=(10, 10))
    col2.markdown(f'<div style="text-align: center"><b>Estimativa de safra por bloco</b> ({etapa_selecionada})</div>', unsafe_allow_html=True)




    # alinhar gráficos
    #dividir_linha(col1, col2, col3)
    # dando espaço entre as linhas
    #espacar_linhas(col1,col2,col3, linhas=3)

    # ==================================================================================================================
    # TRATANDO DADOS DE TAXA DE OCUPAÇÃO
    # ==================================================================================================================


    # inserindo a terceira linha
    fig_taxa_ocupacao, ax_taxa_ocupacao = plt.subplots(1, 1, figsize=(10, 10))
    dados_shape_mesclados.plot(ax=ax_taxa_ocupacao,
                               column='tx_ocupacao',
                               cmap='RdYlGn',
                               legend=True,
                               legend_kwds={'label': 'Valores de Tx de Ocupação', 'orientation': 'vertical'},
                               linewidth=1,
                               edgecolor='lightgray',
                               vmin=0,
                               vmax=1,
                               )
    col3.markdown(f'<div style="text-align: center"><b>Taxa de ocupação por bloco</b> ({etapa_selecionada})</div>',
                  unsafe_allow_html=True)
    col3.pyplot(fig_taxa_ocupacao, use_container_width=True)

    fig_barras_tx_ocupacao = px.bar(dados_gestao_agro,
                      y='tx_ocupacao',
                      x="bloco",
                      # color='yellow',
                      #color_discrete_map="identity",
                      height=alturaPadrao,
                      labels={'bloco': 'Bloco', 'tx_ocupacao': 'Taxa de ocupação por bloco'},
                      # title=f"Valores médios de SAVI por bloco no voo ({etapa_selecionada})",
                      # range_y=[0,1],
                      )

    col3.plotly_chart(fig_barras_tx_ocupacao, use_container_width=True)




    # ==================================================================================================================
    # TRATANDO DADOS DE STATUS TERM
    # ==================================================================================================================

    elementos_baixo_A = dados_gestao_agro['Elementos_baixo_sA'].unique().tolist()

    fig_status_elementosA_shp, ax_status_elementosA = plt.subplots(1, 1, figsize=(10, 10))

    item = col4.selectbox("Elementos horizonte B", ['Ca_sB', 'Mn_sB', 'B_sB', 'Fe_sB'])

    dados_shape_mesclados.plot(ax=ax_status_elementosA,
                               column=item, #'Mn_sB',
                               cmap='YlOrRd',
                               legend=True,
                               #legend_kwds={'label': 'Valores de status termal', 'orientation': 'vertical'},
                               linewidth=2,
                               edgecolor='black',)

    col4.markdown(f'<div style="text-align: center"><b>Indicativo de demanda por fertilização</b> ({etapa_selecionada})</div>',
                  unsafe_allow_html=True)
    col4.pyplot(fig_status_elementosA_shp)

    #camada_adicionada = obter_maps()


    #with st.form(key='mymap'):
    #    m = folium.Map(location=camada_adicionada, zoom_start=12)
    #    folium.GeoJson(camada_adicionada, name="Minha camada", style_function=lambda feature: {"fillColor": "yellow", "color": "black", "weight": 0.5, "fillOpacity": 0.4}).add_to(m)
    #    st_folium(m, height=800, width=800, use_container_width=True, key='Map')
    #'''



