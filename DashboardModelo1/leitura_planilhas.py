import os.path

import numpy as np
import pandas as pd
import psycopg2
from dotenv import load_dotenv

from dados_fazenda import DadosFazenda

from DashboardModelo1 import dados_fazenda


# from DashboardModelo1.dados_fazenda import arquivo


# =====================================================================================================================
# =====================================================================================================================

def valor_float(temp: str) -> float:
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
        return 0.0


# =====================================================================================================================
# =====================================================================================================================

# leitura de dados
def ler_dados_fazenda(nome_arquivo_xls: str):
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
    df_fazenda['Valor'] = df_fazenda['Valor'].map(lambda x: valor_float(x))
    df_talhoes = pd.read_excel(xls_file, sheet_name='Planilha2')
    # print(df_fazenda)
    # print("#"*30)
    # print(df_talhoes)
    return df_fazenda, df_talhoes


# =====================================================================================================================
# =====================================================================================================================

def linhas_planilha_para_lista_custo_guarda_chuva(lista_itens, dataframe_dados, lista_index) -> list:
    """
    Função que extrai das linhas da planilha, os itens e subitens e os organiza em uma lista com dicionários de
    dados com formato {item, subitens {nome e valor}  e total }
    :param lista_itens: lista com organização de itens e quantiade de subitens
    :return: retorna a lista organiza
    """
    dados = []
    item_indice_atual = 0
    for itens in lista_itens:
        while (item_indice_atual < len(lista_index)):
            linha = dataframe_dados.iloc[item_indice_atual]
            # for index, linha in dataframe_dados.iterrows():
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

def linhas_planilha_talhoes_para_lista_custo_talhao_geral(lista_itens: list,
                                                          dataframe_dados: pd.DataFrame,
                                                          lista_talhoes: list,
                                                          lista_indices: list,
                                                          lista_nomes_talhoes: list) -> list:
    """
    Função que extrai das linhas da planilha, os itens e subitens e os organiza em uma lista com dicionários de
    dados com formato {item, subitens {nome e valor}  e total }
    :param lista_itens: lista com organização de itens e quantidade de subitens
    :return: retorna a lista organiza
    """
    item_indice_atual = 0
    for itens in lista_itens:
        while (item_indice_atual < len(lista_indices)):
            linha = dataframe_dados.iloc[item_indice_atual]
            # for index, linha in dataframe_dados.iterrows():
            if itens[0] in linha['Nome']:
                # achou o item - separando o nome
                total = 0.0
                temp_dict = {}
                nome_item = itens[0].split("-")[1]
                for t in range(len(lista_nomes_talhoes)):
                    dict_tmp = {'NomeItem': nome_item.lstrip(), 'totalEtapa1': 0.0, 'totalEtapa2': 0.0,
                                'totalEtapa3': 0.0, }
                    lista_talhoes[t]['itens'].append(dict_tmp)
                # obtendo os subitens individuais do item
                item_indice_atual += 1
                for i in range(itens[1]):
                    valor_etapa1 = dataframe_dados.iloc[item_indice_atual]['ETAPA 1 - VEGETATIVO']
                    valor_etapa2 = dataframe_dados.iloc[item_indice_atual]['ETAPA 2 - INICIO DA \nFASE REPRODUTIVA']
                    valor_etapa3 = dataframe_dados.iloc[item_indice_atual][
                        'ETAPA 3 - FINAL FASE \nREPRODUTIVA E \nMATURAÇÃO E COLHEITA']

                    for t in range(len(lista_nomes_talhoes)):
                        subitem = {'Nome': dataframe_dados.iloc[item_indice_atual]['Nome'],
                                   'Etapa1': float(valor_etapa1.values[t]),
                                   'Etapa2': float(valor_etapa2.values[t]), 'Etapa3': float(valor_etapa3.values[t])
                                   }

                        if 'subitens' not in lista_talhoes[t]['itens'][-1]:
                            lista_talhoes[t]['itens'][-1]['subitens'] = []
                        lista_talhoes[t]['itens'][-1]['subitens'].append(subitem)
                    item_indice_atual += 1
                break
            else:
                item_indice_atual += 1
    # somando os dados gerais
    for dados in lista_talhoes:
        for itens in dados['itens']:
            for subitens in itens['subitens']:
                itens['totalEtapa1'] += subitens['Etapa1']
                itens['totalEtapa2'] += subitens['Etapa2']
                itens['totalEtapa3'] += subitens['Etapa3']
    return lista_talhoes


