from src.zwierzeta.owca import Owca


class Jagnie(Owca):
    def __init__(self, id: int, pozycja: tuple[int, int], imie: str):
        super().__init__(id, pozycja, imie)
        self.symbol = "J"
        self.mlode = True  # jagnie jest mlode az dorosnie i zamieni sie w Owce

    # jagnie nie daje mleka az dorosnie (wtedy Farma zamienia je na Owce)
    def wartosc_produktu(self):
        return 0

    # gdy jagnie dorosnie, staje sie pelna owca z zachowanym stanem
    def stworz_dorosla_wersje(self):
        owca = Owca(self.id, self.pozycja, self.imie)
        return self._przekaz_stan(owca)
