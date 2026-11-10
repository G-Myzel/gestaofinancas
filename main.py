import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).with_name("identifier.sqlite")


def conectar():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS identifier (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                valor REAL NOT NULL CHECK (valor > 0)
            )
        """)
    return con


def db(con, descricao, categoria, valor):
    with con:
        con.execute(
            "INSERT INTO identifier (descricao, categoria, valor) VALUES (?, ?, ?)",
            (descricao, categoria, valor),
        )


def listar_gastos(con):
    return con.execute(
        "SELECT id, descricao, categoria, valor FROM identifier ORDER BY id"
    ).fetchall()


def resumo_gastos(con):
    return con.execute(
        "SELECT COUNT(*) AS quantidade, COALESCE(SUM(valor), 0) AS soma, "
        "COALESCE(AVG(valor), 0) AS media FROM identifier"
    ).fetchone()


def entrada_categoria():
    return input("Informe a categoria: ").strip()


def entrada_descricao():
    return input("Informe a descrição do gasto: ").strip()


def entrada_valor():
    return input("Digite o valor do gasto: ")


def converter(entrada):
    """Converte uma entrada para um valor positivo ou retorna None."""
    try:
        valor = float(entrada.strip().replace(",", "."))
    except (AttributeError, ValueError):
        return None
    return valor if valor > 0 else None


def menu():
    print("\nGESTÃO DE FINANÇAS")
    print("1. Cadastrar gasto")
    print("2. Histórico de gastos")
    print("3. Ver soma e média")
    print("4. Sair")
    return input("Escolha uma opção: ").strip()


def cadastrar_gasto(con):
    descricao = entrada_descricao()
    categoria = entrada_categoria()
    valor = converter(entrada_valor())
    if not descricao or not categoria:
        print("Descrição e categoria são obrigatórias.")
        return
    if valor is None:
        print("Informe um valor maior que zero (ex.: 10,50).")
        return
    db(con, descricao, categoria, valor)
    print("Gasto registrado.")


def exibir_historico(con):
    gastos = listar_gastos(con)
    if not gastos:
        print("Nenhum gasto registrado.")
        return
    for gasto in gastos:
        print(
            f"{gasto['id']}. {gasto['descricao']} | {gasto['categoria']} | "
            f"R$ {gasto['valor']:.2f}"
        )


def exibir_resumo(con):
    resumo = resumo_gastos(con)
    if resumo["quantidade"] == 0:
        print("Nenhum gasto registrado.")
        return
    print(f"Quantidade de gastos: {resumo['quantidade']}")
    print(f"Soma: R$ {resumo['soma']:.2f}")
    print(f"Média por gasto: R$ {resumo['media']:.2f}")


def main():
    with closing(conectar()) as con:
        while True:
            opcao = menu()
            if opcao == "1":
                cadastrar_gasto(con)
            elif opcao == "2":
                exibir_historico(con)
            elif opcao == "3":
                exibir_resumo(con)
            elif opcao == "4":
                print("Até logo!")
                break
            else:
                print("Escolha uma opção de 1 a 4.")


if __name__ == "__main__":
    main()
