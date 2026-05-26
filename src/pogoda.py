import random
from src.config import *


class Pogoda:
    # Krotka dla kazdej klasy

    STANY_POGODY = ("slonecznie", "deszcz", "susza")

    def __init__(self):
        # Stan bazowy
        self.aktualny_stan_pogody = "slonecznie"
        self.poprzedni_stan_pogody = "slonecznie"
        self.historia = []

    def nowy_dzien(self):
        self.poprzedni_stan_pogody = self.aktualny_stan_pogody
        self.historia.append(self.poprzedni_stan_pogody)
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
    def __str__(self):
        return f"Pogoda: {self.aktualny_stan_pogody}"