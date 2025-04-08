from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from api import ResourceTarefa, ResourceUser
from db import DB
from util import load_config

from os import urandom

APP = Flask(__name__)

API = Api(APP)
API.add_resource(ResourceTarefa, '/tarefa/<string:user>', '/tarefa/')
API.add_resource(ResourceUser, '/usuario')

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

APP.config['SECRET_KEY'] = urandom(32)
APP.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{uname}:{passw}@{addr}:{port}/{db}".format(**conf)

DB.init_app(APP)
MIGRATE = Migrate(APP, DB)

if __name__ == '__main__':
    APP.run(host=conf['sv_addr'], port=int(conf["sv_port"]), debug=bool(conf['debug']))