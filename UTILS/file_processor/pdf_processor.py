import fitz
from .FileProcessor import FileProcessor

class PDFFileProcessor(FileProcessor):
    def load_data(self):
        try:
            doc = fitz.open(self.file_path)
            text = "\n".join([page.get_text() for page in doc])
            doc.close()
            return text
        except Exception as e:
            print(f"Error reading PDF file: {e}")
            return ""
