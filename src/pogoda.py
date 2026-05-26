import random
from src.config import *


class Pogoda:
    # Krotka dla kazdej klasy

    STANY_POGODY = ("slonecznie", "deszcz", "susza")

    def __init__(self):
        # Stan bazowy
        self.aktualny_stan_pogody = "slonecznie"

    def nowy_dzien(self):
        self.aktualny_stan_pogody = random.choice(self.STANY_POGODY)
        return self.aktualny_stan_pogody

    # Metoda generujaca ilosc trawy w zaleznosci od pogody
    # Zdarzenie losowe wywolujace balans i mozliwosc smierci glodowej
    def mnoznik_trawy(self):
        if self.aktualny_stan_pogody == "deszcz":
            return MNOZNIK_DESZCZ
        if self.aktualny_stan_pogody == "susza":
            return MNOZNIK_SUSZA
        return MNOZNIK_SLONCE
