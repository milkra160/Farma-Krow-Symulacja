from src.zwierzeta import Zwierze


class Krowa(Zwierze):
    def __init__(self, imie: str, wiek: int, czy_zyje: bool):
        super().__init__(imie, wiek, czy_zyje)

        self.poziom_glodu: int = 0
        self.max_dni_glodowania: int = 3
        self.dni_glodowania_z_rzedu: int = 0


        #krowa bedzie jeść