from datetime import timedelta
import os
from dotenv import load_dotenv



def init_cfg(app):
    # JWT config
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_CSRF_CHECK_FORM'] = True
    # if not os.environ.get("OS") == "Windows_NT":
    #     app.config['JWT_COOKIE_DOMAIN'] = '.qweq.ru'
    # app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    # SQL Alchemy config
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"