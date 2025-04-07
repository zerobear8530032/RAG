import secrets
from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer  # Add this import
from UTILS import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Registertable.query.get(user_id)

class Registertable(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True,default=secrets.token_hex(16))
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    folder_path  = db.Column(db.String(200),nullable=False)
    temp_path  = db.Column(db.String(200),nullable=False)
    chroma_db_path= db.Column(db.String(200),nullable=False)
    
    def __repr__(self):
        return f"id {self.id} , name {self.username} , email {self.email} , password {self.password} , folderpath {self.folder_path} , chroma_db_path {self.chroma_db_path}"
    def __str__(self):
        return f"id {self.id} , name {self.username} , email {self.email} , password {self.password} , folderpath {self.folder_path} , chroma_db_path {self.chroma_db_path}"


    
    SECRET_KEY = app.config["SECRET_KEY"].decode('utf-8')
    SALT = app.config["SALT"].decode('utf-8')

    def get_reset_token(self, expires_sec=1800):
        s = URLSafeTimedSerializer(self.SECRET_KEY)
        return s.dumps({'user_id': self.id}, salt=self.SALT)

    @staticmethod
    def verify_reset_token(token):
        s = URLSafeTimedSerializer(Registertable.SECRET_KEY)
        try:
            user_id = s.loads(token, salt=Registertable.SALT, max_age=1800)['user_id']
        except Exception:
            return None  # Token expired or invalid
        return Registertable.query.get(user_id)



class ContactUsTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    email= db.Column(db.String)
    subject= db.Column(db.String)
    phone= db.Column(db.Integer)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

