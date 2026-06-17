import os
from src.ranking import Ranking


def wynik(nazwa, dni):
    return {
        "nazwa_farmy": nazwa,
        "data": "2026-06-08",
        "dni_przezycia": dni,
        "maks_budzet": 100,
        "maks_stado": 5,
        "powod_konca": "bankructwo",
        "parametry_start": {},
    }


def zrob_ranking():
    plik = "/tmp/ranking_test.json"
    if os.path.exists(plik):
        os.remove(plik)
    return Ranking(plik=plik)


def test_pusty_ranking_gdy_nie_ma_pliku():
    r = zrob_ranking()
    assert r.wczytaj_ranking() == []


def test_czy_dziala_zapis_i_sortowanie_malejaco():
    r = zrob_ranking()
    r.zapisz_wynik(wynik("pierwsza", 12))
    r.zapisz_wynik(wynik("druga", 46))
    r.zapisz_wynik(wynik("trzecia", 58))
    ranking = r.wczytaj_ranking()
    assert [w["dni_przezycia"] for w in ranking] == [58, 46, 12]
