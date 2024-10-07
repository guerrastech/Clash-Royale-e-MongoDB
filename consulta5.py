from conexao_BD import connect_database
from itertools import combinations
from datetime import datetime
from collections import defaultdict

client = connect_database()
collection = client['clashRoyale']['battles']

def listar_combos_cartas(tamanho_combo, percentual_vitorias, start_date, end_date):
    start_timestamp = datetime.strptime(start_date, "%Y-%m-%d")
    end_timestamp = datetime.strptime(end_date, "%Y-%m-%d")

    # Buscar as batalhas dentro do intervalo de datas
    batalhas = collection.find({
        "battleTime": {
            "$gte": start_timestamp,
            "$lte": end_timestamp
        }
    })

    # Dicionário para armazenar estatísticas de combos
    combos_stats = defaultdict(lambda: {'vitorias': 0, 'derrotas': 0})

    # Processar cada batalha
    for battle in batalhas:
        if 'team' in battle:
            # Verifique se o jogador possui cartas
            if 'player' in battle['team'] and 'deck' in battle['team']['player']:
                dados_jogador = battle['team']['player']
                # Acessa o deck do jogador
                deck = dados_jogador['deck']

                # Verifica a estrutura do deck
                print(f"Deck do jogador: {deck}")  
                
                # Acessa o resultado da batalha
                result = 'vitorias' if battle['result'] == "Jogador ganhou" else 'derrotas'

                # Gerar combinações de cartas
                for combo in combinations(deck, tamanho_combo):
                    combo_nomes = tuple(sorted(combo)) 
                    combos_stats[combo_nomes][result] += 1

    # Filtrar combos que atendem ao critério de percentual de vitórias
    combos_finais = {}
    for combo, stats in combos_stats.items():
        total_battles = stats['vitorias'] + stats['derrotas']
        if total_battles > 0:
            win_rate = (stats['vitorias'] / total_battles) * 100
            if win_rate > percentual_vitorias:
                combos_finais[combo] = win_rate

    return combos_finais
