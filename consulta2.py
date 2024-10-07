from conexao_BD import connect_database
from datetime import datetime

client = connect_database()
collection = client['clashRoyale']['battles']

def listar_decks_com_vitória(min_vitoria_percentage, start_date, end_date):
    start_timestamp = datetime.strptime(start_date, "%Y-%m-%d")
    end_timestamp = datetime.strptime(end_date, "%Y-%m-%d")
    
    
    batalhas = collection.find({
        "battleTime": {
            "$gte": start_timestamp,
            "$lte": end_timestamp
        }
    })

   
    decks_stats = {}

    for battle in batalhas:
        player_deck = tuple(battle['team']['player']['deck'])  
        opponent_deck = tuple(battle['team']['opponent']['deck'])

        
        if player_deck not in decks_stats:
            decks_stats[player_deck] = {"victories": 0, "defeats": 0}
        
       
        if battle['result'] == 'Jogador ganhou':
            decks_stats[player_deck]["victories"] += 1
        else:
            decks_stats[player_deck]["defeats"] += 1

    
    decks_com_boa_vitoria = {}
    for deck, stats in decks_stats.items():
        total_battles = stats["victories"] + stats["defeats"]
        if total_battles > 0:
            win_rate = (stats["victories"] / total_battles) * 100
            if win_rate > min_vitoria_percentage:
                decks_com_boa_vitoria[deck] = win_rate

    return decks_com_boa_vitoria



