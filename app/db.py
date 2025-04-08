from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

DB = SQLAlchemy()

class Tarefa(DB.Model):
    __tablename__ = 'tb_tarefa'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    nome = DB.Column(DB.String(100), nullable=False, unique=True)
    is_completa = DB.Column(DB.Boolean(), default=False)
    criada_em = DB.Column(DB.DateTime(), default=func.now())
    user = DB.Column(DB.Integer, ForeignKey('tb_user.id'))
    dono = relationship('User', back_populates='tarefas')
    
    def to_json(self):
        return {"nome": self.nome, "completa": self.is_completa, "criada_em": str(self.criada_em), "user": self.user}

    def __repr__(self):
        return f"<Tarefa {self.nome} {self.criada_em}>"
    
class User(DB.Model):
    __tablename__ = 'tb_user'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    nome = DB.Column(DB.String(32), nullable=False, unique=True)
    tarefas = relationship("Tarefa", back_populates='dono')

    def __repr__(self):
        return f"<User {self.nome}>"