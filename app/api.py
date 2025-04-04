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

        DB.session.add(t)
        DB.session.commit()

        return {"message": "Tarefa criada"}
    
    def delete(self):
        data = request.get_json().get('nome')
        tarefa = Tarefa.query.filter_by(nome=data).first_or_404('Tarefa não encontrada')
        
        DB.session.delete(tarefa)
        DB.session.commit()
        return {"message": f"Tarefa '{tarefa.nome}' removida"}