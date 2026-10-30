import sqlite3


def conexao_banco():
    conexao = sqlite3.connect("contatos.db")
    cursor = conexao.cursor()

    sql = """
        CREATE TABLE IF NOT EXISTS contatos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """

    cursor.execute(sql)
    conexao.commit()

    return conexao, cursor


def adicionar_contato():
    nome = input("Digite o nome do contato: ")
    telefone = input("Digite o telefone do contato: ")
    email = input("Digite o email do contato: ")

    conexao, cursor = conexao_banco()
    cursor.execute(
        "INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)",
        (nome, telefone, email)
    )
    conexao.commit()
    conexao.close()

    print("Contato adicionado com sucesso!")


def listar_contatos():
    conexao, cursor = conexao_banco()
    cursor.execute("SELECT * FROM contatos")
    contatos = cursor.fetchall()
    conexao.close()

    if len(contatos) == 0:
        print("Nenhum contato encontrado.")
    else:
        print("### LISTA DE CONTATOS ###")
        for contato in contatos:
            print(
                f"ID: {contato[0]}, Nome: {contato[1]}, "
                f"Telefone: {contato[2]}, Email: {contato[3]}"
            )


def buscar_contato():
    nome = input("Digite o nome do contato que deseja buscar: ")

    conexao, cursor = conexao_banco()
    cursor.execute(
        "SELECT * FROM contatos WHERE nome LIKE ?",
        ("%" + nome + "%",)
    )
    contatos = cursor.fetchall()
    conexao.close()

    if len(contatos) == 0:
        print("Nenhum contato encontrado.")
    else:
        print("### RESULTADO DA BUSCA ###")
        for contato in contatos:
            print(
                f"ID: {contato[0]}, Nome: {contato[1]}, "
                f"Telefone: {contato[2]}, Email: {contato[3]}"
            )


def atualizar_contato():
    id_contato = input("Digite o ID do contato que deseja atualizar: ")

    conexao, cursor = conexao_banco()
    cursor.execute(
        "SELECT * FROM contatos WHERE id = ?",
        (id_contato,)
    )
    contato = cursor.fetchone()

    if contato is None:
        print("Contato não encontrado.")
        conexao.close()
        return

    print(
        f"Contato encontrado: ID: {contato[0]}, Nome: {contato[1]}, "
        f"Telefone: {contato[2]}, Email: {contato[3]}"
    )

    novo_nome = input(
        "Digite o novo nome (deixe em branco para manter o atual): "
    )
    novo_telefone = input(
        "Digite o novo telefone (deixe em branco para manter o atual): "
    )
    novo_email = input(
        "Digite o novo email (deixe em branco para manter o atual): "
    )

    if novo_nome == "":
        novo_nome = contato[1]
    if novo_telefone == "":
        novo_telefone = contato[2]
    if novo_email == "":
        novo_email = contato[3]

    cursor.execute(
        "UPDATE contatos SET nome = ?, telefone = ?, email = ? WHERE id = ?",
        (novo_nome, novo_telefone, novo_email, id_contato)
    )
    conexao.commit()
    conexao.close()

    print("Contato atualizado com sucesso!")


def remover_contato():
    id_contato = input("Digite o ID do contato que deseja remover: ")

    conexao, cursor = conexao_banco()
    cursor.execute(
        "SELECT * FROM contatos WHERE id = ?",
        (id_contato,)
    )
    contato = cursor.fetchone()

    if contato is None:
        print("Contato não encontrado.")
        conexao.close()
        return

    cursor.execute(
        "DELETE FROM contatos WHERE id = ?",
        (id_contato,)
    )
    conexao.commit()
    conexao.close()

    print("Contato removido com sucesso!")


def menu():
    while True:
        print("\n### CONTATOS ###")
        print("1. Adicionar contato")
        print("2. Listar contatos")
        print("3. Buscar contato")
        print("4. Atualizar contato")
        print("5. Remover contato")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_contato()
        elif opcao == "2":
            listar_contatos()
        elif opcao == "3":
            buscar_contato()
        elif opcao == "4":
            atualizar_contato()
        elif opcao == "5":
            remover_contato()
        elif opcao == "0":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()