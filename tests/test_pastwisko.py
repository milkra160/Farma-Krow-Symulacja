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
    p.pobierz_komorke(0, 0).wejdz(k)
    p.wyczysc()
    assert p.pobierz_komorke(0, 0).czy_wolna() == True


def test_czy_wyczysc_usuwa_drapiezniki():
    p = Pastwisko(5, 5)
    k = p.pobierz_komorke(0, 0)
    k.ma_drapieznika = True
    k.drapieznik = Drapieznik(id=89, pozycja=(0, 0))
    p.wyczysc()
    assert p.pobierz_komorke(0, 0).ma_drapieznika == False
    assert p.pobierz_komorke(0, 0).drapieznik is None


# funkcja poomcnicza do testow
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
    drapiezniki = [
        Drapieznik(id=1, pozycja=(0, 0)),
        Drapieznik(id=2, pozycja=(0, 0)),
        Drapieznik(id=3, pozycja=(0, 0)),
    ]
    p.rozmieszcz_drapiezniki(drapiezniki)
    assert policz_drapiezniki(p) == 3


def test_rozmieszcz_drapiezniki_na_pustej_liscie():
    p = Pastwisko(5, 5)
    p.generuj_trawke(10)
    p.rozmieszcz_drapiezniki([])
    assert policz_drapiezniki(p) == 0


# funkcja pomocnica
def zajmij(p, x, y):
    p.pobierz_komorke(x, y).wejdz(Krowa(id=1, pozycja=(0, 0), imie="X"))


def test_czy_losuj_sasiada_zwraca_wolnego_sasiada():
    p = Pastwisko(5, 5)
    wynik = p._losuj_sasiada(2, 2)
    assert wynik in [(2, 1), (3, 2), (2, 3), (1, 2)]


def test_czy_losuj_sasiada_pomija_zajete_pola():
    p = Pastwisko(5, 5)
    zajmij(p, 2, 1)  # gora
    zajmij(p, 2, 3)  # dol
    zajmij(p, 1, 2)  # lewo
    assert p._losuj_sasiada(2, 2) == (3, 2)  # jedyny wolny (prawo)


def test_cz_losuj_sasiada_brak_wolnych_miejsc_zwraca_ta_sama_kepke():
    p = Pastwisko(5, 5)
    zajmij(p, 2, 1)
    zajmij(p, 2, 3)
    zajmij(p, 1, 2)
    zajmij(p, 3, 2)
    assert p._losuj_sasiada(2, 2) == (2, 2)


def test_czy_losuj_sasiada_nie_wychodzi_poza_plansze():
    p = Pastwisko(5, 5)
    wynik = p._losuj_sasiada(0, 0)
    assert wynik in [(1, 0), (0, 1)]


def test_przypisz_krowy_daje_jesc_zywym_krowom():
    p = Pastwisko(5, 5)
    p.generuj_trawke(10)
    k1 = Krowa(id=1, pozycja=(0, 0), imie="X")
    k2 = Krowa(id=2, pozycja=(0, 0), imie="Y")
    p.przypisz_krowy([k1, k2])
    assert k1.przypisana_kepka is not None
    assert k2.przypisana_kepka is not None
    assert k1.zjadla_dzisiaj == True
    assert k2.zjadla_dzisiaj == True


def test_przypisz_krowy_gdy_jest_malo_kepek():
    p = Pastwisko(5, 5)
    p.generuj_trawke(1)
    k1 = Krowa(id=1, pozycja=(0, 0), imie="X")
    k2 = Krowa(id=2, pozycja=(0, 0), imie="Y")
    p.przypisz_krowy([k1, k2])
    ile_zjadlo = 0
    if k1.zjadla_dzisiaj:
        ile_zjadlo += 1
    if k2.zjadla_dzisiaj:
        ile_zjadlo += 1
    assert ile_zjadlo == 1


def test_przypisz_krowy_co_pozycja_wizualna_na_planszy():
    p = Pastwisko(5, 5)
    p.generuj_trawke(5)
    krowy = []
    for i in range(8):  # wiecej krow niz kepek
        krowy.append(Krowa(id=i, pozycja=(0, 0), imie="X"))
    p.przypisz_krowy(krowy)
    for k in krowy:  # kazda krowa musi miec swoje miejsce na planszy
        x, y = k.pozycja_wizualna
        assert 0 <= x < 5  # zakres planszy
        assert 0 <= y < 5


def test_przypisz_krowy_pomija_martwe_krowy():
    p = Pastwisko(5, 5)
    p.generuj_trawke(5)
    martwa = Krowa(id=1, pozycja=(0, 0), imie="X")
    martwa.zyje = False
    p.przypisz_krowy([martwa])
    assert martwa.przypisana_kepka is None
    assert martwa.zjadla_dzisiaj == False


def test_przypisz_krowy_gdy_krowa_ginie_od_drapieznika():
    p = Pastwisko(5, 5)
    p.generuj_trawke(1)
    kepka = p.kepki_z_trawa()[0]
    kepka.ma_drapieznika = True
    kepka.drapieznik = Drapieznik(id=6, pozycja=(kepka.x, kepka.y))
    krowa = Krowa(id=1, pozycja=(0, 0), imie="X")
    p.przypisz_krowy([krowa])
    assert krowa.zyje == False
    assert krowa.umarla_dzis == True
