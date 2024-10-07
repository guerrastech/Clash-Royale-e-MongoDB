from conexao_BD import connect_database
from datetime import datetime

client = connect_database()
db = client['clashRoyale']
partidas_collection = db['battles']

def calcular_porcentagem_vitorias_derrotas(carta, timestamp_inicial, timestamp_final):
    vitórias = 0
    derrotas = 0
    total = 0

    # Consulta para filtrar as partidas pelo intervalo de tempo
    partidas = partidas_collection.find({
        'battleTime': {'$gte': datetime.utcfromtimestamp(timestamp_inicial / 1000), '$lte': datetime.utcfromtimestamp(timestamp_final / 1000)}
    })

    # Loop através das partidas para contar vitórias e derrotas
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
        'porcentagem_derrotas': (derrotas / total) * 100 if total > 0 else 0,
        'total_partidas': total
    }

# Testando a função 

data_inicio = datetime(2024, 10, 1)
data_fim = datetime(2024, 10, 8)
timestamp_inicial = int(data_inicio.timestamp() * 1000)
timestamp_final = int(data_fim.timestamp() * 1000)

carta_teste = 'Valkyrie'
resultado = calcular_porcentagem_vitorias_derrotas(carta_teste, timestamp_inicial, timestamp_final)

print(resultado)
