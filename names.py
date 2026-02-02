import re

class NameFinder:
    """
    Otsib pealkirjadest inimeste nimed (2–4 sõna).
    """

    NAME_PATTERN = re.compile(
        r"\b([A-ZÕÄÖÜ][a-zõäöü]+(?:[- ][A-ZÕÄÖÜ][a-zõäöü]+){1,3})\b"
    )

    def __init__(self, headlines: list[str]):
        self.headlines = headlines
        self.names = []

    def extract(self):
        """
        Leiab nimed ja eemaldab duplikaadid.
        """
        found = []
        for h in self.headlines:
            matches = self.NAME_PATTERN.findall(h)
            for name in matches:
                found.append(name.strip())

        seen = set()
        self.names = [n for n in found if not (n in seen or seen.add(n))]
