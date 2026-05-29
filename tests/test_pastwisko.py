from src.config import GLOD_Z_JEDZENIA
from src.pastwisko.komorka import Komorka
from src.zwierzeta.drapieznik import Drapieznik

from src.zwierzeta.krowa import Krowa


# komorka ******************************

def test_start_komorki_jest_pusty():
    k = Komorka(x=2,y=3)
    assert k.x == 2
    assert k.y == 3
    assert k.ma_trawke == False
    assert k.czy_wolna() == True

def test_dodaj_trawke():
    k = Komorka(x=2,y=3)
    k.dodaj_trawke()
    assert k.ma_trawke == True

def test_komorka_nie_jest_wolna_po_wejsciu():
    k = Komorka(x=2,y=3)
    krowa = Krowa(id=1, pozycja=(2,3), imie="Łaciata")
    k.wejdz(krowa)
    assert k.czy_wolna() == False
    assert krowa.przypisana_kepka == k

def test_krowa_wejdz_na_komorke_i_zjedz():
    k = Komorka(x=0,y=0)
    k.dodaj_trawke()
    krowa = Krowa(id=1, pozycja=(0,0), imie="Laciata")
    krowa.najedzenie = 50
    wynik = k.wejdz(krowa)

    assert wynik == "zjadla trawe"
    assert krowa.zjadla_dzisiaj == True
    assert krowa.najedzenie == 50 + GLOD_Z_JEDZENIA
    assert krowa.zyje == True

def test_krowa_wchodzi_bez_trawy():
    k = Komorka(x=0,y=0)
    krowa = Krowa(id=1, pozycja=(0,0), imie="Laciata")
    wynik = k.wejdz(krowa)

    assert wynik == "brak trawy"
    assert krowa.zjadla_dzisiaj == False
    assert krowa.zyje == True

def test_krowa_wchodzi_z_drapieznikiem_i_ginie():
    k = Komorka(x=0,y=0)
    krowa = Krowa(id=1, pozycja=(0,0), imie="Laciata")
    drapieznik = Drapieznik(id=89, pozycja=(0,0))
    k.ma_drapieznika = True
    k.drapieznik = drapieznik
    wynik = k.wejdz(krowa)

    assert wynik == "smierc"
    assert krowa.zyje == False
    assert krowa.umarla_dzis == True


