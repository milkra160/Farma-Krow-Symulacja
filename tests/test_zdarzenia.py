from src.finanse import Finanse
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
class SztucznaFarma:
    def __init__(self, stado=None):
        self.stado = stado if stado is not None else []
        self.finanse = Finanse()
        self.pogoda = Pogoda()
        self.cmentarz = []
        self.do_wyleczenia = []
        self.narodziny_dzis = []
        self.zmartwychwstania_dzis = []
        self.szansa_drapieznik = config.SZANSA_DRAPIEZNIK
        self.antena_dni_pozostale = 0
        self.ostatnie_id = 0
        for k in self.stado:
            if k.id > self.ostatnie_id:
                self.ostatnie_id = k.id

    def _nowe_id(self):
        self.ostatnie_id += 1
        return self.ostatnie_id


# ******************** Walentynki
def test_czy_walentynki_zachodza_14_dnia():
    w = Walentynki()
    assert w.czy_zachodzi(14) == True
    assert w.czy_zachodzi(13) == False


def test_walentynki_zwiekszaja_i_cofaja_szanse_na_ciaze():
    sf = SztucznaFarma([])
    w = Walentynki()
    przed = config.SZANSA_NA_CIAZE
    w.zastosuj(sf)
    assert config.SZANSA_NA_CIAZE == przed * 1.5
    w.cofnij(sf)
    assert config.SZANSA_NA_CIAZE == przed


# **************** Nagla susza


def test_nagla_susza_zmniejsza_baze_trawy_i_wymusza_susze():
    sf = SztucznaFarma([])
    przed = config.BAZA_KEPEK_TRAWY
    n = NaglaSusza()
    n.zastosuj(sf)
    assert config.BAZA_KEPEK_TRAWY == przed // 2
    assert sf.pogoda.wymuszony_stan == "susza"
    n.cofnij(sf)
    assert config.BAZA_KEPEK_TRAWY == przed
    assert sf.pogoda.wymuszony_stan is None


# ************ Epidemia


def test_epidemia_zabiera_30_najdzeniea_wszystkim():
    k1 = Krowa(id=1, pozycja=(0, 0), imie="Bart")
    k2 = Krowa(id=2, pozycja=(0, 0), imie="Bart")
    k1.najedzenie = 100
    k2.najedzenie = 50
    Epidemia().zastosuj(SztucznaFarma([k1, k2]))
    assert k1.najedzenie == 70
    assert k2.najedzenie == 20


# ************** Weterynarz


def test_weterynarz_leczy_krowe_do_pelna():
    k = Krowa(id=1, pozycja=(0, 0), imie="Bart")
    k.najedzenie = 1
    sf = SztucznaFarma([k])
    Weterynarz().zastosuj(sf)
    assert k.najedzenie == config.GLOD_START
    assert k in sf.do_wyleczenia


def test_weterynarz_gdy_pusta_farma():
    wynik = Weterynarz().zastosuj(SztucznaFarma([]))
    assert isinstance(wynik, str)


def test_weterynarz_pomija_kury():
    from src.zwierzeta.kura import Kura

    kura = Kura(id=1, pozycja=(0, 0), imie="Gyra")
    sf = SztucznaFarma([kura])
    Weterynarz().zastosuj(sf)
    assert kura not in sf.do_wyleczenia  # kura nie glodnieje - weterynarz ja pomija


# ************ Mleko GMO


def test_mleko_GMO_zwieksza_i_cofa_przychod():
    sf = SztucznaFarma([])
    m = MlekoGMO()
    przed = config.PRZYCHOD_Z_KROWY
    m.zastosuj(sf)
    assert config.PRZYCHOD_Z_KROWY == przed * 1.3
    m.cofnij(sf)
    assert config.PRZYCHOD_Z_KROWY == przed


# ******* METEORYT


def test_meteoryt_zabija_krowy_i_zeruje_budzet():
    k1 = Krowa(id=1, pozycja=(0, 0), imie="Bart")
    k2 = Krowa(id=2, pozycja=(0, 0), imie="Bart")
    farma = SztucznaFarma([k1, k2])
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
    sf = SztucznaFarma([])
    sf.cmentarz.append(k)
    Wielkanoc().zastosuj(sf)
    assert k.zyje == True
    assert k.umarla_dzis == False
    assert k.najedzenie == config.GLOD_START
    assert k in sf.stado
    assert k not in sf.cmentarz


def test_wielkanoc_brak_martwych_krow_nic_nie_zmienia():
    sf = SztucznaFarma([Krowa(id=1, pozycja=(0, 0), imie="Bart")])
    wynik = Wielkanoc().zastosuj(sf)
    assert isinstance(wynik, str)


