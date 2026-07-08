from src.zwierzeta.krowa import Krowa
from src.zwierzeta.drapieznik import Drapieznik
from src.zwierzeta.cielak import Cielak
from src.zwierzeta.owca import Owca
from src.zwierzeta.jagnie import Jagnie
from src.zwierzeta.kura import Kura
from src.config import *
from src.pastwisko.komorka import Komorka

#   Zwierzeta **************************************************


#  Krowa *********************************************************


def test_krowa_zaczyna_z_pelnym_najedzeniem():
    k = Krowa(id=1, pozycja=(0, 0), imie="Łaciata")
    assert k.najedzenie == GLOD_START


def test_krowa_starzeje_sie():
    k = Krowa(id=1, pozycja=(0, 0), imie="Hipolit")
    k.starzej_sie_smierc_glodowa_doroslosc()
    assert k.wiek == 1
    assert k.najedzenie == GLOD_START - GLOD_DZIENNY_UBYTEK


def test_krowa_umiera_z_glodu():
    k = Krowa(id=1, pozycja=(0, 0), imie="Karol")
    k.najedzenie = GLOD_DZIENNY_UBYTEK
    k.starzej_sie_smierc_glodowa_doroslosc()
    assert k.zyje == False
    assert k.umarla_dzis == True


def test_krowa_dorasta():
    k = Krowa(id=1, pozycja=(0, 0), imie="Łaciata")
    k.najedzenie = 999
    for _ in range(WIEK_DOROSLOSCI):
        k.starzej_sie_smierc_glodowa_doroslosc()
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
    k.przypisana_kepka = Komorka(x=0, y=0)
    k.reset_dnia()
    assert k.zjadla_dzisiaj == False
    assert k.umarla_dzis == False
    assert k.przypisana_kepka is None


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


#  Cielak *******************************************************


def test_cielak_ma_symbol_c():
    c = Cielak(id=2, pozycja=(1, 1), imie="Mały")
    assert c.symbol == "c"


def test_cielak_nie_produkuje_mleka():
    c = Cielak(id=2, pozycja=(1, 1), imie="Mały")
    assert c.wartosc_mleka() == 0


def test_cielak_dziedziczy_starzenie():
    c = Cielak(id=2, pozycja=(1, 1), imie="Mały")
    c.starzej_sie_smierc_glodowa_doroslosc()
    assert c.wiek == 1


#  Owca *********************************************************


def test_owca_ma_symbol_O_i_gatunek():
    o = Owca(id=1, pozycja=(0, 0), imie="Bela")
    assert o.symbol == "O"
    assert o.gatunek == "owca"


def test_owca_wolniej_glodnieje_niz_krowa():
    o = Owca(id=1, pozycja=(0, 0), imie="Bela")
    o.starzej_sie_smierc_glodowa_doroslosc()
    assert o.najedzenie == GLOD_START - OWCA_GLOD_DZIENNY_UBYTEK
    assert OWCA_GLOD_DZIENNY_UBYTEK < GLOD_DZIENNY_UBYTEK  # owca traci mniej niz krowa


def test_dorosla_owca_daje_male_mleko():
    o = Owca(id=1, pozycja=(0, 0), imie="Bela")
    o.dorosla = False
    assert o.wartosc_produktu() == 0
    o.dorosla = True
    assert o.wartosc_produktu() == PRZYCHOD_Z_OWCY


def test_tylko_dorosla_owca_produkuje_mleko_owcze():
    o = Owca(id=1, pozycja=(0, 0), imie="Bela")
    assert o.produkuje_mleko_owcze() is False  # jeszcze niedorosla
    o.dorosla = True
    assert o.produkuje_mleko_owcze() is True


def test_owca_rodzi_jagnie():
    o = Owca(id=1, pozycja=(0, 0), imie="Bela")
    mlode = o.stworz_mlode(2, (0, 0), "Mania")
    assert isinstance(mlode, Jagnie)


#  Jagnie *******************************************************


def test_jagnie_ma_symbol_J_i_jest_mlode():
    j = Jagnie(id=2, pozycja=(1, 1), imie="Mania")
    assert j.symbol == "J"
    assert j.mlode is True
    assert j.gatunek == "owca"


def test_jagnie_nie_produkuje_mleka():
    j = Jagnie(id=2, pozycja=(1, 1), imie="Mania")
    assert j.wartosc_produktu() == 0


def test_jagnie_dorasta_na_owce_z_zachowanym_stanem():
    j = Jagnie(id=2, pozycja=(1, 1), imie="Mania")
    j.najedzenie = 55
    j.dorosla = True
    dorosla = j.stworz_dorosla_wersje()
    assert isinstance(dorosla, Owca)
    assert not isinstance(dorosla, Jagnie)
    assert dorosla.najedzenie == 55
    assert dorosla.imie == "Mania"


#  Kura *********************************************************


def test_kura_daje_jajka_i_nie_je_trawy():
    k = Kura(id=1, pozycja=(0, 0), imie="Gyra")
    assert k.gatunek == "kura"
    assert k.je_trawe() is False  # karmi sie z kurnika, nie z trawy
    assert k.wartosc_produktu() == PRZYCHOD_Z_KURY


def test_kura_pada_ze_starosci_po_ustalonym_czasie():
    k = Kura(id=1, pozycja=(0, 0), imie="Gyra")
    for _ in range(KURA_DNI_ZYCIA):
        k.starzej_sie_smierc_glodowa_doroslosc()
        assert k.zyje is True  # przez caly okres zycia zyje
    k.starzej_sie_smierc_glodowa_doroslosc()  # dzien po limicie
    assert k.zyje is False
    assert k.umarla_dzis is True


def test_kura_nie_umiera_z_glodu():
    k = Kura(id=1, pozycja=(0, 0), imie="Gyra")
    k.najedzenie = 0  # nawet z zerowym najedzeniem
    k.starzej_sie_smierc_glodowa_doroslosc()
    assert k.zyje is True  # kura nie umiera z glodu, tylko ze starosci


def test_kura_smierc_dozwolona_tylko_ze_starosci():
    k = Kura(id=1, pozycja=(0, 0), imie="Gyra")
    k.wiek = 3
    assert k.smierc_dozwolona() is False  # mloda - smierc od zdarzenia sie nie liczy
    k.wiek = KURA_DNI_ZYCIA + 1
    assert k.smierc_dozwolona() is True  # przekroczyla wiek zycia


#  Drapieznik *******************************************************


def test_czy_drapieznik_ma_symbol_wykrzyknik():
    d = Drapieznik(id=1, pozycja=(0, 0))
    assert d.symbol == "!"


def test_drapieznik_zabija_krowe():
    k = Krowa(id=1, pozycja=(3, 3), imie="Łaciat")
    d = Drapieznik(id=2, pozycja=(3, 3))
    wynik = d.zaatakuj(k)
    assert wynik is True
    assert k.zyje is False
    assert k.umarla_dzis is True


# Sprawdzamy czy nie ma bledu z ruchem drapieznika( musi miec ruch bo dziedziczy po zwierzeciu)
def test_drapieznik_sie_nie_rusza():
    d = Drapieznik(id=1, pozycja=(3, 3))
    d.ruch()
    assert d.pozycja == (3, 3)
