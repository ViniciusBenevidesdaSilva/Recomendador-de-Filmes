import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from src import leitor_csv


class Recomendador:
    def __init__(self):
        self.projection = leitor_csv.obtem_dados_arquivo_csv('projection.csv')

        self.filmes = leitor_csv.obtem_dados_arquivo_csv()
        self.filmes['Data de Lançamento'] = pd.to_datetime(self.filmes['Data de Lançamento'], format='%d/%m/%Y %H:%M',
                                                           errors='coerce')

    def retorna_recomendacoes(self, filme):
        if filme.upper() not in self.filmes['Título'].str.upper().values:
            return None

        id_filme = list(self.filmes[self.filmes['Título'].str.upper() == filme.upper()]['ID'])[0]

        # Obtendo as coordenadas do filme
        coordenadas_filme = self.projection.loc[
            self.projection['ID'] == id_filme,
            self.projection.columns[self.projection.columns.str.isnumeric()]  # Seleciona colunas numéricas
        ].values[0]

        cluster = list(self.projection[self.projection['ID'] == id_filme]['cluster_pca'])[0]

        # Filtrando os filmes pelo cluster do filme de interesse, excluindo o próprio filme
        filmes_recomendados = self.projection[
            (self.projection['cluster_pca'] == cluster) & (self.projection['ID'] != id_filme)][
            self.projection.columns[self.projection.columns.str.isnumeric()]]

        # Calculando as distâncias euclidianas para todas as colunas numéricas
        filmes_recomendados['distancias'] = euclidean_distances(filmes_recomendados, [coordenadas_filme])

        # Obtendo as 10 recomendações mais próximas
        filmes_recomendados['ID'] = self.projection['ID']
        recomendacoes = filmes_recomendados.sort_values('distancias')['ID'].head(10)

        recomendacoes_detalhes = pd.merge(recomendacoes, self.filmes, on='ID')

        return recomendacoes_detalhes
