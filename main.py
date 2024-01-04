from src.recomendador import Recomendador

filmes = Recomendador().retorna_recomendacoes(filme="O Iluminado")

print('Recomendações Detalhadas:\n')

for index, row in filmes.iterrows():
    print(f'Título: {row["Título"]}')
    print(f'Gênero: {row["Gênero"]}')
    print(f'Ano de Lançamento: {row["Data de Lançamento"].year}')
    print('------------------------------')
