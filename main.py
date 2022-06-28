from flask import Flask, render_template, request, redirect, session, flash                 
import os

from dao import ElementoDao, ClasseDao, CuriosidadesDao, NivelDao, PerguntasDao, UsuarioDao, DesafioDao
from flask_mysqldb import MySQL

from models import Usuario, Tipo_usuario, Elemento, Classe, Curiosidades, Perguntas, Desafio, Nivel

app = Flask(__name__)
app.secret_key = 'LP2'
app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__))+'/uploads'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'tabelaperiodica'
app.config['MYSQL_PORT'] = 3306
db = MySQL(app)

elemento_dao = ElementoDao(db)
usuario_dao = UsuarioDao(db)
classe_dao = ClasseDao(db)
curiosidades_dao = CuriosidadesDao(db)
desafio_dao = DesafioDao(db)
nivel_dao = NivelDao(db)
perguntas_dao = PerguntasDao(db)

@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    lista = elemento_dao.listar()
    return render_template('index.html', elementos=lista)

@app.route('/adm')
def adm():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    lista = elemento_dao.listar()
    return render_template('index1.html', elementos=lista)

@app.route('/curiosidades')
def curiosidades():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    lista = curiosidades_dao.listar()
    lista2 = elemento_dao.listar()
    return render_template('curiosidades.html', curiosidades=lista, elementos = lista2)

@app.route('/desafio')
def desafio():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    lista = perguntas_dao.listar()
    lista2 = desafio_dao.listar()
    lista3 = nivel_dao.listar()
    return render_template('desafio.html', perguntas=lista, desafios = lista2, niveis=lista3)


@app.route('/roteiro_estudo')
def roteiro_estudo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    return render_template('roteiro_estudo.html')

@app.route('/lista_elementos')
def lista_elementos():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=lista_elementos')
    lista = elemento_dao.listar()
    return render_template('lista_elementos.html', titulo="Elementos Cadastrados", elementos = lista)

@app.route('/lista_classes')
def lista_classes():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=lista_classes')
    lista = classe_dao.listar()
    return render_template('lista_classes.html', titulo="Classes Cadastradas", classes=lista)

@app.route('/lista_curiosidades')
def lista_curiosidades():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=lista_curiosidades')
    lista = curiosidades_dao.listar()
    return render_template('lista_curiosidades.html', titulo="Curiosidades Cadastradas", curiosidades=lista)

@app.route('/lista_desafios')
def lista_desafios():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=lista_desafios')
    lista = desafio_dao.listar()
    return render_template('lista_desafios.html', titulo="Desafios Cadastrados", desafios = lista)

@app.route('/lista_perguntas')
def lista_perguntas():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=lista_perguntas')
    lista = perguntas_dao.listar()
    return render_template('lista_perguntas.html', titulo="Perguntas Cadastradas", perguntas = lista)

@app.route('/novo_elemento')
def novo_elemento():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=novo_elemento')
    lista = classe_dao.listar()
    return render_template('novo_elemento.html', titulo="Cadastrando novo elemento", classes=lista)

@app.route('/nova_classe')
def nova_classe():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=nova_classe')
    return render_template('nova_classe.html', titulo="Cadastrando nova classe")

@app.route('/nova_curiosidade')
def nova_curiosidade():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=nova_curiosidade')
    lista = elemento_dao.listar()
    return render_template('nova_curiosidade.html', titulo="Cadastrando nova curiosidade", elementos = lista)

@app.route('/novo_desafio')
def novo_desafio():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=novo_desafio')
    lista = nivel_dao.listar()
    return render_template('novo_desafio.html', titulo="Cadastrando novo desafio", niveis=lista)

@app.route('/nova_pergunta')
def nova_pergunta():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=nova_pergunta')
    lista = desafio_dao.listar()
    return render_template('nova_pergunta.html', titulo="Cadastrando nova pergunta", desafios=lista)

