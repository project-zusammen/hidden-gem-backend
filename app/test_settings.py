from environs import Env

env = Env()
env.read_env()

db_host = env.str("DB_HOST")
db_user = env.str("TEST_DB_USER")
db_password = env.str("TEST_DB_PASSWORD")
db_port = env.str("DB_PORT")
db_name = env.str("DB_NAME")
debug_mode = env.str("DEBUG")

from .settings import get_db_uri

DATABASE_URI = get_db_uri(db_name)
TESTING = True
SQLALCHEMY_DATABASE_URI = DATABASE_URI
BCRYPT_LOG_ROUNDS = 4
DEBUG_TB_ENABLED = False
