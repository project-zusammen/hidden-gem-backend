from environs import Env

env = Env()
env.read_env()

db_user = env.str("TEST_DB_USER")
db_password = env.str("TEST_DB_PASSWORD")
debug_mode = env.str("DEBUG")

from .settings import get_db_uri

DATABASE_URI = get_db_uri(db_user=db_user, db_password=db_password)
TESTING = True
SQLALCHEMY_DATABASE_URI = DATABASE_URI
BCRYPT_LOG_ROUNDS = 4
DEBUG_TB_ENABLED = False
