from src.zwierzeta.krowa import Krowa


class Cielak(Krowa):
    def __init__(self, id: int, pozycja: tuple[int, int], imie: str):
        super().__init__(id, pozycja, imie)
        self.symbol = "c"

    # Cielak nie produkuje mleka az dorosnie (wtedy Farma zamienia go na Krowe)
    def wartosc_produktu(self):
        return 0
