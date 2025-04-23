from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from sqlalchemy import create_engine

from api import ResourceTarefa, ResourceUser
from db import DB, Tarefa
from util import load_config

from os import urandom

def create_app(name:str, conf: dict):
    APP = Flask(name)
    APP.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

    API = Api(APP)
    API.add_resource(ResourceTarefa, '/', '/tarefa/<string:user>', '/tarefa/')
    API.add_resource(ResourceUser, '/usuario')

    APP.config['SECRET_KEY'] = urandom(32)
    APP.config['SQLALCHEMY_DATABASE_URI'] = conf['DATABASE_URI']

    DB.init_app(APP)
    MIGRATE = Migrate()
    MIGRATE.init_app(APP, DB)
    return APP

if __name__ == '__main__':
    conf = load_config()

    if conf is None:
        print("Missing environment variables:")
        print(" - MYSQL_USER")
        print(" - MYSQL_PASS")
        print(" - MYSQL_ADDR")
        print(" - MYSQL_PORT")
        print(" - MYSQL_DB")
        print(" - SERVER_ADDR")
        print(" - SERVER_PORT")
        print(" - DEBUG")
        exit(1)
    
    conf['DATABASE_URI'] = "mysql+pymysql://{uname}:{passw}@{addr}:{port}/{db}".format(**conf)
    APP = create_app(__name__, conf)
    APP.run(host=conf['sv_addr'], port=int(conf["sv_port"]), debug=bool(conf['debug']))