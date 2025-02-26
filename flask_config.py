class Config:
    FLASK_DEBUG = True
    FLASK_APP = "inf349"
    SECRET_KEY = "dev"
    DATABASE = "sqlite:///database.db"

class TestConfig(Config):
    FLASK_DEBUG = True
    DATABASE = "sqlite:///:memory:"
    TESTING = True