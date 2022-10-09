from pathlib import Path

BASEDIR = Path(__file__).parent


class DEVConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSV_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    SERVER_NAME = "localhost:8000"
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = "redis://localhost:6379/0"

class PRODConfig:
    SQLALCHEMY_DATABASE_URI = ""
    CSV_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = ""

Config = DEVConfig
