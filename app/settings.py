from environs import Env

env = Env()
env.read_env()

db_host = env.str("DB_HOST")
db_user = env.str("DB_USER")
db_password = env.str("DB_PASSWORD")
db_port = env.str("DB_PORT")
debug_mode = env.str("DEBUG")

DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/defaultdb"

ENV = env.str("FLASK_ENV", default="production")
print('ENV: ', ENV)
DEBUG = ENV == "dev"
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SECRET_KEY = env.str("SECRET_KEY")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = "SimpleCache"  # Can be "MemcachedCache", "RedisCache", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False