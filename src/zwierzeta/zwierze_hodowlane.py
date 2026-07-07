from src.zwierzeta.zwierze import Zwierze
from src.config import *


# Wspolna warstwa dla kazdego zwierzecia gospodarskiego (krowa, a w przyszlosci kura,
# owca itd). Trzyma cykl zycia: jedzenie, glod, starzenie, dorastanie.
# Dzieki tej klasie dodanie nowego gatunku to juz tylko mala podklasa.
class ZwierzeHodowlane(Zwierze):
    def __init__(self, id: int, pozycja: tuple[int, int], imie: str):
        super().__init__(id, pozycja)
        self.imie = imie
        self.wiek = 0
        self.najedzenie = GLOD_START
        self.dorosla = False

        self.zjadla_dzisiaj = False
        self.umarla_dzis = False

        # zmienne potrzebne do rozmieszczania zwierzat na pastwisku
        self.przypisana_kepka = None
        self.pozycja_wizualna = (0, 0)

    # Balansowanie przebiegu symulacji przez glod, starzenie i smierc glodowa
    def starzej_sie_smierc_glodowa_doroslosc(self):
        self.wiek += 1
        self.najedzenie -= GLOD_DZIENNY_UBYTEK
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

    # na poczatku doby zerujemy cechy zalezne od dnia i zwalniamy przypisana kepke
    def reset_dnia(self):
        self.zjadla_dzisiaj = False
        self.umarla_dzis = False
        self.przypisana_kepka = None

    # zwierze hodowlane nie chodzi samo po planszy - metoda wymagana przez klase bazowa Zwierze
    def ruch(self):
        pass
