from xml.etree.ElementTree import QName

import pandas as pd
from logging import Logger

# =====================================================================================================================
# =====================================================================================================================

def valor_float( temp : str) -> float :
    """
    Converte o dado que vem da planilha
    :param temp:
    :return:
    """
    try:

        temp1 = temp.replace('.', '')
        temp1 = temp1.replace(',', '.')
        temp1 = temp1.split('R$')
        return float(temp1[-1])
    except Exception as e:
        return temp

# =====================================================================================================================
# =====================================================================================================================

# leitura de dados
def ler_dados_fazenda( nome_arquivo_xls : str)  :
    """
        Metodo para obter dados de custo de producão
        :param nome_arquivo_xls: nome do arquivo utilizado para extração dos dados
    """

    xls_file = pd.ExcelFile(nome_arquivo_xls)
    xls_file.parse('Planilha1', skiprows=1, na_values=['NA'])
    xls_file.parse('Planilha2', skiprows=1, na_values=['NA'])
    df_fazenda = pd.read_excel(xls_file, sheet_name='Planilha1')
    df_fazenda.columns = ['Nome', 'Valor']
    df_fazenda = df_fazenda.dropna(thresh=1)
    # limpando os dados dos valores
    df_fazenda['Valor'] = df_fazenda['Valor'].map(lambda x: valor_float(x)   )
    df_talhoes= pd.read_excel(xls_file, sheet_name='Planilha2')
    print(df_fazenda)
    #print("#"*30)
    #print(df_talhoes)
    return df_fazenda, df_talhoes

# =====================================================================================================================
# =====================================================================================================================

def linhas_planilha_para_lista(lista_itens, dataframe_dados, lista_index) -> list :
    """
    Função que extrai das linhas da planilha, os itens e subitens e os organiza em uma lista com dicionários de
    dados com formato {item, subitens {nome e valor}  e total }
    :param lista_itens: lista com organização de itens e quantiade de subitens
    :return: retorna a lista organiza
    """
    dados = []
    item_indice_atual = 0
    for itens in lista_itens:
        while( item_indice_atual < len(lista_index)):
            linha = dataframe_dados.iloc[item_indice_atual]
        #for index, linha in dataframe_dados.iterrows():
            if itens[0] in linha['Nome']:
                total = 0.0
                temp_dict = {}
                nome_item = itens[0].split(".")[1]
                temp_dict['item'] = nome_item
                temp_dict['subitens'] = []
                # obtendo os subitens individuais do item
                item_indice_atual += 1
                for i in range(itens[1]):
                    subitem = {'Nome': dataframe_dados.iloc[item_indice_atual]['Nome']}
                    valor = dataframe_dados.iloc[item_indice_atual]['Valor']
                    subitem['Valor'] = float(valor)
                    total += float(valor)
                    temp_dict['subitens'].append(subitem)
                    item_indice_atual += 1
                temp_dict['total'] = total
                dados.append(temp_dict)
                break
            else:
                item_indice_atual += 1
    return dados

# =====================================================================================================================
# =====================================================================================================================

def carregar_dados_custo(pasta_destino:str="./dados_fazenda") -> dict :
    """

    :param pasta_destino:
    :return:
    """


# =====================================================================================================================
# =====================================================================================================================

if __name__ == '__main__':
    dados_fazenda, dados_talhoes = ler_dados_fazenda('./dadosPlanilha/planilha_saida.xlsx')

    # organizando os dados de interesse para o dashboard
    temp_dados = dados_fazenda.copy()
    temp_dados_custo_geral = pd.DataFrame(columns=temp_dados.columns)
    temp_dados_custo_geral.reset_index(drop=True)
    # removendo as linhas
    lista_linhas_excluir = ['Nome da Fazenda', 'Total de Hectares', 'Quantidade de Talhoes']
    for nome in lista_linhas_excluir:
        i = temp_dados[(temp_dados.Nome == nome)].index
        temp_dados.drop(i, inplace=True)
        print(i)
    #print(dados_custo_geral)
    cont = 0
    row = 0
    lista_linhas_custo_geral= []
    for index, linha in temp_dados.iterrows():
        if linha['Nome'] != 'CUSTOS POR HECTARE':
            lista_linhas_custo_geral.append(index)
            temp_dados_custo_geral.loc[row] = [linha['Nome'], linha['Valor']]
            row += 1
        else:
            break
    #print(lista_linhas_custo_geral)

    # print(temp_dados_custo_geral)
    # organizando uma lista com dicionarios de dados com formato {item, subitens {nome do subitem e valor}  e total }
    itens_custo_geral = [("A. MÃO DE OBRA (CEPEA/AMPA CONAB)", 2),
                         ("B. MANUTENÇÃO", 2),
                         ("C. IMPOSTOS E TAXAS", 9),
                         ("D. FINANCEIRAS", 3),
                         ("F. OUTROS CUSTOS", 5)
                         ]

    dados_custo_geral = linhas_planilha_para_lista(itens_custo_geral, temp_dados_custo_geral, lista_linhas_custo_geral)

    # preparando dados de custos por hectare a partir dos dados da fazenda
    for i in lista_linhas_custo_geral:
        temp_dados.drop(i, inplace=True)
    temp_dados_custo_por_hectare =  temp_dados.copy()
    temp_dados_custo_por_hectare.reset_index(drop=True, inplace=True)
    lista_linhas_custo_geral = []
    for index, linha in temp_dados_custo_por_hectare.iterrows():
        lista_linhas_custo_geral.append(index)

    dados_custo_por_hectare = linhas_planilha_para_lista(itens_custo_geral, temp_dados_custo_por_hectare,lista_linhas_custo_geral)


    """
    for itens in itens_custo_geral:
        for index, linha in temp_dados_custo_geral.iterrows():
            if itens[0] in linha['Nome']:
                total = 0.0
                temp_dict = {}
                nome_item = itens[0].split(".")[1]
                temp_dict['item'] = nome_item
                temp_dict['subitens'] = []
                # obtendo os subitens individuais do item
                for i in range(itens[1]):
                    subitem = {'Nome': temp_dados_custo_geral.iloc[index+i+1]['Nome'],
                               'Valor': temp_dados_custo_geral.iloc[index+i+1]['Valor']
                               }
                    total += subitem['Valor']
                    temp_dict['subitens'].append(subitem)
                temp_dict['total'] = total
                dados_custo_geral.append(temp_dict)
                break
    """
    print(dados_custo_geral)
    print(dados_custo_por_hectare)






