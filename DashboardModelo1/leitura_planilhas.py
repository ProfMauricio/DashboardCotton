import pandas as pd
from logging import Logger


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
    df_fazenda = df_fazenda.dropna()
    # limpando os dados dos valores
    df_fazenda['Valor'] = df_fazenda['Valor'].map(lambda x: valor_float(x)   )
    df_talhoes= pd.read_excel(xls_file, sheet_name='Planilha2')
    #print(df_fazenda)
    #print("#"*30)
    #print(df_talhoes)
    return df_fazenda, df_talhoes


if __name__ == '__main__':
    dados_fazenda, dados_talhoes = ler_dados_fazenda('./dadosPlanilha/planilha_saida.xlsx')
    # organizando os dados de interesse para o dashboard
    dados_custo_geral = dados_fazenda.copy()
    # removendo as linhas
    lista_linhas_excluir = ['Nome da Fazenda', 'Total de Hectares', 'Quantidade de Talhões']
    for nome in lista_linhas_excluir:
        i = dados_custo_geral[(dados_custo_geral.Nome == nome )].index
        dados_custo_geral.drop(i, inplace=True)
        print(i)
    #print(dados_custo_geral)
    cont = 0
    lista_linhas_custo_geral= []
    for index, linha in dados_custo_geral.iterrows():
        if linha['Nome'] != 'Permanente para cada Hectare':
            lista_linhas_custo_geral.append(index)
        else:
            break
    print(lista_linhas_custo_geral)

    dados_custo_geral =  dados_custo_geral.index.map( lambda x: x if x in lista_linhas_custo_geral else None)
    print(dados_custo_geral)
