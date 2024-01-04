import pandas as pd
import numpy as np
import time
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from src.leitor_csv import obtem_dados_arquivo_csv, salvar_data_frame

SEED = 123
np.random.seed(SEED)


def gera_clusters_filmes():
    start_time = time.time()

    print(f'Leitura arquivo')
    dados_filmes = obtem_dados_arquivo_csv(nome_arquivo='filmes.csv')

    _imprime_proxima_etapa('Tratando dados originais', start_time)
    dados_tratados = _realiza_tratamento_dados_filmes(dados=dados_filmes)

    _imprime_proxima_etapa('Corrigindo textos com OneHotEncoder', start_time)
    dados_tratados = _corrige_colunas_texto(dados_tratados)

    _imprime_proxima_etapa('Aplicando PCA para padronização', start_time)
    projection, pca_pipeline = _obtem_pca(dados_tratados)

    _imprime_proxima_etapa('Criando Clusters', start_time)
    projection = _obtem_cluter_kmeans(projection)
    projection['ID'] = dados_filmes['ID']

    _imprime_proxima_etapa('Salvando arquivos', start_time)
    salvar_data_frame(projection, 'projection.csv')

    _imprime_proxima_etapa('Concluído!', start_time)

    return projection, pca_pipeline


def _imprime_proxima_etapa(descricao_etapa, start_time):
    print(f"--- {(time.time() - start_time):.2f} seconds ---")
    print(descricao_etapa)


def _realiza_tratamento_dados_filmes(dados):
    retorno = dados.copy()

    _exclui_colunas(retorno)
    _preenche_nulos(retorno)
    _corrige_formato(retorno)
    _cria_colunas(retorno)

    return retorno


def _exclui_colunas(dados):
    dados.drop(['ID', 'Título', 'URL do Poster', 'Resumo'], axis=1, inplace=True)


def _preenche_nulos(dados):
    dados['Coleção'].fillna('Não Definido', inplace=True)
    dados['Diretor'].fillna('Não Definido', inplace=True)
    dados['Produtora'].fillna('Não Definido', inplace=True)
    dados['País'].fillna('Não Definido', inplace=True)


def _corrige_formato(dados):
    dados['Data de Lançamento'] = pd.to_datetime(dados['Data de Lançamento'], format='%d/%m/%Y %H:%M', errors='coerce')
    dados['Popularidade'] = dados['Popularidade'].str.replace(',', '.').astype(float)
    dados['Orçamento'] = dados['Orçamento'].str.replace(',', '.').astype(float)
    dados['Receita'] = dados['Receita'].str.replace(',', '.').astype(float)
    dados['Avaliação'] = dados['Avaliação'].str.replace(',', '.').astype(float)
    dados['Quantidade de Avaliações'] = dados['Quantidade de Avaliações'].astype(int)


def _cria_colunas(dados):
    # Ano de lançamento
    dados['Ano Lançamento'] = dados['Data de Lançamento'].dt.year
    dados.drop(['Data de Lançamento'], axis=1, inplace=True)

    # Total Avaliação
    dados['Nota'] = dados['Avaliação'] * dados['Quantidade de Avaliações']


def _corrige_colunas_texto(dados):
    colunas_texto = dados.select_dtypes(include=['object']).columns

    for coluna in colunas_texto:
        dados = _gera_dummies(dados, coluna)

    return dados


def _gera_dummies(dados, coluna, top_n=200):
    # Seleciono apenas os top_n mais presentes naquela coluna, a fim de gerar os dados dummy
    contagem_valores = dados[coluna].value_counts()
    valores_top_n = contagem_valores.head(top_n).index.tolist()
    dados[coluna] = dados[coluna].where(dados[coluna].isin(valores_top_n), other='Outros')

    # Aplico o OneHotEncoder na coluna
    ohe = OneHotEncoder(dtype=int)
    coluna_encoded = ohe.fit_transform(dados[[coluna]]).toarray()
    dados = pd.concat([dados, pd.DataFrame(coluna_encoded, columns=ohe.get_feature_names_out([coluna]))], axis=1)
    dados.drop(coluna, axis=1, inplace=True)

    return dados


def _obtem_pca(dados):
    pca_pipeline = Pipeline([('scaler', StandardScaler()), ('PCA', PCA(n_components=0.7, random_state=SEED))])
    embedding_pca = pca_pipeline.fit_transform(dados)
    projection = pd.DataFrame(data=embedding_pca)

    return projection, pca_pipeline


def _obtem_cluter_kmeans(projection, n_clusters=100):
    kmeans_pca = KMeans(n_clusters=n_clusters, n_init=100, verbose=False, random_state=SEED)
    kmeans_pca.fit(projection)

    projection['cluster_pca'] = kmeans_pca.predict(projection)

    return projection

