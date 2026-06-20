import json
import os


# szablon dla kolorów do późniejszego wyświetlania by ułatwić pisanie kodu
ZIELONY = "\033[92m"
ZOLTY = "\033[93m"
RESET = "\033[0m"


# szablon dla wyświetlania rankingu w formie estetycznej tabeli
_SZABLON = (
    "{lp:<4}{nazwa:<13}{seed:<8}{dni:<5}"
    "{budzet_maks:<12}{stado_maks:<11}{krowy:<6}"
    "{budzet_st:<11}{drap:<6}{koniec:<13}"
)


def _klucz_sortowania(wynik: dict):
    return (
        wynik["dni_przezycia"],
        wynik["maks_budzet"],
        wynik["maks_stado"],
    )


# klasa ranking zapisuje wynik symulacji do pliku json i odczytuje je
class Ranking:
    def __init__(self, plik: str = "ranking.json"):
        self.plik = plik

    def wyswietl_kryteria(self):  # kryteria sortowania rankingu
        print()
        print(ZIELONY + "=== JAK OCENIAMY WYNIK (kryteria rankingu) ===" + RESET)
        print("Najlepszy wynik ustalamy po kolei wedlug:")
        print("  1. Liczba przezytych dni  (im wiecej, tym lepiej)")
        print("  2. Przy remisie: maksymalny budzet  (im wiecej, tym lepiej)")
        print("  3. Przy dalszym remisie: maksymalne stado")
        print(
            "Uwaga: uczciwe porownanie konfiguracji ma sens tylko w obrebie tego samego seeda."
        )

    def wczytaj_ranking(self) -> list:
        # zabezpieczenie. Jak nie ma pliku zwracamy pusta liste
        if not os.path.exists(self.plik):
            return []
        try:
            with open(self.plik, "r", encoding="utf-8") as f:
                dane = json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []
        if not isinstance(dane, list):
            return []
        # sortujemy malejaco po dniach przezycia
        dane.sort(key=_klucz_sortowania, reverse=True)
        return dane

    def zapisz_wynik(self, wynik: dict):
        ranking = self.wczytaj_ranking()  # to co juz mamy znajduje sie w pliku
        ranking.append(wynik)  # dodajemy nowy wynik
        ranking.sort(key=_klucz_sortowania, reverse=True)
        with open(self.plik, "w", encoding="utf-8") as f:
            json.dump(ranking, f, ensure_ascii=False, indent=2)

    # wyciaga seed z parametrow startowych danego wyniku (moze byc None)
    def _seed_wyniku(self, wynik: dict):
        return wynik.get("parametry_start", {}).get("seed")

    # buduje kolorowy naglowek tabeli rankingu
    def _naglowek_tabeli(self):
        tekst = _SZABLON.format(
            lp="Lp.",
            nazwa="Farma",
            seed="Seed",
            dni="Dni",
            budzet_maks="Budzet maks",
            stado_maks="Stado maks",
            krowy="Krowy",
            budzet_st="Budzet st.",
            drap="Drap.",
            koniec="Koniec",
        )
        linia = "-" * len(tekst)
        return ZOLTY + tekst + RESET + "\n" + linia

        # jeden wiersz tabeli

    def _wiersz(self, miejsce: int, wynik: dict) -> str:
        p = wynik.get("parametry_start", {})
        return _SZABLON.format(
            lp=f"{miejsce}.",
            nazwa=str(wynik["nazwa_farmy"])[:15],
            seed=str(self._seed_wyniku(wynik)),
            dni=str(wynik["dni_przezycia"]),
            budzet_maks=str(wynik["maks_budzet"]),
            stado_maks=str(wynik["maks_stado"]),
            krowy=str(p.get("liczba_krow_start")),
            budzet_st=str(p.get("budzet_start")),
            drap=str(p.get("szansa_drapieznik")),
            koniec=str(wynik["powod_konca"])[:19],
        )

    def wyswietl_dla_seeda(self, seed):
        ranking = self.wczytaj_ranking()
        tylko_ten_seed = [w for w in ranking if self._seed_wyniku(w) == seed]

        print()
        print(ZIELONY + f"=== RANKING dla seeda {seed} ===" + RESET)  # nogłówek

        print()  # linijka przerwy
        if not tylko_ten_seed:
            print("Brak wyników dla tego seeda.")
            return
        print(self._naglowek_tabeli())
        miejsce = 1
        for wynik in tylko_ten_seed:
            print(self._wiersz(miejsce, wynik))
            miejsce += 1

    def wyswietl_top_10(self):
        ranking = self.wczytaj_ranking()

        print()
        print(ZIELONY + "=== TOP 10 (wszystkie seedy razem) ===" + RESET)
        print()

        if not ranking:
            print("Brak wyników.")
            return
        print(self._naglowek_tabeli())
        miejsce = 1
        for wynik in ranking[:10]:
            print(self._wiersz(miejsce, wynik))
            miejsce += 1
