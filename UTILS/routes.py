import secrets
import pickle
import traceback
from datetime import datetime
from UTILS import app,db,bcrypt,mail
from flask import render_template,flash,redirect,url_for,request,abort,send_from_directory
from UTILS.forms import RegisterForm,LoginForm,UpdateAccountForm,RequestResetForm,ResetPasswordForm,ProductLink,APIGenerator,DeleteAPI,ContactUsForm
from UTILS.models import Registertable
from UTILS.file_processor.User import User
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message
from flask import jsonify,session


@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        print("Form validation successful!")  # Add a print statement to check if form validation is successful
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user= User(name=form.username.data.lower(),email=form.email.data.lower(),user_id=None)
        userdata = Registertable(id=user.id,username=user.name, email=user.email, password=hashed,folder_path=user.folder_path,chroma_db_path=user.chroma_db_path)
        user.create_user_folder()
        db.session.add(userdata)
        db.session.commit()
        print(userdata.__repr__())
        flash("Your account is created and you can login now!", 'success')
        return redirect(url_for('login'))  
    else:
        print("Form validation failed!") 
    return render_template("register.html", title="Register", form=form)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
            userdata=Registertable.query.filter_by(email=form.email.data.lower()).first()
            if(userdata and bcrypt.check_password_hash(userdata.password,form.password.data)):
                 login_user(userdata,remember=form.remember.data)
                 return redirect(url_for("home"))
            elif(userdata):
                flash("check your password","danger")
            else:     
                flash('Wrong Email Entered',"danger")
    return render_template("login.html",title="Login",form=form)




@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request',sender="saboorabdul627@gmail.com",recipients=[user.email])
    msg.body=f''' to Rese your password visit the following link :
    http://127.0.0.1:5000/{url_for('reset_token',token=token,external=True)}   
    if you did not request reset then ignore this email
     
    alternative link http://192.168.100.226:5000/{url_for("reset_token",token=token,external=True)}
    localhost  link http://localhost:5000/{url_for("reset_token",token=token,external=True)}
    '''
    msg.body=f''' to Rese your password visit the following link :
    {url_for('reset_token',token=token,external=True)}   
    if you did not request reset then ignore this email
    alternative link http://192.168.100.226:5000/{url_for("reset_token",token=token,external=True)}
    localhost  link http://localhost:5000/{url_for("reset_token",token=token,external=True)}
   '''
    

    mail.send(msg)


@app.route("/reset_password",methods=['POST','GET'])
def reset_request():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user_data=Registertable.query.filter_by(email=form.email.data).first()
        send_reset_email(user_data)
        flash("check your email to reset password !","info")
        return redirect(url_for('login'))
    return render_template('resetrequest.html',form=form)


@app.route("/reset_password/<token>",methods=['POST','GET'])
def reset_token(token):
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    user_data=Registertable.verify_reset_token(token)
    if user_data is None:
        flash("That is an Inavalid token the link is Expired ",'warning')
        return redirect(url_for('reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        print("Form validation successful!")  # Add a print statement to check if form validation is successful
        hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user_data.password=hashed
        db.session.commit()
        flash("Your Password is reset !", 'success')
        return redirect(url_for('login')) 
    return render_template('resetpassword.html',form=form)


@app.route("/llm")
def llm():
    user_data=Registertable.query.filter_by(username=current_user.username).first()
    user=User(user_data.username,user_data.email,user_data.id)
    return render_template("llm.html",user_data=user_data,user=user)


