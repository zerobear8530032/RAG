import os
from datetime import datetime
from abc import ABC, abstractmethod

class FileProcessor(ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    def get_metadata(self):
        self.file_name = os.path.basename(self.file_path)
        try:
            self.file_size = os.path.getsize(self.file_path)
            self.file_CreatedDate = datetime.fromtimestamp(os.path.getctime(self.file_path)).strftime('%Y-%m-%d %H:%M:%S')
            self.file_ModifiedDate = datetime.fromtimestamp(os.path.getmtime(self.file_path)).strftime('%Y-%m-%d %H:%M:%S')
            return {
                "file_name": self.file_name,
                "file_size": self.file_size,
                "file_CreatedDate": self.file_CreatedDate,
                "file_ModifiedDate": self.file_ModifiedDate,
                "file_path": self.file_path
            }
        except Exception:
            return {}

    @abstractmethod
    def load_data(self):
        pass

    def create_chunks(self, chunk_size=500):
        data = self.load_data()
        doc_name = self.get_metadata()["file_name"]  # Corrected method call
        if not data:
            raise ValueError("File is empty or data could not be loaded.")
        self.chunks = [
            {
                "id": f"{doc_name}_chunk{idx}",  # Custom ID format
                "content": data[i:i + chunk_size],
                "metadata": {"chunk_number": idx, "source": doc_name}
            }
            for idx, i in enumerate(range(0, len(data), chunk_size))
        ]
        return self.chunks
       


        
     