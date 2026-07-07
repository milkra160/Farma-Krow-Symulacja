class Wizualizacja:  # klasa wizualizacja zajmuje sie rysowaniem stopklatki farmy pod koniec dnia
    KOLORY = {
        "zielony": "\033[92m",
        "pomaranczowy": "\033[93m",
        "czerwony": "\033[91m",
        "zolty": "\033[33m",
        "szary": "\033[90m",
        "bialy": "\033[37m",
        "niebieski": "\033[96m",
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
    # gdy plot chroni farme rysujemy podwojna, zolta ramke zamiast zwyklej
    def _zbuduj_plansze(self, pastwisko, log: dict) -> str:
        szerokosc = pastwisko.szerokosc
        if log.get("plot_aktywny"):
            # gorna ramka ma dziury tam gdzie drapieznik przedarl sie przez plot.
            # Dziury zostaja do konca trwania plotu (lista kolumn w logu)
            gorne_znaki = ["═"] * szerokosc
            for kolumna in log.get("plot_dziury", []):
                if 0 <= kolumna < szerokosc:
                    gorne_znaki[kolumna] = " "  # dziura w plocie
            gorna = self._koloruj("╔" + "".join(gorne_znaki) + "╗", "zolty")
            dolna = self._koloruj("╚" + "═" * szerokosc + "╝", "zolty")
            pion = self._koloruj("║", "zolty")
        else:
            gorna = "+" + "-" * szerokosc + "+"
            dolna = gorna
            pion = "|"

        linie = [gorna]
        for rzad in pastwisko.siatka:
            linia = pion
            for komorka in rzad:
                linia += self._symbol_komorki(komorka, log)
            linia += pion
            linie.append(linia)
        linie.append(dolna)

        # gdy wujek lesniczy pilnuje pastwiska - doklejamy jego ludzika obok planszy
        if log.get("lesniczy_aktywny"):
            self._dorysuj_lesniczego(linie)
        return "\n".join(linie)

    #postac lesniczego
    def _dorysuj_lesniczego(self, linie: list):
        ludzik = self._koloruj("\uc6c3", "zielony")  #maly ludzik-stickman
        # linie[0] to gorna ramka - ludzika stawiamy obok pierwszego wiersza pastwiska
        if len(linie) > 1:
            linie[1] += "   " + ludzik

    # glowna metoda, rysuje plansze na ekranie
    def rysuj_plansze(self, pastwisko, log: dict):
        print(self._zbuduj_plansze(pastwisko, log))
        # podpis tlumaczacy zolta ramke - wprost pod plansza, ktorej dotyczy
        if log.get("plot_aktywny"):
            dni = log["plot_dni"]
            if dni == 0:
                tekst = "🚧 Płot chroni farmę — ostatni dzień, jutro się rozpadnie"
            else:
                slowo = "dzień" if dni == 1 else "dni"
                tekst = f"🚧 Płot chroni farmę — jeszcze {dni} {slowo}"
            print(self._koloruj(tekst, "zolty"))
        # alert gdy drapieznik przedarl sie przez plot - tlumaczy dziure w ramce
        if log.get("drapieznik_przez_dziure"):
            print(
                self._koloruj(
                    "🕳️  Drapieżnik wkradł się przez dziurę w płocie!", "czerwony"
                )
            )
        self.legenda()

    # legenda
    def legenda(self):
        print("Legenda: K=krowa  c=cielak  T=trawa  !=drapieznik  .=puste")
        najedzona = self._koloruj("najedzona", "zielony")
        glodna = self._koloruj("głodna", "pomaranczowy")
        zginela = self._koloruj("zginęła", "czerwony")
        print(f"kolory krów: {najedzona} {glodna} {zginela}")
