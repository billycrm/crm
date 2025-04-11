from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm


class MembershipView(ModelView):
    column_list = ('id', 'membership_type', 'active', 'start_date', 'end_date', 'user_id', 'has_used_free_trial')

    form_base_class = SecureForm