from src.zwierzeta.zwierze_hodowlane import ZwierzeHodowlane
from src.config import *
from src import config


# Kura rozni sie od krowy i owcy: nie pasie sie na trawie (karmi ja kurnik), za to chodzi po
# planszy, znosi jajka o duzej stalej wartosci i zyje z gory ustalona liczbe dni. Ginie WYLACZNIE
# ze starosci - zdarzenia moga ja atakowac, ale nie zabija. Kury zdobywa sie tylko w sklepie
# i sie nie rozmnazaja (pole dorosla zostaje False).
class Kura(ZwierzeHodowlane):
    gatunek = "kura"

    def __init__(self, id: int, pozycja: tuple, imie: str):
        super().__init__(id, pozycja, imie)
        self.symbol = "h"  # litera na planszy (kura), litera h calkiem przypomina kure, sa nogi jest szyja

    # kura nie je trawy - karmi sie z kurnika, wiec nie zajmuje kepek (ale chodzi po planszy)
    def je_trawe(self) -> bool:
        return False

    # jajka to staly przychod, niezalezny od trawy (dziala dopoki kura zyje)
    def wartosc_produktu(self) -> int:
        return int(config.PRZYCHOD_Z_KURY)

    # kura ginie wylacznie ze starosci - czyli dopiero gdy przekroczy swoj wiek zycia.
    # Kazda inna "smierc" (od zdarzenia) jest cofana przez Farme.
    def smierc_dozwolona(self) -> bool:
        return self.wiek > config.KURA_DNI_ZYCIA

    # kura nie umiera z glodu (karmi ja kurnik) - zyje ustalona liczbe dni, potem pada ze starosci
    def starzej_sie_smierc_glodowa_doroslosc(self):
        self.wiek += 1
        if self.wiek > config.KURA_DNI_ZYCIA:
            self.zyje = False
            self.umarla_dzis = True
