from src.pogoda import Pogoda
from src.config import MNOZNIK_DESZCZ, MNOZNIK_SUSZA, MNOZNIK_SLONCE


def test_pogoda_startuje_slonecznie():
    p = Pogoda()
    assert p.aktualny_stan_pogody == "slonecznie"


def test_nowy_dzien_zwraca_jeden_z_trzech_stanow():
    p = Pogoda()
    stan = p.nowy_dzien()
    assert stan in ("slonecznie", "deszcz", "susza")


def test_mnoznik_deszcz():
    p = Pogoda()
    p.poprzedni_stan_pogody = "deszcz"
    assert p.mnoznik_trawy() == MNOZNIK_DESZCZ


def test_mnoznik_susza():
    p = Pogoda()
    p.poprzedni_stan_pogody = "susza"
    assert p.mnoznik_trawy() == MNOZNIK_SUSZA


def test_mnoznik_slonce():
    p = Pogoda()
    p.poprzedni_stan_pogody = "slonecznie"
    assert p.mnoznik_trawy() == MNOZNIK_SLONCE
