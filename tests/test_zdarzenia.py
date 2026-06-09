from src import config
from src.pogoda import Pogoda
from src.zwierzeta.krowa import Krowa
from src.zwierzeta.cielak import Cielak
from src.zdarzenia import (
    Walentynki,
    NaglaSusza,
    Epidemia,
    Weterynarz,
    Meteoryt,
    MlekoGMO,
    Wielkanoc,
    UFO,
    Lesniczy,
    PoraDeszczowa,
    ZazdrosnaKoza,
    CudNadOdra,
    ZdarzeniaLosoweMenadzer,
    ZdarzenieLosoweBase,
)


# ****************** Sztuczne klasy
class Sztuczne_finanse:
    def __init__(self):
        self.budzet = 100


class Sztuczna_farma:
    def __init__(self, stado=None):
        self.stado = (
            stado if stado is not None else []
        )  # jesli lista jest wez ja, jesli nie stworz pusta
        self.finanse = Sztuczne_finanse
        self.pogoda = Pogoda


# ******************** Walentynki
def test_czy_walentynki_zachodza_14_dnia():
    w = Walentynki()
    assert w.czy_zachodzi(14) == True
    assert w.czy_zachodzi(13) == False


def test_walentynki_zwiekszaja_i_cofaja_szanse_na_ciaze():
    w = Walentynki()
    przed = config.SZANSA_NA_CIAZE
    w.zastosuj(None)
    assert config.SZANSA_NA_CIAZE == przed * 1.5
    w.cofnij(None)
    assert config.SZANSA_NA_CIAZE == przed


# **************** Nagla susza


def test_nagla_zusza_mnozy_razy_pol_baze_trawy_i_cofa():
    n = NaglaSusza()
    przed = config.BAZA_KEPEK_TRAWY
    n.zastosuj(None)
    assert config.BAZA_KEPEK_TRAWY == przed * 0.5
    n.cofnij(None)
    assert config.BAZA_KEPEK_TRAWY == przed


# ************ Epidemia


def test_epidemia_zabiera_30_najdzeniea_wszystkim():
    k1 = Krowa(id=1, pozycja=(0, 0), imie="Bart")
    k2 = Krowa(id=2, pozycja=(0, 0), imie="Bart")
    k1.najedzenie = 100
    k2.najedzenie = 50
    Epidemia().zastosuj(Sztuczna_farma([k1, k2]))
    assert k1.najedzenie == 70
    assert k2.najedzenie == 20


# ************** Weterynarz


def test_weterynarz_leczy_krowe_do_pelna():
    k = Krowa(id=1, pozycja=(0, 0), imie="Bart")
    k.najedzenie = 1
    Weterynarz().zastosuj(Sztuczna_farma([k]))
    assert k.najedzenie == config.GLOD_START


def test_weterynarz_gdy_pusta_farma():
    wynik = Weterynarz().zastosuj(Sztuczna_farma([]))
    assert isinstance(wynik, str)


# ************ Mleko GMO


def test_mleko_GMO_zwieksza_i_cofa_przychod():
    m = MlekoGMO()
    przed = config.PRZYCHOD_Z_KROWY
    m.zastosuj(None)
    assert config.PRZYCHOD_Z_KROWY == przed * 1.3
    m.cofnij(None)
    assert config.PRZYCHOD_Z_KROWY == przed


# ******* METEORYT


def test_meteoryt_zabija_krowy_i_zeruje_budzet():
    k1 = Krowa(id=1, pozycja=(0, 0), imie="Bart")
    k2 = Krowa(id=2, pozycja=(0, 0), imie="Bart")
    farma = Sztuczna_farma([k1, k2])
    farma.finanse.budzet = 500
    Meteoryt().zastosuj(farma)
    assert farma.finanse.budzet == 0
    assert k1.zyje == False
    assert k2.zyje == False


# +++++++++++ wielkanoc


def test_czy_wielkanoc_wskrzesza_martwa_krowe():
    k = Krowa(id=1, pozycja=(0, 0), imie="Bart")
    k.zyje = False
    k.umarla_dzis = True
    k.najedzenie = 5
    Wielkanoc().zastosuj(Sztuczna_farma([k]))
    assert k.umarla_dzis == False
    assert k.zyje == True
    assert k.najedzenie == config.GLOD_START


def test_wielkanoc_brak_martwych_krow_nic_nie_zmienia():
    k = Krowa(id=1, pozycja=(0, 0), imie="Bart")
    wynik = Wielkanoc().zastosuj(Sztuczna_farma([k]))
    assert isinstance(wynik, str)
    assert k.zyje == True


