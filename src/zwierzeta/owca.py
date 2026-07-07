from src.zwierzeta.zwierze_hodowlane import ZwierzeHodowlane
from src.config import *
from src import config


# Owca dziala jak krowa (starzenie, glod, ciaza, jagnie), ale wolniej glodnieje i jej mleko jest
# malo warte. Oplaca sie dopiero z kotlem serowarskim, ktory przerabia mleko owcze na ser.
# Owce zdobywa sie wylacznie w sklepie (nie ma ich w stadzie startowym).
class Owca(ZwierzeHodowlane):
    gatunek = "owca"
    glod_dzienny_ubytek = OWCA_GLOD_DZIENNY_UBYTEK

    def __init__(self, id: int, pozycja: tuple, imie: str):
        super().__init__(id, pozycja, imie)
        self.symbol = "O"

    # bez kotla mleko owcze sprzedajemy wprost za niewielkie pieniadze; z kotlem trafia na ser
    def wartosc_produktu(self) -> int:
        if self.dorosla:
            return int(config.PRZYCHOD_Z_OWCY)
        return 0

    # tylko dorosla owca daje mleko, ktore kociol serowarski moze przerobic na ser
    def produkuje_mleko_owcze(self) -> bool:
        return self.dorosla

    # potomkiem owcy jest jagnie (import lokalny, bo jagnie dziedziczy po owcy)
    def stworz_mlode(self, id: int, pozycja: tuple, imie: str):
        from src.zwierzeta.jagnie import Jagnie

        return Jagnie(id=id, pozycja=pozycja, imie=imie)
