from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime
DB = SQLAlchemy()

class Tarefa(DB.Model):
    __tablename__ = 'tb_tarefa'
    id = DB.Column(DB.Integer, primary_key=True)
    nome = DB.Column(DB.String(100), nullable=False)
    is_completa = DB.Column(DB.Boolean(), default=False)
    criada_em = DB.Column(DB.DateTime(), default=func.now())
    
    def to_json(self):
        return {"nome": self.nome, "completa": self.is_completa, "criada_em": str(self.criada_em)}

    def __repr__(self):
        return f"<Tarefa {self.nome} {self.criada_em}>"