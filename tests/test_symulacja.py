import io
import os
from contextlib import redirect_stdout
from src.symulacja import Symulacja
from src.ranking import Ranking
from src.wizualizacja import Wizualizacja


def parametry(max_dni=5, krowy=4, budzet=1000.0):
    return {
        "nazwa_farmy": "Test",
        "liczba_krow_start": krowy,
        "budzet_start": budzet,
        "szansa_drapieznik": 0.0,  # wylaczamy losowosc na potrzeby testu
        "maks_drapieznikow": 1,
        "max_dni": max_dni,
        "szansa_zdarzenia": 0.0,
    }


def zrob_symulacje():
    s = Symulacja()
    s.wizualizacja = Wizualizacja(kolory=False)
    plik = "/tmp/ranking_symulacja_test.json"
    if os.path.exists(plik):
        os.remove(plik)
    s.ranking = Ranking(plik=plik)
    return s


def start_symulacji(s):  # pomocnik przechodzi po calej symulacji i nie zasmieca ekranu
    s.tryb_auto = True
    wyjscie = io.StringIO()
    with redirect_stdout(wyjscie):
        s.petla_glowna()


def test_czy_symulacja_konczy_sie_po_uplywie_czasu():
    s = zrob_symulacje()
    s._przygotuj(parametry(max_dni=5))
    start_symulacji(s)
    assert s.farma.dzien == 5
    wyniki = s.ranking.wczytaj_ranking()
    assert len(wyniki) == 1
    assert wyniki[0]["powod_konca"] == "uplynal czas"


def test_czy_bankructwo_konczy_symulacje():
    s = zrob_symulacje()
    s._przygotuj(parametry(max_dni=100, krowy=0, budzet=60.0))
    start_symulacji(s)
    assert s.farma.finanse.czy_bankrut()
    assert s.ranking.wczytaj_ranking()[0]["powod_konca"] == "bankructwo"


def test_czy_uruchom_dzien_zwiekszy_dzien():
    s = zrob_symulacje()
    s._przygotuj(parametry(max_dni=100))
    wyjscie = io.StringIO()
    with redirect_stdout(wyjscie):
        dalej = s.uruchom_dzien()
    assert s.farma.dzien == 1
    assert dalej == True
