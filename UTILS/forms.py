from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField, URLField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL,Optional
from UTILS.models import Registertable
from flask_wtf.file import FileField,FileAllowed

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField("Email", validators=[DataRequired(), Length(min=6), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user_exists = Registertable.query.filter_by(username=username.data).first()
        if user_exists:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        email_exists = Registertable.query.filter_by(email=email.data).first()
        if email_exists:
            raise ValidationError('Email address already registered.')
        
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(min=6), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


    def validate_username(self, username):
        if username.data != current_user.username:
            user_exists = Registertable.query.filter_by(username=username.data).first()
            if user_exists:
                raise ValidationError('Username already taken.')
        

class RequestResetForm(FlaskForm):
    email=StringField('email',validators=[DataRequired(),Email()])
    submit=SubmitField('Request Reset Password')
    def validate_email(self, email):
        email_exists = Registertable.query.filter_by(email=email.data).first()
        if email_exists is None:
            raise ValidationError('No account with that email found ')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit=SubmitField('Reset Password')




class ContactUsForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phonenumber = IntegerField("Phone Number", validators=[Optional()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Message",validators=[DataRequired(), Length(min=8, max=800)])
    submit = SubmitField('Send Message')

class CollectDocumentForm(FlaskForm):
    document = FileField("Select a File", validators=[
        FileAllowed(["txt", "doc", "docx", "pdf", "csv", "json", "html"], 
                    "Only .txt, .doc, .docx, .pdf, .csv, .json, and .html files are allowed!")
    ])
    submit=SubmitField("Upload")


class InputQueryForm(FlaskForm):
    query = StringField("Query",validators=[DataRequired()],render_kw={"placeholder": "Enter Your Query"})
    submit =SubmitField("Send")