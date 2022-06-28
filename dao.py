from models import Usuario, Tipo_usuario, Elemento, Classe, Curiosidades, Perguntas, Desafio, Nivel
'''e um padrão para aplicações que utilizam persistência de dados, onde tem a separação
ddas regras de negócio das regras de acesso a banco de dados, implementda em linguagem OO'''

SQL_DELETA_ELEMENTO = 'delete from elemento where id_elemento = %s'
SQL_CRIA_ELEMENTO = 'INSERT into elemento (nome_elemento, num_atomico, massa_atomica, estado_fisico, simbolo, distribuicao_eletronica, classe) values (%s, %s, %s, %s, %s, %s, %s)'
SQL_ATUALIZA_ELEMENTO = 'UPDATE elemento SET nome_elemento = %s, num_atomico = %s, massa_atomica = %s, estado_fisico = %s, simbolo = %s, distribuicao_eletronica = %s, classe = %s where id_elemento = %s'
SQL_BUSCA_ELEMENTO = 'SELECT E.id_elemento, E.nome_elemento, E.num_atomico, E.massa_atomica, E.estado_fisico, E.simbolo, E.distribuicao_eletronica, E.classe, C.nome_classe as classe from elemento E inner join classe C on E.classe = C.id_classe;'
SQL_ELEMENTO_POR_ID = ' SELECT E.id_elemento, E.nome_elemento, E.num_atomico, E.massa_atomica, E.estado_fisico, E.simbolo, E.distribuicao_eletronica, E.classe, C.nome_classe as classe from elemento E inner join classe C on E.classe = C.id_classe where E.id_elemento = %s'

SQL_DELETA_USUARIO = 'delete from usuario where id_usuario = %s'
SQL_CRIA_USUARIO = 'INSERT into usuario (usuario, nome_usuario, email_usuario, senha) values (%s, %s, %s, %s)'
SQL_ATUALIZA_USUARIO = 'UPDATE usuario SET usuario = %s, nome_usuario = %s, email_usuario = %s, senha = %s where id_usuario = %s'
SQL_BUSCA_USUARIO = 'SELECT id_usuario, usuario, nome_usuario, email_usuario, senha from usuario'
SQL_BUSCA_USUARIO_POR_ID = 'SELECT id_usuario, usuario, nome_usuario, email_usuario, senha FROM usuario where usuario=%s'

SQL_ATUALIZA_CLASSE = 'UPDATE classe SET nome_classe = %s where id_classe = %s'
SQL_CRIA_CLASSE = 'INSERT into classe (nome_classe) values (%s)'
SQL_BUSCA_CLASSE = 'SELECT id_classe, nome_classe from classe'
SQL_DELETA_CLASSE = 'delete from classe where id_classe = %s'
SQL_CLASSE_POR_ID = 'SELECT id_classe, nome_classe from classe where id_classe=%s'

SQL_ATUALIZA_CURIOSIDADE = 'UPDATE curiosidade SET tipo = %s, descricao = %s, elemento = %s where id_curiosidade = %s'
SQL_CRIA_CURIOSIDADE = 'INSERT into curiosidade (tipo, descricao, elemento) values (%s, %s, %s)'
SQL_BUSCA_CURIOSIDADE = 'SELECT CS.id_curiosidade, CS.tipo, CS.descricao, CS.elemento, E.nome_elemento as elemento from curiosidade CS inner join elemento E on CS.elemento = E.id_elemento'
SQL_DELETA_CURIOSIDADE = 'delete from curiosidade where id_curiosidade = %s'
SQL_CURIOSIDADE_POR_ID = 'SELECT CS.id_curiosidade, CS.tipo, CS.descricao, CS.elemento, E.nome_elemento as elemento from curiosidade CS inner join elemento E on CS.elemento = E.id_elemento where CS.id_curiosidade=%s'

SQL_DELETA_DESAFIO = 'delete from desafio where id_desafio = %s'
SQL_CRIA_DESAFIO = 'INSERT into desafio (quantidade_perguntas, nivel) values (%s, %s)'
SQL_ATUALIZA_DESAFIO = 'UPDATE desafio SET quantidade_perguntas = %s, nivel = %s where id_desafio = %s'
SQL_BUSCA_DESAFIO = 'SELECT D.id_desafio, D.quantidade_perguntas, D.nivel, N.nome_nivel as nivel from desafio D inner join nivel N on D.nivel = N.id_nivel'
SQL_DESAFIO_POR_ID = 'SELECT D.id_desafio,  D.quantidade_perguntas, D.nivel, N.nome_nivel as nivel from desafio D inner join nivel N on D.nivel = N.id_nivel where D.id_desafio = %s'

SQL_BUSCA_NIVEL = 'SELECT id_nivel, nome_nivel from nivel'

SQL_DELETA_PERGUNTAS = 'delete from perguntas where id_perguntas = %s'
SQL_CRIA_PERGUNTAS = 'INSERT into perguntas (nome_pergunta, descricao, resposta, desafio) values (%s, %s, %s, %s)'
SQL_ATUALIZA_PERGUNTAS = 'UPDATE perguntas SET nome_pergunta = %s, descricao = %s, resposta = %s, desafio = %s where id_perguntas = %s'
SQL_BUSCA_PERGUNTAS = 'SELECT id_perguntas, nome_pergunta, descricao, resposta,desafio from perguntas'
SQL_PERGUNTAS_POR_ID = 'SELECT id_perguntas, nome_pergunta, descricao, resposta,desafio from perguntas where id_perguntas = %s'

class ElementoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, elemento):
        cursor = self.__db.connection.cursor()

        if (elemento._id):
            cursor.execute(SQL_ATUALIZA_ELEMENTO, (elemento._nome_elemento, elemento._num_atomico, elemento._massa_atomica,elemento._estado_fisico, elemento._simbolo, elemento._distribuicao_eletronica, elemento._classe_id, elemento._id))
        else:
            cursor.execute(SQL_CRIA_ELEMENTO, (elemento._nome_elemento, elemento._num_atomico, elemento._massa_atomica,
                           elemento._estado_fisico, elemento._simbolo, elemento._distribuicao_eletronica, elemento._classe_id))
            cursor._id = cursor.lastrowid

        self.__db.connection.commit()
        return elemento

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_ELEMENTO)
        elementos = traduz_elementos(cursor.fetchall())
        return elementos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_ELEMENTO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Elemento(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_ELEMENTO, (id,))
        self.__db.connection.commit()


def traduz_elementos(elementos):
    def cria_elemento_com_tupla(tupla):
        return Elemento(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], id=tupla[0])
    return list(map(cria_elemento_com_tupla, elementos))

class ClasseDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, classe):
        cursor = self.__db.connection.cursor()

        if (classe._id):
            cursor.execute(SQL_ATUALIZA_CLASSE, (classe._nome_classe, classe._id))

        else:
            cursor.execute(SQL_CRIA_CLASSE, (classe._nome_classe))
            cursor._id = cursor.lastrowid

        self.__db.connection.commit()
        return classe

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_CLASSE)
        classes = traduz_classes(cursor.fetchall())
        return classes

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CLASSE_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Classe(tupla[1], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_CLASSE, (id,))
        self.__db.connection.commit()

def traduz_classes(classes):
    def cria_classe_com_tupla(tupla):
        return Classe(tupla[1], id=tupla[0])
    return list(map(cria_classe_com_tupla, classes))

class CuriosidadesDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, curiosidade):
        cursor = self.__db.connection.cursor()

        if (curiosidade._id):
            cursor.execute(SQL_ATUALIZA_CURIOSIDADE, (curiosidade._tipo, curiosidade._descricao, curiosidade._elemento_id, curiosidade._id))

        else:
            cursor.execute(SQL_CRIA_CURIOSIDADE, (curiosidade._tipo, curiosidade._descricao, curiosidade._elemento_id))
            cursor._id = cursor.lastrowid

        self.__db.connection.commit()
        return curiosidade

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_CURIOSIDADE)
        curiosidades = traduz_curiosidades(cursor.fetchall())
        return curiosidades

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CURIOSIDADE_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Curiosidades(tupla[1], tupla[2], tupla[3], tupla[4], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_CURIOSIDADE, (id,))
        self.__db.connection.commit()

def traduz_curiosidades(curiosidades):
    def cria_curiosidade_com_tupla(tupla):
        return Curiosidades(tupla[1], tupla[2], tupla[3], tupla[4], id=tupla[0])
    return list(map(cria_curiosidade_com_tupla, curiosidades))

class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, usuario):
        cursor = self.__db.connection.cursor()

        if (usuario._id):
            cursor.execute(SQL_ATUALIZA_USUARIO, (usuario._usuario, usuario._nome, usuario._email, usuario._senha, usuario._id))
        else:
            cursor.execute(SQL_CRIA_USUARIO, (usuario._usuario, usuario._nome, usuario._email, usuario._senha))
            cursor._id = cursor.lastrowid

        self.__db.connection.commit()
        return usuario

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_USUARIO)
        usuarios = traduz_usuario(cursor.fetchall())
        return usuarios

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2],tupla[3], tupla[4])

class NivelDao:
    def __init__(self, db):
        self.__db = db

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_NIVEL)
        niveis = traduz_niveis(cursor.fetchall())
        return niveis  

def traduz_niveis(niveis):
    def cria_nivel_com_tupla(tupla):
        return Nivel(tupla[1], id=tupla[0])
    return list(map(cria_nivel_com_tupla, niveis)) 

class DesafioDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, desafio):
        cursor = self.__db.connection.cursor()

        if (desafio._id):
            cursor.execute(SQL_ATUALIZA_DESAFIO, (desafio._quantidade_perguntas, desafio._nivel_id, desafio._id))
        else:
            cursor.execute(SQL_CRIA_DESAFIO, (desafio._quantidade_perguntas, desafio._nivel_id))
            cursor._id = cursor.lastrowid

        self.__db.connection.commit()
        return desafio

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_DESAFIO)
        desafios = traduz_desafios(cursor.fetchall())
        return desafios

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_DESAFIO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Desafio(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_DESAFIO, (id,))
        self.__db.connection.commit()


def traduz_desafios(desafios):
    def cria_desafio_com_tupla(tupla):
        return Desafio(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_desafio_com_tupla, desafios))

class PerguntasDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, pergunta):
        cursor = self.__db.connection.cursor()

        if (pergunta._id):
            cursor.execute(SQL_ATUALIZA_PERGUNTAS, (pergunta._nome_pergunta, pergunta._descricao, pergunta._resposta, pergunta._desafio_id, pergunta._id))
        else:
            cursor.execute(SQL_CRIA_PERGUNTAS, (pergunta._nome_pergunta, pergunta._descricao, pergunta._resposta, pergunta._desafio_id))
            cursor._id = cursor.lastrowid

        self.__db.connection.commit()
        return pergunta

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_PERGUNTAS)
        perguntas = traduz_perguntas(cursor.fetchall())
        return perguntas

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_PERGUNTAS_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Perguntas(tupla[1], tupla[2], tupla[3], tupla[4], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_PERGUNTAS, (id,))
        self.__db.connection.commit()


def traduz_perguntas(perguntas):
    def cria_pergunta_com_tupla(tupla):
        return Perguntas(tupla[1], tupla[2], tupla[3], tupla[4], id=tupla[0])
    return list(map(cria_pergunta_com_tupla, perguntas))