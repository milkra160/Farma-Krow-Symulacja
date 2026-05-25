#Testy dla klasy Zwierzeta
from src.zwierzeta import Zwierze
def test_zwierze_starzeje_sie_gdy_zyje():
    zwierze = Zwierze("Marek",5,True)
    zwierze.starzej_sie()
    assert zwierze.wiek == 6