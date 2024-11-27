from flask import Flask, render_template, url_for, jsonify, request, redirect
import requests
from flask_sqlalchemy import SQLAlchemy

# Importa o módulo pets para manipular dados relacionados aos pets (não está claro no contexto se é necessário)

# Cria a instância da aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados SQLite
# Define o caminho para o banco de dados, nesse caso, o banco será criado no arquivo 'pets.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'

# Desativa o rastreamento de modificações no banco de dados (pode aumentar o desempenho)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Inicializa o banco de dados com a instância da aplicação Flask
db = SQLAlchemy(app)

# Definição do modelo de dados 'petz' que será a tabela no banco de dados
class petz(db.Model):
    # Define a estrutura da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)  # Definindo o campo id como chave primária
    especie = db.Column(db.String(100), nullable=False)  # Definindo a coluna 'especie' como não nula
    raca = db.Column(db.String(100), nullable=False)  # Definindo a coluna 'raca' como não nula
    cor = db.Column(db.String(100), nullable=False)  # Definindo a coluna 'cor' como não nula

    # Representação do objeto quando convertido para string
    def __repr__(self):
        return f"petz('{self.id}', '{self.especie}', '{self.raca}','{self.cor})"
    
    # Método para converter os dados do pet para um formato de dicionário
    def to_dict(self):
        return {
            'id': self.id,
            'especie': self.especie,
            'raca': self.raca,
            'cor': self.cor
        }

# Criação do banco de dados (caso as tabelas não existam)
with app.app_context():
    db.create_all()

# Rota para a página principal
@app.route('/')
def index():
    # Renderiza o arquivo 'index.html' localizado na pasta 'templates/'
    return render_template('index.html')

# Rota para abrir a tela de cadastro
@app.route('/cadastro')
def cadastro():
    # Renderiza o arquivo 'Cadastro.html' localizado na pasta 'templates/'
    return render_template('Cadastro.html')

# Rota para exibir os animais cadastrados no banco de dados
@app.route('/exibir')
def exibir():
    # Consulta todos os pets no banco de dados
    pets = petz.query.all()
    # Renderiza o arquivo 'Exibir.html' passando os pets como variável
    return render_template('Exibir.html', pets=pets)

# Rota para adicionar um novo pet via POST
@app.route('/pets', methods=['POST'])
def add_pet():
    # Obtém os dados enviados no corpo da requisição em formato JSON
    new_pet = request.get_json()
    # Cria uma instância do modelo petz com os dados recebidos
    pet = petz(especie=new_pet['especie'], raca=new_pet['raca'], cor=new_pet['cor'])
    # Adiciona o novo pet à sessão do banco de dados
    db.session.add(pet)
    db.session.commit()  # Comita as mudanças no banco de dados
    # Retorna os dados do novo pet em formato JSON e o status de criação (201)
    return jsonify(new_pet), 201

# Rota para processar o formulário de cadastro de um novo pet
@app.route('/submit', methods=['POST'])
def submit():
    # Obtém os dados do formulário (dados de espécie, raça e cor)
    especie = request.form.get('Espécie')
    raca = request.form.get('Raça')
    cor = request.form.get('Cor')
    # Cria uma nova instância de 'petz' com os dados do formulário
    new_pet = petz(especie=especie, raca=raca, cor=cor)
    # Adiciona o novo pet à sessão do banco de dados
    db.session.add(new_pet)
    db.session.commit()  # Comita as mudanças no banco de dados

    # Redireciona o usuário para a página de exibição de pets
    return redirect('/exibir')

# Rota para obter os pets cadastrados no banco de dados em formato JSON
@app.route('/pets', methods=['GET'])
def get_pets():
    # Consulta todos os pets no banco de dados
    pets = petz.query.all()

    # Converte os pets para uma lista de dicionários
    pets_list = [pet.to_dict() for pet in pets]

    # Retorna os dados dos pets em formato JSON
    return jsonify(pets_list)

# Inicia o servidor Flask, permitindo a execução do aplicativo web
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    
