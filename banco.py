import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

# Criar a tabela de clientes (se ainda não existir)
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE NOT NULL,
    saldo REAL NOT NULL
)
""")

conn.commit()
conn.close()

# Validação de CPF
def validar_cpf(cpf):
    cpf = cpf.strip()  # Remove espaços extras

    if cpf.isdigit() and len(cpf) == 11:
        return True  # ✅ Retorna True se o CPF for válido
    else:
        return False  # ❌ Retorna False se o CPF for inválido
    
# Formatação de CPF
def formatar_cpf(cpf):
    cpf = cpf.strip()

    if len(cpf) == 11 and cpf.isdigit():
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    else:
        return None

# CPF repetido
def cpf_existe(cpf):
    conn = sqlite3.connect("banco.db")  # Conecta ao banco
    cursor = conn.cursor()

    cursor.execute("SELECT cpf FROM clientes WHERE cpf = ?", (cpf,))  # Consulta o CPF no banco
    resultado = cursor.fetchone()  # Obtém o primeiro resultado

    conn.close()  # Fecha a conexão com o banco

    return resultado is not None  # Retorna True se encontrou o CPF, False se não encontrou

# Função para formatar o nome do cliente
def formatar_nome(nome):
    palavras = nome.split()
    nome_formatado = []
    for palavra in palavras:
        if len(palavra) <= 3:
            nome_formatado.append(palavra.lower())
        else:
            nome_formatado.append(palavra.capitalize())
    return ' '.join(nome_formatado)

# Função para cadastrar um novo cliente
def cadastrar_cliente(nome, cpf, saldo):
    """
    Cadastra um novo cliente se o CPF não estiver duplicado.
    """
    nome = formatar_nome(nome)  # Formata o nome do cliente

    if not validar_cpf(cpf):
        print(f"⚠️ CPF inválido ({cpf})! Certifique-se de que tem 11 dígitos numéricos.")
        return  # Sai da função sem cadastrar o cliente
    
    cpf_formatado = formatar_cpf(cpf)
    if not cpf_formatado:
        print(f"⚠️ Erro: CPF não pôde ser formatado corretamente!")
        return

    if cpf_existe(cpf_formatado):
        print(f"⚠️ Erro: O CPF {cpf_formatado} já está cadastrado no sistema!")
        return  # Sai da função sem cadastrar o cliente

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO clientes (nome, cpf, saldo) VALUES (?, ?, ?)", (nome, cpf_formatado, saldo))
        conn.commit()
        print(f"✅ Cliente {nome} cadastrado com sucesso com CPF {cpf_formatado}!")
    except sqlite3.IntegrityError:
        print("⚠️ Erro: CPF já cadastrado!")

    conn.close()

# Função para listar todos os clientes
def listar_clientes():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    
    if clientes:
        print("\n📋 Lista de Clientes:")
        for cliente in clientes:
            print(f"ID: {cliente[0]}, Nome: {cliente[1]}, CPF: {cliente[2]}, Saldo: R$ {cliente[3]:.2f}")
    else:
        print("⚠️ Nenhum cliente cadastrado.")
    
    conn.close()

# Função para atualizar o saldo de um cliente
def atualizar_saldo(cpf, novo_saldo):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    
    cursor.execute("UPDATE clientes SET saldo = ? WHERE cpf = ?", (novo_saldo, cpf))
    if cursor.rowcount == 0:
        print("⚠️ CPF não encontrado.")
    else:
        print("✅ Saldo atualizado com sucesso!")
    
    conn.commit()
    conn.close()

# Função para remover clientes
def remover_clientes(cpfs):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    
    for cpf in cpfs:
        cursor.execute("DELETE FROM clientes WHERE cpf = ?", (cpf,))
        if cursor.rowcount == 0:
            print(f"⚠️ CPF {cpf} não encontrado.")
        else:
            print(f"✅ Cliente com CPF {cpf} removido com sucesso!")
    
    conn.commit()
    conn.close()

while True:
    print("\n💰 Bem-vindo ao Banco Itau! Escolha uma opção:")
    print("1. Cadastrar Cliente")
    print("2. Listar Clientes")
    print("3. Atualizar Saldo")
    print("4. Remover Clientes")
    print("5. Sair")
    
    opcao = input("Digite o número da opção desejada: ")

    if opcao == "1":
        nome = input("Nome do Cliente: ")
        cpf = input("CPF do Cliente: ")
        saldo = float(input("Saldo Inicial: "))
        cadastrar_cliente(nome, cpf, saldo)

    elif opcao == "2":
        listar_clientes()

    elif opcao == "3":
        cpf = input("Digite o CPF do cliente: ")
        novo_saldo = float(input("Novo saldo: "))
        atualizar_saldo(cpf, novo_saldo)

    elif opcao == "4":
        cpfs = input("Digite os CPFs dos clientes a serem removidos, separados por vírgula: ").split(',')
        cpfs = [cpf.strip() for cpf in cpfs]  # Remove espaços extras
        remover_clientes(cpfs)

    elif opcao == "5":
        print("👋 Saindo do sistema...")
        break

    else:
        print("⚠️ Opção inválida! Tente novamente.")