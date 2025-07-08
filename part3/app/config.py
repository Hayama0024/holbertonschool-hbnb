class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False