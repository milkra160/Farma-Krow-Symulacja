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
            litera = krowa.get("symbol", "K")  # K krowa, c cielak, O owca, J jagnie, h kura
            if not krowa["zyje"]:
                return self._koloruj(litera, "czerwony")
            # kura nie pasie sie na trawie, wiec jej kolor nie zalezy od najedzenia - zawsze zolty
            if krowa.get("gatunek") == "kura":
                return self._koloruj(litera, "zolty")
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
        # gdy na farmie stoi kociol serowarski - doklejamy jego garnek z serem obok planszy
        if log.get("kociol", {}).get("aktywny"):
            self._dorysuj_kociol(linie)
        # gdy dziala antena zaglaszajaca - doklejamy jej maszt obok planszy
        if log.get("antena_aktywna"):
            self._dorysuj_antene(linie)
        # gdy stoi kurnik (sa kury) - doklejamy jego domek z kura obok planszy
        if log.get("kurnik_aktywny"):
            self._dorysuj_kurnik(linie)
        return "\n".join(linie)

    # postac lesniczego
    def _dorysuj_lesniczego(self, linie: list):
        ludzik = self._koloruj("\uc6c3", "zielony")  # maly ludzik-stickman
        # linie[0] to gorna ramka - ludzika stawiamy obok pierwszego wiersza pastwiska
        if len(linie) > 1:
            linie[1] += "   " + ludzik

    # symbol kotla serowarskiego obok planszy (jak ludzik lesniczego): garnek z serem, a nad nim
    # unosi sie dym, zeby bylo widac, ze ser sie robi. Dym rysujemy w wierszach nad kotlem, z
    # rosnacym wcieciem ku gorze - dzieki temu wyglada, jakby leniwie znosilo go w bok.
    def _dorysuj_kociol(self, linie: list):
        if len(linie) <= 4:
            return
        linie[2] += "     \U0001f4a8"  # dym
        linie[3] += "    \U0001f4a8"  # dym
        linie[4] += "   \U0001fed5"  # garnek z serem

    # symbol anteny zaglaszajacej obok planszy: szary kwadrat (urzadzenie) z masztem
    # Rysujemy nizej niz kociol, zeby oba znaki sie nie nakladaly.
    def _dorysuj_antene(self, linie: list):
        if len(linie) <= 7:
            return
        maszt = self._koloruj("\\|/", "szary")
        urzadzenie = self._koloruj("\u25a6", "szary")
        linie[6] += "  " + maszt
        linie[7] += "   " + urzadzenie

    # symbol kurnika obok planszy: domek z kura znoszaca jajko. Rysujemy najnizej, pod anten\u0105.
    def _dorysuj_kurnik(self, linie: list):
        if len(linie) <= 10:
            return
        linie[9] += "  \U0001F3E0"  # domek - kurnik
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
        # podpis tlumaczacy maszt anteny obok planszy
        if log.get("antena_aktywna"):
            dni = log.get("antena_dni", 0)
            if dni == 0:
                tekst = "\U0001f4e1 Antena zagłusza UFO — ostatni dzień"
            else:
                slowo = "dzień" if dni == 1 else "dni"
                tekst = f"\U0001f4e1 Antena zagłusza UFO — jeszcze {dni} {slowo}"
            print(self._koloruj(tekst, "niebieski"))
        self.legenda()

    # legenda
    def legenda(self):
        print(
            "Legenda: K=krowa  c=cielak  O=owca  J=jagnię  h=kura  "
            "T=trawa  !=drapieznik  .=puste"
        )
        najedzone = self._koloruj("najedzone", "zielony")
        glodne = self._koloruj("głodne", "pomaranczowy")
        zginely = self._koloruj("zginęły", "czerwony")
        print(f"kolory zwierząt: {najedzone} {glodne} {zginely}")
