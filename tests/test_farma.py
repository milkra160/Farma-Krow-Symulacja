from src.farma import Farma
from src.pastwisko.pastwisko import Pastwisko
from src.pogoda import Pogoda
from src.finanse import Finanse
from src.zdarzenia import ZdarzeniaLosoweMenadzer
from src.zwierzeta.krowa import Krowa
from src.zwierzeta.owca import Owca
from src.zwierzeta.kura import Kura
from src.zdarzenia import Lesniczy
from src.config import (
    KOCIOL_DNI_NA_SER,
    PRZYCHOD_Z_SERA,
    PRZYCHOD_Z_OWCY,
    PRZYCHOD_Z_KURY,
    KURA_DNI_ZYCIA,
    KURA_WZROST_SZANSY_DRAPIEZNIKA,
)


# pomocnicza metoda tworzy farme
def zrob_farme(stado=None):
    return Farma(
        nazwa="Nazwa testowa",
        pastwisko=Pastwisko(5, 5),
        pogoda=Pogoda(),
        finanse=Finanse(),
        zdarzenia=ZdarzeniaLosoweMenadzer(),
        stado=stado,
    )


def test_czy_farma_Startuje_pusta():
    f = zrob_farme()
    assert f.dzien == 0
    assert f.nazwa == "Nazwa testowa"
    assert f.liczba_krow() == 0


def test_dodaj_zwierze():
    a = Krowa(id=1, pozycja=(0, 0), imie="A")
    b = Krowa(id=2, pozycja=(0, 0), imie="B")
    b.zyje = False
    f = zrob_farme([a, b])
    martwe = f.usun_martwe()
    assert f.liczba_krow() == 1
    assert len(martwe) == 1
    assert martwe[0] is b


def test_czy_nowe_id_jest_ciagle_nowe():
    f = zrob_farme()
    assert f._nowe_id() == 1
    assert f._nowe_id() == 2
    assert f._nowe_id() == 3


def test_czy_nowe_id_uwzglednia_stado_startowe():
    f = zrob_farme(
        [Krowa(id=1, pozycja=(0, 0), imie="A"), Krowa(id=5, pozycja=(0, 0), imie="B")]
    )
    assert f._nowe_id() == 6  # licznik startuje od najwyzszego id w stadzie


def test_czy_farma_jest_aktywna():
    f = zrob_farme()
    assert f.czy_aktywna() == True
    f.finanse.budzet = 0
    assert f.czy_aktywna() == False


# tworzymy farme do testow
def stworz_farme(liczba_krow=3):
    stado = []
    for i in range(liczba_krow):
        stado.append(Krowa(id=i, pozycja=(0, 0), imie=f"K{i}"))
    return Farma(
        "Farma",
        Pastwisko(20, 20),
        Pogoda(),
        Finanse(),
        ZdarzeniaLosoweMenadzer(),
        stado,
    )


def test_czy_nowy_dzien_bedzie_zwiekszal_dzien():
    f = stworz_farme()
    log = f.nowy_dzien()
    assert f.dzien == 1
    assert log["dzien"] == 1


def test_czy_slownik_nowy_dzien_ma_klucze():
    f = stworz_farme()
    log = f.nowy_dzien()
    for klucz in [
        "dzien",
        "pogoda",
        "narodziny",
        "martwe",
        "powod_smierci",
        "zjadly",
        "drapiezniki",
        "stan_krow",
        "glodne",
        "kepki_trawy",
        "finanse",
        "zdarzenia",
    ]:
        assert klucz in log


def test_nowy_dzien_czy_pogoda_bedzie_poprawna():
    f = stworz_farme()
    log = f.nowy_dzien()
    assert log["pogoda"] in ("slonecznie", "deszcz", "susza")


def test_czy_nowy_dzien_dobrze_rozlicza_finanse():
    f = stworz_farme()
    log = f.nowy_dzien()
    finanse = log["finanse"]
    assert finanse["bilans"] == finanse["przychod"] - finanse["koszt"]


def test_nowy_dzien_dziala_dla_kilku_dni():
    f = stworz_farme()
    for _ in range(5):
        f.nowy_dzien()
    assert f.dzien == 5


def test_czy_nowy_dzien_zwraca_poprawny_log_krow():
    f = stworz_farme(liczba_krow=1)
    log = f.nowy_dzien()
    krowa_log = log["stan_krow"][0]
    for klucz in [
        "id",
        "imie",
        "pozycja_wizualna",
        "pozycja_kepki",
        "najedzenie",
        "wiek",
        "dorosla",
        "w_ciazy",
        "zjadla",
        "zyje",
        "umarla_dzis",
    ]:
        assert klucz in krowa_log


