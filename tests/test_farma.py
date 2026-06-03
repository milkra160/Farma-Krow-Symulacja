from src.farma import Farma
from src.pastwisko.pastwisko import Pastwisko
from src.pogoda import Pogoda
from src.finanse import Finanse
from src.zdarzenia import ZdarzeniaLosoweMenadzer
from src.zwierzeta.krowa import Krowa


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


def test_dodaj_nowe_id():
    f = zrob_farme()
    assert f._nowe_id() == 1
    f.dodaj_zwierze(Krowa(id=1, pozycja=(0, 0), imie="A"))
    f.dodaj_zwierze(Krowa(id=5, pozycja=(0, 0), imie="B"))
    assert f._nowe_id() == 6


def test_czy_farma_jest_aktywna():
    f = zrob_farme()
    assert f.czy_aktywna() == True
    f.finanse.budzet = 0
    assert f.czy_aktywna() == False
