
import os
import sys
import sqlite3
from statistics import median

print("----------------------")
print("""𝔾𝕖𝕤𝕥𝕒̃𝕠 𝕕𝕖 𝔽𝕚𝕟𝕒𝕟𝕔̧𝕒𝕤""")
print("----------------------")

con = sqlite3.connect('identifier.sqlite') # Cria um banco de dados
cur = con.cursor() # Usado para executar instruções e buscar.
cur.execute("""
                CREATE TABLE IF NOT EXISTS identifier
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    valor REAL NOT NULL
                )
                """) #Gravamos valores nas colunas do bd
#execute("CREATE TABLE identifier(descricao, categoria, valor)") #Cria uma tabela no banco de dados
# res = cur.execute("SELECT name FROM sqlite_master") verifica se a nova tabela foi criada consultado a tabela no sqlmaster
# res.fetchone()

def db(descricao, categoria, valor):
    cur.execute(
        "INSERT INTO identifier (descricao, categoria, valor) VALUES (?, ?, ?)",
        (descricao, categoria, valor)
    )
    con.commit() #fazemos a confirmação do registro

def calculadora():
    valores = cur.execute("SELECT valor FROM identifier")
    vlr = [linha[0] for linha in valores]
    return vlr
def entrada_categoria():
    return input("Informe a Categoria: ")

def entrada_descricao():
    return input("Informe a descrição do gasto: ")

def entrada_valor():
    return input('Digite o valor do gasto: ')


def converter(str):
    """ Devolve o float positivo, ou none se a entrada for Invalida."""
    try:
        valor = float(str.strip().replace(',', '.'))
    except ValueError:
        return None
    return valor if valor > 0 else None

def menu():
    print('1. Cadastrar')
    print('2. Historico de gastos')
    print('3. Soma e Média')
    print('4. Sair')
    opcao = input('Escolha a opção acima: ')
    if opcao.isdigit():
        return int(opcao)
    else:
        input('Escolha uma opção válida: ')


def main():
    while True:
        match menu():
            case 1:
                valor = converter(entrada_valor())
                if valor is None:
                    print("Valor inválido. Informe um número maior que 0 (ex.: 10,50).")
                    continue
                db(entrada_descricao(), entrada_categoria(), valor)
                print("Gasto registrado.")
            case 2:
                print(calculadora())
            case 3:
                lista_gastos = calculadora()
                soma_total = 0
                for i in lista_gastos:
                    soma_total += i
                    media = soma_total / len(lista_gastos)
                print(f', Soma = {soma_total} / Média = {media} ')
            case 4:
                os.system('cls')
                sys.exit()
            case "":
                continue
            case _:
                continue
if __name__ == '__main__':
    main()