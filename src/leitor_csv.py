import os
import csv
import pandas as pd

caminho_filmes = os.path.join(os.getcwd(), 'data', 'filmes.csv')


def cria_arquivos_filmes_csv():
    with open(caminho_filmes, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['ID', 'Título', 'URL do Poster', 'Gênero', 'Coleção', 'Diretor', 'Língua Original', 'Resumo',
                      'Popularidade', 'Produtora', 'País', 'Data de Lançamento', 'Orçamento', 'Receita', 'Duração',
                      'Status', 'Avaliação', 'Quantidade de Avaliações']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()


def salvar_filmes_csv(filmes):
    with open(caminho_filmes, 'a', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['ID', 'Título', 'URL do Poster', 'Gênero', 'Coleção', 'Diretor', 'Língua Original', 'Resumo',
                      'Popularidade', 'Produtora', 'País', 'Data de Lançamento', 'Orçamento', 'Receita', 'Duração',
                      'Status', 'Avaliação', 'Quantidade de Avaliações']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        for filme in filmes:
            writer.writerow(filme.to_dict())


def obtem_dados_arquivo_csv(nome_arquivo='filmes.csv'):
    caminho = os.path.join(os.getcwd(), 'data', nome_arquivo)
    return pd.read_csv(caminho, sep=';')
