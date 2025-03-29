import os
from datetime import datetime
from abc import ABC, abstractmethod
import fitz  # 
from docx import Document
import pandas as pd
import json
from bs4 import BeautifulSoup
import requests


class FileProcessor:
    def __init__(self,file_path):
        self.file_path=file_path
    
    def get_metadata(self):
        self.file_name =os.path.basename(self.file_path)
        try:
            self.file_size =os.path.getsize(self.file_path)
            self.file_CreatedDate = datetime.fromtimestamp(os.path.getctime(self.file_path)).strftime('%Y-%m-%d %H:%M:%S')
            self.file_ModifiedDate = datetime.fromtimestamp(os.path.getmtime(self.file_path)).strftime('%Y-%m-%d %H:%M:%S')
            output= {"file_name":self.file_name,
                    "file_size":self.file_size,
                    "file_CreatedDate":self.file_CreatedDate,
                    "file_ModifiedDate":self.file_ModifiedDate,
                    "file_path":self.file_path}
            return output;
        except(Exception):
            return {}
        

    @abstractmethod
    def load_data(self):
        """Abstract method to load file content. Must be implemented in subclasses."""
        pass

    def create_chunks(self, chunk_size=500):
        """Splits the file content into fixed-size chunks."""
        data = self.load_data()  # Load full file content
        
        if not data:
            raise ValueError("File is empty or data could not be loaded.")
        
        self.chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


    def delete_File(self):
        """Delete the original file after processing."""
        if os.path.exists(self.file_path):
            try:
                os.remove(self.file_path)
                print(f"File deleted: {self.file_path}")
            except PermissionError:
                print(f"Permission denied: Cannot delete {self.file_path}")
            except Exception as e:
                print(f"Error deleting file {self.file_path}: {e}")
        else:
            print("File does not exist.")

    def load_chunks_to_db(self, db_instance):
        """Store extracted chunks into the ChromaDB database."""
        if not self.chunks:
            raise ValueError("No chunks available to store. Call `create_chunks()` first.")

        metadata = self.get_metadata()
        for idx, chunk in enumerate(self.chunks):
            db_instance.add_document({
                "content": chunk,
                "metadata": {
                    "file_name": metadata["file_name"],
                    "chunk_index": idx,
                    "file_path": metadata["file_path"]
                }
            })
        print(f"Chunks for {metadata['file_name']} added to DB.")


    def delete_chunks_from_db(self, db_instance):
        """Delete all chunks related to this file from ChromaDB."""
        if not db_instance:
            print("Error: Database instance is missing.")
            return

        try:
            # Use file path as a unique identifier
            metadata = self.get_metadata()
            file_path = metadata["file_path"]
            
            # Query database to find all chunks linked to this file
            db_instance.delete(
                where={"file_path": file_path}  # Deletes all matching records
            )
            
            print(f"All chunks for {file_path} deleted from ChromaDB.")

        except Exception as e:
            print(f"Error deleting chunks from DB: {e}")

class TextFileProcessor(FileProcessor):
    def load_data(self):
        """Reads a text file and returns its content."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""


class PDFFileProcessor(FileProcessor):
    def load_data(self):
        try:
            """Extracts text from a PDF file."""
            doc = fitz.open(self.file_path)
            text = "\n".join([page.get_text() for page in doc])
            doc.close()
            return text
        except(Exception):
            print(Exception)
            return "";




class WordFileProcessor(FileProcessor):
    def load_data(self):
        try:
            """Extracts text from a Word document."""
            doc = Document(self.file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except(Exception):
            print(Exception)
            return "";



class CSVFileProcessor(FileProcessor):
    def load_data(self):
        try:
            """Reads a CSV file and extracts text content."""
            df = pd.read_csv(self.file_path)
            return df.to_string(index=False)
        except(Exception):
            print(Exception)
            return "";

    


class JSONFileProcessor(FileProcessor):
    def load_data(self):
        try:
            """Reads a JSON file and extracts text content."""
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return json.dumps(data, indent=4)
        except(Exception):
            print(Exception)
            return "";

class HTMLFileProcessor(FileProcessor):
    def load_data(self):
        try:
            if self.file_path.startswith("http"):  # If it's a URL, fetch it
                response = requests.get(self.file_path)
                response.raise_for_status()  # Raise error if request fails
                html_content = response.text
            else:  # If it's a local file, read it
                with open(self.file_path, "r", encoding="utf-8") as file:
                    html_content = file.read()
            
            # Parse the HTML
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Return extracted text
            return soup.get_text(separator="\n")
        
        except Exception as e:
            print(f"Error loading HTML data: {e}")
            return ""

        


if __name__ == "__main__":
    file_path = r"https://www.grammarly.com/blog/parts-of-speech/articles/"  # Ensure the file exists
    processor = HTMLFileProcessor(file_path)

    metadata = processor.get_metadata()
    print(metadata)  # Print metadata info

    processor.create_chunks()
    print("Chunks:", processor.chunks[0])  # Print chunked data
