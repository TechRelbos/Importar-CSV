import csv
import sqlite3
import chardet

# Arquivo CSV
csv_file = 'ambientesset22.csv'

# Banco de dados
db_file = 'dados1.db'

# Detectar a codificação do arquivo CSV
with open(csv_file, 'rb') as file:
    result = chardet.detect(file.read())
    encoding = result['encoding']
'''
Acima contem a importacao das bibliotecas necessarias para trabalhar com arquivos CSV,
a biblioteca dos comandos SQLite e o chardet, que verifica o encoder do arquivo CSV.
'''

# Criar banco de dados (Conectar ao banco depois de criado)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Determinar tabela
table_name = csv_file.split('.')[0]
'''
Acima cria-se a conexao com o banco de dados caso ele seja existente, se nao, gera um banco de dados
Depois, define o nome da tabela, pegando o titulo do arquivo, ocultando a extensao(o que vem depois do '.')
'''

# Abrir e ler o CSV. Depois, ler a primeira linha para pegar o nome das colunas.
with open(csv_file, 'r', encoding='ISO-8859-1') as file:
    csv_reader = csv.reader(file, delimiter=';')  # Define o ponto e vírgula como delimitador
    columns = next(csv_reader) #Funciona como um loop para ler as colunas.

# Cria a tabela com as informações obtidas no código anterior.
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
cursor.execute(create_table_query)
'''
Acima, abre o arquivo csv, verifica o que existe na primeira linha e cria as colunas baseadas nisso.
'''

# Ler os arquivos do CSV e inseri-los na tabela
def inserir(cursor, row, insert_query):
    cursor.execute(insert_query, row)

with open(csv_file, 'r', encoding='ISO-8859-1') as file:
    # Define o ponto e vírgula como delimitador.
    csv_reader = csv.reader(file, delimiter=';')  
    # Aqui pula a primeira linha do arquivo.
    next(csv_reader)  

    for row in csv_reader:
        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['?']*len(columns))})"
        inserir(cursor, row, insert_query)
'''
Acima, abre o arquivo e apos pular a primeira linha(porque ja foi utilizada para criar as colunas),
adiciona linha a linha na tabela, seguindo as colunas.
'''
# Commit e fechar o banco de dados
conn.commit()
conn.close()
print(f'Banco de dados "{db_file}" criado com sucesso, com a tabela "{table_name}" e dados importados.')
'''
Acima, grava as informacoes no banco de dados e o fecha.
Depois exibe uma mensagem confirmando a criacao do banco de dados.
'''