# Importando os pacotes
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Criando um objeto para
# herdar os métodos do Flask
app = Flask(__name__)


# Configuração do banco de dados
# Verificando a conexão

try:
    conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='senac123456789',
    database='locadora'   
    )
    if conexao.is_connected():
        print('Conexão realizada com sucesso')
except OSError as error:
    print('Erro ao conectar: ', error)

# variavel de execução
# de scripts SQL
cursor = conexao.cursor(dictionary=True)

# obs: o dictionary=true é necessario
# para a leitura do resultado da seleção
# dos registros


# Criando as rotas para o 
# carregamento das páginas e
# realização das operações CRUD



# 1) Rota para acesso
# da página principal da aplicação
@app.route('/')
def index():

    # Atribuir um retorno para o
    # carregamento da página 
    # principal do servidor    
    return render_template('index.html')



# 2) Rota para criação de
# registros no banco
@app.route('/criar', methods = ['GET', 'POST'])
def criar():
    
    # Verificar qual método será
    # usado na operação e atribuir
    # variáveis para receber os valores
    # dos campos de texto(inputs)
    if request.method == 'POST':
        
       # Recebendo os valores dos inputs
       nome = request.form['nome']
       endereco = request.form['endereco']
       telefone = request.form['telefone']
       email = request.form['email']
       equipamento= request.form['equipamento']
       preco_diaria= request.form['preco_diaria']
       data_locacao= request.form['data_locacao']
       data_entrega= request.form['data_entrega']
       
        # Comando em SQL para criar
        # o cliente
       comando = 'insert into cliente (nome, endereco, telefone, email, equipamento, preco_diaria, data_locacao, data_entrega)values(%s, %s, %s, %s, %s)'
    
        # Variável que irá receber todos
        # os valores das variáveis anteriores
       valores = (nome, endereco, telefone, email, equipamento, preco_diaria, data_locacao, data_entrega)
    
        # Executar o comando em SQL
       cursor.execute(comando, valores)
        
        # Confirmar a execução do
        # comando no banco de dados
       conexao.commit()
                
        # Atribuir um retorno podendo
        # ser o redirecionamento para
        # outra página
       return 'cliente cadastrado com sucesso'
       #return redirect(url_for(''))
    
        # OBS: o parâmetro em 'url_for'
        # é a função criada para
        # carregar a rota desejada
    
    # Atribuir um retorno para o
    # carregamento da página de
    # de criação do cliente
    return render_template('criar.html')


# 3) Rota para seleção de
# registros no banco
@app.route('/listar')
def listar():
    
    
    comando = 'select * from cliente'
    cursor.execute(comando)
    
    # Variável que irá receber
    # o resultado do comando
    cliente = cursor.fetchall()
    
    # retornar o resultado
    # carregando em outra página
    # e usando um apelido
    return render_template('listar.html', cliente = cliente )

    # esclarecendo
    # a primeira variavel cliente recebe o resultado da execução do 
    # script em sql
    
    # a segunda variavel
    # será o apelido que será levado para 
    # a pagina 'listar.html'



# 4) Rota para atualização de
# registros no banco
@app.route('/editar/<int:id_cliente>', methods = ['GET', 'POST'])
# declarar a função com o id como parâmetro
def editar(id_cliente):

    # ====== SEGUNDO PASSO ==========
    # Comandos para editar 
    # somente um cliente pelo id

    if request.method == 'POST':
        
       # Recebendo o valor dos inputs
       nome = request.form['nome']
       endereco = request.form['endereco']
       telefone = request.form['telefone']
       email = request.form['email']
       equipamento = request.form['equipamento']
       preco_diaria = request.form['preco_diaria']
       data_locacao = request.form['data_locacao']
       data_entrega = request.form['data_entrega']
        # Comando em SQl para editar
        # os clientes
       comando = 'update cliente set nome = %s, endereco = %s, telefone = %s, email = %s, equipamento = %s, preco_diaria = %s, data_locacao = %s, data_entrega = %s where id_cliente = %s'
        
        # Variável que irá receber todos
        # os valores das variáveis anteriores
       valores = (nome, endereco, telefone, email, equipamento, preco_diaria, data_locacao, data_entrega, id_cliente )
        
        # Executar o comando em SQL
       cursor.execute(comando,valores)
        
        # Confirmar a execução do
        # comando no banco de dados
       conexao.commit()
       
       # atribuir um retorno podendo
       # ser o redicionamento para outra
       # pagina
       
       # obs o paramentro de 'url_for()'
       # é o nome da função que dá o nome da rota
       return redirect(url_for('listar'))
        
    # ====== PRIMEIRO PASSO ==========
    # Comandos para selecionar
    # somente um cliente pelo id
    
    comando = 'select * from cliente where id_cliente = %s'
    
    # Variável que irá receber 
    # o valor do id do cliente
    valor = (id_cliente,) 
    
    # Executar o comando em SQL
    cursor.execute(comando,valor)
        
    # variavel que ira receber o
    # resultado do comando
    cliente = cursor.fetchone()
    
    # retornar o resultado
    # carregando em outra página
    # e usando um apelido
    return render_template('editar.html',cliente = cliente)


# 5) Rota para exclusão de
# registros no banco
@app.route('/excluir/<int:id_locadora>')
# declarar função

def excluir(id_cliente):
    # Comando em SQl para excluir
    # o cliente
    comando = 'delete from cliente where id_locadora = %s'    
    
    # Variável que irá receber 
    # o valor do id do cliente
    valor = (id_cliente,)    
    
    # Executar o comando em SQL
    cursor.execute(comando, valor)
    
    # Confirmar a execução do
    # comando no banco de dados
    conexao.commit()
    
    # Atribuir um retorno podendo
    # ser o redirecionamento para
    # outra página
    return redirect(url_for('listar'))


# Criação do método de execução
# do servidor local
if __name__ == '__main__':
    app.run(debug=True)