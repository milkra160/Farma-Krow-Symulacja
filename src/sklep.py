from abc import ABC, abstractmethod
import random
from src import config
from src.zwierzeta.krowa import Krowa
from src.zwierzeta.cielak import Cielak
from src.zwierzeta.owca import Owca
from src.zwierzeta.kura import Kura


# bazowa klasa towaru w sklepie - kazdy towar ma nazwe, opis, cene i potrafi sie "zastosowac"
# na farmie. Analogicznie do zdarzen losowych: dodanie nowego towaru to tylko nowa podklasa,
# zero zmian w klasie Sklep (zasada otwarte-zamkniete)
class Towar(ABC):
    def __init__(self):
        self.nazwa = ""
        self.opis = ""
        self.cena_bazowa = 0  # cena pierwszego zakupu
        self.cena = 0  # aktualna cena (rosnie z kazdym kolejnym zakupem tego towaru)
        self.wzrost_ceny = 0  # o ile drozeje po kazdym zakupie (0 = cena stala)
        self.kupiony_razy = 0  # ile razy juz kupiono ten towar (do balansu cen)
        self.kategoria = (
            ""  # "zwierze" / "pasza" / "ulepszenie" - do statystyk koncowych
        )

    # niektore towary maja sens tylko w pewnych warunkach (np. plot dopiero gdy grozi drapieznik)
    def dostepny(self, farma) -> bool:
        return True

    # nakladamy efekt zakupu na farme (pieniadze sa  juz pobrane przez sklep). Zwraca komunikat
    @abstractmethod
    def zastosuj(self, farma) -> str:
        pass

    # po udanym zakupie kolejna sztuka tego towaru drozeje - balansuje spamowanie jednym towarem
    def zarejestruj_zakup(self):
        self.kupiony_razy += 1
        self.cena = self.cena_bazowa + self.wzrost_ceny * self.kupiony_razy

    def __str__(self) -> str:
        return f"{self.nazwa} - {self.cena} zl"


# --------------------------------------------------------------------


# Dorosla krowa - od razu daje mleko, ale kosztuje najwiecej
class KupDoroslaKrowe(Towar):
    def __init__(self):
        super().__init__()
        self.nazwa = "Dorosla krowa 🐄"
        self.opis = "Dorosla krowa dajaca mleko od nastepnego dnia"
        self.cena_bazowa = config.CENA_DOROSLEJ_KROWY
        self.cena = config.CENA_DOROSLEJ_KROWY
        self.wzrost_ceny = config.WZROST_CENY_KROWY
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
        self.cena_bazowa = config.CENA_CIELAKA
        self.cena = config.CENA_CIELAKA
        self.wzrost_ceny = config.WZROST_CENY_CIELAKA
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
        self.cena_bazowa = config.CENA_PASZY
        self.cena = config.CENA_PASZY
        self.wzrost_ceny = config.WZROST_CENY_PASZY
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
        self.opis = (
            f"Zmniejsza szanse na drapieznika przez {config.PLOT_DNI_TRWANIA} dni"
        )
        self.cena_bazowa = config.CENA_PLOTU
        self.cena = config.CENA_PLOTU
        self.wzrost_ceny = config.WZROST_CENY_PLOTU
        self.kategoria = "ulepszenie"

    # postawienie nowego plotu odnawia ochrone na pelne PLOT_DNI_TRWANIA dni
    def zastosuj(self, farma) -> str:
        farma.plot_dni_pozostale = config.PLOT_DNI_TRWANIA
        farma.plot_dziury = []  # nowy plot jest bez dziur
        return f"Postawiono plot - mniejsza szansa na drapieznika przez {config.PLOT_DNI_TRWANIA} dni"


# --------------------------------------------------------------------


# Antena zaglaszajaca - przez kilka dni blokuje zdarzenie UFO (kosmici nie porywaja krow).
# Postawienie nowej anteny odnawia ochrone na pelne ANTENA_DNI_TRWANIA dni.
class KupAntene(Towar):
    def __init__(self):
        super().__init__()
        self.nazwa = "Antena zaglaszajaca 📡"
        self.opis = f"Blokuje porwania UFO przez {config.ANTENA_DNI_TRWANIA} dni"
        self.cena_bazowa = config.CENA_ANTENY
        self.cena = config.CENA_ANTENY
        self.wzrost_ceny = config.WZROST_CENY_ANTENY
        self.kategoria = "ulepszenie"

    def zastosuj(self, farma) -> str:
        farma.antena_dni_pozostale = config.ANTENA_DNI_TRWANIA
        return (
            f"Postawiono antene - UFO zablokowane przez {config.ANTENA_DNI_TRWANIA} dni"
        )


