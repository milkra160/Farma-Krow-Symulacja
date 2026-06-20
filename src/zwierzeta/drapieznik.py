from src.zwierzeta.zwierze import Zwierze
from src.zwierzeta.krowa import Krowa


# Wprowadzenie drapieznika balansuje przebieg symulacji przez ograniczenie rozrodu krow
class Drapieznik(Zwierze):
    def __init__(self, id: int, pozycja: tuple[int, int]):
        super().__init__(id, pozycja)
        self.symbol = "!"

    def zaatakuj(self, krowa: Krowa) -> bool:
        krowa.zyje = False
        krowa.umarla_dzis = True
        return True

    def ruch(self):
        pass
