import os
from sanic.log import logger
from environs import Env

env = Env()
ENV_FILE = ".env.local" if os.path.exists(".env.local") else ".env"
env.read_env(ENV_FILE)

class Settings:
    HOST = env.str("HOST", "0.0.0.0")
    PORT = env.int("PORT", 8000)
    DEBUG = env.bool("DEBUG", True)
    SECRET_KEY = env.str("SECRET_KEY", "supersecretkey")
    
    DB_USER = env.str("DB_USER", "postgres")
    DB_PASSWORD = env.str("DB_PASSWORD", "password")
    DB_HOST = env.str("DB_HOST", "localhost")
    DB_PORT = env.int("DB_PORT", 5432)
    DB_NAME = env.str("DB_NAME", "SanicPay")

    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    logger.info(f"Loaded settings from {ENV_FILE}")
    logger.info(f"Database URL: {DATABASE_URL}")

settings = Settings()
