from conexao_BD import connect_database 
import requests
from datetime import datetime, timedelta

client = connect_database()
db = client['clashRoyale']
collection = db['battles']
cards_collection = db['cards']  

player_tag = 'QJRU92L'
url = f'https://api.clashroyale.com/v1/players/%23{player_tag}/battlelog'

headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImUyZjZjMmFjLTM0ZmMtNDdlZC04ZmRhLWIwYWYxOTQ4M2Y0ZiIsImlhdCI6MTcyODA4MjI0Mywic3ViIjoiZGV2ZWxvcGVyLzNiOWRkYzI3LTg3ZjAtMGNlYy0zZTRjLTIwZWRkZThmYzYxNiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNzkuMjM1LjIxMS40NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.MXR3bSmT1P_bBMJwQpN7PLMvVmzg9enTZGUc8ofP_ul7qlkoD227l9U0-M6VO6kBcV9fdx6DzWDI-aFrMTXs1A'  # Use a chave correta da API' 
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    dados_batalha = response.json()
    if dados_batalha:
        print("Dados coletados com sucesso!")
    else:
        print("Nenhum dado encontrado.")
else:
    print(f"Erro ao coletar dados: {response.status_code} - {response.text}")

for battle in dados_batalha:
    dados_jogador = battle['team'][0]
    dados_adversario = battle['opponent'][0]

    # Determinando o resultado
    if dados_jogador['crowns'] > dados_adversario['crowns']:
        result = 'Jogador ganhou'
        victory = True
    elif dados_jogador['crowns'] < dados_adversario['crowns']:
        result = 'Jogador perdeu'
        victory = False
    else:
        vida_do_jogador = dados_jogador['kingTowerHitPoints'] + sum(filter(None, dados_jogador.get('princessTowersHitPoints', [])))
        vida_do_oponente = dados_adversario['kingTowerHitPoints'] + sum(filter(None, dados_adversario.get('princessTowersHitPoints', [])))
        
        if vida_do_jogador > vida_do_oponente:
            result = 'Jogador ganhou'
            victory = True
        elif vida_do_jogador < vida_do_oponente:
            result = 'Jogador perdeu'
            victory = False
        else:
            result = 'Empate'
            victory = None  

    # Convertendo battleTime para datetime
    battle_time = datetime.strptime(battle['battleTime'], "%Y%m%dT%H%M%S.%fZ")
    battle_duration = timedelta(minutes=3)  # Duração padrão de batalha (3 minutos)

    player_document = {
        "tag": dados_jogador['tag'],
        "name": dados_jogador['name'],
        "elixirLeaked": dados_jogador['elixirLeaked'],
        "deck": [card['name'] for card in dados_jogador['cards']],
        "supportCards": [card['name'] for card in dados_jogador['supportCards']],
    }
    db.players.update_one({"tag": player_document["tag"]}, {"$set": player_document}, upsert=True)

    if victory is not None:  
        for card in dados_jogador['cards']:
            card_name = card['name']
            if victory:  
                cards_collection.update_one(
                    {"name": card_name},
                    {"$inc": {"victories": 1}},
                    upsert=True  
                )
            else: 
                cards_collection.update_one(
                    {"name": card_name},
                    {"$inc": {"defeats": 1}},
                    upsert=True 
                )

            carta = cards_collection.find_one({"name": card_name})
            total_battles = carta['victories'] + carta['defeats']
            winrate = (carta['victories'] / total_battles * 100) if total_battles > 0 else 0
            
            cards_collection.update_one(
                {"name": card_name},
                {"$set": {"winrate": winrate}}
            )

    battle_document = {
        "type": battle['type'],
        "battleTime": battle_time,
        "battleDuration": battle_duration.total_seconds(),  # Duração em segundos
        "team": {
            "player": {
                "tag": dados_jogador['tag'],
                "name": dados_jogador['name'],
                "deck": player_document['deck']
            },
            "opponent": {
                "tag": dados_adversario['tag'],
                "name": dados_adversario['name'],
                "deck": [card['name'] for card in dados_adversario['cards']]
            }
        },
        "leagueNumber": battle['leagueNumber'],
        "result": result  
    }
    collection.insert_one(battle_document)

print("Dados inseridos com sucesso!")
