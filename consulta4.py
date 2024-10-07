from conexao_BD import connect_database
from datetime import datetime

client = connect_database()
collection = client['clashRoyale']['battles']

def contar_vitorias_com_carta(carta, percentual_trofeus, duracao_maxima, start_date, end_date):
    start_timestamp = datetime.strptime(start_date, "%Y-%m-%d")
    end_timestamp = datetime.strptime(end_date, "%Y-%m-%d")

    
    trofeus_limite = 1 - (percentual_trofeus / 100.0)

    
    batalhas = collection.find({
        "battleTime": {
            "$gte": start_timestamp,
            "$lte": end_timestamp
        }
    })

    total_vitorias = 0

    for battle in batalhas:
       
        battle_time = battle['battleTime']
        duracao_batalha = (battle_time - start_timestamp).seconds / 60  
        
        if duracao_batalha < duracao_maxima:
            dados_jogador = battle['team']['player']
            dados_adversario = battle['team']['opponent']

           
            torres_derrubadas = dados_adversario['crowns'] 
            trofeus_jogador = dados_jogador['startingTrophies']
            trofeus_adversario = dados_adversario['startingTrophies']

            
            if (
                trofeus_jogador * trofeus_limite < trofeus_adversario and
                torres_derrubadas >= 2 and
                carta in [card['name'] for card in dados_jogador['cards']]
            ):
                total_vitorias += 1

    return total_vitorias


carta = "Barbarians"  
percentual_trofeus = 20 
duracao_maxima = 2  
start_date = "2024-01-01"  
end_date = "2024-12-31"  

vitorias = contar_vitorias_com_carta(carta, percentual_trofeus, duracao_maxima, start_date, end_date)

print(f"Total de vitórias envolvendo a carta {carta}: {vitorias}")
