import random
from src.zwierzeta.zwierze_hodowlane import ZwierzeHodowlane
from src.config import *
from src import config


class Krowa(ZwierzeHodowlane):
    def __init__(self, id: int, pozycja: tuple, imie: str):
        super().__init__(id, pozycja, imie)
        self.symbol = "K"

        # mechanika ciazy (specyficzna dla krowy)
        self.w_ciazy = False
        self.dni_do_porodu = 0

    # przychod krowy to mleko - tylko dorosla krowa je produkuje
    def wartosc_produktu(self) -> int:
        if self.dorosla:
            return int(config.PRZYCHOD_Z_KROWY)
        return 0

    # alias dla czytelnosci i zgodnosci ze starym kodem/testami (mleko to produkt krowy)
    def wartosc_mleka(self) -> int:
        return self.wartosc_produktu()

    # mechanika ciazy = balans symulacji
    def losuj_ciaze(self):
        if self.dorosla and not self.w_ciazy and self.najedzenie > 60:
            if random.random() < config.SZANSA_NA_CIAZE:
                self.w_ciazy = True
                self.dni_do_porodu = DNI_CIAZY

    # odliczamy dni do porodu; gdy dojdzie do 0 rodzi sie cielak (zwraca True)
    def aktualizuj_ciaze(self) -> bool:
        if self.w_ciazy:
            self.dni_do_porodu -= 1
            if self.dni_do_porodu == 0:
                self.w_ciazy = False
                return True  # udany porod
        return False
