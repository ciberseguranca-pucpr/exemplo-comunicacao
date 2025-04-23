from flask_restful import Resource
from flask import request
from db import Tarefa, DB, User

class ResourceTarefa(Resource):
    def get(self, user: str = None):
        if user is None:
            a = Tarefa.query.all()
            return list(map(lambda x: x.to_json(), a)), 200

        tarefas = Tarefa.query.filter_by(user=user)
        return list(map(lambda x: x.to_json(), tarefas)), 200
    
    def post(self):
        data = request.get_json()

        t = Tarefa(**data)

        if tarefa_existe(t):
            return {"message": "Tarefa já existe"}, 400
        
        DB.session.add(t)
        DB.session.commit()
        
        return {"message": "Tarefa criada"}, 201
    
    def patch(self):
        data = request.get_json()

        if not data:
            return {"message": "não foi fornecido dados"}, 400

        if len(data) == 0:
            return {"message": "dados vazios"}, 400

        t = Tarefa(**data)
        if not tarefa_existe(t):
            return {"message": "tarefa não existe"}, 404

        t = Tarefa.query.filter_by(nome=t.nome).first()
        t.is_completa = data['is_completa']

        DB.session.commit()

        return {"message": "ok"}, 200

    def delete(self):
        data = request.get_json().get('nome')
        tarefa = Tarefa.query.filter_by(nome=data).first_or_404('Tarefa não encontrada')
        
        DB.session.delete(tarefa)
        DB.session.commit()
        return {"message": f"Tarefa '{tarefa.nome}' removida"}, 200
    
class ResourceUser(Resource):
    def post(self):
        data = request.get_json()

        nome = data.get('nome')
        if nome is None or len(nome) == 0:
            return {"message": "Não foi possível criar usuário. Nome vazio"}, 400  
        
        u = User(nome=nome)

        if self.__user_exist(u):
            return {"message": "usuário já existe"}, 400
        
        DB.session.add(u)
        DB.session.commit()
        return {"message": f'Usuário {u.nome} criado'}, 201
    
    def delete(self):
        data = request.get_json()

        nome = data.get('nome')
        user = User.query.filter_by(nome=nome).first_or_404('Usuário não encontrado')

        DB.session.delete(user)
        DB.session.commit()

        return {"message": "usuário removido"}, 200

    def __user_exist(self, u: User) -> bool:
        users = User.query.filter_by(nome=u.nome).all()

        return len(users) > 0

def tarefa_existe(t: Tarefa) -> bool:
    tarefas = Tarefa.query.filter_by(nome=t.nome).all()
    return len(tarefas) > 0