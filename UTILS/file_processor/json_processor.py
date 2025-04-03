import json
from .FileProcessor import FileProcessor

class JSONFileProcessor(FileProcessor):
    def load_data(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return json.dumps(data, indent=4)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return ""