# ************** UFO


def test_czy_ufo_porywa_zywa_krowe():
    k = Krowa(id=1, pozycja=(0, 0), imie="Bart")
    UFO().zastosuj(Sztuczna_farma([k]))
    assert k.umarla_dzis == True
    assert k.zyje == False


def test_brak_bledu_gdy_ufo_na_pustej_farmie():
    wynik = UFO().zastosuj(Sztuczna_farma([]))
    assert isinstance(wynik, str)


# ************ Lesniczy


def test_lesniczy_eruje_i_cofa_szanse_na_drapieznika():
    l = Lesniczy()
    przed = config.SZANSA_DRAPIEZNIK
    l.zastosuj(None)
    assert config.SZANSA_DRAPIEZNIK == 0
    l.cofnij(None)
    assert config.SZANSA_DRAPIEZNIK == przed


# ************* Pora deszczowa


def test_pora_deszczowa_ustawia_i_cofa_deszcz():
    farma = Sztuczna_farma([])
    oryginal = farma.pogoda.STANY_POGODY
    p = PoraDeszczowa()
    p.zastosuj(farma)
    assert farma.pogoda.STANY_POGODY == ("deszcz",)  # krotka
    assert farma.pogoda.aktualny_stan_pogody == "deszcz"
    p.cofnij(farma)
    assert farma.pogoda.STANY_POGODY == oryginal


# ****************** Zazdrosna koza


def test_zazdrosna_koza_zeruje_i_cofa_trawe():
    z = ZazdrosnaKoza()
    przed = config.BAZA_KEPEK_TRAWY
    z.zastosuj(None)
    assert config.BAZA_KEPEK_TRAWY == 0
    z.cofnij(None)
    assert config.BAZA_KEPEK_TRAWY == przed


# **************** Cud nad Odra


def test_cud_nad_odra_rodzi_cielaka():
    matka = Krowa(id=1, pozycja=(0, 0), imie="Matka")
    matka.dorosla = True
    farma = Sztuczna_farma([matka])
    CudNadOdra().zastosuj(farma)
    assert len(farma.stado) == 2
    assert isinstance(farma.stado[1], Cielak)


def test_cud_nad_odra_gdy_brak_doroslych_krow_nic_nie_dodaje():
    mloda = Cielak(id=1, pozycja=(0, 0), imie="Mloda")
    farma = Sztuczna_farma([mloda])
    wynik = CudNadOdra().zastosuj(farma)
    assert len(farma.stado) == 1
    assert isinstance(wynik, str)

    # **********************************


class SztuczneZdarzenie(ZdarzenieLosoweBase):
    zaszlo = True

    def __init__(self):
        super().__init__()
        self.nazwa = "fake"
        self.opis = "Fake"
        self.dni_trwania = 2
        self.zastosowano = False
        self.cofnieto = False

    def czy_zachodzi(self, dzien: int):
        return SztuczneZdarzenie.zaszlo

    def zastosuj(self, farma):
        self.zastosowano = True
        return self.opis

    def cofnij(self, farma):
        self.cofnieto = True


def test_menager_aktywuje_zdarzenie():
    SztuczneZdarzenie.zaszlo = True
    m = ZdarzeniaLosoweMenadzer(pula=[SztuczneZdarzenie], szansa_zdarzenia=1.0)
    opisy = m.aktualizuj(None, 1)
    assert len(m.aktywne) == 1
    assert m.aktywne[0].zastosowano == True
    assert "Fake" in opisy


def test_menager_nic_nie_robi_gdy_nic_nie_zaszlo():
    SztuczneZdarzenie.zaszlo = False
    m = ZdarzeniaLosoweMenadzer(pula=[SztuczneZdarzenie])
    opisy = m.aktualizuj(None, 1)
    assert len(m.aktywne) == 0
    assert opisy == []


def test_menager_wygasza_cofa():
    SztuczneZdarzenie.zaszlo = True
    m = ZdarzeniaLosoweMenadzer(pula=[SztuczneZdarzenie], szansa_zdarzenia=1.0)
    m.aktualizuj(None, 1)  # aktywuje dni_pozostale = 2
    z = m.aktywne[0]
    SztuczneZdarzenie.zaszlo = False  # zeby nie aktywowac kolejmych
    m.aktualizuj(None, 2)  # w do 1, nadal aktywne
    assert len(m.aktywne) == 1
    m.aktualizuj(None, 3)  # 1 do 0, cofnij usun
    assert len(m.aktywne) == 0
    assert z.cofnieto == True
