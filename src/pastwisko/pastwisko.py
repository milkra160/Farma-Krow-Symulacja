from src.pastwisko.komorka import Komorka
import random


# klasa Pastwisko to model planszy 2D zbudowanej z komorek
class Pastwisko:
    def __init__(self, szerokosc: int, wysokosc: int):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc

        # tworzenie siatki
        self.siatka = []
        for y in range(wysokosc):
            rzad = []
            for x in range(szerokosc):
                rzad.append(Komorka(x, y))
            self.siatka.append(rzad)

    def pobierz_komorke(self, x: int, y: int) -> Komorka:
        return self.siatka[y][x]

    def generuj_trawke(self, ilosc_kepek: int) -> list:
        wszystkie_pozycje = []
        for y in range(self.wysokosc):
            for x in range(self.szerokosc):
                wszystkie_pozycje.append((x, y))

        wybrane_pozycje = random.sample(
            wszystkie_pozycje, ilosc_kepek
        )  # uzywamy random.sample by uniknac powtorzen
        # random.choice moglby powodowac powtorzenia
        for x, y in wybrane_pozycje:
            self.pobierz_komorke(x, y).dodaj_trawke()
        return wybrane_pozycje

    def kepki_z_trawa(self) -> list:
        wynik = []
        for rzad in self.siatka:
            for kratka in rzad:
                if kratka.ma_trawke:
                    wynik.append(kratka)
        return wynik
