import pandas as pd


# db.py
def criar_tabela(conn):
    try:
        cursor = conn.cursor()
        # Verifica se a tabela já existe
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM all_tables
            WHERE table_name = 'DADOS_CLIMATICOS'
        """
        )
        count = cursor.fetchone()[0]

        if count == 0:  # A tabela não existe
            cursor.execute(
                """
                CREATE TABLE dados_climaticos (
                    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                    data_hora TIMESTAMP,
                    temperatura NUMBER,
                    precipitacao NUMBER
                )
            """
            )
            conn.commit()
            print("Tabela criada com sucesso!")
        else:
            print("A tabela 'dados_climaticos' já existe.")
    except Exception as e:
        print("Erro ao criar tabela:", e)


def inserir_dados(conn, data_hora, temperatura, precipitacao):
    print("Aguarde inserindo dados no banco de dados!")

    try:

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO dados_climaticos (data_hora, temperatura, precipitacao)
            VALUES (:1, :2, :3)
        """,
            (data_hora, temperatura, precipitacao),
        )
        conn.commit()
    except Exception as e:
        print("Erro ao inserir dados:", e)


def consultar_dados(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dados_climaticos")
        dados = cursor.fetchall()

        # Exibindo os dados de forma organizada
        print("Dados Climáticos:")
        for row in dados:
            print(
                f"ID: {row[0]}, Data/Hora: {row[1]}, Temperatura: {row[2]}, Precipitação: {row[3]}"
            )
    except Exception as e:
        print("Erro ao consultar dados:", e)


def converter_dados(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dados_climaticos")
        dados = cursor.fetchall()

        # Transformar os dados em um DataFrame do pandas
        df = pd.DataFrame(
            dados, columns=["id", "data_hora", "temperatura", "precipitacao"]
        )

        return df
    except Exception as e:
        print("Erro ao consultar dados:", e)
        return None
