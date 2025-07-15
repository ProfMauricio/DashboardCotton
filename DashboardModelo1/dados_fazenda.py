import requests
import json
from datetime import datetime, timedelta
import re, base64


class DadosFazenda():

    def __init__(self):
        self.token = ""
        self.__user = ""
        self.__pass = ""

    # =================================================================================================================
    # =================================================================================================================

    def realizar_login(self, username : str, password : str ) -> dict:
        return {'status': True}
        self.__user = username
        self.__pass = password
        retorno = {'status': False}
        response = requests.get('https://api.example.com/data', {'username':username, 'password': password})
        try:
            resp_body = response.json()
        except ValueError as value_error:
            resp_body = {'message': str(value_error)}
        retorno.update(resp_body)

        if 'token' in resp_body:
            self.token = resp_body['token']
            self.expiration = datetime.fromtimestamp(resp_body['exp'])
            retorno['status'] = True

        return retorno

    # =================================================================================================================
    # =================================================================================================================

    def __check_expiration(self):
        # Se não tem token, sai
        if not self.token:
            return
        # Se não tem expiração, pega a partir do token
        if not self.expiration:
            self.expiration = self.__get_expiration_from_token()

        # Se ainda não tem expiração, é porque não tem token
        if not self.expiration:
            return

        # Atualiza o token se for vencer nos próximos 5 minutos
        if self.expiration < datetime.now() + timedelta(minutes=5):
            self.__refresh_token()

        if self.expiration < datetime.now():
            raise f"Token expirado em {self.expiration.strftime('%d/%m/%Y %H:%M:%S')}, não é possível continuar"

    # =================================================================================================================
    # =================================================================================================================

    def __get_expiration_from_token(self):
        if not self.token:
            return
        parts = self.token.split(".")
        if len(parts) != 3:
            raise "Token inválido!"
        payload = parts[1]
        dados = json.loads(base64.b64decode(payload.encode('utf-8') + b'==').decode('utf-8'))
        return datetime.fromtimestamp(dados.get('exp', 0))

    # =================================================================================================================
    # =================================================================================================================


    def obter_voo(self, voo : str , nome_arquivo_local: str) :
        end_point = 'https://api.embrapa.qgis.miboutech.com/modulo/gestao-agricola/dados/'
        endpoint = end_point + voo
        try:
            # ajustar o token na requisicao

            response = requests.get(endpoint, stream=True)  # Use stream=True for large files
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            with open(nome_arquivo_local, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Arquivo '{nome_arquivo_local}' obtido com successo.")
            return True

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return False




##

arquivo = DadosFazenda()
resposta = arquivo.realizar_login("mauricio", "teste")
if True : #resposta['success'] :
    print(" Login realizado com sucesso")
    resposta = arquivo.obter_voo('voo_1', 'dados_voo1.csv')
    if resposta :
        print('Arquivo retornado com sucesso')
    else:
        print("Falha ao obter arquivo")


