from flask import Flask, render_template, request, jsonify
from conexao_BD import connect_database
from consulta1 import calcular_porcentagem_vitorias_derrotas
from consulta2 import listar_decks_com_vitória
from consulta3 import contar_derrotas_por_combo
from consulta4 import calcular_vitorias_carta_especifica
from consulta5 import listar_combos_cartas
from datetime import datetime

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/estatisticas', methods=['GET', 'POST'])
def estatisticas():
    client = connect_database()
    db = client['clashRoyale']
    cards_collection = db['cards']
    cartas = list(cards_collection.find({}, {'_id': 0, 'name': 1}))

    resultados = None  # Inicialize resultados
    decks_resultados = None

    if request.method == 'POST':

        if 'cartas_combo' in request.form:
            cartas_combo = request.form.getlist('cartas_combo')  
            data_inicio = request.form['data_inicio']
            data_fim = request.form['data_fim']
            timestamp_inicial = data_inicio 
            timestamp_final = data_fim

            
            resultados = contar_derrotas_por_combo(cartas_combo, timestamp_inicial, timestamp_final)
            return jsonify({'total_derrotas': resultados})

        # Verifica se a requisição é para listar decks
        if 'min_vitoria_percentage' in request.form:
            min_vitoria_percentage = float(request.form['min_vitoria_percentage'])
            data_inicio = request.form['data_inicio']
            data_fim = request.form['data_fim']
            decks_resultados = listar_decks_com_vitória(min_vitoria_percentage, data_inicio, data_fim)
            
            if decks_resultados:
                decks_resultados = {str(k): v for k, v in decks_resultados.items()}

            return jsonify(decks_resultados)

        #Verifica se uma carta específica foi enviada
        if 'carta' in request.form:
            carta = request.form['carta']
            data_inicio = request.form['data_inicio']
            data_fim = request.form['data_fim']
            timestamp_inicial = int(datetime.strptime(data_inicio, '%Y-%m-%d').timestamp())
            timestamp_final = int(datetime.strptime(data_fim, '%Y-%m-%d').timestamp())
            
            # Chama a função para calcular a porcentagem de vitórias e derrotas
            resultados = calcular_porcentagem_vitorias_derrotas(carta, timestamp_inicial, timestamp_final)
            return jsonify(resultados)  # Retorna os resultados em formato JSON
    
        if 'tamanho_combo' in request.form and 'percentual_vitorias' in request.form:
            tamanho_combo = int(request.form['tamanho_combo'])
            percentual_vitorias = float(request.form['percentual_vitorias'])
            data_inicio = request.form['data_inicio']
            data_fim = request.form['data_fim']

            combos_resultados = listar_combos_cartas(tamanho_combo, percentual_vitorias, data_inicio, data_fim)
            combos_resultados = {str(key): value for key, value in combos_resultados.items()}
            return jsonify(combos_resultados)

        # if '1' in request.form and 'percentual_trofeus' in request.form:
        #     carta = request.form['carta']
        #     percentual_trofeus = float(request.form['percentual_trofeus'])
        #     duracao_maxima = float(request.form['duracao_maxima'])  # em minutos
        #     data_inicio = request.form['data_inicio']
        #     data_fim = request.form['data_fim']

        #     resultados = calcular_vitorias_carta_especifica(carta, percentual_trofeus, duracao_maxima, data_inicio, data_fim)
        #     return jsonify({'total_vitorias': resultados})

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    return render_template('estatisticas.html', cartas=cartas, resultados=resultados, decks_resultados=decks_resultados)







def calcular_porcentagem_vitorias_derrotas(carta, timestamp_inicial, timestamp_final):
    client = connect_database()
    db = client['clashRoyale']
    partidas_collection = db['battles']  # Altere para o nome correto da coleção

    vitorias = 0
    derrotas = 0
    
    partidas = partidas_collection.find({
        'timestamp': {
            '$gte': timestamp_inicial,
            '$lte': timestamp_final
        },
        'cartas': carta
    })

    for partida in partidas:
        if partida['resultado'] == 'vitoria':
            vitorias += 1
        elif partida['resultado'] == 'derrota':
            derrotas += 1

    total_partidas = vitorias + derrotas
    if total_partidas > 0:
        porcentagem_vitorias = (vitorias / total_partidas) * 100
        porcentagem_derrotas = (derrotas / total_partidas) * 100
    else:
        porcentagem_vitorias = 0
        porcentagem_derrotas = 0

    return {
        'carta': carta,
        'porcentagem_vitorias': porcentagem_vitorias,
        'porcentagem_derrotas': porcentagem_derrotas,
        'total_partidas': total_partidas
    }





@app.route('/cards')
def cards():
    client = connect_database()
    db = client['clashRoyale']
    cards_collection = db['cards']

    # Coleta as cartas do banco de dados
    cartas = list(cards_collection.find())
    
    return render_template('cards.html', cartas=cartas)

if __name__ == '__main__':
    app.run(debug=True)
