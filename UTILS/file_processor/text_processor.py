from .FileProcessor import FileProcessor

class TextFileProcessor(FileProcessor):
    def load_data(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""