@app.route('/criar_elemento', methods = ['POST',])
def criar():
    nome_elemento = request.form['nome_elemento']
    num_atomico= request.form['num_atomico']
    massa_atomica= request.form['massa_atomica']
    estado_fisico= request.form['estado_fisico']
    simbolo= request.form['simbolo']
    distribuicao_eletronica= request.form['distribuicao_eletronica']
    classe_id = request.form['classe']
    elemento = Elemento(nome_elemento, num_atomico, massa_atomica, estado_fisico, simbolo, distribuicao_eletronica, classe_id, None)

    #lista.append(pet)
    elemento_dao.salvar(elemento)
    return redirect('/lista_elementos')

@app.route('/criar_classe', methods = ['POST',])
def criar_classe():
    nome_classe = request.form['nome_classe']

    classe = Classe(nome_classe)
    classe_dao.salvar(classe)
    return redirect('/lista_classes')

@app.route('/criar_curiosidades', methods = ['POST',])
def criarcuriosidades():
    tipo = request.form['tipo']
    descricao = request.form['descricao']
    elemento_id = request.form['elemento']

    curiosidades = Curiosidades(tipo, descricao, elemento_id, None)
    curiosidades_dao.salvar(curiosidades)
    return redirect('/lista_curiosidades')

@app.route('/criar_desafio', methods = ['POST',])
def criar_desafio():
    quantidade_perguntas = request.form['quantidade_perguntas']
    nivel_id = request.form['nivel_id']
    desafio = Desafio(quantidade_perguntas, nivel_id, None)

    #lista.append(pet)
    desafio_dao.salvar(desafio)
    return redirect('/lista_desafios')

@app.route('/criar_pergunta', methods = ['POST',])
def criar_pergunta():
    nome_pergunta = request.form['nome_pergunta']
    descricao= request.form['descricao']
    resposta= request.form['resposta']
    desafio_id= request.form['desafio_id']

    pergunta = Perguntas(nome_pergunta, descricao, resposta, desafio_id)

    #lista.append(pet)
    perguntas_dao.salvar(pergunta)
    return redirect('/lista_perguntas')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if proxima == None:
        proxima = ''
    return render_template('login.html', proxima = proxima)

@app.route('/cadastrar')
def cadastrar():
    usuario = request.form['usuario']
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']


    cadastrar = Usuario(usuario, nome, email, senha)
    usuario_dao.salvar(cadastrar)
    flash('Usuário cadastrado! Faça o login')
    return redirect('/login')