def test_lesniczy_aktywny_trafia_do_logu():
    f = stworz_farme()
    f.zdarzenia.szansa_zdarzenia = (
        0  # bez losowych zdarzen - testujemy tylko lesniczego
    )
    lesniczy = Lesniczy()
    lesniczy.dni_pozostale = lesniczy.dni_trwania
    lesniczy.zastosuj(f)
    f.zdarzenia.aktywne.append(lesniczy)
    log = f.nowy_dzien()
    assert log["lesniczy_aktywny"] is True


def test_bez_lesniczego_flaga_jest_false():
    f = stworz_farme()
    f.zdarzenia.szansa_zdarzenia = 0
    log = f.nowy_dzien()
    assert log["lesniczy_aktywny"] is False


def test_antena_odlicza_dzien_i_trafia_do_logu():
    f = stworz_farme()
    f.zdarzenia.szansa_zdarzenia = 0
    f.antena_dni_pozostale = 3
    log = f.nowy_dzien()
    assert log["antena_aktywna"] is True
    assert f.antena_dni_pozostale == 2  # ubyl jeden dzien


#  Kury i kurnik ***********************************************


def test_posiadanie_kur_zwieksza_szanse_na_drapieznika():
    # liczy sie sam fakt posiadania kur - dwie kury podnosza szanse tak samo jak jedna
    f = zrob_farme([Kura(1, (0, 0), "A"), Kura(2, (0, 0), "B")])
    f.szansa_drapieznik = 0.2
    assert f._szansa_na_drapieznika(False) == 0.2 + KURA_WZROST_SZANSY_DRAPIEZNIKA


def test_bez_kur_szansa_na_drapieznika_bez_bonusu():
    f = zrob_farme([Krowa(1, (0, 0), "Mu")])
    f.szansa_drapieznik = 0.2
    assert f._szansa_na_drapieznika(False) == 0.2


def test_kura_chodzi_po_planszy():
    kura = Kura(id=1, pozycja=(0, 0), imie="Gyra")
    f = zrob_farme([kura])
    f.zdarzenia.szansa_zdarzenia = 0
    f.szansa_drapieznik = 0
    f.nowy_dzien()
    # kura wedruje po planszy - dostaje pozycje w granicach pastwiska
    assert kura.pozycja_wizualna is not None
    x, y = kura.pozycja_wizualna
    assert 0 <= x < f.pastwisko.szerokosc
    assert 0 <= y < f.pastwisko.wysokosc


def test_ufo_ucieka_przed_kura():
    # UFO trafia na kure (jedyne zwierze) - ucieka przed potomkiem dinozaurow, nikogo nie porywa
    from src.zdarzenia import ZdarzeniaLosoweMenadzer, UFO

    kura = Kura(id=1, pozycja=(0, 0), imie="Gyra")
    f = zrob_farme([kura])
    f.szansa_drapieznik = 0
    f.zdarzenia = ZdarzeniaLosoweMenadzer(pula=[UFO], szansa_zdarzenia=1.0)
    log = f.nowy_dzien()
    assert kura.zyje is True
    assert any("dinozaur" in o.lower() for o in log["zdarzenia"])


def test_kura_przezywa_smiertelne_zdarzenie():
    # zabojcze zdarzenie usmierca cale stado, ale Farma cofa smierc kury (ginie tylko ze starosci)
    from src.zdarzenia import ZdarzenieLosoweBase, ZdarzeniaLosoweMenadzer

    class ZabojczeZdarzenie(ZdarzenieLosoweBase):
        def __init__(self):
            super().__init__()
            self.nazwa = "Kataklizm"
            self.opis = "usmierca wszystkich"
            self.dni_trwania = 1

        def czy_zachodzi(self, dzien):
            return True

        def zastosuj(self, farma):
            for z in farma.stado:
                z.zyje = False
                z.umarla_dzis = True
            return self.opis

        def cofnij(self, farma):
            pass

    kura = Kura(id=1, pozycja=(0, 0), imie="Gyra")
    f = zrob_farme([kura])
    f.szansa_drapieznik = 0
    f.zdarzenia = ZdarzeniaLosoweMenadzer(pula=[ZabojczeZdarzenie], szansa_zdarzenia=1.0)
    f.nowy_dzien()
    assert kura.zyje is True  # zdarzenie ja zabilo, ale Farma cofnela smierc


def test_kura_daje_przychod_z_jajek():
    kura = Kura(id=1, pozycja=(0, 0), imie="Gyra")
    f = zrob_farme([kura])
    f.zdarzenia.szansa_zdarzenia = 0
    f.szansa_drapieznik = 0
    log = f.nowy_dzien()
    assert log["finanse"]["przychod"] == PRZYCHOD_Z_KURY


def test_kurnik_znika_gdy_padnie_ostatnia_kura():
    kura = Kura(id=1, pozycja=(0, 0), imie="Gyra")
    f = zrob_farme([kura])
    f.zdarzenia.szansa_zdarzenia = 0
    f.szansa_drapieznik = 0
    log = f.nowy_dzien()  # dzien 1: kura zyje, kurnik czynny
    assert log["kurnik_aktywny"] is True
    kura.wiek = KURA_DNI_ZYCIA  # nastepny dzien dobije ja ze starosci
    log = f.nowy_dzien()
    assert log["kurnik_aktywny"] is False
    assert log["kurnik_zniknal"] is True
    assert log["powod_smierci"]["Gyra"] == "starość"


#  Kociol serowarski *******************************************


# pomocnik: farma z jedna dorosla owca i wlaczonym kotlem, bez losowosci
def farma_z_owca_i_kotlem():
    owca = Owca(id=1, pozycja=(0, 0), imie="Bela")
    owca.dorosla = True
    f = zrob_farme([owca])
    f.zdarzenia.szansa_zdarzenia = 0
    f.szansa_drapieznik = 0
    f.kociol = True
    return f


def test_ser_splywa_dopiero_po_dojrzeniu_w_kotle():
    f = farma_z_owca_i_kotlem()
    # przez pierwsze KOCIOL_DNI_NA_SER dni mleko dojrzewa - jeszcze zadnego sera
    for _ in range(KOCIOL_DNI_NA_SER):
        log = f.nowy_dzien()
        assert log["kociol"]["ser_dzis"] == 0
        assert log["finanse"]["przychod"] == 0
    # nastepnego dnia pierwsza partia jest gotowa - splywa ser wart wiecej niz mleko
    log = f.nowy_dzien()
    assert log["kociol"]["ser_dzis"] == PRZYCHOD_Z_SERA
    assert log["finanse"]["przychod"] == PRZYCHOD_Z_SERA
    assert PRZYCHOD_Z_SERA > PRZYCHOD_Z_OWCY  # ser oplaca sie bardziej niz samo mleko


def test_kociol_zapowiada_ile_sera_dojrzeje_jutro():
    # dzien przed pierwszym serem kociol powinien juz zapowiadac wartosc partii dojrzewajacej jutro
    f = farma_z_owca_i_kotlem()
    for _ in range(KOCIOL_DNI_NA_SER - 1):
        log = f.nowy_dzien()
        assert log["kociol"]["ser_dzis"] == 0  # ser jeszcze nie splynal
    log = f.nowy_dzien()  # ostatni dzien dojrzewania pierwszej partii
    assert log["kociol"]["ser_dzis"] == 0
    assert log["kociol"]["ser_jutro"] == PRZYCHOD_Z_SERA  # jutro splynie ser wart tyle
    log = f.nowy_dzien()
    assert log["kociol"]["ser_dzis"] == PRZYCHOD_Z_SERA  # i faktycznie splywa


def test_ser_powstaje_nawet_po_smierci_owcy():
    # mleko wrzucone do kotla dojrzewa niezaleznie od owcy - ser splywa nawet gdy owca juz nie zyje
    f = farma_z_owca_i_kotlem()
    owca = f.stado[0]
    for _ in range(KOCIOL_DNI_NA_SER):  # 3 dni mleka = 3 partie czekaja w kotle
        f.nowy_dzien()
    owca.zyje = False  # owca umiera zanim ktorakolwiek partia dojrzala
    log = f.nowy_dzien()
    assert sum(1 for z in f.stado if z.gatunek == "owca") == 0  # brak owiec w stadzie
    assert log["kociol"]["ser_dzis"] == PRZYCHOD_Z_SERA  # a ser i tak splywa
    assert log["finanse"]["przychod"] == PRZYCHOD_Z_SERA


def test_bez_kotla_owca_daje_tylko_mleko():
    owca = Owca(id=1, pozycja=(0, 0), imie="Bela")
    owca.dorosla = True
    f = zrob_farme([owca])
    f.zdarzenia.szansa_zdarzenia = 0
    f.szansa_drapieznik = 0
    log = f.nowy_dzien()
    assert log["kociol"]["aktywny"] is False
    assert log["finanse"]["przychod"] == PRZYCHOD_Z_OWCY
