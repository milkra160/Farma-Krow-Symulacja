# ***Stale dla calej symulacji***
ROZMIAR_PLANSZY: tuple[int, int] = (20, 20)
MAX_DNI: int = 100
SZANSA_NA_ZDARZENIE: float = 0.10


# Stale dla zwierzat
GLOD_START: int = 100
GLOD_DZIENNY_UBYTEK: int = 20
GLOD_Z_JEDZENIA: int = 30

WIEK_DOROSLOSCI: int = 10
SZANSA_NA_CIAZE: float = 0.08
DNI_CIAZY: int = 7

PRZYCHOD_Z_KROWY: int = 20

SZANSA_DRAPIEZNIK: float = 0.15
MAKS_DRAPIEZNIKOW: int = 2

IMIONA_KROW: list = [
    "Łaciata",
    "Bogdan",
    "Zbys",
    "Cecylia",
    "Jakub",
    "Marek",
    "Zuzanna",
    "Anna",
    "Karol",
    "Karolina",
]


# Stale pogoda i pastwisko
MNOZNIK_DESZCZ: float = 1.2
MNOZNIK_SUSZA: float = 0.8
MNOZNIK_SLONCE: float = 1.0

BAZA_KEPEK_TRAWY: int = 12

# finanse
BUDZET_START: float = 500
KOSZT_DZIENNY_FARMY: int = 50
