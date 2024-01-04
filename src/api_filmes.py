import requests
import configparser
import os
from datetime import datetime
from src import leitor_csv
from models.filme_model import Filme


def _obtem_chave_api():
    if not os.path.exists('./config/config.ini'):
        return None

    config = configparser.ConfigParser()
    config.read('./config/config.ini')

    if 'API' not in config or 'CHAVE' not in config['API']:
        return None

    api_key = config['API']['CHAVE']
    return api_key


def _realiza_chamada_api(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


class TmdbApiService:

    def __init__(self):
        self.chave_api = _obtem_chave_api()

        if not self.chave_api:
            raise Exception('Chave da API não localizada no arquivo /config/config.ini')

    def obter_qtd_paginas_filmes(self):
        url = f'https://api.themoviedb.org/3/discover/movie?api_key={self.chave_api}'

        try:
            data = _realiza_chamada_api(url)
            return int(data['total_pages'])

        except requests.exceptions.RequestException:
            return 0

    def obter_detalhes_filmes_por_id(self, id_pesquisado):
        url = f"https://api.themoviedb.org/3/movie/{id_pesquisado}?api_key={self.chave_api}&language=pt-BR"

        try:
            data = _realiza_chamada_api(url)
            return data

        except requests.exceptions.RequestException:
            return None

    def obter_diretor_filme_por_id(self, id_pesquisado):
        url = f"https://api.themoviedb.org/3/movie/{id_pesquisado}/credits?api_key={self.chave_api}&language=pt-BR"

        try:
            data = _realiza_chamada_api(url)
            diretor = next((membro.get('name') for membro in data.get('crew', []) if membro.get('job') == 'Director'),
                           None)
            return diretor

        except requests.exceptions.RequestException as err:
            return None

    def obter_ids_filmes_por_pagina(self, pagina):
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={self.chave_api}" \
              f"&language=pt-BR&include_adult=false&include_video=false&page={pagina}"
        try:
            data = _realiza_chamada_api(url)
            return [int(filme['id']) for filme in data.get('results', [])]

        except requests.exceptions.RequestException as err:
            return []

    def obter_detalhes_filmes_por_pagina(self, pagina):
        return [self.obter_detalhes_filmes_por_id(id_encontrado) for id_encontrado in self.obter_ids_filmes_por_pagina(pagina)]


def importa_filmes_para_csv(pagina_inicial=1, pagina_final=None, recriar_cvs=True):

    api_service = TmdbApiService()

    if not pagina_final:
        pagina_final = api_service.obter_qtd_paginas_filmes()

    if recriar_cvs:
        leitor_csv.cria_arquivo_filmes_csv()

    for pagina in range(pagina_inicial, pagina_final + 1):
        filmes = []

        print(f'{pagina}/{pagina_final}')

        for filme_json in api_service.obter_detalhes_filmes_por_pagina(pagina):
            try:
                diretor = api_service.obter_diretor_filme_por_id(filme_json.get('id')) if filme_json.get('id') else None

                filmes.append(_converte_json_para_filme(filme_json, diretor))
            except Exception as e:
                print(f'Erro no filme de id {filme_json.get("id")}: {e}')

        leitor_csv.salvar_filmes_csv(filmes)


def _converte_json_para_filme(filme_json, diretor):

    retorno = Filme(
        id_filme=int(filme_json.get('id')),
        titulo=filme_json.get('title'),
        poster_url='https://image.tmdb.org/t/p/w300_and_h450_bestv2' + filme_json.get('poster_path'),
        genero=filme_json['genres'][0]['name'] if filme_json.get('genres') else None,
        colecao=filme_json['belongs_to_collection']['name'] if filme_json.get('belongs_to_collection') else None,
        diretor=diretor,
        lingua_original=filme_json['original_language'],
        resumo=filme_json.get('overview'),
        popularidade=filme_json.get('popularity'),
        produtora=filme_json['production_companies'][0]['name'] if filme_json.get('production_companies') else None,
        pais=filme_json['production_countries'][0]['name'] if filme_json.get('production_countries') else None,
        data_lancamento=datetime.strptime(filme_json.get('release_date'), '%Y-%m-%d') if filme_json.get('release_date') != '' else None,
        orcamento=filme_json.get('budget'),
        receita=filme_json.get('revenue'),
        duracao=filme_json.get('runtime'),
        status=filme_json.get('status'),
        avaliacao=filme_json.get('vote_average'),
        qtd_avaliacoes=filme_json.get('vote_count')
    )

    return retorno
