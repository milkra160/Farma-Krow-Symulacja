import random
from src.zwierzeta import Zwierze
from src.krowa import Krowa

class Morderca(Zwierze):
    def __init__(self,imie: str, wiek: int, czy_zyje: bool):
        super().__init__(imie, wiek, czy_zyje)
        self.szansa_pojawienia_sie_drapieznika: float = 0.15



