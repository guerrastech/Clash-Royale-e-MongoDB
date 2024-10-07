from conexao_BD import connect_database
from datetime import datetime

client = connect_database()
collection = client['clashRoyale']['battles']

def contar_derrotas_por_combo(combo_de_cartas, start_date, end_date):
    start_timestamp = datetime.strptime(start_date, "%Y-%m-%d")
    end_timestamp = datetime.strptime(end_date, "%Y-%m-%d")
    
    combo_set = set(combo_de_cartas)

    batalhas = collection.find({
        "battleTime": {
            "$gte": start_timestamp,
            "$lte": end_timestamp
        }
    })

    total_derrotas = 0

    for battle in batalhas:
        player_deck = set(battle['team']['player']['deck'])
        
        if combo_set.issubset(player_deck):
            if battle['result'] != 'Jogador ganhou':
                total_derrotas += 1

    return total_derrotas
