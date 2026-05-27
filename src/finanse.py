
class Finanse:
    def __init__(self, budzet_start: float):
        self.budzet = budzet_start
        self.historia = []

    def rozlicz_dzien(self, przychod: float, koszt: float, dzien: int):
        bilans = przychod - koszt
        self.budzet += bilans

        #słownik służący do wyświetlania finansów pod koniec dnia
        stan_finansow = {
            "budzet": float(self.budzet),
            "przychod": float(przychod),
            "koszt": float(koszt),
            "blians": float(bilans),
            "bankrut": self.czy_bankrut()
        }

        self.historia.append({
            "dzien": dzien,
            "stan": stan_finansow
        })
        return stan_finansow

    def czy_bankrut(self) -> bool:
        return self.budzet <= 0
#test