import streamlit as st
import pandas as pd
import plotly.express as px

from dados_fazenda import DadosFazenda

def obter_dados_voos(lista_arq : list[str]) -> list :
    """
    rotina que lê uma planilha
    :param nome_arq:
    :return:
    """
    global dados_agricolas_voos
    for i, nome_arq in enumerate(lista_arq):
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
    etapas = ['Etapa 1', 'Etapa 2', 'Etapa 3' ]
    lista_voos = ['voo1', 'voo3', 'voo4']
    lista_nome_arquivos = ['./dadosPlanilha/voos/tabela_dados_voo1.csv',
                  #'./dadosPlanilha/voos/tabela_dados_voo2.csv',
                  './dadosPlanilha/voos/tabela_dados_voo3.csv',
                  './dadosPlanilha/voos/tabela_dados_voo4.csv']



    # carregando os arquivos na memoria
    leitura_dados = DadosFazenda()
    # buscando os arquivos
    for i,voo in enumerate(lista_voos):
        resposta = leitura_dados.obter_voo(voo, lista_nome_arquivos[i])
        if resposta :
            print('Voo obtido com sucesso')

    obter_dados_voos(lista_nome_arquivos)

    # ajustando o site para  gestão agrícola
    st.set_page_config(layout="wide")
    st.title("Gestão agrícola e recomendações para suporte a decisão")
    # filtro dos voos realizados
    voo_selecionado = st.sidebar.selectbox("Dados de qual etapa",
                                           etapas )

    lista_etapa_indice = {f'Etapa{i+1}':i for i in range(len(etapas))}

    # obtendo os dados do voo selecionado
    dados_gestao_agro =  dados_agricolas_voos[etapas.index(voo_selecionado)]

    indice_filtro_ndvi={'Etapa 1': 0.1,
                        'Etapa 2': 0.6,
                        'Etapa 3': 0.6,
                        'voo4': 0.6}
    dados_gestao_agro['ndvi_cores'] = dados_gestao_agro['ndvi_avg'].map(lambda x: 'red' if x < indice_filtro_ndvi[voo_selecionado] else 'green')
    # gráficos de NDVI
    fig_ndvi  = px.bar(dados_gestao_agro, y='ndvi_avg', x="bloco",
                       color='ndvi_cores', color_discrete_map="identity",
                       labels={'bloco':'Bloco', 'ndvi_avg':'Valor médio de NVDI por bloco'},
                       title=f"Valores médios de NDVI por bloco no voo ({voo_selecionado})")

    col1, col2, col3 = st.columns([4, 1, 1])
    col1.plotly_chart(fig_ndvi)

    #df_ndvi_filtro =

    # gráficos de GLI
    fig_gli = px.bar(dados_gestao_agro, y='gli_avg', x="bloco",
                     labels={'bloco': 'Bloco', 'ndvi_avg': 'Valor médio de GLI por bloco'},
                     text_auto=True,
                     title=f"Valores médios de GLI por bloco no voo ({voo_selecionado})")

    fig_gli.update_xaxes(
        type="category",
    )

    col1, col2, col3 = st.columns([4, 1, 1])
    col1.plotly_chart(fig_gli)


    # gráficos de SAVI
    fig_savi = px.bar(dados_gestao_agro, y='savi_avg', x="bloco",
                     labels={'bloco': 'Bloco', 'savi_avg': 'Valor médio de SAVI por bloco'},
                     title=f"Valores médios de SAVI por bloco no voo ({voo_selecionado})")


    col1.plotly_chart(fig_savi)


    # graficos de Termal/Produtividade
    fig_savi = px.bar(dados_gestao_agro, y='prod', x="bloco",
                     labels={'bloco': 'Bloco', 'prod': 'Valor médio de Produtividade por bloco'},
                     title=f"Valores médios de Produtividade por bloco no voo ({voo_selecionado})")




    col1.plotly_chart(fig_savi)












