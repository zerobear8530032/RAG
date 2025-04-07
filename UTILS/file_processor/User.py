import secrets
import os
class User:
    BASE_PATH = os.path.join(os.getcwd(), "users")  
    def __init__(self,name,email,user_id):
        self.id = user_id if user_id else secrets.token_hex(16)
        self.name=name
        self.email=email
        self.folder_path = os.path.join(self.BASE_PATH, self.id)
        self.temp_path = os.path.join(self.folder_path, "temp")
        self.chroma_db_path = os.path.join(self.folder_path, "chroma_db")
    @classmethod
    def from_db(cls, name,email,user_id):
        """
        Create a User object from database data.
        user_data should be a dictionary containing 'id', 'name', and 'email'.
        """
        return cls(name=name, email=email, user_id=user_id)



    def __str__(self):
        return f"id : {self.id} , name : {self.name} , email : {self.email} , folder_Path : {self.folder_path} , temp_path {self.temp_path},chroma_db_path :{self.chroma_db_path}"

    def create_user_folder(self):
        """Creates a folder for the user if it doesn't exist."""
        os.makedirs(self.folder_path, exist_ok=True)
        os.makedirs(self.chroma_db_path, exist_ok=True)
        os.makedirs(self.temp_path, exist_ok=True)
    
    def get_chroma_db_path(self):
        """Returns the path to the user's ChromaDB instance."""
        return self.chroma_db_path
    
if ('__main__'== __name__):
    # Create a new user (ID is auto-generated)
    user = User(name="Abdul Saboor", email="saboor@example.com")

    print("Generated User ID:", user.id)
    print("User folder:", user.folder_path)
    print("ChromaDB path:", user.get_chroma_db_path())
    user.create_user_folder()
