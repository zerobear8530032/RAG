import os
import shutil

class User:
    def __init__(self, base_path, username):
        self.base_path = os.path.abspath(base_path)  # Ensure absolute path
        self.dir = username  # Store username
        self.user_folder = os.path.join(self.base_path, self.dir)  # Create user folder path
        self.create_user_folder()  # Automatically create folder
    

    def create_user_folder(self):
        """Creates a folder for the user if it doesn't exist."""
        if not os.path.exists(self.user_folder):
            os.makedirs(self.user_folder)
            print(f"Folder created: {self.user_folder}")
        else:
            print(f"Folder already exists: {self.user_folder}")

    def deleteDir(self):
        """Deletes the user’s folder."""
        if os.path.exists(self.user_folder):
            shutil.rmtree(self.user_folder)
            print(f"Deleted directory: {self.user_folder}")
        else:
            print(f"Directory does not exist: {self.user_folder}")
if '__main__'== __name__:
    # Example Usage
    username = input("Enter username: ")  # Get username from user
    user = User("D:/python/flasks/RAG/RAG/DataBase", username)  # Create user instance
    print(f"user folder name:{user.user_folder}")
    # To delete the folder
    user.deleteDir()
