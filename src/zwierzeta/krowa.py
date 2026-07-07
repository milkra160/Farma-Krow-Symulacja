from src.zwierzeta.zwierze_hodowlane import ZwierzeHodowlane
from src import config


class Krowa(ZwierzeHodowlane):
    gatunek = "krowa"

    def __init__(self, id: int, pozycja: tuple, imie: str):
        super().__init__(id, pozycja, imie)
        self.symbol = "K"

    # przychod krowy to mleko - tylko dorosla krowa je produkuje
    def wartosc_produktu(self) -> int:
        if self.dorosla:
            return int(config.PRZYCHOD_Z_KROWY)
        return 0

    # alias dla czytelnosci i zgodnosci ze starym kodem/testami (mleko to produkt krowy)
    def wartosc_mleka(self) -> int:
        return self.wartosc_produktu()

    # potomkiem krowy jest cielak (import lokalny, bo cielak dziedziczy po krowie)
    def stworz_mlode(self, id: int, pozycja: tuple, imie: str):
        from src.zwierzeta.cielak import Cielak

        return Cielak(id=id, pozycja=pozycja, imie=imie)
