import os

SECRET_KEY = "oa8dqji01-%@^%@1d^4c#johe$2(s18!joc31ipxwvix4+_9+"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
