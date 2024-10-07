from pymongo import MongoClient
from conexao_BD import connect_database


client = connect_database()
collection = client['clashRoyale']['battles']

def calcular_vitorias_carta_especifica(carta, percentual_trofeus, duracao_maxima):
    client = connect_database()
    db = client['clashRoyale']
    partidas_collection = db['battles']  # Nome da coleção de partidas
    
    # Filtro de vitórias envolvendo a carta X e outras condições
    pipeline = [
        {
            '$match': {
                'team.player.deck': carta,  # O vencedor usou a carta X
                'battleDuration': {'$lt': duracao_maxima},  # Partida durou menos de 120 segundos
                'team.opponent.leagueNumber': {'$gte': 2},  # Perdedor destruiu ao menos duas torres
                '$expr': {
                    # Verifica se o vencedor tem Z% menos troféus que o perdedor
                    '$lt': [
                        '$team.player.trofeus',
                        {'$multiply': ['$team.opponent.trofeus', 1 - percentual_trofeus / 100]}
                    ]
                }
            }
        },
        {
            '$count': 'total_vitorias'  # Conta o número de vitórias que satisfazem os critérios
        }
    ]
    
    # Executa a consulta agregada no MongoDB
    resultado = list(partidas_collection.aggregate(pipeline))
    
    if resultado:
        print(resultado)
        return resultado[0]['total_vitorias']
    else:
        return 0  

def testar_calcular_vitorias():
    carta = "Valkyrie"  
    percentual_trofeus = 10  
    duracao_maxima = 120 

    total_vitorias = calcular_vitorias_carta_especifica(carta, percentual_trofeus, duracao_maxima)
    
    print(f'Total de vitórias para a carta {carta}: {total_vitorias}')


testar_calcular_vitorias()
