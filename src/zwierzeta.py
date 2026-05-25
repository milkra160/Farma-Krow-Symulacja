class Zwierze:
    def __init__(self, imie : str, wiek : str, czy_zyje : bool):
        self.imie: str = imie
        self.wiek: int = wiek
        self.czy_zyje: bool = czy_zyje

    def starzej_sie(self) -> None:
        #zwieksza wiek zwierzecia o 1 jesli zyje
        if not self.czy_zyje:
            return
        self.wiek += 1





