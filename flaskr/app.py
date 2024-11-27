from flask import Flask, flash, render_template, url_for, jsonify, request, redirect
import requests
from flask_sqlalchemy import SQLAlchemy
import os

# Importa o módulo pets para manipular dados relacionados aos pets (não está claro no contexto se é necessário)

# Cria a instância da aplicação Flask
app = Flask(__name__)
app.secret_key = "some_secret_key"

# Configuração do banco de dados SQLite
# Define o caminho para o banco de dados, nesse caso, o banco será criado no arquivo 'pets.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://petshop_db_cr0t_user:D6vXThnqLThMtSgZ4SQJtzv7gAibBOHg@dpg-ct3kgk68ii6s73d77pj0-a:5432/petshop_db_cr0t'



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
@app.route('/excluir/<int:id>', methods=['GET'])
def excluir(id):
    pet = petz.query.get(id)  # Encontra o pet pelo ID

    if pet:
        db.session.delete(pet)  # Remove o pet
        db.session.commit()
        db.session.execute("ALTER SEQUENCE petz_id_seq RESTART WITH 1")
        db.session.commit()  # Commit da transação para o banco de dados
        flash("Pet excluído com sucesso!", "success")
    else:
        flash("Pet não encontrado.", "error")

    return redirect('/exibir')
#@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pet = petz.query.get_or_404(id)  # Encontra o pet pelo ID
    
    if request.method == 'POST':
        # Atualiza os dados com os valores do formulário
        pet.especie = request.form['Espécie']
        pet.raca = request.form['Raça']
        pet.cor = request.form['Cor']
        
        db.session.commit()  # Comita as alterações no banco de dados

        flash('Pet atualizado com sucesso!', 'success')  # Mensagem de sucesso
        return redirect(url_for('exibir'))  # Redireciona para a lista de pets


# Rota para exibir os animais cadastrados no banco de dados
@app.route('/exibir')
def exibir():
    # Consulta todos os pets no banco de dados
    pet = petz.query.all()
    # Renderiza o arquivo 'Exibir.html' passando os pets como variável
    return render_template('Exibir.html', pets=pet)

# Rota para adicionar um novo pet via POST
@app.route('/pets', methods=['POST'])
def adicionar_pet():
    # Obtém os dados enviados no corpo da requisição em formato JSON
    novo_pet = request.get_json()
    # Cria uma instância do modelo petz com os dados recebidos
    pet = petz(especie=novo_pet['especie'], raca=novo_pet['raca'], cor=novo_pet['cor'])
    # Adiciona o novo pet à sessão do banco de dados
    db.session.add(pet)
    db.session.commit()  # Comita as mudanças no banco de dados
    # Retorna os dados do novo pet em formato JSON e o status de criação (201)
    return jsonify(novo_pet), 201

# Rota para processar o formulário de cadastro de um novo pet
@app.route('/submit', methods=['POST'])
def submit():
    # Obtém os dados do formulário (dados de espécie, raça e cor)
    especie = request.form.get('Espécie')
    raca = request.form.get('Raça')
    cor = request.form.get('Cor')
    if not especie or not raca or not cor:
        flash("Todos os campos são obrigatórios.", "error")
        return redirect('/exibir')
    # Cria uma nova instância de 'petz' com os dados do formulário
    novo_pet = petz(especie=especie, raca=raca, cor=cor)
    # Adiciona o novo pet à sessão do banco de dados
    db.session.add(novo_pet)
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

    
