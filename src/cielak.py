from src.krowa import Krowa

class Cielak(Krowa):
    def __init__(self, id: int, pozycja: tuple, imie: str):
        super().__init__(id, pozycja, imie)
        self.symbol = "c"

    #wartosc mleka to preludium do sensu symulacji, konfigurowanie tej metody bedzie w przyszlosci
    def wartosc_mleka(self):
        return 0