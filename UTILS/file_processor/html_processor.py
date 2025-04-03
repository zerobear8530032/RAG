import requests
from bs4 import BeautifulSoup
from .FileProcessor import FileProcessor

class HTMLFileProcessor(FileProcessor):
    def load_data(self):
        try:
            if self.file_path.startswith("http"):
                response = requests.get(self.file_path)
                response.raise_for_status()
                html_content = response.text
            else:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    html_content = file.read()

            soup = BeautifulSoup(html_content, "html.parser")
            return soup.get_text(separator="\n")

        except Exception as e:
            print(f"Error loading HTML data: {e}")
            return ""
