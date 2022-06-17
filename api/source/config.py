class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOTS = 'localhost'
    MYSQL_USER = 'user'
    MYSQL_PASSWORD = 'mypassword'
    MYSQL_DB = 'api_flask'

config = {
    'development': DevelopmentConfig
}