from src.config import *
import random
import sys
from datetime import date
from src.pastwisko.pastwisko import Pastwisko
from src.pogoda import Pogoda
from src.finanse import Finanse
from src.zdarzenia import ZdarzeniaLosoweMenadzer
from src.farma import Farma
from src.zwierzeta.krowa import Krowa
from src.logger import Logger, zielony, czerwony, zolty
from src.wizualizacja import Wizualizacja
from src.ranking import Ranking
from src.sklep import Sklep


# Klasa symulacja - spina farme, logger, wizualizacje  i ranking
# prowadzi petle dni i obsluguje sterowanie uzytkownika
class Symulacja:
    def __init__(self):
        self.farma = None
        self.wizualizacja = Wizualizacja()
        self.logger = Logger()
        self.ranking = Ranking()
        self.sklep = Sklep()
        self.parametry = None
        self.max_dni = MAX_DNI
        self.tryb_auto = False
        # statystuki zbierane przez cala gre do rankingu
        self.maks_budzet = 0
        self.maks_stado = 0
        self.maks_stado_dzien = 0 #ktorego dnia stado bylo najwieksze
        self.suma_narodzin = 0
        self.suma_zgonow = 0
        self.suma_zmartwychwstan = 0
        # liczniki zakupow w sklepie (do statystyk koncowych)
        self.kupione = {"zwierze": 0, "pasza": 0, "ulepszenie": 0}

    # tworzymy wszystkie komponenty i stado startowe w prywatnej metodzie
    def _przygotuj(self, parametry: dict):
        self.parametry = parametry
        self.max_dni = parametry["max_dni"]

        szerokosc, wysokosc = ROZMIAR_PLANSZY
        pastwisko = Pastwisko(szerokosc, wysokosc)
        pogoda = Pogoda()
        finanse = Finanse()
        finanse.budzet = parametry["budzet_start"]
        zdarzenia = ZdarzeniaLosoweMenadzer(
            szansa_zdarzenia=parametry["szansa_zdarzenia"]
        )

        # stado startowe. Krowy dorosle by dawaly mleko juz od poerwszego dnia
        stado = []
        for i in range(parametry["liczba_krow_start"]):
            krowa = Krowa(id=i + 1, pozycja=(0, 0), imie=random.choice(IMIONA_KROW))
            krowa.dorosla = True
            krowa.wiek = WIEK_DOROSLOSCI
            stado.append(krowa)

        # skladamy farme i nadpisujemy parametry z configu parametrami od uzytkowanika
        self.farma = Farma(
            parametry["nazwa_farmy"], pastwisko, pogoda, finanse, zdarzenia, stado
        )
        self.farma.szansa_drapieznik = parametry["szansa_drapieznik"]
        self.farma.maks_drapieznikow = parametry["maks_drapieznikow"]

        # statystyki startowe
        self.maks_budzet = finanse.budzet
        self.maks_stado = self.farma.liczba_krow()

    def zakoncz(self, powod: str):
        wynik = {
            "nazwa_farmy": self.farma.nazwa,
            "data": date.today().isoformat(),
            "dni_przezycia": self.farma.dzien,
            "maks_budzet": self.maks_budzet,
            "maks_stado": self.maks_stado,
            "powod_konca": powod,
            "parametry_start": self.parametry,
        }
        self.logger.drukuj_podsumowanie_koncowe(
            self.farma.dzien, powod, {"budzet": self.farma.finanse.budzet}
        )

        # statystyki z historii + liczniki zebrane w trakcie gry
        historia_pogody = self.farma.pogoda.historia
        historia_finansow = self.farma.finanse.historia
        # ile krow, a ile owiec zostalo w stadzie na koniec gry
        krowy_koncowe = sum(1 for z in self.farma.stado if z.gatunek == "krowa")
        owce_koncowe = sum(1 for z in self.farma.stado if z.gatunek == "owca")
        statystyki = {
            "narodziny": self.suma_narodzin,
            "zmartwychwstania": self.suma_zmartwychwstan,
            "zgony": self.suma_zgonow,
            "maks_stado": self.maks_stado,
            "maks_stado_dzien": self.maks_stado_dzien,
            "wszystkie_krowy": self.parametry["liczba_krow_start"] + self.suma_narodzin,
            "zdarzenia": self.farma.zdarzenia.licznik_zdarzen,
            "dni_slonca": historia_pogody.count("slonecznie"),
            "dni_deszczu": historia_pogody.count("deszcz"),
            "dni_suszy": historia_pogody.count("susza"),
            "suma_przychodow": sum(w["stan"]["przychod"] for w in historia_finansow),
            "suma_kosztow": sum(w["stan"]["koszt"] for w in historia_finansow),
            "budzet_koncowy": self.farma.finanse.budzet,
            "kupione_zwierzeta": self.kupione["zwierze"],
            "kupione_pasze": self.kupione["pasza"],
            "kupione_ulepszenia": self.kupione["ulepszenie"],
            "krowy_koncowe": krowy_koncowe,
            "owce_koncowe": owce_koncowe,
        }
        self.logger.drukuj_statystyki(statystyki)

        self.ranking.zapisz_wynik(wynik)
        self.ranking.wyswietl_kryteria()
        self.ranking.wyswietl_dla_seeda(self.parametry.get("seed"))
        self.ranking.wyswietl_top_10()

    # liczy jeden dzien, potem drukuje log i plansze. Zwraca fasle gdy symulacja ma sie skonczyc
    def uruchom_dzien(self) -> bool:
        log = self.farma.nowy_dzien()
        self.logger.drukuj_log(log)
        self.wizualizacja.rysuj_plansze(self.farma.pastwisko, log)
        self.suma_narodzin += len(log["narodziny"])  # do statystyk
        self.suma_zgonow += len(log["martwe"])  # do statystyk
        self.suma_zmartwychwstan += len(log["zmartwychwstania"])  # do statystyk

        # aktualizujemy rekordy do rankingu
        if self.farma.finanse.budzet > self.maks_budzet:
            self.maks_budzet = self.farma.finanse.budzet
        if self.farma.liczba_krow() > self.maks_stado:
            self.maks_stado = self.farma.liczba_krow()
            self.maks_stado_dzien = self.farma.dzien

        # warunki zakonczenia
        if self.farma.liczba_krow() == 0:
            self.zakoncz("wymarcie stada")
            return False
        if self.farma.finanse.czy_bankrut():
            self.zakoncz("bankructwo")
            return False
        if self.farma.dzien >= self.max_dni:
            self.zakoncz("uplynal czas")
            return False
        return True

    # symyluje n dni z rzedu brz przerw
    # zwraca false jesli po drodze symulacja sie zakonczyla
    def _symuluj_n_dni(self, n: int) -> bool:
        for _ in range(n):
            if not self.uruchom_dzien():
                return False
        return True

    # petla glowna, pyta uzytkownika co dzien albo leci do konca
    def petla_glowna(self):
        while True:
            if self.tryb_auto:
                if not self.uruchom_dzien():
                    break
                continue

            # tryb krokowy, pokazujemy menu i czekamy na uzytkownika
            print(
                "[Enter} Nastepny dzień   [s] +10dni   [a] Do końca  [k] Sklep  [c] Zakończ"
            )
            sys.stdout.flush()  # kolejna próba naprawienia błędu podwójnej generacji jednym enterem
            wybor = input("> ").strip().lower()

            if wybor == "":
                dalej = self.uruchom_dzien()
            elif wybor == "s":
                dalej = self._symuluj_n_dni(10)
            elif wybor == "a":
                self.tryb_auto = True
                dalej = self.uruchom_dzien()
            elif wybor == "k":
                self._otworz_sklep()  # sklep nie zabiera dnia - po zakupach wracamy do menu
                continue
            elif wybor == "c":
                self.zakoncz("ręczne zakonczenie")
                break
            else:
                print("Wybierz jedna z odpowiedzi")
                continue

            if not dalej:
                break

    # terminalowy sterownik sklepu. Cala logika zakupu siedzi w klasie Sklep,
    # tutaj tylko wyswietlamy katalog i czytamy wybor - pygame podepnie sie pod te same metody
    def _otworz_sklep(self):
        while True:
            print(zolty("=== SKLEP ==="))
            print(f"Budżet: {self.farma.finanse.budzet:.0f} zł")
            dostepne = self.sklep.dostepne_towary(self.farma)
            for i in range(len(dostepne)):
                towar = dostepne[i]
                print(f"  [{i + 1}] {towar.nazwa} - {towar.cena} zł  ({towar.opis})")
            print("  [w] Wyjście ze sklepu")

            sys.stdout.flush()
            wybor = input("sklep > ").strip().lower()
            if wybor == "w" or wybor == "":
                break

            # sprawdzamy czy uzytkownik podal poprawny numer towaru
            try:
                indeks = int(wybor) - 1
            except ValueError:
                print(czerwony("Podaj numer towaru albo [w] by wyjść"))
                continue
            if indeks < 0 or indeks >= len(dostepne):
                print(czerwony("Nie ma towaru o tym numerze"))
                continue

            towar = dostepne[indeks]
            udalo_sie, komunikat = self.sklep.kup(towar, self.farma)
            if udalo_sie:
                print(zielony(komunikat))
                # ksiegujemy zakup: licznik do statystyk + bufor do logu najblizszego dnia
                self.kupione[towar.kategoria] += 1
                self.farma.zakupy_dzis.append(komunikat)
            else:
                print(czerwony(komunikat))

    def start(self, parametry: dict):
        self._przygotuj(parametry)
        self.petla_glowna()
