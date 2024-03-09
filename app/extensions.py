from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Namespace
from flask_caching import Cache
from app.settings import redis_cache_config

import os
import pymysql

pymysql.install_as_MySQLdb()

authorizations = {"bearer": {"type": "apiKey", "in": "header", "name": "X-API-KEY"}}

bcrypt = Bcrypt()
db = SQLAlchemy()
api = Api()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
ns = Namespace("api", authorizations=authorizations)

# if os.environ["DEBUG"].lower() == "true":
#     cache = Cache(config={"CACHE_TYPE": "null"})
# else:
cache = Cache(config=redis_cache_config)

ns.cache = cache