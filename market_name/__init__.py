from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# app = Flask(__name__) ## app object, adding extra configuration to recognize db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db' ##dictionary, uniform resource identifier
app.config['SECRET_KEY'] = 'd14a8fd67390991a3bdc0f40'



db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from market_name import routes