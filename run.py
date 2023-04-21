from market_name import app,db
from market_name import routes
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from market_name.models import User,Admin_T,Show,Theatre,Booking
from wtforms import SelectField
from flask_login import LoginManager
from flask_admin import BaseView, expose
from flask_login import logout_user,current_user
from flask import redirect, url_for
from flask_admin import AdminIndexView
login_manager = LoginManager()

admin1=Admin(app)
admin1.login_manager = login_manager
admin1.add_view(ModelView(User,db.session))

class BookAdminView(ModelView):
    # Override the `create_form()` method to customize the fields displayed in the form
    form_columns = ['id','name','srno','seatno','price','theatre_id']
    def create_form(self):
        form = super(BookAdminView, self).create_form()
        form.threatre_id = SelectField('Theatre', coerce=str, choices=[(t.id, t.name) for t in Theatre.query.all()])
        return form
class TAdminView(ModelView):
    # Override the `create_form()` method to customize the fields displayed in the form
    form_columns = ['id','name','location']
    def create_form(self):
        form = super(TAdminView, self).create_form()
        return form
# Register your custom form class with Flask-Admin
admin1.add_view(BookAdminView(Show, db.session))
admin1.add_view(TAdminView(Theatre,db.session))

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect(url_for('log_page'))
        
admin1.add_view(LogoutView(name='Logout', endpoint='logout'))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
