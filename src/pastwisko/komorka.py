from src.zwierzeta import krowa
from src.zwierzeta.drapieznik import Drapieznik
from src.zwierzeta.krowa import Krowa


#komorka to jedno pole 2D pastwiskoa
#komorka moze miec w sobie trawe albo drapieznika


class Komorka:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.ma_trawke = False
        self.zajeta_przez = None
        self.ma_drapieznika = False
        self.drapieznik = None # Mozliwosc wywolania metody czy_zabija

    def dodaj_trawke(self):
        self.ma_trawke = True

    def czy_wolna(self)-> bool:
        if self.zajeta_przez is None:
            return True
        else:
            return False

    #krowa wchodzi na komorke. Zwracamy to co sie wydarzylo: smierc, zjadla trawe lub brak trawy
    def wejdz(self, krowa: Krowa) -> str:
        self.zajeta_przez = krowa
        krowa.przypisana_kepka = self #komorka

        if self.ma_drapieznika:
            self.drapieznik.czy_zabija(krowa)
            return "smierc"
        if self.ma_trawke:
            krowa.jedz()
            return "zjadla trawe"
        return "brak trawy"



