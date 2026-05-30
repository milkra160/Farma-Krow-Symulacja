
from abc import ABC, abstractmethod
import random
import config

class ZdarzenieLosoweBase(ABC):
    def __init__(self):
        self.nazwa = ""
        self.opis = ""
        self.dni_trwania = 1
        self.dni_pozostale = 0


    @abstractmethod
    def czy_zachodzi(self, dzien: int) -> bool:
        pass

    @abstractmethod
    def zastosuj(self, farma) -> str:
        pass

    @abstractmethod
    def cofnij (self, farma) -> None:
        pass

    def __str__(self) -> str:
        return f"{self.nazwa} (pozostało: {self.dni_pozostale} dni)"

    #ZDARZENIA LOSOWE

class Walentynki(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Walentynki 💘"
        self.opis = "Szansa na ciążę +50% przez 1 dzień"
        self.dni_trwania = 1
        self.oryginalna_szansa = config.SZANSA_NA_CIAZE

    def czy_zachodzi(self, dzien: int) -> bool:
        return dzien == 14

    def zastosuj(self, farma) -> str:
        self.oryginalna_szansa = config.SZANSA_NA_CIAZE
        config.SZANSA_NA_CIAZE *= 1.5
        return f"{self.nazwa} {self.opis}"

    def cofnij(self, farma) -> None:
        config.SZANSA_NA_CIAZE = self.oryginalna_szansa
#-------------------------------------------------------------

class NaglaSusza(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Nagła Susza ☀️"
        self.opis = "Liczba kępek trawy zmnniejszona o połowę na czas 3 dni"
        self.dni_trwania = 3
        self.oryginalna_baza = config.BAZA_KEPEK_TRAWY

    def czy_zachodzi(self, dzien: int) -> bool:
        return random.random() < 0.05

    def zastosuj(self, farma) -> str:
        self.oryginalna_baza = config.BAZA_KEPEK_TRAWY
        config.BAZA_KEPEK_TRAWY = config.BAZA_KEPEK_TRAWY // 2
        return f"{self.nazwa} {self.opis}"

    def cofnij(self, farma) -> None:
        config.BAZA_KEPEK_TRAWY = self.oryginalna_baza

#--------------------------------------------------------------------

class Epidemia(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Epidemia 🦠"
        self.opis = "Wszystkie krowy tracą 30 pkt najedzenia natychmiast"
        self.dni_trwania = 1

    def czy_zachodzi(self, dzien: int) -> bool:
        return random.random() < 0.05

    def zastosuj(self, farma) -> str:
        for krowa in farma.stado:
            krowa.najedzenie -= 30
        return f"{self.nazwa} {self.opis}"

    def cofnij(self, farma) -> None:
        pass

#----------------------------------------------------------------------

class Weterynarz(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Weterynarz 💉"
        self.opis = "Jedna losowa krowa odzyskuje pełne najedzenie"
        self.dni_trwania = 1

    def czy_zachodzi(self, dzien: int) -> bool:
        return random.random() < 0.05

    def zastosuj(self, farma) -> str:
        if farma.stado:
            krowa = random.choice(farma.stado)
            krowa.najedzenie = config.GLOD_START
            return f"{self.nazwa}: {self.opis} ({krowa.imie})"
        else:
            return f"{self.nazwa}: Brak krów do wyleczenia"

    def cofnij(self, farma) -> None:
        pass

#--------------------------------------------------------------------

class MlekoGMO(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Pasza z GMO 🥛"
        self.opis = "Gospodarz nakarmił krowy zmodyfikowaną paszą i krowy zaczęły produkować więcej mleka: Przychód z mleka zwiększonyo 30% przez 5 dni"
        self.dni_trwania = 5
        self.oryginalny_przychod = config.PRZYCHOD_Z_KROWY

    def czy_zachodzi(self, dzien: int) -> bool:
        return random.random() < 0.05

    def zastosuj(self, farma) -> str:
        self.oryginalny_przychod = config.PRZYCHOD_Z_KROWY
        config.PRZYCHOD_Z_KROWY = config.PRZYCHOD_Z_KROWY * 1.3
        return f"{self.nazwa} {self.opis}"

    def cofnij(self, farma) -> None:
        config.PRZYCHOD_Z_KROWY = self.oryginalny_przychod

#--------------------------------------------------------------------

class Meteoryt(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Uderzenie Meteorytu ☄️"
        self.opis = "Meteoryt doszczętnie niszczy farmę. Koniec symulacji."
        self.dni_trwania = 1

    def czy_zachodzi(self, dzien: int) -> bool:
        return random.random() < 0.001

    def zastosuj(self, farma) -> str:
        farma.finanse.budzet = 0.0
        for krowa in farma.stado:
            krowa.zyje = False
            krowa.umarla_dzis = True
        return f"KATASTROFA! {self.nazwa}: {self.opis}"

    def cofnij(self, farma) -> None:
        pass

#-------------------------------------------------------------

class Wielkanoc(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Wielkanoc 🐣"
        self.opis = "Wydarzył się CUD! Jedna losowa martwa krowa zmartwychwstaje"
        self.dni_trwania = 1

    def czy_zachodzi(self, dzien: int) -> bool:
        return random.random() < 0.04

    def zastosuj(self, farma) -> str:
        martwe = []
        for krowa in farma.stado:
            if krowa.zyje == False:
                martwe.append(krowa)

        if len(martwe) > 0:
            wskrzeszona = random.choice(martwe)
            wskrzeszona.zyje = True
            wskrzeszona.umarla_dzis = False
            wskrzeszona.najedzenia = config.GLOD_START
            return f"{self.nazwa}: {self.opis} ({wskrzeszona.imie} wraca do stada!)"

        return  f"{self.nazwa}: Miał dokonać się cud, ale żadna krowa dotychczas nie umarła."

    def cofnij(self, farma) -> None:
        pass

#-----------------------------------------------------------------

class UFO(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Inwazja UFO 👽"
        self.opis = "Kosmici porywają jedną losową krowę, by przeprowadzić na niej eksperymenty"
        self.dni_trwania = 1

    def czy_zachodzi(self, dzien: int) -> bool:
        return random.random() < 0.06

    def zastosuj(self, farma) -> str:
        zywe = []
        for krowa in farma.stado:
            if krowa.zyje == True:
                zywe.append(krowa)

        if len(zywe) > 0:
            porwana = random.choice(zywe)
            porwana.zyje = False
            porwana.umarla_dzis = True
            return f"{self.nazwa}: {self.opis} ({porwana.imie} zniknęła w snopie światła)"

        return f"{self.nazwa}: Statek UFO przeleciał nad pustym pastwiskiem."

    def cofnij(self, farma) -> None:
        pass

#------------------------------------------------------------------------

class Lesniczy(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Wujek Leśniczy 🌲"
        self.opis = "Wujek pilnuje pastwiska przez weekend. Brak drapieżników przez 3 dni"
        self.dni_trwania = 3
        self.oryginalna_szansa = config.SZANSA_DRAPIEZNIK

    def czy_zachodzi(self, dzien: int) -> bool:
        return random.random() < 0.05

    def zastosuj(self, farma) -> str:
        self.oryginalna_szansa = config.SZANSA_DRAPIEZNIK
        config.SZANSA_DRAPIEZNIK = 0.0
        return f"{self.nazwa}: {self.opis}"

    def cofnij(self, farma) -> None:
        config.SZANSA_DRAPIEZNIK = self.oryginalna_szansa

#-------------------------------------------------------------------------

class PoraDeszczowa(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Pora Deszczowa 🌧️"
        self.opis = "Przez najbliższe 3 dni pogoda to wyłącznie deszcz"
        self.dni_trwania = 3
        self.oryginalne_stany = []

    def czy_zachodzi(self, dzien: int) -> bool:
        return random.random() < 0.05

    def zastosuj(self, farma) -> str:
        self.oryginalne_stany = list(farma.pogoda.STANY_POGODY)
        farma.pogoda.STANY_POGODY = ("deszcz",)
        farma.pogoda.aktualny_stan_pogody = "deszcz"
        return f"{self.nazwa}: {self.opis}"

    def cofnij(self, farma) -> None:
        farma.pogoda.STANY_POGODY = tuple(self.oryginalne_stany)

#--------------------------------------------------------------------

class ZazdrosnaKoza(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Zazdrosna Koza 🐐"
        self.opis = "Koza wstała wcześniej i zjadła całą trawę przed krowami: Brak trawy dzisiaj"
        self.dni_trwania = 1
        self.oryginalne_baza = config.BAZA_KEPEK_TRAWY
        
    def czy_zachodzi(self, dzien: int) -> bool:
        return random.random() < 0.05
    
    def zastosuj(self, farma) -> str:
        self.oryginalne_baza = config.BAZA_KEPEK_TRAWY
        config.BAZA_KEPEK_TRAWY = 0
        return f"{self.nazwa}: {self.opis}"
    
    def cofnij(self, farma) -> None:
        config.BAZA_KEPEK_TRAWY = self.oryginalne_baza
        
#--------------------------------------------------------------

class CudNadOdra(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Cud nad Odrą ✨"
        self.opis = "Losowa dorosła krowa natychmiastowo rodzi cielaka"
        self.dni_trwania = 1

    def czy_zachodzi(self, dzien: int) -> bool:
        return random.random() < 0.04

    def zastosuj(self, farma) -> str:
        dorosle = []
        for krowa in farma.stado:
            if krowa.zyje == True and krowa.dorosla == True:
                dorosle.append(krowa)

        if len(dorosle) > 0:
            matka = random.choice(dorosle)
            from src.zwierzeta.cielak import Cielak

            nowe_id = 1
            najwieksze_id = 0
            if len(farma.stado) > 0:
                for k in farma.stado:
                    if k.id > najwieksze_id:
                        najwieksze_id = k.id
                nowe_id = najwieksze_id + 1

            nowy_cielak = Cielak(nowe_id, matka.pozycja, f"Cielak_{nowe_id}")
            farma.stado.append(nowy_cielak)
            return f"{self.nazwa}: {self.opis} (Matka: {matka.imie})"

        return f"{self.nazwa}: Brak dorosłych krów zdolnych do nagłego porodu"

    def cofnij(self, farma) -> None:
        pass