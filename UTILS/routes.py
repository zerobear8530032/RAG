from google import genai
import os
import shutil
import requests
import secrets
import pickle
import traceback
from werkzeug.utils import secure_filename
from datetime import datetime
from UTILS import app,db,bcrypt,mail
from flask import render_template,flash,redirect,url_for,request,abort,send_from_directory
from UTILS.forms import RegisterForm,LoginForm,RequestResetForm,InputQueryForm,ResetPasswordForm,ContactUsForm,CollectDocumentForm
from UTILS.models import Registertable,ContactUsTable
from UTILS.file_processor import FileProcessor,CSVFileProcessor,HTMLFileProcessor,ChromaDBManager,JSONFileProcessor,PDFFileProcessor,TextFileProcessor,WordFileProcessor
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
        userdata = Registertable(id=user.id,username=user.name, email=user.email, password=hashed,folder_path=user.folder_path,temp_path=user.temp_path,chroma_db_path=user.chroma_db_path)
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



def clean_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
   
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)  # remove file or symbolic link
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # remove directory and contents
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")


@app.route("/delete_file", methods=["POST"])
@login_required
def delete_file():
    # Get the filename from the form
    filename = request.form.get("filename")

    # Get the user's folder
    try:
        user_data = Registertable.query.filter_by(username=current_user.username).first()
        user_folder = user_data.temp_path
    except:
        flash("User authentication failed. Please log in again.", "error")
        return redirect(url_for("login"))

    if not filename:
        flash("No file specified for deletion.", "error")
        return redirect(url_for("uploadDocument"))

    # Full path to the file
    file_path = os.path.join(user_folder, filename)

    # Check and delete
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            flash(f"{filename} has been deleted successfully.", "success")
        except Exception as e:
            flash(f"Error deleting file: {str(e)}", "error")
    else:
        flash("File not found.", "error")

    return redirect(url_for("uploadDocument"))


@login_required
@app.route("/UploadDocuments", methods=["GET", "POST"])
def uploadDocument():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    user_data=Registertable.query.filter_by(username=current_user.username).first()
    user=User(user_data.username,user_data.email,user_data.id)
    database= ChromaDBManager(user)
    form = CollectDocumentForm()
    user_folder = user.temp_path
    used_bytes = get_folder_size(user_folder)
    max_bytes = 100 * 1024 * 1024  
    used_percentage = round((used_bytes / max_bytes) * 100, 2)
    if not os.path.exists(user_folder):
        flash("User folder not found! Contact support.", "error")
        return redirect(url_for("UploadDocuments"))
    
    if form.validate_on_submit():
        file = form.document.data
        filename = secure_filename(file.filename)
        # Check if file would exceed limit
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset pointer

        if used_bytes + file_size > max_bytes:
            flash("Upload failed. Storage limit of 100 MB exceeded.", "error")
            return redirect(url_for("uploadDocument"))
        filepath = os.path.join(user_folder, filename)
        file.save(filepath)  # Save inside the user's folder
        try:
            _,file_extension = os.path.splitext(filepath)
            flash("File Chunking in Progress...", "info")
            match(file_extension):
                case ".txt":
                    chunking = TextFileProcessor(file_path=filepath)
                    print("text file")
                    chunking.create_chunks()
                    database.add_chunks_to_db(chunking.chunks)
                    # clean_folder(user_folder)
                case ".pdf":
                    chunking = PDFFileProcessor(file_path=filepath)
                    print("pdf file")
                    chunking.create_chunks()
                    database.add_chunks_to_db(chunking.chunks)
                    # clean_folder(user_folder)
                case ".doc":
                    chunking = WordFileProcessor(file_path=filepath)
                    print("doc")
                    chunking.create_chunks()
                    database.add_chunks_to_db(chunking.chunks)
                    # clean_folder(user_folder)
                case ".docx":
                    chunking = WordFileProcessor(file_path=filepath)
                    print("docx file")
                    chunking.create_chunks()
                    database.add_chunks_to_db(chunking.chunks)
                    # clean_folder(user_folder)
                case ".csv":
                    chunking = CSVFileProcessor(file_path=filepath)
                    print("docx file")
                    chunking.create_chunks()
                    database.add_chunks_to_db(chunking.chunks)
                    # clean_folder(user_folder)
                case ".json":
                    chunking = JSONFileProcessor(file_path=filepath)
                    print("docx file")
                    chunking.create_chunks()
                    database.add_chunks_to_db(chunking.chunks)
                    # clean_folder(user_folder)
                case ".html":
                    chunking = HTMLFileProcessor(file_path=filepath)
                    print("docx file")
                    chunking.create_chunks()
                    database.add_chunks_to_db(chunking.chunks)
                    # clean_folder(user_folder)
            flash(f"File uploaded successfully: {filename}", "success")
        except Exception as e:
            flash(f"Error processing file: {str(e)}", "error")
            return redirect(url_for("UploadDocuments"))
    allfiles=os.listdir(user_folder)
    filenames=[ os.path.basename(file) for file in allfiles]
    flash("sdfsdf")
    return render_template("UploadDocuments.html", form=form,filenames=filenames,  used_storage=used_bytes,max_storage=max_bytes,used_percentage=used_percentage)

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    user_data = Registertable.query.filter_by(username=current_user.username).first()
    if not user_data:
        abort(403)
    user_folder = User(user_data.username, user_data.email, user_data.id).temp_path
    filepath = os.path.join(user_folder, filename)

    if not os.path.exists(filepath):
        flash("File not found!", "error")
        return redirect(url_for('uploadDocument'))

    return send_from_directory(user_folder, filename, as_attachment=True)


