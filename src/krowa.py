from src.zwierzeta import Zwierze


class Krowa(Zwierze):
    def __init__(self, imie: str, wiek: int, czy_zyje: bool):
        super().__init__(imie, wiek, czy_zyje)

        #Ustawienie poziomow glodu i stalych by zbalansowac przebieg symulacji

        self.poziom_glodu: int = 0
        self.max_dni_glodowania: int = 3
        self.dni_glodowania_z_rzedu: int = 0

    def aktualizuj_stan(self, czy_zjadla_trawe: bool) -> None:
        if not self.czy_zyje:
            return
        if czy_zjadla_trawe:
            self.poziom_glodu = 0
            self.dni_glodowania_z_rzedu = 0
        else:
            self.poziom_glodu += 1
            self.dni_glodowania_z_rzedu += 1

        if self.dni_glodowania_z_rzedu >= self.max_dni_glodowania:
            self.czy_zyje = False

