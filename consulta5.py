from conexao_BD import connect_database
from itertools import combinations
from datetime import datetime
from collections import defaultdict

client = connect_database()
collection = client['clashRoyale']['battles']

def listar_combos_cartas(tamanho_combo, percentual_vitorias, start_date, end_date):
    start_timestamp = datetime.strptime(start_date, "%Y-%m-%d")
    end_timestamp = datetime.strptime(end_date, "%Y-%m-%d")

    
    batalhas = collection.find({
        "battleTime": {
            "$gte": start_timestamp,
            "$lte": end_timestamp
        }
    })

    
    combos_stats = defaultdict(lambda: {'vitorias': 0, 'derrotas': 0})

    for battle in batalhas:
        
        if 'team' in battle and 'player' in battle['team'] and 'opponent' in battle['team']:
            dados_jogador = battle['team']['player']
            dados_adversario = battle['team']['opponent']
            
            
            if 'crowns' in dados_jogador and 'crowns' in dados_adversario:
                if dados_jogador['crowns'] > dados_adversario['crowns']:
                    result = 'vitoria'
                else:
                    result = 'derrota'

                
                if 'cards' in dados_jogador:
                    for combo in combinations(dados_jogador['cards'], tamanho_combo):
                        combo_nomes = tuple(sorted(card['name'] for card in combo))
                        combos_stats[combo_nomes][result] += 1


    combos_finais = {}
    for combo, stats in combos_stats.items():
        total_battles = stats['vitorias'] + stats['derrotas']
        if total_battles > 0:
            win_rate = (stats['vitorias'] / total_battles) * 100
            if win_rate > percentual_vitorias:
                combos_finais[combo] = win_rate

    return combos_finais


tamanho_combo = 3  
percentual_vitorias = 60  
start_date = "2024-01-01"  
end_date = "2024-12-31"  

combos_vitoriosos = listar_combos_cartas(tamanho_combo, percentual_vitorias, start_date, end_date)

print("Combos de cartas que produziram mais de {}% de vitórias:".format(percentual_vitorias))
for combo, win_rate in combos_vitoriosos.items():
    print(f"Combo: {combo}, Taxa de Vitória: {win_rate:.2f}%")
