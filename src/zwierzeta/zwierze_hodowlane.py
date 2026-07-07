import random
from src.zwierzeta.zwierze import Zwierze
from src.config import *
from src import config


# Wspolna warstwa dla kazdego zwierzecia gospodarskiego (krowa, owca, a w przyszlosci kura
# itd). Trzyma cykl zycia: jedzenie, glod, starzenie, dorastanie i wspolna mechanike ciazy.
# Dzieki tej klasie dodanie nowego gatunku to juz tylko mala podklasa.
class ZwierzeHodowlane(Zwierze):
    # nazwa gatunku (do statystyk i rozdzielania tabel w logu); nadpisywana przez podklasy
    gatunek = "zwierze"
    # ile najedzenia gatunek traci dziennie - owca wolniej glodnieje niz krowa, wiec to nadpisuje
    glod_dzienny_ubytek = GLOD_DZIENNY_UBYTEK

    def __init__(self, id: int, pozycja: tuple[int, int], imie: str):
        super().__init__(id, pozycja)
        self.imie = imie
        self.wiek = 0
        self.najedzenie = GLOD_START
        self.dorosla = False
        self.mlode = False  # True dla mlodych (cielak, jagnie) az dorosna i staja sie dorosle

        # mechanika ciazy wspolna dla kazdego gatunku hodowlanego
        self.w_ciazy = False
        self.dni_do_porodu = 0

        self.zjadla_dzisiaj = False
        self.umarla_dzis = False

        # zmienne potrzebne do rozmieszczania zwierzat na pastwisku
        self.przypisana_kepka = None
        self.pozycja_wizualna = (0, 0)

    # Balansowanie przebiegu symulacji przez glod, starzenie i smierc glodowa
    def starzej_sie_smierc_glodowa_doroslosc(self):
        self.wiek += 1
        self.najedzenie -= self.glod_dzienny_ubytek
        if self.wiek >= WIEK_DOROSLOSCI:
            self.dorosla = True
        if self.najedzenie <= 0:
            self.zyje = False
            self.umarla_dzis = True

    def jedz(self):
        # Minimum zapobiega przekroczeniu limitu najedzenia przez zwierze
        self.najedzenie = min(self.najedzenie + GLOD_Z_JEDZENIA, GLOD_START)
        self.zjadla_dzisiaj = True

    # metoda ktora tworzy komunikat zwiastujacy mozliwa przyszla smierc glodowa lub katastrofe
    def czy_glodna(self) -> bool:
        return self.najedzenie < 40

    # polimorficzna wartosc produktu (mleko, jajka, welna...). Domyslnie zwierze nic nie daje -
    # konkretny gatunek nadpisuje te metode. Dzieki temu Farma liczy przychod jednym wywolaniem.
    def wartosc_produktu(self) -> int:
        return 0

    # czy zwierze produkuje mleko owcze trafiajace do kotla serowarskiego. Domyslnie nie -
    # tylko dorosla owca nadpisuje to na True. Dzieki temu Farma nie musi rozpoznawac klas.
    def produkuje_mleko_owcze(self) -> bool:
        return False

    # na poczatku doby zerujemy cechy zalezne od dnia i zwalniamy przypisana kepke
    def reset_dnia(self):
        self.zjadla_dzisiaj = False
        self.umarla_dzis = False
        self.przypisana_kepka = None

    # zwierze hodowlane nie chodzi samo po planszy - metoda wymagana przez klase bazowa Zwierze
    def ruch(self):
        pass

    # --- rozmnazanie (wspolne dla wszystkich gatunkow hodowlanych) ---

    # mechanika ciazy = balans symulacji
    def losuj_ciaze(self):
        if self.dorosla and not self.w_ciazy and self.najedzenie > 60:
            if random.random() < config.SZANSA_NA_CIAZE:
                self.w_ciazy = True
                self.dni_do_porodu = DNI_CIAZY

    # odliczamy dni do porodu; gdy dojdzie do 0 rodzi sie mlode (zwraca True)
    def aktualizuj_ciaze(self) -> bool:
        if self.w_ciazy:
            self.dni_do_porodu -= 1
            if self.dni_do_porodu == 0:
                self.w_ciazy = False
                return True  # udany porod
        return False

    # tworzy mlode tego samego gatunku (krowa -> cielak, owca -> jagnie). Nadpisywane przez gatunek.
    def stworz_mlode(self, id: int, pozycja: tuple, imie: str):
        raise NotImplementedError

    # zwraca dorosla wersje zwierzecia. Dorosle zostaja soba; mlode (cielak/jagnie) nadpisuja
    # to tak, by po osiagnieciu wieku doroslosci zamienic sie na doroslego osobnika swojego gatunku.
    def stworz_dorosla_wersje(self):
        return self

    # przepisuje stan mlodego na jego dorosla wersje (uzywane przy dorastaniu)
    def _przekaz_stan(self, nowy):
        nowy.wiek = self.wiek
        nowy.najedzenie = self.najedzenie
        nowy.dorosla = True
        nowy.zyje = self.zyje
        nowy.w_ciazy = self.w_ciazy
        nowy.dni_do_porodu = self.dni_do_porodu
        nowy.pozycja_wizualna = self.pozycja_wizualna
        nowy.przypisana_kepka = self.przypisana_kepka
        nowy.zjadla_dzisiaj = self.zjadla_dzisiaj
        nowy.umarla_dzis = self.umarla_dzis
        return nowy
