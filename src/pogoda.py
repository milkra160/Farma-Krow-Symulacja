import random
from src.config import *


class Pogoda:
    # mozliwe stany pogody - ta sama krotka wspoldzielona przez kazda instancje

    STANY_POGODY = ("slonecznie", "deszcz", "susza")

    def __init__(self):
        # Stan bazowy
        self.aktualny_stan_pogody = "slonecznie"
        self.poprzedni_stan_pogody = "slonecznie"
        self.wymuszony_stan = None
        self.historia = []

    # losuje stan pogody na dzis (chyba ze zdarzenie wymusza stan), poprzedni idzie do historii
    def nowy_dzien(self):
        self.poprzedni_stan_pogody = self.aktualny_stan_pogody
        self.historia.append(self.poprzedni_stan_pogody)
        if self.wymuszony_stan is not None:
            self.aktualny_stan_pogody = self.wymuszony_stan
        else:
            self.aktualny_stan_pogody = random.choice(self.STANY_POGODY)
        return self.aktualny_stan_pogody

    # Metoda generujaca ilosc trawy w zaleznosci od pogody

    def mnoznik_trawy(self):
        # trawa rosnie wg pogody z DNIA POPRZEDNIEGO (opoznienie o 1 dzien)
        if self.poprzedni_stan_pogody == "deszcz":
            return MNOZNIK_DESZCZ
        if self.poprzedni_stan_pogody == "susza":
            return MNOZNIK_SUSZA
        return MNOZNIK_SLONCE

    def __str__(self):
        return f"Pogoda: {self.aktualny_stan_pogody}"
