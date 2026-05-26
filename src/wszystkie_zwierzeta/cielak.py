from src.wszystkie_zwierzeta.krowa import Krowa

class Cielak(Krowa):
    def __init__(self, id: int, pozycja: tuple, imie: str):
        super().__init__(id, pozycja, imie)
        self.symbol = "c"

    #wartosc mleka to preludium do sensu symulacji, konfigurowanie tej metody bedzie w przyszlosci
    #Cielak nie produkuje mleka
    def wartosc_mleka(self):
        return 0

    