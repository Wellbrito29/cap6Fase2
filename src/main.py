# Importação dos módulos
import os
import oracledb
import pandas as pd

# Try para tentativa de Conexão com o Banco de Dados
try:
    # Efetua a conexão com o Usuário no servidor
    conn = oracledb.connect(
        user="RM552157", password="140492", dsn="oracle.fiap.com.br:1521/ORCL"
    )
    # Cria as instruções para cada módulo
    inst_cadastro = conn.cursor()
    inst_consulta = conn.cursor()
    inst_alteracao = conn.cursor()
    inst_exclusao = conn.cursor()
except Exception as e:
    # Informa o erro
    print("Erro: ", e)
    # Flag para não executar a Aplicação
    conexao = False
else:
    print("Conexão com o Banco de Dados estabelecida com sucesso!")
    # Flag para executar a Aplicação
    conexao = True
