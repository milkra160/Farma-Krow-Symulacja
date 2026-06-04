from src.config import *
from src.finanse import Finanse
from src.pastwisko.pastwisko import Pastwisko
from src.pogoda import Pogoda
from src.zdarzenia import ZdarzeniaLosoweMenadzer
from src.zwierzeta.krowa import Krowa
from src.zwierzeta.cielak import Cielak
import random
from src.zwierzeta.drapieznik import Drapieznik


# Farma to klasa glowna symulacji> Zarzadza stadem, pastwiskiem, pogoda
# finansami i zdarzeniami
class Farma:
    def __init__(
        self,
        nazwa: str,
        pastwisko: Pastwisko,
        pogoda: Pogoda,
        finanse: Finanse,
        zdarzenia: ZdarzeniaLosoweMenadzer,
        stado: list = None,
    ):
        self.nazwa = nazwa
        self.stado = stado if stado is not None else []
        self.drapiezniki = []
        self.pastwisko = pastwisko
        self.pogoda = pogoda
        self.finanse = finanse
        self.zdarzenia = zdarzenia
        self.dzien = 0
        self.szansa_drapieznik = SZANSA_DRAPIEZNIK
        self.maks_drapieznikow = MAKS_DRAPIEZNIKOW

    def dodaj_zwierze(self, zwierze):
        self.stado.append(zwierze)

    # usuwamy martwe krowy ze stada i zwracamy je ( by potem zapisac to w logach)
    def usun_martwe(self) -> list:
        martwe = []
        zywe = []
        for krowa in self.stado:
            if krowa.zyje:
                zywe.append(krowa)
            else:
                martwe.append(krowa)
        self.stado = zywe
        return martwe

    def liczba_krow(self) -> int:
        return len(self.stado)

    # farma dziala dopooki nie zbankrutuje
    def czy_aktywna(self) -> bool:
        return not self.finanse.czy_bankrut()

    # hermetyzacja. metoda wylacznie uzywana w tej klasie. Zabezpiecza przed
    # bledem z id w przypadku porodu cielaka
    def _nowe_id(self) -> int:
        if len(self.stado) == 0:
            return 1
        najwyzsze = 0
        for krowa in self.stado:
            if krowa.id > najwyzsze:
                najwyzsze = krowa.id
        return najwyzsze + 1

    def _rozmnazanie(
        self,
    ) -> list:  # prywatna metoda, zwraca liste imion nowo narodzonych cielakow
        # losujemy ciaze
        for krowa in self.stado:
            if krowa.zyje:
                krowa.losuj_ciaze()

        # zbieramy krowie matki ktorym dzis konczy sie ciaza
        matki = []
        for krowa in self.stado:
            if krowa.zyje and krowa.aktualizuj_ciaze():
                matki.append(krowa)

        # rodzimy cielaki
        narodziny = []
        for matka in matki:
            nowe_id = self._nowe_id()
            imie = random.choice(IMIONA_KROW)
            cielak = Cielak(id=nowe_id, pozycja=matka.pozycja, imie=imie)
            self.dodaj_zwierze(cielak)
            narodziny.append(cielak.imie)
        return narodziny

    # Najwazniejsza i glowna metoda nowy_dzien!! jedna doba symulacji. Zwraca logi dnia
    def nowy_dzien(self) -> dict:
        # start. nowy dzien
        self.dzien += 1

        # reset krow na now dzien
        for krowa in self.stado:
            krowa.reset_dnia()

        # losowanie nowego stanu pogody
        stan_pogody = self.pogoda.nowy_dzien()

        # czyscimy pastwisko i dodajemy nowa trawe
        self.pastwisko.wyczysc()
        ile_kepek = int(BAZA_KEPEK_TRAWY * self.pogoda.mnoznik_trawy())
        self.pastwisko.generuj_trawke(ile_kepek)

        # drapiezniki - losujemy czy sie pojawia
        self.drapiezniki = []
        if random.random() < self.szansa_drapieznik:
            ile = random.randint(1, self.maks_drapieznikow)
            for i in range(ile):
                self.drapiezniki.append(Drapieznik(id=i, pozycja=(0, 0)))
            self.pastwisko.rozmieszcz_drapiezniki(self.drapiezniki)

        # przypisujemy krowy do kepek. Krowa je lub ginie od drapieznika
        self.pastwisko.przypisz_krowy(self.stado)

        # czynniki naturalne
        for krowa in self.stado:
            krowa.starzej_sie_smierc_glodowa_doroslosc()

        # rozmnazanie
        narodziny = self._rozmnazanie()

        # usuwmy martwe krowy i zwracamy do logu
        martwe = self.usun_martwe()

        # zdarzenia losowe
        opisy_zdarzen = self.zdarzenia.aktualizuj(self, self.dzien)

        # finanse
        przychod = 0
        for krowa in self.stado:
            przychod += krowa.wartosc_mleka()
        stan_finansow = self.finanse.rozlicz_dzien(
            przychod, KOSZT_DZIENNY_FARMY, self.dzien
        )

        # log z dnia:
        najedzone_krowy = []
        glodne_krowy = []
        for krowa in self.stado:
            if krowa.zjadla_dzisiaj:
                najedzone_krowy.append(krowa.imie)
            else:
                glodne_krowy.append(krowa.imie)

        martwe_imiona_krow = []
        for krowa in martwe:
            martwe_imiona_krow.append(krowa.imie)

        log = {
            "dzien": self.dzien,
            "pogoda": stan_pogody,
            "narodziny": narodziny,
            "martwe": martwe_imiona_krow,
            "zjadly": najedzone_krowy,
            "glodne": glodne_krowy,
            "finanse": stan_finansow,
            "zdarzenia": opisy_zdarzen,
        }
        return log