@app.route("/about",methods=["GET","POST"])
def about():
    return render_template("about.html")
@app.route("/service",methods=["GET","POST"])
def service():
    return render_template("services.html")


@app.route("/clear_chat", methods=["POST"])
@login_required
def clear_chat():
    session["chat_history"] = []
    flash("Chats Cleared Successfully","success")
    return redirect(url_for("query"))


@app.route("/query", methods=["GET", "POST"])
@login_required
def query():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    form = InputQueryForm()
    username = current_user.username
    user_data = Registertable.query.filter_by(username=username).first()

    # Initialize chat history in session if not exists
    if "chat_history" not in session:
        session["chat_history"] = []

    chat_history = session.get("chat_history", [])

    if form.validate_on_submit():
        message = form.query.data
        form.query.data=None
        user = User(user_data.username, user_data.email, user_data.id)
        database = ChromaDBManager(user)

        # Query ChromaDB
        data = database.query_document(message)["documents"][0]
        llmquery = f"""You are a helpful assistant. Use the context below to answer the question.
        Context:{data}
        Question:{message}
        Answer:"""

        client = genai.Client(api_key="AIzaSyAggQIrB0LMp_cDGtB9rNY5bBD2K4lQlrY")
        response = client.models.generate_content(model="gemini-2.0-flash", contents=llmquery)
        reply = response.text

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append new messages to chat history
        chat_history.append({"sender": "sent", "text": message, "time": timestamp})
        chat_history.append({"sender": "received", "text": reply, "time": timestamp})

        # Save updated chat history to session
        session["chat_history"] = chat_history

    return render_template("chat.html", username=username, form=form, chat_history=chat_history)

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total_size += os.path.getsize(fp)
    return total_size























@app.route("/login2",methods=['POST','GET'])
def login2():
    # # if current_user.is_authenticated:
    # #      return redirect(url_for('home'))
    form=LoginForm()
    # # if form.validate_on_submit():
    #         userdata=Registertable.query.filter_by(email=form.email.data.lower()).first()
    #         if(userdata and bcrypt.check_password_hash(userdata.password,form.password.data)):
    #              login_user(userdata,remember=form.remember.data)
    #              return redirect(url_for("home"))
    #         elif(userdata):
    #             flash("check your password","danger")
    #         else:     
    #             flash('Wrong Email Entered',"danger")
    return render_template("login1.html",title="Login",form=form)


@app.route("/contact",methods=['POST','GET'])
def contact():
    form= ContactUsForm()
    if(form.validate_on_submit()):
        contact_data=ContactUsTable(name=form.name.data.lower(),email=form.email.data.lower(),subject=form.subject.data,phone=form.phonenumber.data,message=form.message.data)
        db.session.add(contact_data)
        db.session.commit()
        flash("Your Feed Back Submit Successfully","success")
        return redirect(url_for('contact'))
    print(form.errors)
    return render_template("contact.html",form=form)

