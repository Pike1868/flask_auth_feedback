class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql:///flask_feedback_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    SECRET_KEY = 'secret'
    DEBUG = True
    
class Testing:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///flask_feedback_db_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_RECORD_QUERIES = True
    SECRET_KEY = 'secret'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG = True