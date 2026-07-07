from src.farma import Farma
from src.pastwisko.pastwisko import Pastwisko
from src.pogoda import Pogoda
from src.finanse import Finanse
from src.zdarzenia import ZdarzeniaLosoweMenadzer
from src.zwierzeta.krowa import Krowa
from src.sklep import Sklep, KupDoroslaKrowe, KupCielaka, WorekPaszy, Plot
from src.config import *


# pomocnicza metoda tworzy farme z zadanym budzetem
def zrob_farme(budzet=1000, stado=None):
    finanse = Finanse()
    finanse.budzet = budzet
    return Farma(
        nazwa="Nazwa testowa",
        pastwisko=Pastwisko(5, 5),
        pogoda=Pogoda(),
        finanse=finanse,
        zdarzenia=ZdarzeniaLosoweMenadzer(),
        stado=stado,
    )


#  Finanse.wydaj *************************************************


def test_wydaj_pobiera_kase():
    f = Finanse()
    f.budzet = 500
    assert f.wydaj(200) is True
    assert f.budzet == 300


def test_wydaj_odmawia_gdy_za_malo():
    f = Finanse()
    f.budzet = 100
    assert f.wydaj(200) is False
    assert f.budzet == 100


def test_wydaj_nie_pozwala_zejsc_do_zera():
    f = Finanse()
    f.budzet = 200
    assert f.wydaj(200) is False  # zostawienie 0 = bankructwo, wiec zakaz
    assert f.budzet == 200


#  Sklep *******************************************************


def test_sklep_ma_domyslny_katalog():
    sklep = Sklep()
    assert len(sklep.katalog) == 4


def test_kup_dorosla_krowe_dodaje_krowe_i_pobiera_kase():
    f = zrob_farme(budzet=1000)
    sklep = Sklep()
    udalo_sie, _ = sklep.kup(KupDoroslaKrowe(), f)
    assert udalo_sie is True
    assert f.liczba_krow() == 1
    assert f.stado[0].dorosla is True
    assert f.finanse.budzet == 1000 - CENA_DOROSLEJ_KROWY


def test_kup_cielaka_dodaje_niedoroslego():
    f = zrob_farme(budzet=1000)
    sklep = Sklep()
    sklep.kup(KupCielaka(), f)
    assert f.liczba_krow() == 1
    assert f.stado[0].symbol == "c"
    assert f.stado[0].dorosla is False


def test_kup_bez_kasy_sie_nie_udaje():
    f = zrob_farme(budzet=50)  # za malo na cokolwiek
    sklep = Sklep()
    udalo_sie, _ = sklep.kup(KupDoroslaKrowe(), f)
    assert udalo_sie is False
    assert f.liczba_krow() == 0
    assert f.finanse.budzet == 50


def test_worek_paszy_dolewa_najedzenia():
    krowa = Krowa(id=1, pozycja=(0, 0), imie="Mucka")
    krowa.najedzenie = 30
    f = zrob_farme(budzet=1000, stado=[krowa])
    Sklep().kup(WorekPaszy(), f)
    assert krowa.najedzenie == 30 + PASZA_NAJEDZENIE


def test_worek_paszy_nie_przekracza_maksa():
    krowa = Krowa(id=1, pozycja=(0, 0), imie="Mucka")
    krowa.najedzenie = 90
    f = zrob_farme(budzet=1000, stado=[krowa])
    Sklep().kup(WorekPaszy(), f)
    assert krowa.najedzenie == GLOD_START


def test_plot_daje_ochrone_na_kilka_dni():
    f = zrob_farme(budzet=1000)
    Sklep().kup(Plot(), f)
    assert f.plot_dni_pozostale == PLOT_DNI_TRWANIA


def test_plot_tnie_szanse_ale_nie_zeruje():
    f = zrob_farme(budzet=1000)
    f.szansa_drapieznik = 0.4
    # ze stojacym plotem szansa jest przemnozona przez mnoznik, bez plotu - pelna
    assert f._szansa_na_drapieznika(True) == 0.4 * PLOT_MNOZNIK_SZANSY
    assert f._szansa_na_drapieznika(False) == 0.4


def test_plot_odlicza_dzien():
    f = zrob_farme(budzet=1000)
    f.zdarzenia.szansa_zdarzenia = 0  # wylaczamy losowe zdarzenia by test byl stabilny
    Sklep().kup(Plot(), f)
    log = f.nowy_dzien()
    assert log["plot_aktywny"] is True
    assert f.plot_dni_pozostale == PLOT_DNI_TRWANIA - 1  # ubyl jeden dzien


def test_plot_zniszczony_dzien_po_wygasnieciu():
    f = zrob_farme(budzet=1000)
    f.zdarzenia.szansa_zdarzenia = 0
    f.szansa_drapieznik = 0  # brak drapieznikow - czysty test odliczania
    Sklep().kup(Plot(), f)
    # przez caly czas trwania plot stoi i sie nie niszczy
    for _ in range(PLOT_DNI_TRWANIA):
        log = f.nowy_dzien()
        assert log["plot_aktywny"] is True
        assert log["plot_zniszczony"] is False
    # dopiero nastepnego dnia, gdy plotu juz nie ma, pada komunikat o zniszczeniu
    log = f.nowy_dzien()
    assert log["plot_aktywny"] is False
    assert log["plot_zniszczony"] is True


def test_dziura_w_plocie_zostaje_do_konca_plotu():
    f = zrob_farme(budzet=1000)
    f.zdarzenia.szansa_zdarzenia = 0
    f.szansa_drapieznik = 0  # sami sterujemy dziurami, bez nowych drapieznikow
    Sklep().kup(Plot(), f)
    f.plot_dziury = [3]  # udajemy ze drapieznik wczesniej przedarl sie w kolumnie 3
    log = f.nowy_dzien()
    assert 3 in log["plot_dziury"]  # dziura trwa nadal
    # po wygasnieciu plotu dziury znikaja razem z nim
    for _ in range(PLOT_DNI_TRWANIA):
        f.nowy_dzien()
    assert f.plot_dziury == []
