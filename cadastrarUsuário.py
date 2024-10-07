import requests
from conexao_BD import connect_database 

API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImUyZjZjMmFjLTM0ZmMtNDdlZC04ZmRhLWIwYWYxOTQ4M2Y0ZiIsImlhdCI6MTcyODA4MjI0Mywic3ViIjoiZGV2ZWxvcGVyLzNiOWRkYzI3LTg3ZjAtMGNlYy0zZTRjLTIwZWRkZThmYzYxNiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNzkuMjM1LjIxMS40NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.MXR3bSmT1P_bBMJwQpN7PLMvVmzg9enTZGUc8ofP_ul7qlkoD227l9U0-M6VO6kBcV9fdx6DzWDI-aFrMTXs1A'  # Use a chave correta da API
player_tag = 'GC99VQPLP'
url = f'https://api.clashroyale.com/v1/players/%23{player_tag}/battlelog'

headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImUyZjZjMmFjLTM0ZmMtNDdlZC04ZmRhLWIwYWYxOTQ4M2Y0ZiIsImlhdCI6MTcyODA4MjI0Mywic3ViIjoiZGV2ZWxvcGVyLzNiOWRkYzI3LTg3ZjAtMGNlYy0zZTRjLTIwZWRkZThmYzYxNiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxNzkuMjM1LjIxMS40NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.MXR3bSmT1P_bBMJwQpN7PLMvVmzg9enTZGUc8ofP_ul7qlkoD227l9U0-M6VO6kBcV9fdx6DzWDI-aFrMTXs1A'  # Use a chave correta da API
}

response = requests.get(url, headers=headers)


if response.status_code == 200:
    data = response.json()
    if data:
        print("Dados coletados com sucesso!")
        print(data) 
    else:
        print("Nenhum dado encontrado.")
else:
    print(f"Erro ao coletar dados: {response.status_code} - {response.text}")




