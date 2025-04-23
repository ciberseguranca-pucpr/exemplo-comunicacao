import pytest
from main import create_app
from sqlalchemy import create_engine
from db import Tarefa, User
from pathlib import Path
from shutil import rmtree

def new_app(database_uri: str):
    app = create_app('test', dict(
        uname='',
        passw='',
        addr='',
        port=0,
        db='',
        SERVER_ADDR='',
        SERVER_PORT='',
        DEBUG=True,
        DATABASE_URI=f"sqlite:////{database_uri}"
    ))
    app.config.update(TESTING=True)

    return app

@pytest.fixture
def client():
    base = Path(__file__).parent.absolute()
    p = base / Path("instance/test.db")

    if not p.parent.exists():
        p.parent.mkdir(exist_ok=True)

    with new_app(str(p.absolute())).test_client() as client:
        engine = create_engine(f"sqlite:///{p.absolute()}")
        Tarefa.metadata.create_all(engine)
        User.metadata.create_all(engine)
        yield client
        
        rmtree(p.parent)

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == []

def test_create_user(client):
    response = client.post('/usuario', json={
        'nome': 'teste'
    })

    recv_json = response.get_json()
    assert recv_json['message'] == "Usuário teste criado"
    assert response.status_code == 201

def test_create_user_exist(client):
    response = client.post('/usuario', json={
        'nome': 'teste'
    })
    recv_json = response.get_json()
    assert recv_json['message'] == "Usuário teste criado"
    assert response.status_code == 201

    response = client.post('/usuario', json={
        'nome': 'teste'
    })

    recv_json = response.get_json()
    assert recv_json['message'] == "usuário já existe"
    assert response.status_code == 400

def test_create_empty_user(client):
    response = client.post('/usuario', json={
        'nome': ''
    })

    recv_json = response.get_json()
    assert recv_json['message'] == "Não foi possível criar usuário. Nome vazio"
    assert response.status_code == 400