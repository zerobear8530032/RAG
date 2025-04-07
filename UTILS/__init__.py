import secrets
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from UTILS.file_processor import ChromaDBManager,CSVFileProcessor,HTMLFileProcessor,FileProcessor,JSONFileProcessor,PDFFileProcessor,WordFileProcessor,TextFileProcessor,User

app = Flask(__name__)
app.config["SECRET_KEY"] = b"9e166102899e65f779885fafe818473a"
app.config["SALT"] = b"0fa2ed81e1e8a1e98da72ce5a2b5fef3"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)
bcrypt =Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
app.config['MAIL_SERVER']="smtp.googlemail.com"
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']="saboorabdul627@gmail.com"
app.config['MAIL_PASSWORD']="axcakapeekqjzpzm"
mail = Mail(app)


from UTILS import routes
app.app_context().push()
