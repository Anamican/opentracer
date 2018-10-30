from pathlib import Path
import json


class FileHandler:
    """
        This class is used for file handling operations only
    """
    def __init__(self, filename):
        self.filename = filename

    def check_if_file_exists(self):
        file_path = Path(self.filename)
        return file_path.is_file()

    def get_file_contents(self):
        # Not checking file empty and other cases for the sake of simplicity
        if self.check_if_file_exists() is True:
            with open(self.filename) as f:
                file_content = json.load(f)
            return file_content
        else:
            raise FileNotFoundError