# =====================================================================================================================
# =====================================================================================================================

def carregar_dados_custo(pasta_destino: str = "./dados_fazenda") -> (dict, dict):
    """

    :param pasta_destino: Pasta onde os dados armazenados no servidor
    :return: retorna 4 dicionarios com os dados de variaveis globais (guarda-chuva - geral e por hectares) e
    dados de variáveis por talhão nas fases ( geral e por hectare)
    """
    #
    arquivo_custo_padrao = 'planilha_saida.xlsx'
    nome_arquivo_dados = os.path.join(pasta_destino, arquivo_custo_padrao)
    dados_fazenda, dados_talhoes = ler_dados_fazenda(nome_arquivo_dados)
    info_fazenda = {'NomeFazenda': "Teste",  # dados_fazenda.iloc[2, 1],
                    'TotalHectares': "300.43",  # dados_fazenda.iloc[3, 1],
                    'QuantidadeTalhoes': 10,  # dados_fazenda.iloc[4, 1],
                    }

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
    # print(dados_custo_geral)
    cont = 0
    row = 0
    lista_linhas_custo_geral = []
    for index, linha in temp_dados.iterrows():
        if linha['Nome'] != 'CUSTOS POR HECTARE':
            lista_linhas_custo_geral.append(index)
            temp_dados_custo_geral.loc[row] = [linha['Nome'], linha['Valor']]
            row += 1
        else:
            break
    # print(lista_linhas_custo_geral)

    # print(temp_dados_custo_geral)
    # organizando uma lista com dicionarios de dados com formato {item, subitens {nome do subitem e valor}  e total }
    itens_custo_geral = [("A. MÃO DE OBRA (CEPEA/AMPA CONAB)", 2),
                         ("B. MANUTENÇÃO", 2),
                         ("C. IMPOSTOS E TAXAS", 9),
                         ("D. FINANCEIRAS", 3),
                         ("F. OUTROS CUSTOS", 5)
                         ]

    dados_custo_geral = linhas_planilha_para_lista_custo_guarda_chuva(itens_custo_geral, temp_dados_custo_geral,
                                                                      lista_linhas_custo_geral)

    # preparando dados de custos por hectare a partir dos dados da fazenda
    for i in lista_linhas_custo_geral:
        temp_dados.drop(i, inplace=True)
    temp_dados_custo_por_hectare = temp_dados.copy()
    temp_dados_custo_por_hectare.reset_index(drop=True, inplace=True)
    lista_linhas_custo_geral = []
    for index, linha in temp_dados_custo_por_hectare.iterrows():
        lista_linhas_custo_geral.append(index)

    dados_custo_por_hectare = linhas_planilha_para_lista_custo_guarda_chuva(itens_custo_geral,
                                                                            temp_dados_custo_por_hectare,
                                                                            lista_linhas_custo_geral)

    # print(dados_custo_geral)
    # print(dados_custo_por_hectare)

    ###################
    # Custos por talhão
    ##################
    temp_dados_talhoes = dados_talhoes.copy()
    # temp_dados_talhoes = pd.DataFrame(columns=temp_dados.columns)
    temp_dados_talhoes.dropna(axis=1, how='all', inplace=True)
    temp_dados_talhoes = temp_dados_talhoes.dropna(thresh=1)

    # lendo a primeira linha para determinar o nome das colunas
    linha_header = temp_dados_talhoes.iloc[0]
    temp_dados_talhoes.columns = linha_header
    temp_dados_talhoes.reset_index(drop=True)
    cont = 0
    row = 0
    lista_colunas = list(temp_dados_talhoes.columns)
    lista_colunas[0] = 'Nome'
    temp_dados_talhoes.columns = lista_colunas
    dados_talhoes_geral = pd.DataFrame(columns=lista_colunas)
    lista_indices_linhas_talhao_geral = []
    for index, linha in temp_dados_talhoes.iterrows():
        if linha['Nome'] != 'CUSTO POR HECTARE':
            lista_indices_linhas_talhao_geral.append(index)
            dados_talhoes_geral.loc[row] = linha
            row += 1
        else:
            break
    dados_talhoes_geral.reset_index(drop=True, inplace=True)
    # a partir dos dados gera uma lista com os dados com cada elemento da lista sendo
    # um talhão
    lista_talhoes_geral = []
    cjto_nomes_talhoes_geral = []

    # lendo os nomes dos talhoes nas três primeiras linhas
    for index, linha in dados_talhoes_geral.iterrows():
        if linha['Nome'] == 'Nome do Talhao':
            str_talhao = linha["ETAPA 1 - VEGETATIVO"].dropna().unique()
            for itens in str_talhao:
                cjto_nomes_talhoes_geral.append(itens)
            break

    print(cjto_nomes_talhoes_geral)

    # criando itens na lista com de talhoes gerais para guardar dados dos talhoes
    for talhao in cjto_nomes_talhoes_geral:
        dict_talhao = {'nome': talhao, 'itens': []}
        lista_talhoes_geral.append(dict_talhao)
    # obtendo dados de area
    for index, linha in dados_talhoes_geral.iterrows():
        if linha['Nome'] == 'Area do Talhao (Ha)':
            str_talhao = linha["ETAPA 1 - VEGETATIVO"].dropna()
            for i, itens in enumerate(str_talhao):
                lista_talhoes_geral[i]['area'] = itens
            break

    # obtendo dados de coordenadas
    for index, linha in dados_talhoes_geral.iterrows():
        if linha['Nome'] == 'Georreferenciamento (utm x;y em metros)':
            str_talhao = linha["ETAPA 1 - VEGETATIVO"].dropna()
            for i, itens in enumerate(str_talhao):
                coord = itens.split(';')
                lista_talhoes_geral[i]['coord_x'] = coord[0]
                lista_talhoes_geral[i]['coord_y'] = coord[1]
            indice = index
            break
    print(lista_talhoes_geral)

    # obtendo dados de sementes
    indice += 1
    flag = False
    lista_itens = [('1 - SEMENTES', 3),
                   ('2 - FERTILIZANTES', 3),
                   ('3 - OPERAÇÕES COM MÁQUINAS', 14),
                   ('4 - AGROTÓXICOS', 9)]

    lista_talhoes_geral = linhas_planilha_talhoes_para_lista_custo_talhao_geral(dataframe_dados=dados_talhoes_geral,
                                                                                lista_itens=lista_itens,
                                                                                lista_talhoes=lista_talhoes_geral,
                                                                                lista_indices=lista_indices_linhas_talhao_geral,
                                                                                lista_nomes_talhoes=cjto_nomes_talhoes_geral)

    return info_fazenda, dados_custo_geral, dados_custo_por_hectare, lista_talhoes_geral


