from src.config import *
from src.finanse import Finanse
from src.pastwisko.pastwisko import Pastwisko
from src.pogoda import Pogoda
from src.zdarzenia import ZdarzeniaLosoweMenadzer
from src.zwierzeta.krowa import Krowa
from src.zwierzeta.cielak import Cielak
import random
from src.zwierzeta.drapieznik import Drapieznik
from src import config


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
        self.cmentarz = []  # krowy ktore zdechly (potrzebne dla Wielkanocy)
        self.narodziny_dzis = []
        # licznik do nadawania UNIKALNYCH id - nigdy nie powtarzamy numeru
        self.ostatnie_id = 0
        for krowa in self.stado:
            if krowa.id > self.ostatnie_id:
                self.ostatnie_id = krowa.id
        self.dzien = 0
        self.szansa_drapieznik = SZANSA_DRAPIEZNIK
        self.maks_drapieznikow = MAKS_DRAPIEZNIKOW

    # dorzuca nowe zwierze (krowe/cielaka) do stada
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
        self.cmentarz.extend(martwe)
        return martwe

    def liczba_krow(self) -> int:
        return len(self.stado)

    # farma dziala dopooki nie zbankrutuje
    def czy_aktywna(self) -> bool:
        return not self.finanse.czy_bankrut()

    # hermetyzacja. metoda wylacznie uzywana w tej klasie. Zabezpiecza przed
    # nadaje kolejny, nigdy nie powtarzajacy sie numer id
    def _nowe_id(self) -> int:
        self.ostatnie_id += 1
        return self.ostatnie_id

    # cielaki ktore osiagnely wiek doroslosci zamieniamy na pelne krowy (symbol c -> K)
    def _dorosnij_cielaki(self):
        nowe_stado = []
        dorastajace_dzisiaj = []
        for zwierze in self.stado:
            if zwierze.symbol == "c" and zwierze.dorosla:
                krowa = Krowa(zwierze.id, zwierze.pozycja, zwierze.imie)

                krowa.wiek = zwierze.wiek
                krowa.najedzenie = zwierze.najedzenie
                krowa.dorosla = True
                krowa.zyje = zwierze.zyje
                krowa.w_ciazy = zwierze.w_ciazy
                krowa.dni_do_porodu = zwierze.dni_do_porodu
                krowa.pozycja_wizualna = zwierze.pozycja_wizualna
                krowa.przypisana_kepka = zwierze.przypisana_kepka
                krowa.zjadla_dzisiaj = zwierze.zjadla_dzisiaj
                krowa.umarla_dzis = zwierze.umarla_dzis

                krowa.symbol = "K"
                nowe_stado.append(krowa)
                dorastajace_dzisiaj.append(krowa.imie)
            else:
                nowe_stado.append(zwierze)

        self.stado = nowe_stado
        return dorastajace_dzisiaj

    def _rozmnazanie(
        self,
    ) -> list:  # prywatna metoda, zwraca liste imion nowo narodzonych cielakow
        ciaze_dzis = []

        # zbieramy krowie matki ktorym dzis konczy sie ciaza
        matki = []
        for krowa in self.stado:
            if krowa.zyje and krowa.aktualizuj_ciaze():
                matki.append(krowa)

        # losujemy ciaze
        for krowa in self.stado:
            if krowa.zyje:
                byla_w_ciazy = krowa.w_ciazy
                krowa.losuj_ciaze()
                if krowa.w_ciazy and not byla_w_ciazy:
                    ciaze_dzis.append(f"{krowa.imie} (za {krowa.dni_do_porodu} dni)")

        # rodzimy cielaki
        narodziny = []
        for matka in matki:
            nowe_id = self._nowe_id()
            imie = random.choice(IMIONA_KROW)
            cielak = Cielak(id=nowe_id, pozycja=matka.pozycja, imie=imie)
            # cielak pojawia sie na wolnej kratce obok matki
            x, y = matka.pozycja_wizualna
            cielak.pozycja_wizualna = self.pastwisko._losuj_sasiada(x, y)
            self.dodaj_zwierze(cielak)
            narodziny.append(f"{cielak.imie} (matka: {matka.imie})")
        return narodziny, ciaze_dzis

    # Najwazniejsza i glowna metoda nowy_dzien!! jedna doba symulacji. Zwraca logi dnia
    def nowy_dzien(self) -> dict:
        # start. nowy dzien
        self.dzien += 1

        # reset krow na now dzien
        for krowa in self.stado:
            krowa.reset_dnia()

        # czyscimy liste narodzin ze zdarzen na nowy dzien
        self.narodziny_dzis = []
        # zdarzenia losowe
        opisy_zdarzen = self.zdarzenia.aktualizuj(self, self.dzien)

        # losowanie nowego stanu pogody
        stan_pogody = self.pogoda.nowy_dzien()

        # czyscimy pastwisko i dodajemy nowa trawe
        self.pastwisko.wyczysc()
        ile_kepek = int(config.BAZA_KEPEK_TRAWY * self.pogoda.mnoznik_trawy())
        self.pastwisko.generuj_trawke(ile_kepek)

        # drapiezniki - losujemy czy sie pojawia
        self.drapiezniki = []
        wolne_kepki = self.pastwisko.kepki_z_trawa()
        if len(wolne_kepki) > 0 and random.random() < self.szansa_drapieznik:
            ile = random.randint(1, self.maks_drapieznikow)
            ile = min(ile, len(wolne_kepki))  # nie wiecej drapieznikow niz kepek
            for i in range(ile):
                self.drapiezniki.append(Drapieznik(id=i, pozycja=(0, 0)))
            self.pastwisko.rozmieszcz_drapiezniki(self.drapiezniki)

        # jesli krowa nie zyje przez wejsciwem na pastwisko to np ofiara zdarznia
        martwe_przed_drapieznikami = []
        for krowa in self.stado:
            if not krowa.zyje:
                martwe_przed_drapieznikami.append(krowa.id)

        # przypisujemy krowy do kepek. Krowa je lub ginie od drapieznika
        self.pastwisko.przypisz_krowy(self.stado)

        # jesli jjakas krowa juz nie zyje to musi byc ofiara drapieznika
        zabite_przez_drapieznika = []
        for krowa in self.stado:
            if not krowa.zyje and krowa.id not in martwe_przed_drapieznikami:
                zabite_przez_drapieznika.append(krowa.id)

        # czynniki naturalne
        for krowa in self.stado:
            krowa.starzej_sie_smierc_glodowa_doroslosc()  # do poprawy, nazwa/rozdzielić funkcje?

        # dorastanie cielakow
        dorastajace = self._dorosnij_cielaki()

        # rozmnazanie
        narodziny, ciaze_dzis = self._rozmnazanie()
        narodziny.extend(self.narodziny_dzis)

        # usuwmy martwe krowy i zwracamy do logu
        martwe = self.usun_martwe()
        # zbieramy wszystkie krowy by zbudowac dla nich pelny raport stan_krow
        wszystkie_krowy_dzis = []
        for krowa in self.stado:
            wszystkie_krowy_dzis.append(krowa)
        for krowa in martwe:
            wszystkie_krowy_dzis.append(krowa)

        stan_krow = []
        for krowa in wszystkie_krowy_dzis:
            # zabezpieczenie. Glodne krowy maja przypisana_kepka = None
            pozycja_kepki = None
            if krowa.przypisana_kepka is not None:
                pozycja_kepki = (krowa.przypisana_kepka.x, krowa.przypisana_kepka.y)

            stan_krow.append(
                {
                    "id": krowa.id,
                    "imie": krowa.imie,
                    "symbol": krowa.symbol,
                    "pozycja_wizualna": krowa.pozycja_wizualna,
                    "pozycja_kepki": pozycja_kepki,
                    "najedzenie": krowa.najedzenie,
                    "wiek": krowa.wiek,
                    "dorosla": krowa.dorosla,
                    "w_ciazy": krowa.w_ciazy,
                    "zjadla": krowa.zjadla_dzisiaj,
                    "zyje": krowa.zyje,
                    "umarla_dzis": krowa.umarla_dzis,
                }
            )

        # wyznaczanie powodu smierci
        powod_smierci = {}
        imiona_martwych_krow = []
        for krowa in martwe:
            imiona_martwych_krow.append(krowa.imie)
            # smierc glodowa
            if krowa.id in zabite_przez_drapieznika:
                powod_smierci[krowa.imie] = "drapieznik"
            elif krowa.id in martwe_przed_drapieznikami:
                powod_smierci[krowa.imie] = "zdarzenie losowe"
            else:
                powod_smierci[krowa.imie] = "glod"

        # zbieramy koordynaty trawy do wizualizacji
        pozycje_trawy = []
        for kepka in self.pastwisko.kepki_z_trawa():
            pozycje_trawy.append((kepka.x, kepka.y))

        # zbieramy koordynaty drapieznikow do wizualizacji
        pozycje_drapieznikow = []
        for d in self.drapiezniki:
            pozycje_drapieznikow.append(d.pozycja)

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

        log = {
            "dzien": self.dzien,
            "pogoda": stan_pogody,
            "narodziny": narodziny,
            "martwe": imiona_martwych_krow,
            "powod_smierci": powod_smierci,
            "dorastanie": dorastajace,
            "zjadly": najedzone_krowy,
            "glodne": glodne_krowy,
            "drapiezniki": pozycje_drapieznikow,
            "stan_krow": stan_krow,
            "kepki_trawy": pozycje_trawy,
            "finanse": stan_finansow,
            "zdarzenia": opisy_zdarzen,
            "ciaze": ciaze_dzis,
        }
        return log
