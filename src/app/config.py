# FIXME переписать на os.environ или pydantic или dotenv
POSTGRES_DB = 'movies_auth'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'passW'
#POSTGRES_HOST = 'postgres_auth'
POSTGRES_HOST = '127.0.0.1'
POSTGRES_PORT = '5432'
SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
