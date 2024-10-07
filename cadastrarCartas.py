import requests
from conexao_BD import connect_database


client = connect_database()
db = client['clashRoyale']
collection = db['cards']

url = 'https://api.clashroyale.com/v1/cards'
headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImUyZjZjMmFjLTM0ZmMtNDdlZC04ZmRhLWIwYWYxOTQ4M2Y0ZiIsImlhdCI6MTcyODA4MjI0Mywic3ViIjoiZGV2ZWxvcGVyLzNiOWRkYzI3LTg3ZjAtMGNlYy0zZTRjLTIwZWRkZThmYzYxNiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNzkuMjM1LjIxMS40NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.MXR3bSmT1P_bBMJwQpN7PLMvVmzg9enTZGUc8ofP_ul7qlkoD227l9U0-M6VO6kBcV9fdx6DzWDI-aFrMTXs1A'  # Use a chave correta da API}'  # Substitua pela sua chave
}
response = requests.get(url, headers=headers)



if response.status_code == 200:
    data = response.json()
    cartas = data['items'] 

    for carta in cartas:
        carta_doc = {
            "name": carta['name'],
            "id": carta['id'],
            "icon_url": carta['iconUrls']['medium'],
            "rarity": carta['rarity'],
            "victories": 0, 
            "defeats": 0,
            "winrate": 0
        }
        collection.update_one({"name": carta['name']}, {"$set": carta_doc}, upsert=True)

    print("Cartas cadastradas com sucesso!")
else:
    print(f"Erro ao coletar dados: {response.status_code} - {response.text}")
