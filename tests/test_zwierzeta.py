from src.wszystkie_zwierzeta.krowa import Krowa
from src.wszystkie_zwierzeta.drapieznik import Drapieznik
from src.wszystkie_zwierzeta.cielak import Cielak
from src.config import *

#   Zwierzeta **************************************************


#  Krowa *********************************************************


def test_krowa_zaczyna_z_pelnym_najedzeniem():
    k = Krowa(id=1, pozycja=(0, 0), imie="Łaciata")
    assert k.najedzenie == GLOD_START


def test_krowa_starzeje_sie():
    k = Krowa(id=1, pozycja=(0, 0), imie="Hipolit")
    k.starzej_sie()
    assert k.wiek == 1
    assert k.najedzenie == GLOD_START - GLOD_DZIENNY_UBYTEK


def test_krowa_umiera_z_glodu():
    k = Krowa(id=1, pozycja=(0, 0), imie="Karol")
    k.najedzenie = GLOD_DZIENNY_UBYTEK
    k.starzej_sie()
    assert k.zyje == False
    assert k.umarla_dzis == True


def test_krowa_dorasta():
    k = Krowa(id=1, pozycja=(0, 0), imie="Łaciata")
    k.najedzenie = 999
    for _ in range(WIEK_DOROSLOSCI):
        k.starzej_sie()
    assert k.dorosla == True


def test_krowa_je():
    k = Krowa(id=1, pozycja=(0, 0), imie="Łaciata")
    k.najedzenie = 50
    k.jedz()
    assert k.najedzenie == 50 + GLOD_Z_JEDZENIA
    assert k.zjadla_dzisiaj == True


def test_krowa_nie_je_powyzej_max():
    k = Krowa(id=1, pozycja=(0, 0), imie="Stanislaw")
    k.najedzenie = 90
    k.jedz()
    assert k.najedzenie == GLOD_START


def test_krowa_reset_dnia():
    k = Krowa(id=1, pozycja=(0, 0), imie="Marek")
    k.zjadla_dzisiaj = True
    k.umarla_dzis = True
    k.reset_dnia()
    assert k.zjadla_dzisiaj == False
    assert k.umarla_dzis == False


def test_krowa_czy_gloda():
    k = Krowa(id=1, pozycja=(0, 0), imie="Beata")
    k.najedzenie = 39
    assert k.czy_glodna() == True
    k.najedzenie = 40
    assert k.czy_glodna() == False


def test_krowa_wartosc_mleka():
    k = Krowa(id=1, pozycja=(0, 0), imie="Mela")
    k.dorosla = False
    assert k.wartosc_mleka() == 0

    k.dorosla = True
    assert k.wartosc_mleka() == PRZYCHOD_Z_KROWY


def test_krowa_odliczanie_ciaza_i_porod():
    k = Krowa(id=1, pozycja=(0, 0), imie="Mela")
    k.dorosla = True
    k.w_ciazy = True
    k.dni_do_porodu = 2

    # dzien 1
    urodzila = k.aktualizuj_ciaze()
    assert k.dni_do_porodu == 1
    assert urodzila == False
    assert k.w_ciazy == True
    # dzien 2
    urodzila = k.aktualizuj_ciaze()
    assert k.dni_do_porodu == 0
    assert urodzila == True
    assert k.w_ciazy == False


#  Cielak *******************************************************


def test_cielak_ma_symbol_c():
    c = Cielak(id=2, pozycja=(1, 1), imie="Mały")
    assert c.symbol == "c"


def test_cielak_nie_produkuje_mleka():
    c = Cielak(id=2, pozycja=(1, 1), imie="Mały")
    assert c.wartosc_mleka() == 0


def test_cielak_dziedziczy_starzenie():
    c = Cielak(id=2, pozycja=(1, 1), imie="Mały")
    c.starzej_sie()
    assert c.wiek == 1


#  Drapieznik *******************************************************


def test_drapieznik_zabija_na_tym_samym_polu():
    d = Drapieznik(id=10, pozycja=(3, 3))
    k = Krowa(id=1, pozycja=(3, 3), imie="Łaciata")
    assert d.czy_zabija(k) == True
    assert k.zyje == False
    assert k.umarla_dzis == True


def test_drapieznik_nie_zabija_na_innym_polu():
    d = Drapieznik(id=10, pozycja=(3, 3))
    k = Krowa(id=1, pozycja=(5, 5), imie="Łaciata")
    assert d.czy_zabija(k) == False
    assert k.zyje == True
