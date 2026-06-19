class Wizualizacja:  # klasa wizualizacja zajmuje sie rysowaniem stopklatki farmy pod koniec dnia
    KOLORY = {
        "zielony": "\033[92m",
        "pomaranczowy": "\033[93m",
        "czerwony": "\033[91m",
        "zolty": "\033[33m",
        "szary": "\033[90m",
        "bialy": "\033[37m",
        "reset": "\033[0m",  # wylaczenie kolorow by nie psuc planszy w dalszych dniach
    }

    def __init__(self, kolory: bool = True):
        self.kolory = kolory  # robimy to w celu mozliwosci wylaczenia kolorow

    def _koloruj(self, tekst: str, kolor: str) -> str:
        if not self.kolory:
            return tekst
        return self.KOLORY[kolor] + tekst + self.KOLORY["reset"]

    # szuka w logu krowy stojacej na polu x,y zwraca jej slownikalbo None
    def _krowa_na_polu(self, log: dict, x: int, y: int):
        znaleziona = None
        for krowa in log["stan_krow"]:
            if krowa["pozycja_wizualna"] == (x, y):
                # martwa krowa ma pierwszenstwo
                if not krowa["zyje"]:
                    return krowa
                if znaleziona is None:
                    znaleziona = krowa
        return znaleziona

    # decyduje jaki symbol i kolor ma dana komorka
    def _symbol_komorki(self, komorka, log: dict) -> str:
        krowa = self._krowa_na_polu(log, komorka.x, komorka.y)
        if krowa is not None:
            litera = krowa.get("symbol", "K")  # K krowa, c cielak
            if not krowa["zyje"]:
                return self._koloruj(litera, "czerwony")
            if krowa["zjadla"]:
                return self._koloruj(litera, "zielony")
            return self._koloruj(litera, "pomaranczowy")
        if komorka.ma_drapieznika:
            return self._koloruj("!", "czerwony")
        if komorka.ma_trawke:
            return self._koloruj("T", "bialy")
        return self._koloruj(".", "szary")

    # buduje cala plansze jako tekst (latwiej z testami)
    def _zbuduj_plansze(self, pastwisko, log: dict) -> str:
        szerokosc = pastwisko.szerokosc
        linie = []
        linie.append("+" + "-" * szerokosc + "+")  # gorna ramka
        for rzad in pastwisko.siatka:
            linia = "|"
            for komorka in rzad:
                linia += self._symbol_komorki(komorka, log)
            linia += "|"
            linie.append(linia)
        linie.append("+" + "-" * szerokosc + "+")  # dolna ramka
        return "\n".join(linie)

    # glowna metoda, rysuje plansze na ekranie
    def rysuj_plansze(self, pastwisko, log: dict):
        print(self._zbuduj_plansze(pastwisko, log))
        self.legenda()

    # legenda
    def legenda(self):
        print("Legenda: K=krowa  c=cielak  T=trawa  !=drapieznik  .=puste")
        print("kolory: zielony=najedzona  pomaranczowy=glodna  czerwony=zginela")
