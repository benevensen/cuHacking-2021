import os


class Config:
    JWT_SECRET = os.getenv("JWT_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite://///etc/shg/db.sqlite"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


def get_config() -> Config:
    return CONFIG_LEVELS.get(os.getenv('CONFIG_LEVEL'), DevelopmentConfig)


CONFIG_LEVELS = {
    'Development': DevelopmentConfig,
    'Production': ProductionConfig
}
