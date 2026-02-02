import os
import json
from urllib.parse import urlparse

class JSONSaver:
    """
    Salvestab nimekirja JSON‑faili, mis põhineb domeenil.
    """

    def __init__(self, url: str, names: list[str]):
        self.url = url
        self.names = names

    def determine_filename(self) -> str:
        """
        Domeeni põhjal määrab faili nime.
        """
        parsed = urlparse(self.url)
        domain = parsed.netloc.lower()
        parts = domain.split(".")
        base = parts[0]
        dir_path = os.path.join(os.path.dirname(__file__), "json_files")
        os.makedirs(dir_path, exist_ok=True)
        return os.path.join(dir_path, f"{base}.json")

    def save(self) -> str:
        """
        Kirjutab nimed JSON‑faili ja tagastab faili tee.
        """
        data = {"names": self.names}
        filename = self.determine_filename()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return filename
