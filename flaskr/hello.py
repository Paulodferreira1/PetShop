from flask import Flask, render_template,url_for, jsonify, request,redirect
import requests
from flask_sqlalchemy import SQLAlchemy

from .pets import pets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'  # Caminho para o banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o rastreamento de modificações
# Inicializando o banco de dados
db = SQLAlchemy(app)
class petz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especie = db.Column(db.String(100), nullable=False)
    raca = db.Column(db.String(100),nullable=False)
    cor = db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"petz('{self.id}', '{self.especie}', '{self.raca}','{self.cor})"
    def to_dict(self):
        return {
        'id': self.id,
        'especie': self.especie,
        'raca': self.raca,
        'cor': self.cor
        }
     # Criando o banco de dados (tabelas) se não existirem
with app.app_context():
    db.create_all() 

# Rota para a página principal
@app.route('/')
def index():
    return render_template('index.html')  # Renderiza o arquivo index.html dentro de templates/
#Rota para abrir a tela de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('Cadastro.html')
#Rota para exibir os animais cadastrados
@app.route('/exibir')
def exibir():
    pets = petz.query.all()
    return render_template('Exibir.html',pets=pets)
#Rota para puxar os cadastros dos pets
#Rota para adicionar pets
@app.route('/pets', methods=['POST'])
def add_pet():
    new_pet = request.get_json()
    pet = petz(especie=new_pet['especie'], raca=new_pet['raca'], cor=new_pet['cor'])
    db.session.add(pet)
    db.session.commit()
    return jsonify(new_pet), 201
@app.route('/submit', methods=['POST'])
def submit():
    # Obtendo dados do formulário
    especie = request.form.get('Espécie')
    raca = request.form.get('Raça')
    cor= request.form.get('Cor')
    new_pet = petz(especie=especie, raca=raca,cor=cor)
    db.session.add(new_pet)
    db.session.commit()

    
    dados = {
        'especie':especie,
        'raca':raca,
        'cor':cor
        
    }
        # Resposta ao usuário após o POST
    return redirect(url_for('exibir'))
@app.route('/pets', methods=['GET'])
def get_pets():
    pets = petz.query.all()  # Consultando todos os pets no banco de dados

    # Convertendo os pets para uma lista de dicionários
    pets_list = [pet.to_dict() for pet in pets]

    return jsonify(pets_list)  # Retorna os dados no formato JSON
# Definindo um modelo (tabela) no banco de dados
# Iniciar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
