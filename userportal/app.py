import flask
from flask import g
from flask_admin import Admin
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from database.models.membership import Membership
from database.models.user import User
from database.models.token import TokenBlocklist, TokenList
from database.models.logs import Logs
from resources import config
from database.db import create_db, db
from routes.membership import membership_bp
from routes.user import user_bp
from routes.auth import auth_bp


# create flask app
app = flask.Flask(__name__)
app.secret_key = "super secret key"

# init app
config.init_cfg(app)
app.register_blueprint(membership_bp, url_prefix='/api/v1')
app.register_blueprint(user_bp, url_prefix='/api/v1')
app.register_blueprint(auth_bp, url_prefix='/api/v1')


# init jwt
jwt = JWTManager(app)

# init cors
CORS(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})


# init db
with app.app_context():
    create_db(app, jwt)

@app.add_template_global
def inject_csrf_token():
    if hasattr(g, 'csrf_token'):
        flask.g.csrf_token = g.csrf_token


# run app
if __name__ == '__main__':
    app.run("0.0.0.0", 5000, debug=True)
