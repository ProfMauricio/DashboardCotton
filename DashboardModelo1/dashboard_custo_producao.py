import streamlit as st
import pandas as pd
import plotly.express as px


def valor_float( temp : str) -> float :
    """
    Converte o dado que vem da planilha
    :param temp:
    :return:
    """
    temp1 = temp.replace('.', '')
    temp1 = temp1.replace(',', '.')
    return float(temp1[2:])



# leitura de dados
def ler_dados_fazenda()-> pd.DataFrame :
    """
        Metodo para obter dados de custo de producoa
    """
    df_fazenda = pd.read_csv('./dadosPlanilha/dadosGuardaChuva_Exemplo1.csv', header=None,)
    df_fazenda.columns = ['Nomes', 'Valores']

    
    print(df_fazenda)
    return df_fazenda

    """
    fazenda = {
        'Nome': [df_fazenda.iloc[0, 1]],
        'Total de Hectares': [df_fazenda.iloc[1, 1]],
        'Quantidade de Talhões': [df_fazenda.iloc[2, 1]],
        }

    temp1 = 'teste'
    fazenda['Custo permanente'] = [valor_float(df_fazenda.iloc[3, 1])]
    fazenda['Custo temporário'] = [valor_float(df_fazenda.iloc[4, 1])]
    mp = valor_float(df_fazenda.iloc[5,1])
    mt = valor_float(df_fazenda.iloc[6,1])
    fazenda['Manutenção'] = [mp + mt]
    fazenda['Tarifas'] = 0
    for i in range(7,17):
        fazenda['Tarifas'] += valor_float(df_fazenda.iloc[i,1])
    fazenda['Tarifas'] = [ fazenda['Tarifas'] ]
    fazenda['Financiamentos'] = [ valor_float(df_fazenda.iloc[17,1])]
    fazenda['Seguro da Produção'] = [ valor_float(df_fazenda.iloc[18,1])]
    fazenda['Seguro de Maquinario'] = [ valor_float(df_fazenda.iloc[19,1])]
    fazenda['Assistência Técnica'] = [ valor_float(df_fazenda.iloc[20,1])]
    fazenda['Combustível Utilitários'] = [valor_float(df_fazenda.iloc[21,1])]


    df = pd.DataFrame(fazenda)
    print(df)
    return df
    """


if __name__ == '__main__':
    # dados originais 
    dados_fazenda = ler_dados_fazenda()
    # organizando os dados de interesse para o dashboard     
    dados_custo = dados_fazenda.copy()
    # removendo as linhas 
    lista_linhas_excluir = ['Nome da Fazenda', 'Total de Hectares', 'Quantidade de Talhões']
    for nome in lista_linhas_excluir:
        i = dados_custo[(dados_custo.Nomes == nome )].index
        dados_custo.drop(i, inplace=True)
        print(i)


    tam = len(dados_custo)

    for i in range(0,tam):
        dados_custo.iloc[i,1] = valor_float(dados_custo.iloc[i,1])
    print(dados_custo)

    # separando os dados de custo geral dos custos por hectare
    dados_custo_geral = dados_custo.loc[ [i for i in range(3,24)]]
    dados_custo_hectares = dados_custo.loc[ [i for i in range(24,tam)]]
    for i in range(len(dados_custo_hectares)):
        tmp = dados_custo_hectares.iloc[i,0]
        tmp = tmp.replace("para cada Hectare", "")
        dados_custo_hectares.iloc[i,0] = tmp

    ################
    # Manipulação dos dashboards
    #################
    # Configurar o layout da página
    st.set_page_config(layout="wide")
    st.title(f'Custo de produção - Fazenda {dados_fazenda.iloc[0,1]}')
    st.image('./logo_embrapa.png', width=200)
    col1, col2  = st.columns([7,3])

    fig_guarda_chuva_geral  = px.bar(dados_custo_geral, y='Valores', x="Nomes",
                                     labels={'Nomes':'Despesas', 'Valores':'Valores em R$'},
                                     title="Custos gerais de produção")
    #fig_guarda_cuhva.update_layout(
    #    #plot_bgcolor='white',x
    #    # paper_bgcolor='white',
    #    legend_title_text='Tipos de Custos'
    #)
    st.divider()
    col1.plotly_chart(fig_guarda_chuva_geral)
    #colocando os dados de fazenda
    col2.write(dados_custo_geral)

    fig_guarda_chuva_custos_hectare =px.bar(dados_custo_hectares, y='Valores', x="Nomes",
                                            labels={'Nomes':'Despesas', 'Valores':'Valores em R$ por cada ha'},
                                            title="Custos de produção por hectare")

    col1.plotly_chart(fig_guarda_chuva_custos_hectare)
    col1.title("Valores por cada Hectare")
    col1.write(dados_custo_hectares)




