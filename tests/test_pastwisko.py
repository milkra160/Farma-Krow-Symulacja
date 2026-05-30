from src.config import GLOD_Z_JEDZENIA
from src.pastwisko.komorka import Komorka
from src.pastwisko.pastwisko import Pastwisko
from src.zwierzeta.drapieznik import Drapieznik

from src.zwierzeta.krowa import Krowa


# komorka ******************************


def test_start_komorki_jest_pusty():
    k = Komorka(x=2, y=3)
    assert k.x == 2
    assert k.y == 3
    assert k.ma_trawke == False
    assert k.czy_wolna() == True


def test_dodaj_trawke():
    k = Komorka(x=2, y=3)
    k.dodaj_trawke()
    assert k.ma_trawke == True


def test_komorka_nie_jest_wolna_po_wejsciu():
    k = Komorka(x=2, y=3)
    krowa = Krowa(id=1, pozycja=(2, 3), imie="Łaciata")
    k.wejdz(krowa)
    assert k.czy_wolna() == False
    assert krowa.przypisana_kepka == k


def test_krowa_wejdz_na_komorke_i_zjedz():
    k = Komorka(x=0, y=0)
    k.dodaj_trawke()
    krowa = Krowa(id=1, pozycja=(0, 0), imie="Laciata")
    krowa.najedzenie = 50
    wynik = k.wejdz(krowa)

    assert wynik == "zjadla trawe"
    assert krowa.zjadla_dzisiaj == True
    assert krowa.najedzenie == 50 + GLOD_Z_JEDZENIA
    assert krowa.zyje == True


def test_krowa_wchodzi_bez_trawy():
    k = Komorka(x=0, y=0)
    krowa = Krowa(id=1, pozycja=(0, 0), imie="Laciata")
    wynik = k.wejdz(krowa)

    assert wynik == "brak trawy"
    assert krowa.zjadla_dzisiaj == False
    assert krowa.zyje == True


def test_krowa_wchodzi_z_drapieznikiem_i_ginie():
    k = Komorka(x=0, y=0)
    krowa = Krowa(id=1, pozycja=(0, 0), imie="Laciata")
    drapieznik = Drapieznik(id=89, pozycja=(0, 0))
    k.ma_drapieznika = True
    k.drapieznik = drapieznik
    wynik = k.wejdz(krowa)

    assert wynik == "smierc"
    assert krowa.zyje == False
    assert krowa.umarla_dzis == True


# Pastwisko *******************************************
def test_czy_pastwisko_ma_wymiary():
    p = Pastwisko(5, 3)
    assert p.wysokosc == 3
    assert p.szerokosc == 5


def test_pastwisko_buduje_siatke_komorek():
    p = Pastwisko(5, 3)
    assert len(p.siatka) == 3  # liczba rzedow = wysokosc
    assert len(p.siatka[0]) == 5  # liczba kolumn = szerokosc
    assert isinstance(
        p.siatka[0][0], Komorka
    )  # sprawdzamy czy obiekt siatka nalezy do klasy komorka, by uniknac przyszlych bledow


def test_pobierz_komorke_zwraca_wlasciwa_wartosc():
    p = Pastwisko(5, 3)
    k = p.pobierz_komorke(2, 1)
    assert k.x == 2
    assert k.y == 1


def test_czy_generuj_trawke_ustala_tyle_ile_trzeva():
    p = Pastwisko(5, 5)
    pozycje = p.generuj_trawke(7)
    assert len(pozycje) == 7
    assert len(p.kepki_z_trawa()) == 7


def test_pozycje_generuj_trawke_sa_unikalne():
    p = Pastwisko(5, 5)
    pozycje = p.generuj_trawke(10)
    assert len(set(pozycje)) == 10


def test_kepki_z_trawa_maja_trawe():
    p = Pastwisko(4, 4)
    p.generuj_trawke(3)
    kepki = p.kepki_z_trawa()
    assert len(kepki) == 3
    for k in kepki:
        assert k.ma_trawke == True


def test_generuj_trawke_na_wlasciwych_polach():
    p = Pastwisko(4, 4)
    pozycje = p.generuj_trawke(5)
    for x, y in pozycje:
        assert p.pobierz_komorke(x, y).ma_trawke == True

def test_usun_trawke():
    k = Komorka(x=0, y=0)
    k.dodaj_trawke()
    k.usun_trawke()
    assert k.ma_trawke == False

def test_czy_wyczysc_usuwa_trawe():
    p = Pastwisko(5, 5)
    p.generuj_trawke(5)
    p.wyczysc()
    assert len(p.kepki_z_trawa()) == 0

def test_czy_wwyczysc_usuwa_trawe_z_komorek():
    p = Pastwisko(5, 5)
    k = Krowa(id=1, pozycja=(0, 0), imie="Laciata")
    p.pobierz_komorke(0,0).wejdz(k)
    p.wyczysc()
    assert p.pobierz_komorke(0,0).czy_wolna() == True

def test_czy_wyczysc_usuwa_drapiezniki():
    p = Pastwisko(5, 5)
    k = p.pobierz_komorke(0, 0)
    k.ma_drapieznik = True
    k.drapieznik = Drapieznik(id=89, pozycja=(0, 0))
    p.wyczysc()
    assert p.pobierz_komorke(0, 0).ma_drapieznika == False
    assert p.pobierz_komorke(0, 0).drapieznik is None

#funkcja poomcnicza do testow
def policz_drapiezniki(pastwisko):
    ile = 0
    for rzad in pastwisko.siatka:
        for kratka in rzad:
            if kratka.ma_drapieznika:
                ile += 1
    return ile

def test_rozmieszcz_drapiezniki_stawia_je_na_trawie():
    p = Pastwisko(5, 5)
    p.generuj_trawke(10)
    d1 = Drapieznik(id=1, pozycja=(0, 0))
    d2 = Drapieznik(id=2, pozycja=(0, 0))
    p.rozmieszcz_drapiezniki([d1, d2])

    assert policz_drapiezniki(p) == 2
    for rzad in p.siatka:
        for kratka in rzad:
            if kratka.ma_drapieznika:
                assert kratka.ma_trawke == True
                assert kratka.drapieznik is not None

def test_rozmieszcz_drapiezniki_na_rozne_kepki():
    p = Pastwisko(5, 5)
    p.generuj_trawke(10)
    drapiezniki = [Drapieznik(id=1, pozycja=(0, 0)), Drapieznik(id=2, pozycja=(0, 0)), Drapieznik(id=3, pozycja=(0, 0))]
    p.rozmieszcz_drapiezniki(drapiezniki)
    assert policz_drapiezniki(p) == 3

def test_rozmieszcz_drapiezniki_na_pustej_liscie():
    p = Pastwisko(5, 5)
    p.generuj_trawke(10)
    p.rozmieszcz_drapiezniki([])
    assert policz_drapiezniki(p) == 0





