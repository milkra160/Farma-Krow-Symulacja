# klasa Logger formatuje i drukuje dzienny log w terminalu


#kolory
CZERWONY = "\033[91m"
ZIELONY = "\033[92m"
ZOLTY = "\033[93m"
SZARY = "\033[90m"
RESET = "\033[0m"

def czerwony(tekst):
    return f"{CZERWONY}{tekst}{RESET}"

def zielony(tekst):
    return f"{ZIELONY}{tekst}{RESET}"

def zolty(tekst):
    return f"{ZOLTY}{tekst}{RESET}"

def szary(tekst):
    return f"{SZARY}{tekst}{RESET}"


class Logger:

    SZEROKOSC = 56 #szerokosc "logu dnia"

    def drukuj_log(self, log: dict):
        print()

        # naglowek dnia (wysrodkowany)
        naglowek = f" DZIEŃ {log['dzien']} | pogoda: {log['pogoda']}"
        print(zolty(naglowek.center(self.SZEROKOSC, "=")))

        # aktywne zdarzenia losowe (osobna sekcja)

        if len(log["zdarzenia"]) > 0:
            print(zolty("ZDARZENIA LOSOWE:"))
            for opis in log["zdarzenia"]:
                print(f" - {opis}")
        else:
            print(szary("ZDARZENIA LOSOWE: brak"))

        print(szary("-" * self.SZEROKOSC))

        # finanse (wyrownane w kolumnach)
        finanse = log["finanse"]
        print("FINANSE")
        print(f"   przychód: {finanse['przychod']:>8.0f}      koszt:  {finanse['koszt']:>8.0f}")
        print(f"   bilans:   {finanse['bilans']:>8.0f}      budżet: {finanse['budzet']:>8.0f}")
        print(szary("-" * self.SZEROKOSC))

        # STADO: narodziny/dorastanie/zgony

        if len(log["narodziny"]) > 0:
            print(zielony(f"   narodziny:  {', '.join(log['narodziny'])}"))
        if log.get("dorastanie") and len(log["dorastanie"]) > 0:
            print(f"   dorosły:    {', '.join(log['dorastanie'])}")
        if len(log["martwe"]) > 0:
            czesci = []
            for imie in log["martwe"]:
                czesci.append(f"{imie} ({log['powod_smierci'][imie]})")
            print(czerwony(f"   zgony:      {', '.join(czesci)}"))

        # statystyki stada

        ile_zjadlo = len(log["zjadly"])
        ile_glodnych = len(log["glodne"])
        rozmiar_stada = ile_zjadlo + ile_glodnych
        print(
            f"   razem: {rozmiar_stada} krów | "
            f"najedzonych: {ile_zjadlo} | głodnych: {ile_glodnych}"
        )
        print("=" * self.SZEROKOSC)

    def drukuj_podsumowanie_koncowe(self, dni: int, powod: str, finanse: dict):
        print() #linijka przerwy / estetyka
        print(czerwony("-" * 30))
        print(czerwony("KONIEC SYMULACJI"))
        print(czerwony(f"Powód zakończenia: {powod}"))
        print(czerwony(f"Liczba przetrwanych dni: {dni}"))
        print(czerwony(f"Końcowy budżet: {finanse['budzet']}"))
        print(czerwony("-" * 30))
