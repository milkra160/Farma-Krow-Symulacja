#Testy dla klasy Zwierzeta
from src.zwierzeta import Zwierze
def test_zwierze_starzeje_sie_gdy_zyje():
    zwierze = Zwierze("Marek",5,True)
    zwierze.starzej_sie()
    assert zwierze.wiek == 6

def test_zwierze_nie_starzeje_sie_gdy_jest_martwe():
    zwierze = Zwierze("Czarek",8,False)
    zwierze.starzej_sie()
    assert zwierze.wiek == 8

#testy dla klasy Krowa
from src.krowa import Krowa
def test_krowa_zwieksza_glod_gdy_nie_zje_trawy():
    krowa = Krowa("Marek",3,True)
    krowa.aktualizuj_stan(False)
    assert krowa.poziom_glodu == 1
    assert krowa.dni_glodowania_z_rzedu == 1
    assert krowa.czy_zyje == True

def test_krowa_zeruje_glod_gdy_zje_trawe():
    krowa = Krowa("Marek",3,True)
    krowa.poziom_glodu = 2
    krowa.dni_glodowania_z_rzedu = 2
    krowa.aktualizuj_stan(True)

    assert krowa.poziom_glodu == 0
    assert krowa.dni_glodowania_z_rzedu == 0
    assert krowa.czy_zyje == True

def test_krowa_umiera_gdy_gloduje_3_dni():
    krowa = Krowa("Marek",3,True)
    krowa.dni_glodowania_z_rzedu = 2
    krowa.aktualizuj_stan(False)
    assert krowa.czy_zyje == False
