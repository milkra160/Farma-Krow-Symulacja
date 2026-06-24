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


def test_czy_nowe_id_jest_ciagle_nowe():
    f = zrob_farme()
    assert f._nowe_id() == 1
    assert f._nowe_id() == 2
    assert f._nowe_id() == 3


def test_czy_nowe_id_uwzglednia_stado_startowe():
    f = zrob_farme([Krowa(id=1, pozycja=(0, 0), imie="A"),
                    Krowa(id=5, pozycja=(0, 0), imie="B")])
    assert f._nowe_id() == 6  #licznik startuje od najwyzszego id w stadzie


def test_czy_farma_jest_aktywna():
    f = zrob_farme()
    assert f.czy_aktywna() == True
    f.finanse.budzet = 0
    assert f.czy_aktywna() == False


# tworzymy farme do testow
def stworz_farme(liczba_krow=3):
    stado = []
    for i in range(liczba_krow):
        stado.append(Krowa(id=i, pozycja=(0, 0), imie=f"K{i}"))
    return Farma(
        "Farma",
        Pastwisko(20, 20),
        Pogoda(),
        Finanse(),
        ZdarzeniaLosoweMenadzer(),
        stado,
    )


def test_czy_nowy_dzien_bedzie_zwiekszal_dzien():
    f = stworz_farme()
    log = f.nowy_dzien()
    assert f.dzien == 1
    assert log["dzien"] == 1


def test_czy_slownik_nowy_dzien_ma_klucze():
    f = stworz_farme()
    log = f.nowy_dzien()
    for klucz in [
        "dzien",
        "pogoda",
        "narodziny",
        "martwe",
        "powod_smierci",
        "zjadly",
        "drapiezniki",
        "stan_krow",
        "glodne",
        "kepki_trawy",
        "finanse",
        "zdarzenia",
    ]:
        assert klucz in log


def test_nowy_dzien_czy_pogoda_bedzie_poprawna():
    f = stworz_farme()
    log = f.nowy_dzien()
    assert log["pogoda"] in ("slonecznie", "deszcz", "susza")


def test_czy_nowy_dzien_dobrze_rozlicza_finanse():
    f = stworz_farme()
    log = f.nowy_dzien()
    finanse = log["finanse"]
    assert finanse["bilans"] == finanse["przychod"] - finanse["koszt"]


def test_nowy_dzien_dziala_dla_kilku_dni():
    f = stworz_farme()
    for _ in range(5):
        f.nowy_dzien()
    assert f.dzien == 5


def test_czy_nowy_dzien_zwraca_poprawny_log_krow():
    f = stworz_farme(liczba_krow=1)
    log = f.nowy_dzien()
    krowa_log = log["stan_krow"][0]
    for klucz in [
        "id",
        "imie",
        "pozycja_wizualna",
        "pozycja_kepki",
        "najedzenie",
        "wiek",
        "dorosla",
        "w_ciazy",
        "zjadla",
        "zyje",
        "umarla_dzis",
    ]:
        assert klucz in krowa_log