# =====================================================================================================================
# =====================================================================================================================

def ativar_conexao():
    try:
        load_dotenv()
        nome_base = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        port = os.getenv('DB_PORT')
        host = os.getenv('DB_HOST')
        conn = psycopg2.connect(
            dbname=nome_base,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return conn
    except Exception as e:
        print(e)
        return None


# ======================================================================================================================
# ======================================================================================================================

def obter_id_custo(descricao, conexao) -> int:
    try:
        cursor = conexao.cursor()
        consulta = f"select id from dashboard.tipos_despesas_guarda_chuva where descricao like '%{descricao}%'"
        cursor.execute(consulta)
        id = cursor.fetchone()
        cursor.close()
        return id[0]
    except Exception as e:
        return 0


# ======================================================================================================================
# ======================================================================================================================

def obter_detalhe_custo(descricao, id_tipo_custo, conexao):
    try:
        cursor = conexao.cursor()
        consulta = f"select id from dashboard.detalhes_tipos_despesa_guarda_chuva where tipo_despesas_id = {id_tipo_custo} and nome like '%{descricao}%'"
        cursor.execute(consulta)
        id = cursor.fetchone()
        cursor.close()
        return id[0]
    except Exception as e:
        return 0


# ======================================================================================================================
# ======================================================================================================================

def gravar_dados_gestao_custos_guarda_chuva(local_custo_geral, conexao):
    for item_custo in local_custo_geral:
        id_tipo_custo = obter_id_custo(item_custo['item'], conexao)
        for subitem in item_custo['subitens']:
            temp = subitem['Nome'].split()
            nro = len(temp[0])
            nome = subitem['Nome'][nro + 1:]
            id_detalhe_item_custo = obter_detalhe_custo(nome, id_tipo_custo, conexao)
            ## estruturando a inserção
            cursor = conexao.cursor()
            consulta = f"insert into dashboard.gestao_custos_despesas_guarda_chuva_fazenda(fazenda_id, detalhes_tipo_custo_id, valor, data_criacao, safra ) values (1,{id_detalhe_item_custo},{subitem['Valor']}, now(), '2025' )"
            cursor.execute(consulta)
            conexao.commit()


# ======================================================================================================================
# ======================================================================================================================


def obter_id_custo_producao(descricao, conexao):
    try:
        cursor = conexao.cursor()
        consulta = f"select id from dashboard.tipos_custos_producao where descricao like '%{descricao}%'"
        cursor.execute(consulta)
        id = cursor.fetchone()
        cursor.close()
        return id[0]
    except Exception as e:
        return 0


# ======================================================================================================================
# ======================================================================================================================

def obter_detalhe_custo_producao(descricao, id_tipo_custo, conexao):
    try:
        cursor = conexao.cursor()
        consulta = f"select id from dashboard.detalhes_tipos_custos_producao where tipo_custo_id = {id_tipo_custo} and nome like '%{descricao}%'"
        cursor.execute(consulta)
        id = cursor.fetchone()
        cursor.close()
        return id[0]
    except Exception as e:
        return 0


# ======================================================================================================================
# ======================================================================================================================

def obter_id_etapa(etapa, conexao):
    try:
        cursor = conexao.cursor()
        consulta = f"select id from dashboard.fases_cultura where nome like '%{etapa}%'"
        cursor.execute(consulta)
        id = cursor.fetchone()
        cursor.close()
        return id[0]
    except Exception as e:
        return 0


def gravar_dados_gestao_custos_producao_talha(talhoes_custo_geral, etapa, conexao):
    # buscando o id da etapa utilizada
    id_etapa = obter_id_etapa(etapa, conexao)
    cursor = conexao.cursor()

    for ind_talhao, item_custo in enumerate(talhoes_custo_geral):
        for subitem in item_custo['itens']:
            id_tipo_custo_producao = obter_id_custo_producao(subitem['NomeItem'], conexao)
            for valor_por_etapa in subitem['subitens']:
                temp = valor_por_etapa['Nome'].split('-')
                nro = len(temp[0])
                nome = valor_por_etapa['Nome'][nro + 2:]
                nome = nome.lstrip()
                nome = nome.rstrip()
                id_custo_especificacao = obter_detalhe_custo_producao(nome, id_tipo_custo_producao,
                                                                      conexao)
                consulta = (
                    f"insert into dashboard.gestao_custos_producao_por_talhao(talhao_id, custo_especificacao_id, valor, safra, fase_cultura_id, descricao, data_criacao) values "
                    f"({ind_talhao + 1},{id_custo_especificacao},{valor_por_etapa[etapa]},{2025},{id_etapa},'{nome}', now())")
                cursor.execute(consulta)
                conexao.commit()
    cursor.close()


def obter_dados_voos(dados: dict) -> list:
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


def gravar_bloco( bloco:int, coord_x:float, coord_y:float, conexao, fazenda:int=1, talhao_id:int=1,):
    """

    :param bloco:
    :param coord_x:
    :param coord_y:
    :param conexao:
    :param fazenda:
    :param talhao_id:
    :return:
    """
    cursor = conexao.cursor()
    consulta = f"insert into dashboard.blocos(longitude, latitude, talhao_id, bloco, data_criacao) values ({coord_x},{coord_y},{talhao_id}, {bloco}, now() )"
    cursor.execute(consulta)
    conexao.commit()

# ======================================================================================================================
# ======================================================================================================================


def obter_id_bloco(param, conexao):
    cursor = conexao.cursor()
    consulta = f"select id from dashboard.blocos where bloco = {param}"
    cursor.execute(consulta)
    id = cursor.fetchall()
    cursor.close()
    return id[0][0]


# ======================================================================================================================
# ======================================================================================================================


def gravar_dados_gestao_agricola_elementos_horizonte(linha, id_gestao_agricola, id_fase,  conexao ):
    # construindo dados para horizonte A

    bloco_id = obter_id_bloco(linha['bloco'], conexao)
    cursor = conexao.cursor()
    consulta = (f"insert into dashboard.gestao_agricola_medidas_elementos_horizonte(bloco_id, fase_cultura_id, "
                f"gestao_agricola_talhao_id, horizonte, ")
    consulta += f"ph_h2o, ph_cacl2, p_resina, k_trocavel, mo, ca, zn, b, mn, fe, na, s, mg, elementos_baixo, data_criacao ) "
    consulta += f"values ({bloco_id},{id_fase},{id_gestao_agricola_talhao}, 'A', {linha['pH_H2O_sA']},{linha['pH_CaCl2_sA']},"
    consulta += f"{linha['P_resina_sA']}, {linha['K_trocavel_sA']}, {linha['MO_sA']},{linha['Ca_sA']},{linha['Zn_sA']},"
    consulta += f"{linha['B_sA']},{linha['Mn_sA']},{linha['Fe_sA']},{linha['Na_sA']},{linha['S_sA']},{linha['Mg_sA']},"
    elementos_baixo = linha['Elementos_baixo_sA'].replace("'", '"')
    consulta += f"'{elementos_baixo}', now())"
    cursor.execute(consulta)
    conexao.commit()

    consulta = (f"insert into dashboard.gestao_agricola_medidas_elementos_horizonte(bloco_id, fase_cultura_id, "
                f"gestao_agricola_talhao_id, horizonte, ")
    consulta += f"ph_h2o, ph_cacl2, p_resina, k_trocavel, mo, ca, zn, b, mn, fe, na, s, mg, elementos_baixo, data_criacao ) "
    consulta += f"values ({bloco_id},{id_fase},{id_gestao_agricola_talhao}, 'B', {linha['pH_H2O_sB']},{linha['pH_CaCl2_sB']},"
    consulta += f"{linha['P_resina_sB']}, {linha['K_trocavel_sB']}, {linha['MO_sB']},{linha['Ca_sB']},{linha['Zn_sB']},"
    consulta += f"{linha['B_sB']},{linha['Mn_sB']},{linha['Fe_sB']},{linha['Na_sB']},{linha['S_sB']},{linha['Mg_sB']},"
    elementos_baixo = linha['Elementos_baixo_sA'].replace("'", '"')
    consulta += f"'{elementos_baixo}', now())"
    cursor.execute(consulta)
    conexao.commit()
    cursor.close()

# ======================================================================================================================
# ======================================================================================================================

def obter_id_talhao(talhao, conexao):
    try:
        cursor = conexao.cursor()
        consulta = f"select id from dashboard.talhoes where nome like '%{talhao}%'"
        cursor.execute(consulta)
        id = cursor.fetchone()
        cursor.close()
        return id[0]
    except Exception as e:
        return 0

# ======================================================================================================================
# ======================================================================================================================

def gravar_dados_gestao_agricola_talhao(talhao, fase_cultura, safra, conexao) -> int :
    """
    Função para gestão de talhão e seus respecivos blocos
    :param talhao:
    :param fase_cultura:
    :param safra:
    :param conexao:
    :return: Retorna o id de gestão do talhao
    """
    id_fase = obter_id_etapa(fase_cultura, conexao)
    id_talhao = obter_id_talhao(talhao, conexao)
    cursor = conexao.cursor()
    consulta = (f"insert into dashboard.gestao_agricola_talhao(talhao_id, fase_cultura_id, safra, data_criacao) values "
                f"({id_talhao},{id_fase},{safra}, now()) returning id")
    cursor.execute(consulta)
    conexao.commit()
    id_talhao = cursor.fetchone()[0]
    return id_talhao

# ======================================================================================================================
# ======================================================================================================================

def gravar_dados_gestao_agricola_indics_calculados_talhao(linha, id_fase, id_gestao_agricola_talhao,  conexao):
    bloco_id = obter_id_bloco(linha['bloco'], conexao)
    cursor = conexao.cursor()
    consulta = (f"insert into dashboard.gestao_agricola_indices_calculados_talhao(bloco_id, fase_cultura_id, "
                f"gestao_agricola_talhao_id, ndvi, savi, gli, tx_ocupacao, status_term, data_criacao) ")
    consulta += f"values ({bloco_id},{id_fase},{id_gestao_agricola_talhao}, "
    consulta += f"{linha['ndvi']},{linha['savi']},{linha['gli']},{linha['tx_ocupacao']},'{linha['status_term']}',now())"
    cursor.execute(consulta)
    conexao.commit()
    cursor.close()


# ======================================================================================================================
# ======================================================================================================================


# ======================================================================================================================
# ======================================================================================================================




# ======================================================================================================================
# ======================================================================================================================
#
#       PRINCIPAL TEMPORÁRIO
#
# ======================================================================================================================
# ======================================================================================================================


if __name__ == '__main__':
    conexao = ativar_conexao()

    local_custo_geral, local_custo_hectare, talhoes_custo_geral, lista_talhoes = carregar_dados_custo(
        pasta_destino='./dadosPlanilha')
    print(local_custo_geral)
    #conexao = ativar_conexao()
    gravar_dados_gestao_custos_guarda_chuva(local_custo_hectare, conexao)
    gravar_dados_gestao_custos_producao_talha(lista_talhoes, "Etapa1", conexao)
    gravar_dados_gestao_custos_producao_talha(lista_talhoes, "Etapa2", conexao)
    gravar_dados_gestao_custos_producao_talha(lista_talhoes, "Etapa3", conexao)
    print(local_custo_hectare)
    print(talhoes_custo_geral)


    dados_agricolas_voos = []
    dados_fazenda = {
        'etapas': ['Etapa 1', 'Etapa 2', 'Etapa 3'],
        'etapas_voos': ['etapa1', 'etapa2', 'etapa3'],
        'nomes_arquivos': ['./dadosPlanilha/voos/relatorio_manejo_agricola_etapa1.csv',
                           './dadosPlanilha/voos/relatorio_manejo_agricola_etapa2.csv',
                           './dadosPlanilha/voos/relatorio_manejo_agricola_etapa3.csv'],
        'status': [False, False, False],
    }

    # carregando os arquivos na memoria


    leitura_dados = DadosFazenda()
    flag_leitura_dados_remoto = True
    # buscando os arquivos
    for i, etapa in enumerate(dados_fazenda['etapas_voos']):
        resposta = leitura_dados.obter_voo(etapa, dados_fazenda['nomes_arquivos'][i])
        if i < 2:
            resposta = True
        dados_fazenda['status'][i] = resposta
        if resposta:
            print('Voo obtido com sucesso')

    dados_agricolas_voos = obter_dados_voos(dados_fazenda)
    #print(dados_agricolas_voos)

    # gravando os blocos apenas uma vez
    df_blocos = dados_agricolas_voos[0]

    for index, linha in df_blocos.iterrows():
        #print(linha)
        gravar_bloco(linha['bloco'], linha['utm-x'], linha['utm-y'], conexao)


    # criando o registro de gestão do talhao
    fase = linha['etp_veg']
    if 'Etapa 1' in fase:
        fase = 'Etapa1'
    elif 'Etapa 2' in fase:
        fase = 'Etapa2'
    elif 'Etapa 3' in fase:
        fase = 'Etapa3'
    #id_fase = obter_id_etapa(fase, conexao)
    #id_gestao_agricola_talhao = gravar_dados_gestao_agricola_talhao(talhao='Talhão 1', fase_cultura=fase, safra='2025',conexao=conexao)

    for ind, dados_etapa in enumerate(dados_agricolas_voos):
        for index, linha in dados_etapa.iterrows():
            fase = linha['etp_veg']
            if 'Etapa 1' in fase:
                fase = 'Etapa1'
            elif 'Etapa 2' in fase:
                fase = 'Etapa2'
            elif 'Etapa 3' in fase:
                fase = 'Etapa3'
            break
        id_fase = obter_id_etapa(fase, conexao)
        id_gestao_agricola_talhao = gravar_dados_gestao_agricola_talhao(talhao='Talhão 1', fase_cultura=fase,
                                                                        safra='2025',
                                                                        conexao=conexao)
        for index, linha in dados_etapa.iterrows():
            linha = linha.replace(np.nan, 0, regex=True)
            if (ind > 0 ):
                gravar_dados_gestao_agricola_elementos_horizonte(linha, id_fase, id_gestao_agricola_talhao, conexao)
            gravar_dados_gestao_agricola_indics_calculados_talhao(linha, id_fase, id_gestao_agricola_talhao, conexao)