# --------------------------------------------------------------------


# Dorosla owca - tansza od krowy i dluzej zyje (wolniej glodnieje), ale jej mleko jest malo warte.
# Oplaca sie dopiero z kotlem serowarskim, ktory przerabia mleko owcze na wart wiecej ser.
class KupDoroslaOwce(Towar):
    def __init__(self):
        super().__init__()
        self.nazwa = "Dorosla owca 🐑"
        self.opis = "Dluzej zyje niz krowa, ale jej mleko jest malo warte - oplaca sie z kotlem serowarskim"
        self.cena_bazowa = config.CENA_DOROSLEJ_OWCY
        self.cena = config.CENA_DOROSLEJ_OWCY
        self.wzrost_ceny = config.WZROST_CENY_OWCY
        self.kategoria = "zwierze"

    def zastosuj(self, farma) -> str:
        imie = random.choice(config.IMIONA_KROW)
        owca = Owca(id=farma._nowe_id(), pozycja=(0, 0), imie=imie)
        owca.dorosla = True
        owca.wiek = config.WIEK_DOROSLOSCI
        farma.dodaj_zwierze(owca)
        return f"Kupiono dorosla owce {imie}"


# --------------------------------------------------------------------


# Kura - nie je trawy (karmi ja kurnik), znosi jajka o duzej wartosci, ale zyje tylko kilka dni
# i jako glosna, latwa ofiara podnosi szanse na drapieznika dla calego stada.
class KupKure(Towar):
    def __init__(self):
        super().__init__()
        self.nazwa = "Kura 🐔"
        self.opis = (
            f"Znosi jajka za {config.PRZYCHOD_Z_KURY} zl/dzien przez "
            f"{config.KURA_DNI_ZYCIA} dni. Nie je trawy, ale wabi drapiezniki"
        )
        self.cena_bazowa = config.CENA_KURY
        self.cena = config.CENA_KURY
        self.wzrost_ceny = config.WZROST_CENY_KURY
        self.kategoria = "zwierze"

    def zastosuj(self, farma) -> str:
        imie = random.choice(config.IMIONA_KROW)
        kura = Kura(id=farma._nowe_id(), pozycja=(0, 0), imie=imie)
        farma.dodaj_zwierze(kura)
        return f"Kupiono kure {imie}"


# --------------------------------------------------------------------


# Kociol serowarski - maszyna kupowana raz na cala gre. Przerabia mleko doroslych owiec na ser:
# mleko trafia do kotla i po KOCIOL_DNI_NA_SER dniach wychodzi jako ser wart wiecej niz mleko.
class KupKociolSerowarski(Towar):
    def __init__(self):
        super().__init__()
        self.nazwa = "Kociol serowarski 🧀"
        self.opis = (
            f"Przerabia mleko owcze na ser po {config.KOCIOL_DNI_NA_SER} dniach "
            f"({config.PRZYCHOD_Z_SERA} zl za owce). Jeden na farme"
        )
        self.cena_bazowa = config.CENA_KOTLA
        self.cena = config.CENA_KOTLA
        self.kategoria = "ulepszenie"

    # kociol moze byc tylko jeden - gdy juz stoi, znika z oferty sklepu
    def dostepny(self, farma) -> bool:
        return not farma.kociol

    def zastosuj(self, farma) -> str:
        farma.kociol = True
        return "Kupiono kociol serowarski - mleko owcze bedzie teraz przerabiane na ser"


# --------------------------------------------------------------------
# Sklep zarzadza katalogiem towarow i przeprowadza transakcje.
# Jest niezalezny od interfejsu


class Sklep:
    def __init__(self, katalog=None):
        if katalog is None:
            katalog = [
                KupDoroslaKrowe(),
                KupCielaka(),
                KupDoroslaOwce(),
                KupKure(),
                KupKociolSerowarski(),
                WorekPaszy(),
                Plot(),
                KupAntene(),
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
        towar.zarejestruj_zakup()  # kolejna sztuka tego towaru bedzie drozsza
        return True, komunikat
