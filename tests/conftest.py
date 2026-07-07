import pytest
from src import config


# Zdarzenia losowe mutuja stale w globalnym module config (np. MlekoGMO zmienia PRZYCHOD_Z_KROWY,
# NaglaSusza BAZA_KEPEK_TRAWY, Walentynki SZANSA_NA_CIAZE) i cofaja to dopiero, gdy zdarzenie
# wygasnie. Test, ktory skonczy sie z aktywnym zdarzeniem, zostawia zmutowana stala i psuje kolejne
# testy. Ta fikstura robi migawke prostych stalych configu przed kazdym testem i przywraca je po
# nim, dzieki czemu testy sa od siebie niezalezne bez wzgledu na kolejnosc uruchomienia.
@pytest.fixture(autouse=True)
def przywroc_stale_configu():
    migawka = {
        nazwa: wartosc
        for nazwa, wartosc in vars(config).items()
        if nazwa.isupper() and isinstance(wartosc, (int, float))
    }
    yield
    for nazwa, wartosc in migawka.items():
        setattr(config, nazwa, wartosc)
