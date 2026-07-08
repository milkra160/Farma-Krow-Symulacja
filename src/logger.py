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

        # twoje dzialania: zakupy zrobione w sklepie + status plotu
        zakupy = log.get("zakupy", [])
        if len(zakupy) > 0 or log.get("plot_zniszczony"):
            print(zielony("TWOJE DZIAŁANIA:"))
            for zakup in zakupy:
                print(f"   🛒 {zakup}")
            if log.get("plot_zniszczony"):
                print(czerwony("   🚧 Płot się zniszczył!"))
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

        # kociol serowarski - ile mleka owczego dodano dzis, ile sera powstalo i ile sera dojrzeje
        # nastepnego dnia (mleko dojrzewa w ser z opoznieniem)
        kociol = log.get("kociol")
        if kociol and kociol["aktywny"]:
            print("KOCIOŁ SEROWARSKI:")
            if kociol["ser_dzis"] > 0:
                print(zielony(f"   ser gotowy dzisiaj: +{kociol['ser_dzis']} zł"))
            if kociol["mleko_dzis"] > 0:
                print(f"   mleko owcze dodane do kotła: {kociol['mleko_dzis']}")
            if kociol["ser_jutro"] > 0:
                print(f"   ser gotowy jutro: +{kociol['ser_jutro']} zł")
            if kociol["partie_w_kotle"] == 0 and kociol["ser_dzis"] == 0:
                print(szary("   kocioł pusty — czeka na mleko owcze"))
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
            print(
                niebieski(f"   zmartwychwstanie: {', '.join(log['zmartwychwstania'])}")
            )

        # statystyki stada
        if log.get("ciaze") and len(log["ciaze"]) > 0:
            print(rozowy(f"   ciąża:      {', '.join(log['ciaze'])}"))

        # osobne tabele dla krow i owiec - ta sama forma, kazdy gatunek liczony niezaleznie
        self._sekcja_gatunku(log, "krowa", "ŻYWE KROWY")
        self._sekcja_gatunku(log, "owca", "ŻYWE OWCE")
        if log.get("kurnik_zniknal"):
            print(szary("Kurnik opustoszał — padła ostatnia kura"))
        self._sekcja_kury(log)
        print("=" * self.SZEROKOSC)

    # wypisuje jeden gatunek: licznik najedzonych/glodnych + tabele zywych z paskiem najedzenia.
    # Ta sama forma dla krow i owiec - rozdzielamy je po polu "gatunek" ze stanu zwierzat.
    def _sekcja_gatunku(self, log: dict, gatunek: str, tytul: str):
        zwierzeta = [k for k in log["stan_krow"] if k.get("gatunek") == gatunek]
        if len(zwierzeta) == 0:
            return
        zywe = [k for k in zwierzeta if k["zyje"]]
        najedzone = sum(1 for k in zywe if k["zjadla"])
        glodne = len(zywe) - najedzone
        print(szary("-" * self.SZEROKOSC))
        print(f"{tytul}: {len(zywe)} | najedzonych: {najedzone} | głodnych: {glodne}")
        for k in zywe:
            print(
                f"   {k['symbol']} {k['imie']:<12} {self._pasek_glodu(k['najedzenie'])} {k['najedzenie']:>3}/100"
            )

    # osobna sekcja dla kur: nie maja paska glodu (kurnik je karmi), wiec zamiast najedzenia
    # pokazujemy ile z ustalonej dlugosci zycia juz uplynelo - widac, ktora kura zaraz padnie
    def _sekcja_kury(self, log: dict):
        kury = [k for k in log["stan_krow"] if k.get("gatunek") == "kura"]
        if len(kury) == 0:
            return
        zywe = [k for k in kury if k["zyje"]]
        dni_zycia = log.get("kura_dni_zycia", 7)
        print(szary("-" * self.SZEROKOSC))
        print(f"ŻYWE KURY: {len(zywe)}  (kurnik czynny)")
        for k in zywe:
            print(f"   \U0001F414 {k['imie']:<12} wiek {k['wiek']}/{dni_zycia} dni")

    # rysuje pasek najedzenia krowy (0-100), kolor zalezy od poziomu glodu
    def _pasek_glodu(self, najedzenie: int) -> str:
        dlugosc = 10
        pelne = najedzenie * dlugosc // 100  # ile kratek wypelnic(najedzenie 0-100)
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
        print(
            f"Maksmalne stado: {s['maks_stado']} zwierząt (dzień {s['maks_stado_dzien']})"
        )
        print(
            f"Stado na koniec: {s['krowy_koncowe']} krów | "
            f"{s['owce_koncowe']} owiec | {s['kury_koncowe']} kur"
        )
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
        print(linia())
        print(
            f"Zakupy w sklepie: zwierzęta {s['kupione_zwierzeta']}, "
            f"worki paszy {s['kupione_pasze']}, "
            f"ulepszenia {s['kupione_ulepszenia']}"
        )
        print("=" * SZEROKOSC)
