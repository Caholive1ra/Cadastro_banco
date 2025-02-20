from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco
def conectar_banco():
    return sqlite3.connect("banco.db")

@app.route('/listar_clientes', methods=['GET'])
def listar_clientes():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, cpf, saldo FROM clientes")
    clientes = cursor.fetchall()
    conn.close()

    # Transformar os dados em um formato JSON
    lista_clientes = []
    for cliente in clientes:
        lista_clientes.append({
            "id": cliente[0],
            "nome": cliente[1],
            "cpf": cliente[2],
            "saldo": cliente[3]
        })

    return jsonify(lista_clientes)

# Rota para remover múltiplos clientes pelo CPF
@app.route('/remover_clientes', methods=['POST'])
def remover_clientes():
    dados = request.json  # Recebe os CPFs enviados pelo front-end
    cpfs = dados.get("cpfs", [])

    if not cpfs:
        return jsonify({"erro": "Nenhum CPF foi enviado!"}), 400

    conn = conectar_banco()
    cursor = conn.cursor()

    excluidos = 0
    for cpf in cpfs:
        cursor.execute("DELETE FROM clientes WHERE cpf = ?", (cpf,))
        excluidos += cursor.rowcount

    conn.commit()
    conn.close()

    if excluidos > 0:
        return jsonify({"mensagem": f"{excluidos} clientes removidos com sucesso!"}), 200
    else:
        return jsonify({"erro": "Nenhum cliente encontrado com os CPFs fornecidos!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
