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

# Stale dla owiec (dostepne wylacznie w sklepie)
# Owca wolniej glodnieje niz krowa (krowa traci 20/dzien), wiec zyje dluzej przy tej samej trawie.
OWCA_GLOD_DZIENNY_UBYTEK: int = 12
# Mleko owcze sprzedawane wprost jest malo warte - oplaca sie dopiero po przerobieniu na ser.
PRZYCHOD_Z_OWCY: int = 5
# Ser z mleka jednej owcy. Ma byc o 10 zl korzystniejszy od krowy (PRZYCHOD_Z_KROWY = 20).
PRZYCHOD_Z_SERA: int = 30
# Kociol serowarski potrzebuje tylu dni, by mleko owcze dojrzalo w ser.
KOCIOL_DNI_NA_SER: int = 3

# Stale dla kur (dostepne wylacznie w sklepie).
# Kura nie je trawy - karmi ja kurnik - za to jajka daja duzy staly przychod.
PRZYCHOD_Z_KURY: int = 40
# Kura zyje ustalona liczbe dni, potem pada ze starosci (nie z glodu).
KURA_DNI_ZYCIA: int = 7
# Kazda zywa kura jest glosna i wabi drapiezniki - podnosi szanse na drapieznika o tyle.
KURA_WZROST_SZANSY_DRAPIEZNIKA: float = 0.10

# sklep - ceny towarow
CENA_DOROSLEJ_KROWY: int = 200
CENA_CIELAKA: int = 100
CENA_DOROSLEJ_OWCY: int = 120
CENA_KURY: int = 160  # kura - znosi jajka przez KURA_DNI_ZYCIA dni
CENA_KOTLA: int = 600  # kociol serowarski - jeden na farme
CENA_PASZY: int = 40  # worek paszy dolewa najedzenia calemu stadu
PASZA_NAJEDZENIE: int = 40  # ile najedzenia dodaje jeden worek paszy
CENA_PLOTU: int = 150  # plot zmniejsza szanse na drapieznika przez kilka dni
PLOT_DNI_TRWANIA: int = 7  # ile dni stoi plot zanim sie zniszczy
PLOT_MNOZNIK_SZANSY: float = (
    0.25  # plot zostawia 25% szansy - reszta drapieznikow odpada
)

CENA_ANTENY: int = 180  # antena zaglaszajaca sygnal UFO
ANTENA_DNI_TRWANIA: int = 5  # przez tyle dni antena blokuje zdarzenie UFO

# sklep - wzrost ceny towaru po kazdym jego zakupie (balans - kolejne sztuki drozeja)
WZROST_CENY_KROWY: int = 20
WZROST_CENY_CIELAKA: int = 10
WZROST_CENY_OWCY: int = 15
WZROST_CENY_PASZY: int = 5
WZROST_CENY_PLOTU: int = 20
WZROST_CENY_ANTENY: int = 25
WZROST_CENY_KURY: int = 20
