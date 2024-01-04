from src import leitor_csv


class Pesquisador:
    def __init__(self):
        self.titulos = leitor_csv.obtem_dados_arquivo_csv()['Título'].tolist()

    def obtem_lista_titulo_pesquisado(self, titulo_pesquisado):
        filmes_filtrados = [titulo for titulo in self.titulos if titulo.lower().startswith(titulo_pesquisado.lower())]
        return filmes_filtrados

