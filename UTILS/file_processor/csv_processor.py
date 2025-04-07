import pandas as pd
from .FileProcessor import FileProcessor

class CSVFileProcessor(FileProcessor):
    def load_data(self):
        try:
            df = pd.read_csv(self.file_path)
            return df.to_string(index=False)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return ""
