import os
from datetime import timedelta
from os import getenv

from attr import frozen
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@frozen
class PostgresConfig:
    user: str = getenv('POSTGRES_USER', 'urbaton')
    password: str = getenv('POSTGRES_PASSWORD', 'urbaton')
    database: str = getenv('POSTGRES_DB', 'urbaton')
    host: str = getenv('POSTGRES_HOST', '127.0.0.1')
    port: int = getenv('POSTGRES_PORT', 5432)


@frozen
class JWTConfig:
    secret_key = getenv('JWT_SECRET_KEY', 'AnyaKillMePlease')
    access_token_expires = timedelta(seconds=int(getenv('JWT_ACCESS_TOKEN_EXPIRES', 300)))
    error_message_key = 'error'


@frozen
class Config:
    db = PostgresConfig()
    jwt = JWTConfig()


config = Config()
