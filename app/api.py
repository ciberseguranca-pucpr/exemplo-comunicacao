from flask_restful import Resource
from flask import request
from db import Tarefa, DB

class ResourceTarefa(Resource):
    def get(self):
        a = Tarefa.query.all()
        return list(map(lambda x: x.to_json(), a))
    
    def post(self):
        data = request.get_json()

        t = Tarefa(**data)

        if tarefa_existe(t):
            return {"message": "Tarefa já existe"}
        
        DB.session.add(t)
        DB.session.commit()
        
        return {"message": "Tarefa criada"}
    
    def patch(self):
        data = request.get_json()

        if not data:
            return {"message": "não foi fornecido dados"}

        if len(data) == 0:
            return {"message": "dados vazios"}

        t = Tarefa(**data)
        if not tarefa_existe(t):
            return {"message": "tarefa não existe"}

        t = Tarefa.query.filter_by(nome=t.nome).first()
        t.is_completa = data['is_completa']

        DB.session.commit()

        return {"message": "ok"}

    def delete(self):
        data = request.get_json().get('nome')
        tarefa = Tarefa.query.filter_by(nome=data).first_or_404('Tarefa não encontrada')
        
        DB.session.delete(tarefa)
        DB.session.commit()
        return {"message": f"Tarefa '{tarefa.nome}' removida"}

def tarefa_existe(t: Tarefa) -> bool:
    tarefas = Tarefa.query.filter_by(nome=t.nome).all()
    return len(tarefas) > 0