def test_wielkanoc_wskrzesza_kure_z_nowym_zyciem():
    from src.zwierzeta.kura import Kura

    k = Kura(id=1, pozycja=(0, 0), imie="Gyra")
    k.wiek = 99  # padla ze starosci
    k.zyje = False
    sf = SztucznaFarma([])
    sf.cmentarz.append(k)
    opis = Wielkanoc().zastosuj(sf)
    assert k.zyje is True
    assert k.wiek == 0  # zmartwychwstanie = nowy pelny cykl zycia
    assert "kura" in opis.lower()  # komunikat zgodny z gatunkiem, nie "krowa"


# ************** UFO


def test_czy_ufo_porywa_zywa_krowe():
    k = Krowa(id=1, pozycja=(0, 0), imie="Bart")
    UFO().zastosuj(SztucznaFarma([k]))
    assert k.umarla_dzis == True
    assert k.zyje == False


def test_brak_bledu_gdy_ufo_na_pustej_farmie():
    wynik = UFO().zastosuj(SztucznaFarma([]))
    assert isinstance(wynik, str)


def test_ufo_ucieka_gdy_trafi_na_kure():
    from src.zwierzeta.kura import Kura

    k = Kura(id=1, pozycja=(0, 0), imie="Gyra")
    opis = UFO().zastosuj(SztucznaFarma([k]))
    assert k.zyje is True  # kura nie porwana
    assert "dinozaur" in opis.lower()


def test_ufo_zablokowane_gdy_dziala_antena():
    sf = SztucznaFarma([])
    assert UFO().zablokowane(sf) is False  # brak anteny - UFO moze zajsc
    sf.antena_dni_pozostale = 3
    assert UFO().zablokowane(sf) is True  # antena dziala - UFO zablokowane


def test_menager_nie_dopuszcza_ufo_przy_antenie():
    # przy dzialajacej antenie UFO nie porywa krowy, a w opisach pada info o zaglusonym sygnale
    k = Krowa(id=1, pozycja=(0, 0), imie="Bart")
    sf = SztucznaFarma([k])
    sf.antena_dni_pozostale = 5
    m = ZdarzeniaLosoweMenadzer(pula=[UFO], szansa_zdarzenia=1.0)
    opisy = m.aktualizuj(sf, 1)
    assert k.zyje is True  # krowa nie porwana
    assert len(m.aktywne) == 0  # UFO nie stalo sie aktywnym zdarzeniem
    assert any("Antena" in o for o in opisy)


# ************ Lesniczy


def test_lesniczy_zeruje_i_cofa_szanse_na_drapieznika():
    sf = SztucznaFarma([])
    sf.szansa_drapieznik = 0.15
    l = Lesniczy()
    l.zastosuj(sf)
    assert sf.szansa_drapieznik == 0.0
    l.cofnij(sf)
    assert sf.szansa_drapieznik == 0.15


# ************* Pora deszczowa


def test_pora_deszczowa_ustawia_i_cofa_deszcz():
    sf = SztucznaFarma([])
    p = PoraDeszczowa()
    p.zastosuj(sf)
    assert sf.pogoda.wymuszony_stan == "deszcz"
    p.cofnij(sf)
    assert sf.pogoda.wymuszony_stan is None


# ****************** Zazdrosna koza


def test_zazdrosna_koza_zeruje_i_cofa_trawe():
    sf = SztucznaFarma([])
    z = ZazdrosnaKoza()
    przed = config.BAZA_KEPEK_TRAWY
    z.zastosuj(sf)
    assert config.BAZA_KEPEK_TRAWY == 0
    z.cofnij(sf)
    assert config.BAZA_KEPEK_TRAWY == przed


# **************** Cud nad Odra


def test_cud_nad_odra_rodzi_cielaka():
    matka = Krowa(id=1, pozycja=(0, 0), imie="Matka")
    matka.dorosla = True
    sf = SztucznaFarma([matka])
    CudNadOdra().zastosuj(sf)
    assert len(sf.stado) == 2
    assert isinstance(sf.stado[1], Cielak)


def test_cud_nad_odra_owca_rodzi_jagnie():
    from src.zwierzeta.owca import Owca
    from src.zwierzeta.jagnie import Jagnie

    matka = Owca(id=1, pozycja=(0, 0), imie="Bela")
    matka.dorosla = True
    sf = SztucznaFarma([matka])
    CudNadOdra().zastosuj(sf)
    assert len(sf.stado) == 2
    assert isinstance(sf.stado[1], Jagnie)  # owca rodzi jagnie, nie cielaka


def test_cud_nad_odra_gdy_brak_doroslych_krow_nic_nie_dodaje():
    mloda = Cielak(id=1, pozycja=(0, 0), imie="Mloda")
    sf = SztucznaFarma([mloda])
    wynik = CudNadOdra().zastosuj(sf)
    assert len(sf.stado) == 1
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
    assert any("Fake" in o for o in opisy)


def test_menager_nic_nie_robi_gdy_nic_nie_zaszlo():
    SztuczneZdarzenie.zaszlo = False
    m = ZdarzeniaLosoweMenadzer(pula=[SztuczneZdarzenie], szansa_zdarzenia=1.0)
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
