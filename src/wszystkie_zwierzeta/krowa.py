from src.wszystkie_zwierzeta.zwierzeta import Zwierze
from src.config import *


class Krowa(Zwierze):
    def __init__(self, id: int, pozycja: tuple, imie: str):
        super().__init__(id, pozycja)
        #Ustawienie poziomow glodu i przypisanie konkretnych zmiennych dla krowy
        #by zbalansowac przebieg symulacji
        self.imie = imie
        self.wiek = 0
        self.najedzenie = GLOD_START
        self.dorosla = False
        self.zjadla_dzisiaj = False
        self.umarla_dzis = False
        self.symbol = "K"

    def starzej_sie(self):
        #Balansowanie przebiegu symulacji przez glod i smierc krow
        self.wiek += 1
        self.najedzenie -= GLOD_DZIENNY_UBYTEK
        if self.wiek >= WIEK_DOROSLOSCI:
            self.dorosla = True
        if self.najedzenie <= 0:
            self.zyje = False
            self.umarla_dzis = True

    def jedz(self):
        #Minimum zapobiega przekroczeniu limitu najedzenia przez krowe
        self.najedzenie = min(self.najedzenie + GLOD_Z_JEDZENIA, GLOD_START)
        self.zjadla_dzisiaj = True

    def reset_dnia(self):
        self.zjadla_dzisiaj = False
        self.umarla_dzis = False

    def ruch(self):
        pass

