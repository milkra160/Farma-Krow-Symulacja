import json
import os

#pomocnik do sortowania. Zwraca to po czym sortujemy (liczbe dni przezycia)
def _pomocnik_dni_przezycia(wynik: dict) ->int :
    return wynik["dni_przezycia"]

#klasa ranking zapisuje wynik symulacji do pliku json i odczytuje je
class Ranking:
    def __init__(self, plik: str = "ranking.json"):
        self.plik = plik

    def wczytaj_ranking(self) -> list:
        #zabezpieczenie. Jak nie ma pliku zwracamy pusta liste
        if not os.path.exists(self.plik):
            return []
        with open(self.plik, "r", encoding="utf-8") as f:
            dane = json.load(f)
        # sortujemy malejaco po dniach przezycia
        dane.sort(key=_pomocnik_dni_przezycia, reverse=True)
        return dane

    def zapisz_wynik(self, wynik: dict):
        ranking = self.wczytaj_ranking() # to co juz mamy znajduje sie w pliku
        ranking.append(wynik) #dodajemy nowy wynik
        ranking.sort(key=_pomocnik_dni_przezycia, reverse=True)
        with open(self.plik, "w", encoding="utf-8") as f:
            json.dump(ranking, f, ensure_ascii=False, indent=2)

    def wyswietl_top_10(self):
        ranking = self.wczytaj_ranking()
        print("---TOP 10---")
        miejsce = 1
        for wynik in ranking[:10]: #bierzemy tylko top 10
            print(f"{miejsce}. {wynik['nazwa_farmy']} - "
                  f"{wynik['dni_przezycia']} dni, budzet maks {wynik['maks_budzet']}")







