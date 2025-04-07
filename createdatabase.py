
from UTILS import app, db
# from UTILS.models import Registertable
# from UTILS.file_processor.User import User
# # user_data = Registertable.query.filter(Registertable.id == "80938a7764e68761c83ecee13304ba4b").first()
# # print("Fetched User Data:", user_data.username)
# # name=input("Enter your name :")
# # email=input("Enter your email :")
# # user= User(name,email)
# # user.create_user_folder()
# # userdata = Registertable(username=user.name, email=user.email, password="password",folder_path=user.folder_path,chroma_db_path=user.chroma_db_path)
# # db.session.add(userdata)
# # db.session.commit()
db.create_all()
print(db.__repr__())
