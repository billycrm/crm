from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from wtforms.fields.simple import PasswordField

from database.models.user import User


class UserView(ModelView):

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(UserView, self).__init__(User, session, **kwargs)

    column_list = ('id', 'username', 'email', 'name', 'email_confirmed', 'user_confirmed', 'role', 'admin')

    form_extra_fields = {
        'password': PasswordField('Password')

    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = generate_password_hash(form.password.data, method='sha256')
