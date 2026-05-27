from src.finanse import Finanse

def test_czy_barnkrut():
    f = Finanse()
    f.budzet = 0
    assert f.czy_bankrut()
