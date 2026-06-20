# klasa Logger formatuje i drukuje dzienny log w terminalu


#kolory
CZERWONY = "\033[91m"
ZIELONY = "\033[92m"
ZOLTY = "\033[93m"
SZARY = "\033[90m"
ROZOWY = "\033[95m"
RESET = "\033[0m"
WYBLAKLY_ZIELONY = "\033[2;32m"
WYBLAKLY_CZERWONY = "\033[2;31m"


def wyblakly_zielony(tekst):
    return f"{WYBLAKLY_ZIELONY}{tekst}{RESET}"

def wyblakly_czerwony(tekst):
    return f"{WYBLAKLY_CZERWONY}{tekst}{RESET}"

def czerwony(tekst):
    return f"{CZERWONY}{tekst}{RESET}"

def zielony(tekst):
    return f"{ZIELONY}{tekst}{RESET}"

def zolty(tekst):
    return f"{ZOLTY}{tekst}{RESET}"

def szary(tekst):
    return f"{SZARY}{tekst}{RESET}"

def rozowy(tekst):
    return f"{ROZOWY}{tekst}{RESET}"


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

        #iloesc kepek trawy
        ile_kepek = len(log["kepki_trawy"])
        print(f"KĘPKI TRAWY: {ile_kepek}")
        print(szary("-" * self.SZEROKOSC))

        # finanse (wyrownane w kolumnach)
        finanse = log["finanse"]
        print("FINANSE:")
        print(f"   przychód: {finanse['przychod']:>8.0f}      koszt:  {finanse['koszt']:>8.0f}")

        bilans = finanse["bilans"]
        if bilans >= 0:
            zmiana = wyblakly_zielony(f"(+{bilans:.0f})")
        else:
            zmiana = wyblakly_czerwony(f"({bilans:.0f})")

        print(f"   bilans:   {bilans:>8.0f}      budżet: {finanse['budzet']:>8.0f} {zmiana}")
        print(szary("-" * self.SZEROKOSC))

        # STADO: narodziny/dorastanie/zgony

        if len(log["narodziny"]) > 0:
            print(zielony(f"   narodziny:  {', '.join(log['narodziny'])}"))
        if log.get("dorastanie") and len(log["dorastanie"]) > 0:
            print(f"   stała się dziś dorosła:    {', '.join(log['dorastanie'])}")
        if len(log["martwe"]) > 0:
            czesci = []
            for imie in log["martwe"]:
                czesci.append(f"{imie} ({log['powod_smierci'][imie]})")
            print(czerwony(f"   zgony:      {', '.join(czesci)}"))

        # statystyki stada
        if log.get("ciaze") and len(log["ciaze"]) > 0:
            print(rozowy(f"   ciąża:      {', '.join(log['ciaze'])}"))
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

    def drukuj_statystyki(self, s: dict):
        print()  # pusta linia dla estetyki
        print(czerwony("=== STATYSTYKI KOŃCOWE ==="))
        print(f"Łączne narodziny:   {s['narodziny']}")
        print(f"Łączne zgony:       {s['zgony']}")
        print(f"Zdarzenia losowe:   {s['zdarzenia']}")
        print(f"Pogoda: słońce {s['dni_slonca']} / deszcz {s['dni_deszczu']} / susza {s['dni_suszy']}")
        print(
            f"Finanse: przychód {s['suma_przychodow']:.0f} zł, "
            f"koszt {s['suma_kosztow']:.0f} zł, "
            f"budżet końcowy {s['budzet_koncowy']:.0f} zł"
        )