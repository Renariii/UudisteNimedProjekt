import requests
from bs4 import BeautifulSoup

class WebScraper:
    """
    Laeb etteantud URL HTML, leiab pealkirjad (h1–h6).
    """

    def __init__(self, url: str):
        self.url = url
        self.html = ""
        self.headlines = []

    def download_html(self):
        """
        Laeb veebilehe HTML.
        """
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        self.html = response.text

    def parse_headlines(self):
        """
        Parsib HTML‑ist pealkirjad ja eemaldab duplikaadid.
        """
        if not self.html:
            self.download_html()

        soup = BeautifulSoup(self.html, "html.parser")
        raw = []
        for tag in ["h1","h2","h3","h4","h5","h6"]:
            for element in soup.find_all(tag):
                text = element.get_text(strip=True)
                if text:
                    raw.append(text)

        seen = set()
        self.headlines = [h for h in raw if not (h in seen or seen.add(h))]
