import tkinter as tk
from tkinter import ttk, messagebox
from scraper import WebScraper
from names import NameFinder
from saver import JSONSaver

class AppGUI:
    """
    Tkinter graafiline kasutajaliides.
    """

    PORTALS = {
        "Delfi": "https://www.delfi.ee",
        "Postimees": "https://www.postimees.ee",
        "Õhtuleht": "https://www.ohtuleht.ee"
    }

    def __init__(self, root):
        self.root = root
        root.title("Nimede leidja")
        root.geometry("480x200")

        ttk.Label(root, text="Vali portaal või sisesta URL:").pack(pady=6)

        self.combo = ttk.Combobox(root, values=list(self.PORTALS.keys()))
        self.combo.pack(pady=4)

        self.url_entry = ttk.Entry(root, width=50)
        self.url_entry.pack(pady=6)

        ttk.Button(root, text="Leia nimed", command=self.run_search).pack(pady=10)

    def run_search(self):
        url = self.url_entry.get().strip()
        if not url and self.combo.get():
            url = self.PORTALS[self.combo.get()]

        if not url:
            messagebox.showerror("Viga", "Sisesta URL või vali portaal!")
            return

        try:
            scraper = WebScraper(url)
            scraper.parse_headlines()

            finder = NameFinder(scraper.headlines)
            finder.extract()

            if not finder.names:
                messagebox.showinfo("Tulemus", "Ei leitud nimesid.")
                return

            saver = JSONSaver(url, finder.names)
            path = saver.save()
            messagebox.showinfo("Valmis!", f"Salvestatud:\n{path}")
        except Exception as e:
            messagebox.showerror("Tõrge", str(e))
