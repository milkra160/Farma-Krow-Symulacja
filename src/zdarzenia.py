from abc import ABC, abstractmethod
import random
from src import config


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
    def cofnij(self, farma) -> None:
        pass

    def __str__(self) -> str:
        return f"{self.nazwa} (pozostało: {self.dni_pozostale} dni)"

    # ZDARZENIA LOSOWE


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


# -------------------------------------------------------------


class NaglaSusza(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Nagła Susza ☀️"
        self.opis = "Liczba kępek trawy zmnniejszona o połowę na czas 3 dni"
        self.dni_trwania = 3
        self.oryginalna_baza = config.BAZA_KEPEK_TRAWY

    def czy_zachodzi(self, dzien: int) -> bool:
        return True

    def zastosuj(self, farma) -> str:
        self.oryginalna_baza = config.BAZA_KEPEK_TRAWY
        self.poprzedni_wymuszony = farma.pogoda.wymuszony_stan
        farma.pogoda.wymuszony_stan = "susza"
        config.BAZA_KEPEK_TRAWY = config.BAZA_KEPEK_TRAWY // 2
        return f"{self.nazwa} {self.opis}"

    def cofnij(self, farma) -> None:
        config.BAZA_KEPEK_TRAWY = self.oryginalna_baza
        farma.pogoda.wymuszony_stan = self.poprzedni_wymuszony



# --------------------------------------------------------------------


class Epidemia(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Epidemia 🦠"
        self.opis = "Wszystkie krowy tracą 30 pkt najedzenia natychmiast"
        self.dni_trwania = 1

    def czy_zachodzi(self, dzien: int) -> bool:
        return True

    def zastosuj(self, farma) -> str:
        for krowa in farma.stado:
            krowa.najedzenie -= 30
        return f"{self.nazwa} {self.opis}"

    def cofnij(self, farma) -> None:
        pass


# ----------------------------------------------------------------------


class Weterynarz(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Weterynarz 💉"
        self.opis = "Jedna losowa krowa odzyskuje pełne najedzenie"
        self.dni_trwania = 1

    def czy_zachodzi(self, dzien: int) -> bool:
        return True

    def zastosuj(self, farma) -> str:
        if farma.stado:
            krowa = random.choice(farma.stado)
            krowa.najedzenie = config.GLOD_START
            self.opis = f"Krowa {krowa.imie} odzyskuje pełne najedzenie"
        else:
            self.opis = "Brak krów do wyleczenia"
        return self.opis

    def cofnij(self, farma) -> None:
        pass


# --------------------------------------------------------------------


class MlekoGMO(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Pasza z GMO 🥛"
        self.opis = "Gospodarz nakarmił krowy zmodyfikowaną paszą i krowy zaczęły produkować więcej mleka: Przychód z mleka zwiększonyo 30% przez 5 dni"
        self.dni_trwania = 5
        self.oryginalny_przychod = config.PRZYCHOD_Z_KROWY

    def czy_zachodzi(self, dzien: int) -> bool:
        return True

    def zastosuj(self, farma) -> str:
        self.oryginalny_przychod = config.PRZYCHOD_Z_KROWY
        config.PRZYCHOD_Z_KROWY = config.PRZYCHOD_Z_KROWY * 1.3
        return f"{self.nazwa} {self.opis}"

    def cofnij(self, farma) -> None:
        config.PRZYCHOD_Z_KROWY = self.oryginalny_przychod


# --------------------------------------------------------------------


class Meteoryt(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Uderzenie Meteorytu ☄️"
        self.opis = "Meteoryt doszczętnie niszczy farmę. Koniec symulacji."
        self.dni_trwania = 1

    def czy_zachodzi(self, dzien: int) -> bool:
        return random.random() < 0.009

    def zastosuj(self, farma) -> str:
        farma.finanse.budzet = 0.0
        for krowa in farma.stado:
            krowa.zyje = False
            krowa.umarla_dzis = True
        return f"KATASTROFA! {self.nazwa}: {self.opis}"

    def cofnij(self, farma) -> None:
        pass


# -------------------------------------------------------------


class Wielkanoc(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Wielkanoc 🐣"
        self.opis = "Wydarzył się CUD! Jedna losowa martwa krowa zmartwychwstaje"
        self.dni_trwania = 1

    def czy_zachodzi(self, dzien: int) -> bool:
        return True

    def zastosuj(self, farma) -> str:
        if len(farma.cmentarz) > 0:
            wskrzeszona = random.choice(farma.cmentarz)
            farma.cmentarz.remove(wskrzeszona)
            wskrzeszona.zyje = True
            wskrzeszona.umarla_dzis = False
            wskrzeszona.zjadla_dzisiaj = False
            wskrzeszona.przypisana_kepka = None
            wskrzeszona.najedzenie = config.GLOD_START
            farma.stado.append(wskrzeszona)
            self.opis = f"Zmartwychwstała krowa {wskrzeszona.imie}!"
            return f"{self.nazwa}: {self.opis} ({wskrzeszona.imie} wraca do stada!)"
        else:
            self.opis = "Miał być cud, ale żadna krowa dotychczas nie umarła"
            return f"{self.nazwa}: {self.opis}"

    def cofnij(self, farma) -> None:
        pass


# -----------------------------------------------------------------


class UFO(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Inwazja UFO 👽"
        self.opis = (
            "Kosmici porywają jedną losową krowę, by przeprowadzić na niej eksperymenty"
        )
        self.dni_trwania = 1

    def czy_zachodzi(self, dzien: int) -> bool:
        return True

    def zastosuj(self, farma) -> str:
        zywe = []
        for krowa in farma.stado:
            if krowa.zyje == True:
                zywe.append(krowa)

        if len(zywe) > 0:
            porwana = random.choice(zywe)
            porwana.zyje = False
            porwana.umarla_dzis = True
            self.opis = f"Kosmici porwali krowę {porwana.imie}"
        else:
            self.opis = "Statek UFO przeleciał nad pustym pastwiskiem"
        return self.opis

    def cofnij(self, farma) -> None:
        pass


# ------------------------------------------------------------------------


class Lesniczy(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Wujek Leśniczy 🌲"
        self.opis = (
            "Wujek pilnuje pastwiska przez weekend. Brak drapieżników przez 3 dni"
        )
        self.dni_trwania = 3
        self.oryginalna_szansa = config.SZANSA_DRAPIEZNIK

    def czy_zachodzi(self, dzien: int) -> bool:
        return True

    def zastosuj(self, farma) -> str:
        self.oryginalna_szansa = farma.szansa_drapieznik
        farma.szansa_drapieznik = 0.0
        return f"{self.nazwa}: {self.opis}"

    def cofnij(self, farma) -> None:
        farma.szansa_drapieznik = self.oryginalna_szansa


# -------------------------------------------------------------------------


class PoraDeszczowa(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Pora Deszczowa 🌧️"
        self.opis = "Przez najbliższe 3 dni pogoda to wyłącznie deszcz"
        self.dni_trwania = 3
        self.oryginalne_stany = []

    def czy_zachodzi(self, dzien: int) -> bool:
        return True

    def zastosuj(self, farma) -> str:
        self.poprzedni_wymuszony = farma.pogoda.wymuszony_stan
        farma.pogoda.wymuszony_stan = "deszcz"
        return f"{self.nazwa}: {self.opis}"

    def cofnij(self, farma) -> None:
        farma.pogoda.wymuszony_stan = self.poprzedni_wymuszony


# --------------------------------------------------------------------


class ZazdrosnaKoza(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Zazdrosna Koza 🐐"
        self.opis = "Koza wstała wcześniej i zjadła całą trawę przed krowami: Brak trawy dzisiaj"
        self.dni_trwania = 1
        self.oryginalne_baza = config.BAZA_KEPEK_TRAWY

    def czy_zachodzi(self, dzien: int) -> bool:
        return True

    def zastosuj(self, farma) -> str:
        self.oryginalne_baza = config.BAZA_KEPEK_TRAWY
        config.BAZA_KEPEK_TRAWY = 0
        return f"{self.nazwa}: {self.opis}"

    def cofnij(self, farma) -> None:
        config.BAZA_KEPEK_TRAWY = self.oryginalne_baza


# --------------------------------------------------------------


class CudNadOdra(ZdarzenieLosoweBase):
    def __init__(self):
        super().__init__()
        self.nazwa = "Cud nad Odrą ✨"
        self.opis = "Losowa dorosła krowa natychmiastowo rodzi cielaka"
        self.dni_trwania = 1

    def czy_zachodzi(self, dzien: int) -> bool:
        return True

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

            imie = random.choice(config.IMIONA_KROW)
            nowy_cielak = Cielak(nowe_id, matka.pozycja, imie)
            farma.stado.append(nowy_cielak)
            farma.narodziny_dzis.append(imie)
            self.opis = f"Urodził się cielak {imie} (matka: {matka.imie})"
        else:
            self.opis = "Brak dorosłych krów zdolnych do nagłego porodu"
        return self.opis

    def cofnij(self, farma) -> None:
        pass

    # ----------------------------------------------------------------------------
    # menedzer zarzaca pula zdarzen losowych i cyklem zycia
    # pula to lista klas z ktorem losujemy i tworzymy obiekty


class ZdarzeniaLosoweMenadzer:
    def __init__(self, pula=None, szansa_zdarzenia: float = config.SZANSA_NA_ZDARZENIE):
        if pula is None:
            pula = [
                Walentynki,
                NaglaSusza,
                Epidemia,
                Weterynarz,
                Meteoryt,
                MlekoGMO,
                Wielkanoc,
                UFO,
                Lesniczy,
                PoraDeszczowa,
                ZazdrosnaKoza,
                CudNadOdra,
            ]
        self.pula = pula
        self.aktywne = []
        self.szansa_zdarzenia = szansa_zdarzenia

    def aktualizuj(self, farma, dzien: int) -> list:
        # odliczamy dni aktywnym. te ktore wygasly cofamy i usuwamy
        nadal_aktywne = []
        opisy = []
        for zdarzenie in self.aktywne:
            zdarzenie.dni_pozostale -= 1
            if zdarzenie.dni_pozostale <= 0:
                zdarzenie.cofnij(farma)
            else:
                nadal_aktywne.append(zdarzenie)
                opisy.append(f"{zdarzenie.nazwa} (pozostało {zdarzenie.dni_pozostale} dni)")
        self.aktywne = nadal_aktywne

        #czy trwa jakies dlugie zdarzenie
        trwa_dlugie = False
        for zdarzenia in self.aktywne:
            if zdarzenia.dni_trwania > 1:
                trwa_dlugie = True

        if random.random() < self.szansa_zdarzenia:
            nowe = random.choice(self.pula)()
            blokada = nowe.dni_trwania > 1 and trwa_dlugie
            if nowe.czy_zachodzi(dzien) and not blokada:
                nowe.dni_pozostale = nowe.dni_trwania
                nowe.zastosuj(farma)
                self.aktywne.append(nowe)
                opisy.append(f"{nowe.nazwa}: {nowe.opis}")

        return opisy
