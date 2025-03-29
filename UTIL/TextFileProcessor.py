from abc import ABC
import os

class TextFileProcessor(FileProcessor):
    def load_data(self):
        """Reads a text file and returns its content."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""