from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
# from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf.csrf import CSRFProtect
from flask_restx import Api

import pymysql
pymysql.install_as_MySQLdb()

bcrypt = Bcrypt()
# csrf_protect = CSRFProtect()
# login_manager = LoginManager()
db = SQLAlchemy()
api = Api()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()