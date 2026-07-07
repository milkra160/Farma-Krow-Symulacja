from src.config import *


# klasa Finanse pilnuje budzetu farmy i zapisuje historie kazdego dnia
class Finanse:
    def __init__(self):
        self.budzet = BUDZET_START
        self.historia = []

    # rozlicza dobe: bilans = przychod - koszt, aktualizuje budzet i dopisuje do historii
    def rozlicz_dzien(self, przychod: float, koszt: float, dzien: int):
        bilans = przychod - koszt
        self.budzet += bilans

        # słownik służący do wyświetlania finansów pod koniec dnia
        stan_finansow = {
            "budzet": float(self.budzet),
            "przychod": float(przychod),
            "koszt": float(koszt),
            "bilans": float(bilans),
            "bankrut": self.czy_bankrut(),
        }

        self.historia.append({"dzien": dzien, "stan": stan_finansow})
        return stan_finansow

    # farma bankrutuje gdy budzet spadnie do zera lub ponizej
    def czy_bankrut(self) -> bool:
        return self.budzet <= 0

    # wydaje kase w sklepie. Zwraca True gdy sie udalo. Nie pozwalamy zejsc do zera
    # (to od razu oznaczaloby bankructwo), wiec wymagamy zeby cos zostalo w budzecie
    def wydaj(self, kwota: float) -> bool:
        if kwota >= self.budzet:
            return False
        self.budzet -= kwota
        return True
