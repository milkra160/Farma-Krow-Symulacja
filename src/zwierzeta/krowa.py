import random
from src.zwierzeta.zwierze import Zwierze
from src.config import *


class Krowa(Zwierze):
    def __init__(self, id: int, pozycja: tuple, imie: str):
        super().__init__(id, pozycja)
        # Ustawienie poziomow glodu i przypisanie konkretnych zmiennych dla krowy
        # by zbalansowac przebieg symulacji
        self.imie = imie
        self.wiek = 0
        self.najedzenie = GLOD_START

        # mechanika ciazy
        self.dorosla = False
        self.w_ciazy = False
        self.dni_do_porodu = 0

        self.zjadla_dzisiaj = False
        self.umarla_dzis = False
        self.symbol = "K"

        #zmienne potrzebne do rozmieszczania krów
        self.przypisana_kepka = None #przygotowanie miejsca gdzie będzie przypisana kępka trawy
        self.pozycja_wizualna = (0,0) #domyślne współżędne pozycji wizualnej krowy

    def starzej_sie_smierc_glodowa_doroslosc(self):
        # Balansowanie przebiegu symulacji przez glod i smierc krow
        self.wiek += 1
        self.najedzenie -= GLOD_DZIENNY_UBYTEK
        if self.wiek >= WIEK_DOROSLOSCI:
            self.dorosla = True
        if self.najedzenie <= 0:
            self.zyje = False
            self.umarla_dzis = True

    def jedz(self):
        # Minimum zapobiega przekroczeniu limitu najedzenia przez krowe
        self.najedzenie = min(self.najedzenie + GLOD_Z_JEDZENIA, GLOD_START)
        self.zjadla_dzisiaj = True

    # metoda ktora tworzy komunikat zwiastujacy mozliwa przyszla smierc glodowa lub katastrofe
    def czy_glodna(self) -> bool:
        return self.najedzenie < 40

    def wartosc_mleka(self) -> int:
        if self.dorosla:
            return PRZYCHOD_Z_KROWY
        return 0

    # mechanika ciazy = balans symulacji
    def losuj_ciaze(self):
        if self.dorosla and not self.w_ciazy and self.najedzenie > 60:
            if random.random() < SZANSA_NA_CIAZE:
                self.w_ciazy = True
                self.dni_do_porodu = 0

    def aktualizuj_ciaze(self) -> bool:
        if self.w_ciazy:
            self.dni_do_porodu -= 1
            if self.dni_do_porodu == 0:
                self.w_ciazy = False
                return True  # udany porod
        return False

    def reset_dnia(self):
        self.zjadla_dzisiaj = False
        self.umarla_dzis = False

    def ruch(self):
        pass
