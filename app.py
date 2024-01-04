from flask import Flask, render_template, request, jsonify
from src.recomendador import Recomendador
from src.pesquisar import Pesquisador


app = Flask(__name__)
recomendador = Recomendador()
pesquisador = Pesquisador()


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        titulo_filme = request.form['titulo_filme']

        try:
            recomendacoes = recomendador.retorna_recomendacoes(titulo_filme)
            return render_template('index.html', titulo_filme=titulo_filme, recomendacoes=recomendacoes)
        except Exception as erro:
            return render_template('index.html', titulo_filme=titulo_filme, erro=erro)

    return render_template('index.html')


@app.route('/recomendacoes/<filme>', methods=['GET', 'POST'])
def recomendacoes(filme):
    if request.method == 'POST':
        filme = request.form['titulo_filme']

    try:
        recomendacoes = recomendador.retorna_recomendacoes(filme)
        return render_template('index.html', titulo_filme=filme, recomendacoes=recomendacoes)
    except Exception as erro:
        return render_template('index.html', titulo_filme=filme, erro=erro)


@app.route('/get_sugestoes', methods=['GET'])
def get_sugestoes():
    titulo_pesquisado = request.args.get('inputText')

    if len(titulo_pesquisado) < 3:
        return jsonify([])

    sugestoes = pesquisador.obtem_lista_titulo_pesquisado(titulo_pesquisado=titulo_pesquisado)

    return jsonify(sugestoes)


if __name__ == '__main__':
    app.run(debug=True)
