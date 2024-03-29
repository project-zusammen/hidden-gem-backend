from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

import pymysql

pymysql.install_as_MySQLdb()

authorizations = {"bearer": {"type": "apiKey", "in": "header", "name": "X-API-KEY"}}

bcrypt = Bcrypt()
db = SQLAlchemy()
api = Api(prefix="/api")
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
