from conexao_BD import connect_database
from datetime import datetime, timedelta

client = connect_database()
db = client['clashRoyale']
collection = db['cards']

def calcular_porcentagem_vitorias_derrotas(carta, timestamp_inicial, timestamp_final):
    vitórias = 0
    derrotas = 0
    total = 0

    partidas_collection = client['clashRoyale']['battles']

    partidas = partidas_collection.find({
        'battleTime': {'$gte': timestamp_inicial, '$lte': timestamp_final},
    })

    for partida in partidas:
        total += 1
        
        # Verifique se a carta está no deck do jogador
        if carta in partida['team']['player']['deck']:
            if partida['result'] == "Jogador ganhou":
                vitórias += 1
            else:
                derrotas += 1

    return {
        'carta': carta,
        'porcentagem_vitorias': (vitórias / total) * 100 if total > 0 else 0,
        'porcentagem_derrotas': (derrotas / total) * 100 if total > 0 else 0
    }






def main(carta_escolhida, timestamp_inicial, timestamp_final):
    resultados = calcular_porcentagem_vitorias_derrotas(carta_escolhida, timestamp_inicial, timestamp_final)
    
    print(f"Carta: {resultados['carta']}")
    print(f"Porcentagem de vitórias: {resultados['porcentagem_vitorias']:.2f}%")
    print(f"Porcentagem de derrotas: {resultados['porcentagem_derrotas']:.2f}%")
    print('-' * 40)
    return resultados
