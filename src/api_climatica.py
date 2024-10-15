import requests


def coletar_dados_climaticos(latitude, longitude):

    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation"
        resposta = requests.get(url)
        dados = resposta.json()

        # Extrair dados de interesse (temperatura, precipitação, etc.)
        temperatura = dados["hourly"]["temperature_2m"]
        precipitacao = dados["hourly"]["precipitation"]

        print("Dados climáticos coletados com sucesso!")
        return temperatura, precipitacao
    except Exception as e:
        print("Erro ao coletar dados climáticos:", e)
        return None
