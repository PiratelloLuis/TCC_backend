import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS
from db import Database
import re

app = Flask(__name__)
CORS(app)

API_KEY = 'AIzaSyDKfb0y3IhQMcx7Rmsw8ICh5MucvrtIg_s'
genai.configure(api_key=API_KEY)
db = Database()


@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = db.listar_alunos()
    return jsonify(alunos)


@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    nome = data['nome']
    id_aluno = db.inserir_aluno(nome)
    return jsonify({'id': id_aluno, 'nome': nome}), 201


@app.route('/perguntas', methods=['POST'])
def adicionar_pergunta():
    data = request.get_json()
    texto = data['texto']
    id_pergunta = db.inserir_pergunta(texto)
    return jsonify({'id': id_pergunta}), 201


@app.route('/respostas', methods=['POST'])
def adicionar_resposta():
    data = request.get_json()
    id_pergunta = data['id_pergunta']
    id_aluno = data['id_aluno']
    resposta = data['resposta']
    db.inserir_resposta(id_pergunta, id_aluno, resposta)
    return jsonify({'message': 'Resposta cadastrada com sucesso!'}), 201


@app.route('/corrigir', methods=['POST'])
def corrigir():
    data = request.get_json()
    nome_aluno = data['nome_aluno']
    perguntas = data['perguntas']
    respostas = data['respostas']
    id_aluno = data['id_aluno']

    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
        f"Contexto: Você irá corrigir as seguintes perguntas: "
        + ", ".join([f"{i + 1}.{perguntas[i]}" for i in range(len(perguntas))]) +
        f" e verificar as respostas do {nome_aluno}: "
        + ", ".join([f"{i + 1}.{respostas[i]}" for i in range(len(respostas))]) +
        " e escrever a porcentagem de acerto do usuário"
    )

    resposta_gpt = response.text
    print(resposta_gpt)

    porcentagem = re.search(r'(\d{1,3})%', resposta_gpt)
    if porcentagem:
        nota = int(porcentagem.group(1))
        db.atualizar_nota(id_aluno, nota)
        return jsonify({'nota': nota}), 200
    else:
        return jsonify({'error': 'Não foi possível extrair a porcentagem.'}), 400


if __name__ == '__main__':
    app.run(debug=True)
