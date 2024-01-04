import locale

locale.setlocale(locale.LC_NUMERIC, 'pt_BR.UTF-8')


class Filme:
    def __init__(self, id_filme, titulo, poster_url, genero, colecao, diretor, lingua_original, resumo, popularidade,
                 produtora, pais, data_lancamento, orcamento, receita, duracao, status, avaliacao, qtd_avaliacoes):
        self.id_filme = id_filme
        self.titulo = titulo
        self.poster_url = poster_url
        self.genero = genero
        self.colecao = colecao
        self.diretor = diretor
        self.lingua_original = lingua_original
        self.resumo = resumo
        self.popularidade = popularidade
        self.produtora = produtora
        self.pais = pais
        self.data_lancamento = data_lancamento
        self.orcamento = orcamento
        self.receita = receita
        self.duracao = duracao
        self.status = status
        self.avaliacao = avaliacao
        self.qtd_avaliacoes = qtd_avaliacoes

    def __str__(self):
        return f"{self.titulo} ({self.data_lancamento.year}) - {self.genero}"

    def to_dict(self):
        return {
            'ID': self.id_filme,
            'Título': self.titulo,
            'URL do Poster': self.poster_url,
            'Gênero': self.genero,
            'Coleção': self.colecao,
            'Diretor': self.diretor,
            'Língua Original': self.lingua_original,
            'Resumo': self.resumo,
            'Popularidade': locale.format_string("%.3f", self.popularidade, grouping=True),
            'Produtora': self.produtora,
            'País': self.pais,
            'Data de Lançamento': self.data_lancamento,
            'Orçamento': locale.format_string("%.2f", self.orcamento, grouping=True),
            'Receita': locale.format_string("%.2f", self.receita, grouping=True),
            'Duração': self.duracao,
            'Status': self.status,
            'Avaliação': locale.format_string("%.3f", self.avaliacao, grouping=True),
            'Quantidade de Avaliações': self.qtd_avaliacoes
        }
