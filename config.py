# config.py

DATABASE = {
    'user': 'postgres',
    'password': 'newpassword',
    'host': 'localhost:5432',
    'dbname': 'InExp'
}

SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}/{DATABASE['dbname']}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
