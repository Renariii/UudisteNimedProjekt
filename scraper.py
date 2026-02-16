import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time


class NewsScraper:
    """
    Klassi eesmärk on koguda uudistepealkirjad veebilehtedelt ja eraldada nimesid.
    """

    def __init__(self, url):
        """
        Konstruktor, mis võtab URL-i ja valmistab selle töötlemiseks ette.
        :param url: URL, mille sisu laaditakse ja analüüsitakse
        """
        self.url = url
        self.names_and_headlines = []  # Loend paaride jaoks: nimi ja vastav pealkiri
        self.base_url = self.get_base_url(url)
        self.file_name = f"json_files/{self.base_url}.json"  # Salvestame JSON faili õigesse kausta

    def get_base_url(self, url):
        """
        Funktsioon, mis tagastab veebilehe põhiosa (ilma protokolli ja lõpp-punktita).
        Näiteks: 'kroonika.delfi.ee' või 'delfi.ee'
        :param url: veebilehe URL
        :return: veebilehe nimi (nt 'delfi')
        """
        match = re.search(r'https?://(www\.)?([^/]+)', url)
        if match:
            return match.group(2).split('.')[0]  # Võtab enne .-d osa, nt delfi või kroonika
        return 'unknown'

    def scrape_names_and_headlines(self):
        """
        Laeb veebilehe sisu alla ja otsib pealkirjadest nimed ning salvestab ka pealkirjad.
        :return: loetelu kogutud nimedest ja pealkirjadest
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Kontrollime, et veebileht on saadud edukalt
        except requests.exceptions.RequestException as e:
            print(f"Viga veebilehe laadimisel: {e}")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')

        # Täpsustame otsingut, et haarata ainult need elemendid, mis sisaldavad uudiste pealkirju
        headings = soup.find_all(['h2', 'h3', 'h1', 'article', 'span', 'div'])

        for heading in headings:
            heading_text = heading.get_text(strip=True)

            # Eemaldame kõik, mis ei ole uudiste pealkirjad
            # Vältime elemente, mis sisaldavad kontaktinfot, autoriõigusi jne.
            if not heading_text or "©" in heading_text or "info@" in heading_text or "kontakt" in heading_text.lower():
                continue  # Jäta need välja, mis sisaldavad autoriõigusi või e-posti aadresse

            # Otsime nimesid, mis võivad sisaldada suuri tähti ja lõppevad mõne tähega
            names_in_title = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+', heading_text)
            if names_in_title:
                for name in names_in_title:
                    # Iga nimi saab oma pealkirja
                    self.names_and_headlines.append({'name': name, 'pealkiri': heading_text, 'aadress': self.url})

        return self.names_and_headlines

    def save_to_json(self):
        """
        Salvestab kogutud andmed JSON faili.
        :return: None
        """
        data = {
            'uudised': self.names_and_headlines
        }

        # Salvestame JSON faili
        try:
            with open(self.file_name, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            print(f"Fail {self.file_name} on salvestatud!")
        except Exception as e:
            print(f"Tekkis viga faili salvestamisel: {e}")

    def run(self):
        """
        Kogub nimed, pealkirjad ja salvestab need JSON faili.
        :return: None
        """
        try:
            self.scrape_names_and_headlines()
            self.save_to_json()
        except Exception as e:
            print(f"Viga töötluses: {e}")


# Erinevad veebilehed, mida skrapitakse
urls = [
    "https://www.postimees.ee",
    "https://www.delfi.ee",
    "https://www.ohtuleht.ee",
    "https://kroonika.delfi.ee"
]

# Eraldi kaust, kus salvestatakse JSON failid
if not os.path.exists('json_files'):
    os.makedirs('json_files')

# Läbime kõik veebilehed
for url in urls:
    scraper = NewsScraper(url)
    scraper.run()
    time.sleep(2)  # Annab aega järgmiseks päringuks, et vältida serveri koormamist


