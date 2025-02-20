import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

# Buscar todos os CPFs salvos no banco
cursor.execute("SELECT id, cpf FROM clientes")
clientes = cursor.fetchall()

for cliente in clientes:
    id_cliente, cpf = cliente
    
    # Se o CPF já estiver formatado, pula para o próximo
    if "." in cpf and "-" in cpf:
        continue  

    # Formata corretamente o CPF
    cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"  

    # Atualiza o CPF no banco
    cursor.execute("UPDATE clientes SET cpf = ? WHERE id = ?", (cpf_formatado, id_cliente))

conn.commit()
conn.close()

print("✅ CPFs corrigidos e formatados corretamente no banco!")

