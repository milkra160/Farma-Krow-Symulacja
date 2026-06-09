from src.wizualizacja import Wizualizacja
from src.pastwisko.pastwisko import Pastwisko


def stworz_plansze_i_log():
    p = Pastwisko(5, 5)
    p.pobierz_komorke(1, 1).dodaj_trawke()
    p.pobierz_komorke(3, 2).ma_drapieznika = True
    log = {
        "stan_krow": [
            {"pozycja_wizualna": (0, 0), "zyje": True, "zjadla": True, "symbol": "K"},
            {"pozycja_wizualna": (2, 4), "zyje": True, "zjadla": False, "symbol": "K"},
            {"pozycja_wizualna": (4, 4), "zyje": False, "zjadla": False, "symbol": "K"},
        ],
    }
    return p, log


def test_czy_plansza_ma_ramke_i_wymiary():
    p, log = stworz_plansze_i_log()
    linie = Wizualizacja(kolory=False)._zbuduj_plansze(p, log).split("\n")
    assert len(linie) == 7  # 5 rzedow i 2 ramki
    assert linie[0] == "+-----+"
    assert linie[-1] == "+-----+"


def test_czy_symbole_na_planszy_sa_poprawne():
    p, log = stworz_plansze_i_log()
    linie = Wizualizacja(kolory=False)._zbuduj_plansze(p, log).split("\n")
    assert linie[1][1] == "K"
    assert linie[2][2] == "T"
    assert linie[3][4] == "!"
    assert linie[5][5] == "K"
