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

    # zwraca komorke o wspolrzednych x,y (siatka jest indeksowana [y][x])
    def pobierz_komorke(self, x: int, y: int) -> Komorka:
        return self.siatka[y][x]

    # losuje unikalne pola i sadzi na nich trawe, zwraca liste wybranych pozycji
    def generuj_trawke(self, ilosc_kepek: int) -> list:
        wszystkie_pozycje = []
        for y in range(self.wysokosc):
            for x in range(self.szerokosc):
                wszystkie_pozycje.append((x, y))

        ilosc_kepek = max(0, min(ilosc_kepek, len(wszystkie_pozycje)))
        wybrane_pozycje = random.sample(wszystkie_pozycje, ilosc_kepek)
        # uzywamy random.sample by uniknac powtorzen
        # random.choice moglby powodowac powtorzenia
        for x, y in wybrane_pozycje:
            self.pobierz_komorke(x, y).dodaj_trawke()
        return wybrane_pozycje

    # zbiera wszystkie kratki na ktorych aktualnie rosnie trawa
    def kepki_z_trawa(self) -> list:
        wynik = []
        for rzad in self.siatka:
            for kratka in rzad:
                if kratka.ma_trawke:
                    wynik.append(kratka)
        return wynik

    def wyczysc(self):  # resetujemy kazda kepke z trawa do stanu poczatkowego
        for rzad in self.siatka:
            for kratka in rzad:
                kratka.usun_trawke()
                kratka.zajeta_przez = None
                kratka.ma_drapieznika = False
                kratka.drapieznik = None

    def rozmieszcz_drapiezniki(self, drapiezniki: list):
        kepki = self.kepki_z_trawa()  # poniewaz drapieznik staje tylko na trawie
        # losujemy tyle kepek ile jest drapieznikow (bez powtorzen)
        wybrane_kepki = random.sample(kepki, len(drapiezniki))
        for i in range(len(drapiezniki)):
            kepka = wybrane_kepki[i]
            kepka.ma_drapieznika = True
            kepka.drapieznik = drapiezniki[i]
            drapiezniki[i].pozycja = (kepka.x, kepka.y)

    # Docelowo krowa po zjedzeniu kepki trawy powinna przenosic sie na wolna kratke na okolo swojej kepki ( jednej z czterech)
    # Znak _ przed nazwa metody pzrekazuje nam informacje o hermetyzacji. Nie powinnismy udostepniac tej metody innym klasom
    def _losuj_sasiada(self, x: int, y: int) -> tuple:
        # cztery pola wokol kepki
        # *********** gora ****** prawo *** lewo *** dol
        sasiedzi = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        wolne = []
        for sx, sy in sasiedzi:
            # sasiad mussi miescic sie na planszy
            if 0 <= sx < self.szerokosc and 0 <= sy < self.wysokosc:
                if self.pobierz_komorke(sx, sy).czy_wolna():
                    wolne.append((sx, sy))
        if len(wolne) > 0:
            return random.choice(wolne)  # losowanie wolnego sasiada

        # gdy brak wolnych sasiadow krowa zostaje na tej samej kepce
        return (x, y)

    def przypisz_krowy(self, krowy: list):  # Bierzemy tylko zywe krowy
        zywe = []
        for krowa in krowy:
            if krowa.zyje:
                zywe.append(krowa)

        # zbieramy wolne kepki trawy i mieszamy je losowo
        wolne_kepki = []
        for kepka in self.kepki_z_trawa():
            if kepka.czy_wolna():
                wolne_kepki.append(kepka)
        random.shuffle(wolne_kepki)

        # przydzielamy kepki do krow. Kazda krowa dostaje kepke dopoki ich starcza
        for i in range(len(zywe)):
            krowa = zywe[i]
            if i < len(wolne_kepki):
                kepka = wolne_kepki[i]
                kepka.wejdz(krowa)  # Ustawiamy przypisana kepke, krowa je lub nie
                krowa.pozycja_wizualna = self._losuj_sasiada(kepka.x, kepka.y)
            else:
                # brak wolnej kepki = krowa nie je( stoi gdziekolwiek)
                x = random.randint(0, self.szerokosc - 1)
                y = random.randint(0, self.wysokosc - 1)
                krowa.pozycja_wizualna = (x, y)
