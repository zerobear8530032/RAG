from docx import Document
from .FileProcessor import FileProcessor

class WordFileProcessor(FileProcessor):
    def load_data(self):
        try:
            doc = Document(self.file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"Error reading Word file: {e}")
            return ""
