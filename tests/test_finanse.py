from src.config import BUDZET_START
from src.finanse import Finanse


def test_czy_barnkrut_gdy_zerowy_budzet():
    f = Finanse()
    f.budzet = 0
    assert f.czy_bankrut() == True

def test_czy_bankrut_gdy_budzet_ujemny():
    f = Finanse()
    f.budzet = -100
    assert f.czy_bankrut() == True

def test_czy_bankrut_gdy_budzet_dodatni():
    f = Finanse()
    f.budzet = 100
    assert f.czy_bankrut() == False

def test_czy_bankrut_slownik():
    f = Finanse()
    f.budzet = 0
    stan = f.rozlicz_dzien(0,50,1)
    assert stan["bankrut"] == True

def test_budzet_startowy():
    f = Finanse()
    assert f.budzet == BUDZET_START

def test_rozlicz_dzien_dla_zysku():
    f = Finanse()
    f.budzet = 100
    f.rozlicz_dzien(50,20,1)
    assert f.budzet == 130

def test_rozlicz_dzien_dla_straty():
    f = Finanse()
    f.budzet = 100
    f.rozlicz_dzien(10,40,1)
    assert f.budzet == 70

def test_rozlicz_dzien_zwroci_slownik():
    f = Finanse()
    f.budzet = 100
    stan = f.rozlicz_dzien(50,20,1)
    assert stan["przychod"] == 50
    assert stan["koszt"] == 20
    assert stan["bilans"] == 30
    assert stan["bankrut"] == False
    assert stan["budzet"] == 130

def test_rozlicz_dzien_zapisze_historie():
    f = Finanse()
    f.rozlicz_dzien(50,20,1)
    f.rozlicz_dzien(10,5,2)
    assert len(f.historia[0]["dzien"]) == 1
    assert len(f.historia[1]["dzien"]) == 2