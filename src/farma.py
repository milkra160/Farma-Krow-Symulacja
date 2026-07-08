from src.config import *
from src.finanse import Finanse
from src.pastwisko.pastwisko import Pastwisko
from src.pogoda import Pogoda
from src.zdarzenia import ZdarzeniaLosoweMenadzer, Lesniczy
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
        self.zmartwychwstania_dzis = []
        self.do_wyleczenia = []
        # zakupy zrobione w sklepie od ostatniego dnia (pokazujemy je w logu najblizszego dnia)
        self.zakupy_dzis = []
        # ile dni jeszcze stoi plot chroniacy przed drapieznikami (0 = brak plotu)
        self.plot_dni_pozostale = 0
        # kolumny w ktorych drapieznik przedarl sie przez plot - dziury zostaja do konca plotu
        self.plot_dziury = []
        # czy plot stal wczoraj - dzieki temu komunikat o zniszczeniu pada dzien po wygasnieciu
        self.plot_stal_wczoraj = False
        # kociol serowarski (kupowany w sklepie, jeden na farme) przerabia mleko owcze na ser
        self.kociol = False
        # partie mleka dojrzewajace w kotle: kazda to [dni_do_gotowe, wartosc_sera_w_zl]
        self.kociol_kolejka = []
        # ile dni jeszcze dziala antena zaglaszajaca sygnal UFO (0 = brak anteny)
        self.antena_dni_pozostale = 0
        # kurnik pojawia sie sam z pierwsza kura i znika, gdy padnie ostatnia. Ta flaga pamieta,
        # czy wczoraj byly kury - dzieki temu komunikat o zniknieciu kurnika pada we wlasciwym dniu
        self.mial_kury_wczoraj = False
        # icznik do nadawania UNIKALNYCH id - nigdy nie powtarzamy numeru
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

    # liczba zywych kur w stadzie (kury wabia drapiezniki i maja wlasna sekcje w logu)
    def _liczba_kur(self) -> int:
        return sum(1 for z in self.stado if z.gatunek == "kura" and z.zyje)

    # szansa na drapieznika. Samo posiadanie kur ja podnosi (glosne, wabia drapiezniki) - liczy sie
    # fakt, a nie liczba kur. Plot obniza szanse.
    def _szansa_na_drapieznika(self, plot_aktywny: bool) -> float:
        szansa = self.szansa_drapieznik
        if self._liczba_kur() > 0:
            szansa += config.KURA_WZROST_SZANSY_DRAPIEZNIKA
        if plot_aktywny:
            szansa *= config.PLOT_MNOZNIK_SZANSY
        return min(szansa, 1.0)

    # mlode (cielak c -> krowa K, jagnie J -> owca O), ktore osiagnely wiek doroslosci,
    # zamieniamy na dorosle osobniki ich gatunku. Kazde mlode samo wie, w co dorasta.
    def _dorosnij_mlode(self):
        nowe_stado = []
        dorastajace_dzisiaj = []
        for zwierze in self.stado:
            if zwierze.mlode and zwierze.dorosla:
                dorosly = zwierze.stworz_dorosla_wersje()
                nowe_stado.append(dorosly)
                dorastajace_dzisiaj.append(dorosly.imie)
            else:
                nowe_stado.append(zwierze)

        self.stado = nowe_stado
        return dorastajace_dzisiaj

    # Obsluga kotla serowarskiego na jedna dobe. Najpierw dojrzewaja partie juz w kotle (te,
    # ktorym skonczyl sie czas, wychodza jako gotowy ser), a dzisiejsze mleko owcze wchodzi jako
    # nowa partia z licznikiem KOCIOL_DNI_NA_SER. Pipeline jest rownolegly: mleko z kazdego dnia
    # dojrzewa niezaleznie, wiec ser splywa codziennie, tyle ze z opoznieniem. Zwraca stan do logu.
    def _przetworz_kociol(self, mleko_owcze_dzis: int) -> dict:
        ser_dzis = 0
        if not self.kociol:
            return {
                "aktywny": False,
                "mleko_dzis": 0,
                "ser_dzis": 0,
                "ser_jutro": 0,
                "partie_w_kotle": 0,
            }

        # dojrzewanie partii juz w kotle - te z licznikiem 0 zamieniamy na gotowy ser
        pozostale = []
        for partia in self.kociol_kolejka:
            partia[0] -= 1
            if partia[0] <= 0:
                ser_dzis += partia[1]
            else:
                pozostale.append(partia)
        self.kociol_kolejka = pozostale

        # dzisiejsze mleko owcze wchodzi do kotla jako nowa partia
        if mleko_owcze_dzis > 0:
            wartosc = mleko_owcze_dzis * config.PRZYCHOD_Z_SERA
            self.kociol_kolejka.append([config.KOCIOL_DNI_NA_SER, wartosc])

        # ile sera dojrzeje nastepnego dnia = suma partii, ktorym zostal jeszcze jeden dzien.
        # Dzieki temu gracz z gory wie, ile pieniedzy da kociol jutro.
        ser_jutro = sum(partia[1] for partia in self.kociol_kolejka if partia[0] == 1)

        return {
            "aktywny": True,
            "mleko_dzis": mleko_owcze_dzis,
            "ser_dzis": ser_dzis,
            "ser_jutro": ser_jutro,
            "partie_w_kotle": len(self.kociol_kolejka),
        }

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

        # rodzimy mlode - kazda matka rodzi mlode swojego gatunku (cielaka lub jagnie)
        narodziny = []
        for matka in matki:
            nowe_id = self._nowe_id()
            imie = random.choice(IMIONA_KROW)
            mlode = matka.stworz_mlode(nowe_id, matka.pozycja, imie)
            # mlode pojawia sie na wolnej kratce obok matki
            x, y = matka.pozycja_wizualna
            mlode.pozycja_wizualna = self.pastwisko._losuj_sasiada(x, y)
            self.dodaj_zwierze(mlode)
            narodziny.append(f"{mlode.imie} (matka: {matka.imie})")
        return narodziny, ciaze_dzis

    # Najwazniejsza i glowna metoda nowy_dzien!! jedna doba symulacji. Zwraca logi dnia
    def nowy_dzien(self) -> dict:
        # start. nowy dzien
        self.dzien += 1

        # reset krow na now dzien
        for krowa in self.stado:
            krowa.reset_dnia()

        # czyscimy liste zdarzen na nowy dzien
        self.narodziny_dzis = []
        self.zmartwychwstania_dzis = []
        self.do_wyleczenia = []

        # zdarzenia losowe
        opisy_zdarzen = self.zdarzenia.aktualizuj(self, self.dzien)

        # losowanie nowego stanu pogody
        stan_pogody = self.pogoda.nowy_dzien()

        # czyscimy pastwisko i dodajemy nowa trawe
        self.pastwisko.wyczysc()
        ile_kepek = int(config.BAZA_KEPEK_TRAWY * self.pogoda.mnoznik_trawy())
        self.pastwisko.generuj_trawke(ile_kepek)

        # plot, jesli stoi, zmniejsza szanse na drapieznika i odliczamy mu dzien.
        # Komunikat o zniszczeniu pada dopiero w dniu, w ktorym plotu juz nie ma
        plot_aktywny = self.plot_dni_pozostale > 0
        if plot_aktywny:
            self.plot_dni_pozostale -= 1
        plot_zniszczony = self.plot_stal_wczoraj and not plot_aktywny
        if plot_zniszczony:
            self.plot_dziury = []  # nie ma plotu - nie ma dziur
        self.plot_stal_wczoraj = plot_aktywny

        # antena, jesli dziala, blokuje dzis zdarzenie UFO (sprawdzane wyzej w zdarzeniach na
        # jeszcze nieodliczonej wartosci) i odliczamy jej dzien
        antena_aktywna = self.antena_dni_pozostale > 0
        if antena_aktywna:
            self.antena_dni_pozostale -= 1

        # drapiezniki - losujemy czy sie pojawia. Plot tnie szanse, ale jej nie zeruje -
        # drapieznik moze i tak  wkrasc sie przez dziure w plocie
        self.drapiezniki = []
        drapieznik_przez_dziure = False
        wolne_kepki = self.pastwisko.kepki_z_trawa()
        if len(wolne_kepki) > 0 and random.random() < self._szansa_na_drapieznika(
            plot_aktywny
        ):
            ile = random.randint(1, self.maks_drapieznikow)
            ile = min(ile, len(wolne_kepki))  # nie wiecej drapieznikow niz kepek
            for i in range(ile):
                self.drapiezniki.append(Drapieznik(id=i, pozycja=(0, 0)))
            self.pastwisko.rozmieszcz_drapiezniki(self.drapiezniki)
            if plot_aktywny:
                drapieznik_przez_dziure = True  # przedarl sie mimo stojacego plotu
                # dziura po nim zostaje w plocie az plot zniknie
                for d in self.drapiezniki:
                    kolumna = d.pozycja[0]
                    if kolumna not in self.plot_dziury:
                        self.plot_dziury.append(kolumna)

        # jesli krowa nie zyje przez wejsciwem na pastwisko to np ofiara zdarznia
        martwe_przed_drapieznikami = []
        for krowa in self.stado:
            if not krowa.zyje:
                martwe_przed_drapieznikami.append(krowa.id)

        # przypisujemy do kepek tylko zwierzeta pasace sie na trawie - kury jedza z kurnika,
        # wiec nie zajmuja kepek
        self.pastwisko.przypisz_krowy([z for z in self.stado if z.je_trawe()])

        # kury nie pasa sie, ale wedruja po farmie - dostaja losowa pozycje na planszy
        for kura in self.stado:
            if kura.zyje and not kura.je_trawe():
                x = random.randint(0, self.pastwisko.szerokosc - 1)
                y = random.randint(0, self.pastwisko.wysokosc - 1)
                kura.pozycja_wizualna = (x, y)

        # jesli jjakas krowa juz nie zyje to musi byc ofiara drapieznika
        zabite_przez_drapieznika = []
        for krowa in self.stado:
            if not krowa.zyje and krowa.id not in martwe_przed_drapieznikami:
                zabite_przez_drapieznika.append(krowa.id)

        # czynniki naturalne
        for krowa in self.stado:
            krowa.starzej_sie_smierc_glodowa_doroslosc()  # do poprawy, nazwa/rozdzielić funkcje?

        # weterynarz dobija do pelna najedzenia na koniec dnia ( po dziennym ubytku)
        for krowa in self.do_wyleczenia:
            if krowa.zyje:
                krowa.najedzenie = GLOD_START

        # kury moga zginac wylacznie ze starosci - jesli cos innego (zdarzenie) je "zabilo",
        # wracaja do zycia. Zdarzenie moglo je zaatakowac, ale nie moze ich usmiercic.
        for zwierze in self.stado:
            if not zwierze.zyje and not zwierze.smierc_dozwolona():
                zwierze.zyje = True
                zwierze.umarla_dzis = False

        # dorastanie mlodych (cielaki -> krowy, jagnieta -> owce)
        dorastajace = self._dorosnij_mlode()

        # rozmnazanie
        narodziny, ciaze_dzis = self._rozmnazanie()
        narodziny.extend(self.narodziny_dzis)

        # usuwmy martwe krowy i zwracamy do logu
        martwe = self.usun_martwe()

        # kurnik istnieje dopoki zyje choc jedna kura; znika, gdy padnie ostatnia
        kurnik_aktywny = self._liczba_kur() > 0
        kurnik_zniknal = self.mial_kury_wczoraj and not kurnik_aktywny
        self.mial_kury_wczoraj = kurnik_aktywny
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
                    "gatunek": krowa.gatunek,
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
            elif krowa.gatunek == "kura":
                powod_smierci[krowa.imie] = "starość"
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

        # czy wujek lesniczy pilnuje pastwiska. jesli tak to rysujemy jego postac
        lesniczy_aktywny = False
        for z in self.zdarzenia.aktywne:
            if isinstance(z, Lesniczy):
                lesniczy_aktywny = True

        # finanse - kazde zwierze liczy swoj przychod polimorficznie.
        # Wyjatek: gdy stoi kociol, mleko doroslych owiec nie idzie na sprzedaz wprost, tylko
        # trafia do kotla, gdzie po kilku dniach dojrzeje w wart wiecej ser.
        przychod = 0
        mleko_owcze_dzis = 0
        for zwierze in self.stado:
            if self.kociol and zwierze.produkuje_mleko_owcze():
                mleko_owcze_dzis += 1
            else:
                przychod += zwierze.wartosc_produktu()

        stan_kotla = self._przetworz_kociol(mleko_owcze_dzis)
        przychod += stan_kotla["ser_dzis"]

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
            "zmartwychwstania": self.zmartwychwstania_dzis,
            "martwe": imiona_martwych_krow,
            "powod_smierci": powod_smierci,
            "dorastanie": dorastajace,
            "zjadly": najedzone_krowy,
            "glodne": glodne_krowy,
            "drapiezniki": pozycje_drapieznikow,
            "stan_krow": stan_krow,
            "kepki_trawy": pozycje_trawy,
            "finanse": stan_finansow,
            "kociol": stan_kotla,
            "zdarzenia": opisy_zdarzen,
            "ciaze": ciaze_dzis,
            "zakupy": self.zakupy_dzis,
            "plot_aktywny": plot_aktywny,
            "plot_dni": self.plot_dni_pozostale,
            "plot_zniszczony": plot_zniszczony,
            "plot_dziury": list(self.plot_dziury),
            "drapieznik_przez_dziure": drapieznik_przez_dziure,
            "lesniczy_aktywny": lesniczy_aktywny,
            "antena_aktywna": antena_aktywna,
            "antena_dni": self.antena_dni_pozostale,
            "kurnik_aktywny": kurnik_aktywny,
            "kurnik_zniknal": kurnik_zniknal,
            "kura_dni_zycia": config.KURA_DNI_ZYCIA,
        }
        # zakupy zostaly juz zapisane do logu = czyscimy bufor na kolejny dzien
        self.zakupy_dzis = []
        return log
