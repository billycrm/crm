import os

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(__file__))


def create_db(app, jwt):
    db.init_app(app)
    db.create_all()

    from database.models.token import TokenBlocklist
    from database.models.user import User

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    users = db.session.query(User).count()

    if users == 0:
        from database.models.user import User
        admin = User(username='admin', password='11211121', admin=True, name='Администратор', email="billy@admin.admin",
                     email_confirmed=True, user_confirmed=True)
        db.session.add(admin)
        db.session.commit()
        print('Database created!')


