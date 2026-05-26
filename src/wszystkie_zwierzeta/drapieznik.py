from src.wszystkie_zwierzeta.zwierzeta import Zwierze
from src.wszystkie_zwierzeta.krowa import Krowa


# Wprowadzenie drapieznika balansuje przebieg symulacji przez ograniczenie rozrodu krow
class Drapieznik(Zwierze):
    def __init__(self, id: int, pozycja: tuple[int, int]):
        super().__init__(id, pozycja)
        self.symbol = "!"

    def czy_zabija(self, krowa: Krowa) -> bool:
        if krowa.pozycja == self.pozycja:
            krowa.zyje = False
            krowa.umarla_dzis = True
            return True
        return False

    def ruch(self):
        pass
