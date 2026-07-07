from abc import ABC, abstractmethod
import random
from src import config
from src.zwierzeta.krowa import Krowa
from src.zwierzeta.cielak import Cielak


# bazowa klasa towaru w sklepie - kazdy towar ma nazwe, opis, cene i potrafi sie "zastosowac"
# na farmie. Analogicznie do zdarzen losowych: dodanie nowego towaru to tylko nowa podklasa,
# zero zmian w klasie Sklep (zasada otwarte-zamkniete)
class Towar(ABC):
    def __init__(self):
        self.nazwa = ""
        self.opis = ""
        self.cena = 0
        self.kategoria = ""  # "zwierze" / "pasza" / "ulepszenie" - do statystyk koncowych

    # niektore towary maja sens tylko w pewnych warunkach (np. plot dopiero gdy grozi drapieznik)
    def dostepny(self, farma) -> bool:
        return True

    # nakladamy efekt zakupu na farme (pieniadze sa  juz pobrane przez sklep). Zwraca komunikat
    @abstractmethod
    def zastosuj(self, farma) -> str:
        pass

    def __str__(self) -> str:
        return f"{self.nazwa} - {self.cena} zl"


# --------------------------------------------------------------------


# Dorosla krowa - od razu daje mleko, ale kosztuje najwiecej
class KupDoroslaKrowe(Towar):
    def __init__(self):
        super().__init__()
        self.nazwa = "Dorosla krowa 🐄"
        self.opis = "Dorosla krowa dajaca mleko od nastepnego dnia"
        self.cena = config.CENA_DOROSLEJ_KROWY
        self.kategoria = "zwierze"

    def zastosuj(self, farma) -> str:
        imie = random.choice(config.IMIONA_KROW)
        krowa = Krowa(id=farma._nowe_id(), pozycja=(0, 0), imie=imie)
        krowa.dorosla = True
        krowa.wiek = config.WIEK_DOROSLOSCI
        farma.dodaj_zwierze(krowa)
        return f"Kupiono dorosla krowe {imie}"


# --------------------------------------------------------------------


# Cielak - tanszy, ale musi najpierw dorosnac zeby dawac mleko
class KupCielaka(Towar):
    def __init__(self):
        super().__init__()
        self.nazwa = "Cielak 🐮"
        self.opis = "Tanszy, ale zacznie dawac mleko dopiero gdy dorosnie"
        self.cena = config.CENA_CIELAKA
        self.kategoria = "zwierze"

    def zastosuj(self, farma) -> str:
        imie = random.choice(config.IMIONA_KROW)
        cielak = Cielak(id=farma._nowe_id(), pozycja=(0, 0), imie=imie)
        farma.dodaj_zwierze(cielak)
        return f"Kupiono cielaka {imie}"


# --------------------------------------------------------------------


# Worek paszy - ratuje glodne stado niezaleznie od trawy na pastwisku
class WorekPaszy(Towar):
    def __init__(self):
        super().__init__()
        self.nazwa = "Worek paszy 🌾"
        self.opis = f"Dodaje {config.PASZA_NAJEDZENIE} najedzenia calemu stadu"
        self.cena = config.CENA_PASZY
        self.kategoria = "pasza"

    def zastosuj(self, farma) -> str:
        nakarmione = 0
        for zwierze in farma.stado:
            if zwierze.zyje:
                zwierze.najedzenie = min(
                    zwierze.najedzenie + config.PASZA_NAJEDZENIE, config.GLOD_START
                )
                nakarmione += 1
        return f"Nakarmiono pasza {nakarmione} zwierzat"


# --------------------------------------------------------------------


# Plot - przez kilka dni mocno zmniejsza szanse na drapieznika, potem sie niszczy
class Plot(Towar):
    def __init__(self):
        super().__init__()
        self.nazwa = "Plot 🚧"
        self.opis = f"Zmniejsza szanse na drapieznika przez {config.PLOT_DNI_TRWANIA} dni"
        self.cena = config.CENA_PLOTU
        self.kategoria = "ulepszenie"

    # postawienie nowego plotu odnawia ochrone na pelne PLOT_DNI_TRWANIA dni
    def zastosuj(self, farma) -> str:
        farma.plot_dni_pozostale = config.PLOT_DNI_TRWANIA
        farma.plot_dziury = []  # nowy plot jest bez dziur
        return f"Postawiono plot - mniejsza szansa na drapieznika przez {config.PLOT_DNI_TRWANIA} dni"


# --------------------------------------------------------------------
# Sklep zarzadza katalogiem towarow i przeprowadza transakcje.
#Jest niezalezny od interfejsu


class Sklep:
    def __init__(self, katalog=None):
        if katalog is None:
            katalog = [
                KupDoroslaKrowe(),
                KupCielaka(),
                WorekPaszy(),
                Plot(),
            ]
        self.katalog = katalog

    # towary aktualnie dostepne do kupienia (z uwzglednieniem warunkow towaru)
    def dostepne_towary(self, farma) -> list:
        dostepne = []
        for towar in self.katalog:
            if towar.dostepny(farma):
                dostepne.append(towar)
        return dostepne

    # proba zakupu: sprawdzamy budzet, pobieramy pieniadze i nakladamy efekt.
    def kup(self, towar: Towar, farma) -> tuple:
        if not towar.dostepny(farma):
            return False, "Ten towar jest teraz niedostepny"
        if not farma.finanse.wydaj(towar.cena):
            return False, "Za malo pieniedzy w budzecie"
        komunikat = towar.zastosuj(farma)
        return True, komunikat
