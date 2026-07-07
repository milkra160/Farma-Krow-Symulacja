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
    # męskie
    "Bogdan",
    "Tomasz",
    "Krzysztof",
    "Stanisław",
    "Henryk",
    "Janusz",
    "Andrzej",
    "Michał",
    "Piotr",
    "Ryszard",
    "Marek",
    "Jakub",
    "Karol",
    "Maciej",
    "Wojciech",
    "Dariusz",
    "Grzegorz",
    "Jerzy",
    "Włodzimierz",
    "Tadeusz",
    # żeńskie
    "Anna",
    "Barbara",
    "Katarzyna",
    "Krystyna",
    "Maria",
    "Jolanta",
    "Elżbieta",
    "Teresa",
    "Jadwiga",
    "Zuzanna",
    "Karolina",
    "Cecylia",
    "Magdalena",
    "Agnieszka",
    "Dorota",
    "Krystyna",
    "Halina",
    "Danuta",
    "Irena",
    "Urszula",
]


# Stale pogoda i pastwisko
MNOZNIK_DESZCZ: float = 1.2
MNOZNIK_SUSZA: float = 0.8
MNOZNIK_SLONCE: float = 1.0

BAZA_KEPEK_TRAWY: int = 12

# finanse
BUDZET_START: float = 500
KOSZT_DZIENNY_FARMY: int = 50

# sklep - ceny towarow
CENA_DOROSLEJ_KROWY: int = 200
CENA_CIELAKA: int = 100
CENA_PASZY: int = 40  # worek paszy dolewa najedzenia calemu stadu
PASZA_NAJEDZENIE: int = 40  #ile najedzenia dodaje jeden worek paszy
CENA_PLOTU: int = 150  # plot zmniejsza szanse na drapieznika przez kilka dni
PLOT_DNI_TRWANIA: int = 7  #ile dni stoi plot zanim sie zniszczy
PLOT_MNOZNIK_SZANSY: float = 0.25  # plot zostawia 25% szansy - reszta drapieznikow odpada
