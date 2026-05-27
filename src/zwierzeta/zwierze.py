from abc import ABC, abstractmethod
# definiujemy klase abstrakcyjna zeby zapobiec tworzeniu obiektow z te klasy
# tworzymy abstrakcyjna metode odpowiadajaca za ruch by uniknac bladow w klasach dziedziczacych


class Zwierze(ABC):
    def __init__(self, id: int, pozycja: tuple[int,int]):
        self.id = id
        self.pozycja = pozycja  # pozycja w klasycznym ukladzie wspolrzednych X Y
        self.zyje = True
        self.symbol = (
            "?"  # Symbol bazowy. Ulatwia przyszle pisane kodu i konfiguralnosc
        )

    @abstractmethod
    def ruch(self):
        pass
