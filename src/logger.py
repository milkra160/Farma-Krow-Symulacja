# klasa Logger formatuje i drukuje dzienny log w terminalu

SZEROKOSC = 56
# kolory
CZERWONY = "\033[91m"
ZIELONY = "\033[92m"
ZOLTY = "\033[93m"
SZARY = "\033[90m"
ROZOWY = "\033[95m"
NIEBIESKI = "\033[96m"
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

def niebieski(tekst):
    return f"{NIEBIESKI}{tekst}{RESET}"

def naglowek(tytul):
    return zolty(f" {tytul} ".center(SZEROKOSC, "="))

def linia():
    return szary("-" * SZEROKOSC)


class Logger:
    SZEROKOSC = 56  # szerokosc "logu dnia"

    def drukuj_log(self, log: dict):
        print()

        # naglowek dnia (wysrodkowany)
        # naglowek dnia (wspolny styl)
        print(zolty(naglowek(f"DZIEŃ {log['dzien']} | pogoda: {log['pogoda']}")))

        # aktywne zdarzenia losowe (osobna sekcja)

        if len(log["zdarzenia"]) > 0:
            print(zolty("ZDARZENIA LOSOWE:"))
            for opis in log["zdarzenia"]:
                print(f" - {opis}")
        else:
            print(szary("ZDARZENIA LOSOWE: brak"))

        print(szary("-" * self.SZEROKOSC))

        # iloesc kepek trawy
        ile_kepek = len(log["kepki_trawy"])
        print(f"KĘPKI TRAWY: {ile_kepek}")
        print(szary("-" * self.SZEROKOSC))

        # finanse (wyrownane w kolumnach)
        finanse = log["finanse"]
        print("FINANSE:")
        print(
            f"   przychód: {finanse['przychod']:>8.0f}      koszt:  {finanse['koszt']:>8.0f}"
        )

        bilans = finanse["bilans"]
        if bilans >= 0:
            zmiana = wyblakly_zielony(f"(+{bilans:.0f})")
        else:
            zmiana = wyblakly_czerwony(f"({bilans:.0f})")

        print(
            f"   bilans:   {bilans:>8.0f}      budżet: {finanse['budzet']:>8.0f} {zmiana}"
        )
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

        if log.get("zmartwychwstania") and len(log["zmartwychwstania"]) > 0:
            print(niebieski(f"   zmartwychwstanie: {', '.join(log['zmartwychwstania'])}"))

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
        # aktualnie zywe krowy z paskiem najedzenia
        zywe = []
        for k in log["stan_krow"]:
            if k["zyje"]:
                zywe.append(k)

        if len(zywe) > 0:
            print(szary("-" * self.SZEROKOSC))
            print("ŻYWE KROWY:")
            for k in zywe:
                symbol = "K"
                if k["symbol"] == "c":
                    symbol = "c"
                print(
                    f"   {symbol} {k['imie']:<12} {self._pasek_glodu(k['najedzenie'])} {k['najedzenie']:>3}/100"
                )
        print("=" * self.SZEROKOSC)

    # rysuje pasek najedzenia krowy (0-100), kolor zalezy od poziomu glodu
    def _pasek_glodu(self, najedzenie: int) -> str:
        dlugosc = 10
        pelne = najedzenie * dlugosc // 100  #ile kratek wypelnic(najedzenie 0-100)
        if pelne > dlugosc:
            pelne = dlugosc
        if pelne < 0:
            pelne = 0
        puste = dlugosc - pelne
        pasek = "\u2588" * pelne + "\u2591" * puste

        if najedzenie >= 60:
            return zielony(pasek)
        elif najedzenie >= 30:
            return zolty(pasek)
        else:
            return czerwony(pasek)

    def drukuj_podsumowanie_koncowe(self, dni: int, powod: str, finanse: dict):
        print()
        print(naglowek("KONIEC SYMULACJI"))
        print(f"   powód zakończenia:  {powod}")
        print(f"   przetrwane dni:     {dni}")
        print(f"   końcowy budżet:     {finanse['budzet']:.0f} zł")
        print("=" * SZEROKOSC)

    def drukuj_statystyki(self, s: dict):
        print()  # pusta linia dla estetyki
        print(czerwony("=== STATYSTYKI KOŃCOWE ==="))
        print(f"Łączne narodziny:   {s['narodziny']}")
        print(f"Łączne zmartwychwstania: {s['zmartwychwstania']}")
        print(f"Łączne zgony:       {s['zgony']}")
        print(f"Krów łącznie na farmie: {s['wszystkie_krowy']}")
        print(f"Maksmalne stado: {s['maks_stado']} krów (dzień {s['maks_stado_dzien']})")
        print(f"Zdarzenia losowe:   {s['zdarzenia']}")
        print(linia())
        print(
            f"Pogoda: słońce {s['dni_slonca']} / deszcz {s['dni_deszczu']} / susza {s['dni_suszy']}"
        )
        print(
            f"Finanse: przychód {s['suma_przychodow']:.0f} zł, "
            f"koszt {s['suma_kosztow']:.0f} zł, "
            f"budżet końcowy {s['budzet_koncowy']:.0f} zł"
        )
        print("=" * SZEROKOSC)