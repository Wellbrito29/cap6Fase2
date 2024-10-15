# Importação dos módulos
import os
import oracledb
import pandas as pd
from api_climatica import coletar_dados_climaticos
from datetime import datetime
from db import criar_tabela, inserir_dados, consultar_dados, converter_dados
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


# Gerar dados simulados de rendimento da colheita de cana
def gerar_rendimento_simulado(temperaturas, precipitacoes):
    rendimento_cana = (
        (0.5 * temperaturas)
        - (0.3 * precipitacoes)
        + np.random.normal(0, 5, len(temperaturas))
    )
    rendimento_cana = np.maximum(rendimento_cana, 0)
    return rendimento_cana


# Função principal
def main():
    # Tentar conexão com o Banco de Dados
    try:
        conn = oracledb.connect(
            user="RM552157", password="140492", dsn="oracle.fiap.com.br:1521/ORCL"
        )
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return  # Encerrar a execução em caso de erro na conexão
    else:
        print("Conexão com o Banco de Dados estabelecida com sucesso!")

        # Leitura das coordenadas de latitude e longitude do arquivo JSON
        try:
            with open("../config/latlong.json", "r") as arquivo:
                dados = json.load(arquivo)
                latitude = dados["lat"]
                longitude = dados["long"]
                print(
                    f"Dados carregados com sucesso: Latitude: {latitude}, Longitude: {longitude}"
                )
        except Exception as e:
            print("Erro ao ler o arquivo de configuração:", e)

        # Criar a tabela caso ainda não exista
        criar_tabela(conn)

        # Coletar dados climáticos para a localização especificada
        temperaturas, precipitacoes = coletar_dados_climaticos(latitude, longitude)

        # Verificar se houve sucesso na coleta dos dados
        if temperaturas and precipitacoes:
            try:
                # Inserir dados no banco de dados
                for i in range(len(temperaturas)):
                    inserir_dados(
                        conn, datetime.now(), temperaturas[i], precipitacoes[i]
                    )
            except Exception as e:
                print("Erro ao inserir dados no banco:", e)
        else:
            print("Erro: Dados climáticos não foram coletados com sucesso.")

        # Consultar dados e converter para DataFrame
        df = converter_dados(conn)

        # Predição básica usando Regressão Linear
        if not df.empty and "temperatura" in df.columns:
            # Criar uma variável de índice de tempo
            df["indice_tempo"] = range(len(df))

            # Dividir dados em features (X) e target (y)
            X = df[["indice_tempo"]]  # Variável independente
            y = df["temperatura"]  # Variável dependente

            # Dividir dados em treino e teste
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # Criar e treinar o modelo de Regressão Linear
            modelo = LinearRegression()
            modelo.fit(X_train, y_train)

            # Fazer predições
            predicoes = modelo.predict(X_test)

            # Visualizar os resultados da temperatura
            plt.figure(figsize=(10, 6))
            plt.scatter(X_test, y_test, color="blue", label="Temperatura Real")
            plt.plot(X_test, predicoes, color="red", label="Temperatura Predita")
            plt.xlabel("Índice de Tempo")
            plt.ylabel("Temperatura")
            plt.title("Predição de Temperatura com Regressão Linear")
            plt.legend()

            # Salvar gráfico de temperatura
            plt.savefig("resultado_predicao_temperatura.png")
            plt.close()  # Fechar a figura após salvar

            # Agora gerar dados simulados para rendimento da cana
            rendimento_cana = gerar_rendimento_simulado(
                df["temperatura"], df["precipitacao"]
            )

            # Criar um DataFrame para os dados simulados
            df_rendimento = pd.DataFrame(
                {
                    "temperatura": df["temperatura"],
                    "precipitacao": df["precipitacao"],
                    "rendimento_cana": rendimento_cana,
                }
            )

            # Treinar um modelo de regressão linear para prever o rendimento da cana
            X_rendimento = df_rendimento[
                ["temperatura", "precipitacao"]
            ]  # Variáveis independentes
            y_rendimento = df_rendimento["rendimento_cana"]  # Variável dependente

            # Criar e treinar o modelo de regressão
            modelo_rendimento = LinearRegression()
            modelo_rendimento.fit(X_rendimento, y_rendimento)

            # Fazer predições com base nas temperaturas e precipitações
            y_pred_rendimento = modelo_rendimento.predict(X_rendimento)

            # Exibir o gráfico com os valores reais e previstos
            plt.figure(figsize=(10, 6))
            plt.plot(
                df_rendimento.index, y_rendimento, label="Rendimento Real", color="blue"
            )
            plt.plot(
                df_rendimento.index,
                y_pred_rendimento,
                label="Rendimento Previsto",
                color="red",
                linestyle="--",
            )
            plt.xlabel("Observações")
            plt.ylabel("Rendimento da Cana")
            plt.legend()
            plt.title(
                "Simulação de Impacto Climático no Rendimento da Colheita de Cana"
            )

            # Salvar gráfico de rendimento
            plt.savefig("resultado_predicao_rendimento.png")
            plt.close()  # Fechar a figura após salvar

            # Exibir coeficientes do modelo
            print("Coeficiente de Temperatura:", modelo_rendimento.coef_[0])
            print("Coeficiente de Precipitação:", modelo_rendimento.coef_[1])


# Executar a função principal
if __name__ == "__main__":
    main()
