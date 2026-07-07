from src.zwierzeta.krowa import Krowa


class Cielak(Krowa):
    def __init__(self, id: int, pozycja: tuple[int, int], imie: str):
        super().__init__(id, pozycja, imie)
        self.symbol = "c"
        self.mlode = True  # cielak jest mlody az dorosnie i zamieni sie w Krowe

    # Cielak nie produkuje mleka az dorosnie (wtedy Farma zamienia go na Krowe)
    def wartosc_produktu(self):
        return 0

    # gdy cielak dorosnie, staje sie pelna krowa z zachowanym stanem
    def stworz_dorosla_wersje(self):
        krowa = Krowa(self.id, self.pozycja, self.imie)
        return self._przekaz_stan(krowa)
