from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Namespace

import pymysql

pymysql.install_as_MySQLdb()

bcrypt = Bcrypt()
db = SQLAlchemy()
api = Api()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
ns = Namespace("api")