@app.route('/autenticar', methods = ['POST',])
def autenticar():
    usuario = usuario_dao.busca_por_id(request.form['usuario'])
    if usuario:
        if usuario._senha == request.form['senha']:
            session['usuario_logado']=request.form['usuario']
            flash(request.form['usuario'] + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            if proxima_pagina == '':
                return redirect('/')
            else:
                return redirect('/{}'.format(proxima_pagina))
    flash('Não logado ou usuário não cadastrado, tente novamente!')
    return redirect('/login')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect('/login')

@app.route('/editar_elemento/<int:id>')
def editar_elemento(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    elementos = elemento_dao.busca_por_id(id)
    lista = classe_dao.listar()
    return render_template('editar_elemento.html',titulo="Editando Dados dos Elementos", elemento = elementos, classes = lista)

@app.route('/editar_classe/<int:id>')
def editar_classe(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar_classe')))
    classe = classe_dao.busca_por_id(id)
    return render_template('editar_classe.html', titulo="Editando Dados do Cliente", classe=classe)

@app.route('/editar_curiosidades/<int:id>')
def editar_curiosidades(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar_curiosidades')))
    curiosidade = curiosidades_dao.busca_por_id(id)
    lista = elemento_dao.listar()
    return render_template('editar_curiosidades.html', titulo="Editando Dados das Curiosidades", curiosidade=curiosidade, elementos=lista)

@app.route('/editar_desafio/<int:id>')
def editar_desafio(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar_desafio')))
    desafios = desafio_dao.busca_por_id(id)
    lista = nivel_dao.listar()
    return render_template('editar_desafio.html',titulo="Editando Dados dos Desafios", desafio = desafios, niveis = lista)

@app.route('/editar_pergunta/<int:id>')
def editar_pergunta(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar_pergunta')))
    perguntas = perguntas_dao.busca_por_id(id)
    lista = desafio_dao.listar()
    return render_template('editar_pergunta.html',titulo="Editando Dados das Perguntas", pergunta = perguntas, desafios = lista)


@app.route('/atualizar_elemento', methods = ['POST',])
def atualizar_elemento():
    nome_elemento = request.form['nome_elemento']
    num_atomico= request.form['num_atomico']
    massa_atomica= request.form['massa_atomica']
    estado_fisico= request.form['estado_fisico']
    simbolo= request.form['simbolo']
    distribuicao_eletronica= request.form['distribuicao_eletronica']
    classe_id = request.form['classe']
    id = request.form['id']

    elemento = Elemento(nome_elemento, num_atomico, massa_atomica, estado_fisico, simbolo, distribuicao_eletronica,classe_id, None, id)
    elemento_dao.salvar(elemento)
    return redirect('/lista_elementos')

@app.route('/atualizar_classe', methods = ['POST',])
def atualizar_classe():
    nome_classe = request.form['nome_classe']
    id = request.form['id']
    classe = Classe(nome_classe, id)

    classe_dao.salvar(classe)
    return redirect('/lista_classes')

@app.route('/atualizar_curiosidades', methods = ['POST',])
def atualizar_curiosidades():
    tipo = request.form['tipo']
    descricao = request.form['descricao']
    elemento_id = request.form['elemento']
    id = request.form['id']

    curiosidades = Curiosidades(tipo, descricao, elemento_id, None, id)
    curiosidades_dao.salvar(curiosidades)
    return redirect('/lista_curiosidades')

@app.route('/atualizar_desafio', methods = ['POST',])
def atualizar_desafio():
    quantidade_perguntas = request.form['quantidade_perguntas']
    nivel_id= request.form['nivel_id']
    id = request.form['id']

    desafio = Desafio(quantidade_perguntas, nivel_id, None, id)
    desafio_dao.salvar(desafio)
    return redirect('/lista_desafios')

@app.route('/atualizar_pergunta', methods = ['POST',])
def atualizar_pergunta():
    nome_pergunta = request.form['nome_pergunta']
    descricao = request.form['descricao']
    resposta = request.form['resposta']
    desafio_id = request.form['desafio_id']
    id = request.form['id']

    pergunta = Perguntas(nome_pergunta, descricao, resposta, desafio_id, id)
    perguntas_dao.salvar(pergunta)
    return redirect('/lista_perguntas')

@app.route('/deletar/<int:id>')
def deletar(id):
    elemento_dao.deletar(id)
    return redirect('/lista_elementos')

@app.route('/deletar_classes/<int:id>')
def deletar_classes(id):
    classe_dao.deletar(id)
    return redirect('/lista_classes')

@app.route('/deletar_curiosidades/<int:id>')
def deletar_curiosidades(id):
    curiosidades_dao.deletar(id)
    return redirect('/lista_curiosidades')

@app.route('/deletar_desafio/<int:id>')
def deletar_desafio(id):
    desafio_dao.deletar(id)
    return redirect('/lista_desafios')

@app.route('/deletar_pergunta/<int:id>')
def deletar_pergunta(id):
    perguntas_dao.deletar(id)
    return redirect('/lista_perguntas')
    
@app.route('/uploads/<nome_arquivo>')
def upload_file(nome_arquivo):
    return send_from_directory(app.config['UPLOAD_PATH'],nome_arquivo)
if __name__ == '__main__':
    app.run(debug=True)
