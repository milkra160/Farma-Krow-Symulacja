from src.config import *
from src.symulacja import Symulacja
import os
import random
import sys

os.system("")

#kolory
ZIELONY ="\033[92m"
ZOLTY ="\033[93m"
CZERWONY="\033[91m"
BLEKITNY = "\033[96m"
RESET ="\033[0m"



#funkcja zmieniająca tekst na zielony
def zielony(tekst):
    return f"{ZIELONY}{tekst}{RESET}"

#funkcja zmieniająca tekst na zolty
def zolty(tekst):
    return f"{ZOLTY}{tekst}{RESET}"

#tekst na czerwony
def czerwony(tekst):
    return f"{CZERWONY}{tekst}{RESET}"

#tekst na blekitny
def blekitny(tekst):
    return f"{BLEKITNY}{tekst}{RESET}"


#funkcja czyszcząca bufor przed każdym inputem w main, naprawia to błąd z wyświetlaniem dnia dwa razy przy
#pojedynczym wciśnięciu ENTER
def wczytaj(prompt=""):
    sys.stdout.flush()
    return input(prompt)

#pytamy użytkownika o wprowadzenie seedu, jeśli nic nie poda to
#lostujemy losowy seed, tak żeby w przyszłości mozna było porównywac seedy
def zapytaj_o_seed():
    while True:
        sys.stdout.flush()
        odpowiedz = input("Podaj seed (liczba całkowita >= 0, Enter = losowy): ").strip()

        # Enter = losujemy nowy seed
        if odpowiedz == "":
            seed = random.randrange(1, 1_000_000)
            random.seed(seed)
            print(zolty(f"Wylosowano nowy seed: {seed} (zapisz go, jeśli chcesz powtórzyć tę grę)"))
            return seed

        # proba zamiany na liczbe calkowita
        try:
            seed = int(odpowiedz)
        except ValueError:
            print(czerwony("Seed musi być liczbą całkowitą (np. 1, 42, 1000). Spróbuj ponownie."))
            continue

        # seed nie moze byc ujemny
        if seed < 0:
            print(czerwony("Seed nie może być ujemny. Podaj liczbę >= 0. Spróbuj ponownie."))
            continue

        random.seed(seed)
        print(zolty(f"Ustawiono seed: {seed}"))
        return seed


# pyta uzytkownika o jeden parametr. Enter = wartosc domyslna
def zapytaj(tekst, domyslne, typ, opis="", minimum=None, maksimum=None):
    if opis:
        print(blekitny(opis))

    # budujemy opis dozwolonego zakresu do komunikatu o bledzie
    if minimum is not None and maksimum is not None:
        zakres = f"z przedziału {minimum}–{maksimum}"
    elif minimum is not None:
        zakres = f"nie mniejsza niż {minimum}"
    elif maksimum is not None:
        zakres = f"nie większa niż {maksimum}"
    else:
        zakres = ""

    while True:
        sys.stdout.flush()
        odpowiedz = input(f"{tekst} [{domyslne}]: ").strip()
        if odpowiedz == "":
            return domyslne  # Enter = wartosc domyslna

        # proba zamiany na wlasciwy typ (int/float)
        try:
            wartosc = typ(odpowiedz)
        except ValueError:
            print(czerwony("To nie jest poprawna liczba. Spróbuj ponownie."))
            continue

        # sprawdzenie zakresu z czytelnym komunikatem
        poza_zakresem = (minimum is not None and wartosc < minimum) or \
                        (maksimum is not None and wartosc > maksimum)
        if poza_zakresem:
            print(czerwony(f"Wartość poza zakresem – dozwolone {zakres}. Spróbuj ponownie."))
            continue

        return wartosc

#przywitanie użytkownika i opis zmiennych ustwaianych na początku symulacji

def main():
    print("=" * 60)
    print("                     FARMA KRÓW")
    print("=" * 60)
    print(zielony(
        "Zarządzasz fermą krów mlecznych. 1 tura = 1 dzień.\n"
        "Dorosła krowa daje 20 zł mleka dziennie, a utrzymanie farmy\n"
        "kosztuje 50 zł dziennie. Czyli potrzebujesz min. 3 dorosłych\n"
        "krów, żeby wyjść na zero.\n"
        "Celem symulacji jest sprawdzenie jakie ustawienie zmiennych\n"
        "początkowych, da jak najlepsze wyniki:\n"
        "(długość czasu trwania, budżet maksymalny i końcowy)\n"
        "Wielkości ustawione w '[]' to wartości domyślne,\n"
        "naciśnij 'ENTER' by użyć wartości domyślnych\n"
    ))

    seed = zapytaj_o_seed()
    print() #linijka przerwy

    parametry = {
        "seed": seed,
        "nazwa_farmy": zapytaj("Nazwa farmy", "Moja Farma", str,
                               "Nazwa farmy – pojawi się w rankingu."),
        "liczba_krow_start": zapytaj("Liczba krów startowych", 5, int,
                                     "Ile dorosłych krów na start. Każda = +20 zł/dzień.",
                                     minimum=1, maksimum=400),
        "budzet_start": zapytaj("Budżet startowy", BUDZET_START, float,
                                "Pieniądze na start. Dzień kosztuje 50 zł.",
                                minimum=1),
        "szansa_drapieznik": zapytaj("Szansa na drapieżnika (0-1)", SZANSA_DRAPIEZNIK, float,
                                     "0 = nigdy, 1 = codziennie.",
                                     minimum=0, maksimum=1),
        "maks_drapieznikow": zapytaj("Maksymalna liczba drapieżników", MAKS_DRAPIEZNIKOW, int,
                                     "Ilu naraz może się pojawić.",
                                     minimum=1, maksimum=10),
        "max_dni": zapytaj("Maksymalna liczba dni", MAX_DNI, int,
                           "Po tylu dniach symulacja sama się kończy.",
                           minimum=1),
        "szansa_zdarzenia": zapytaj("Szansa na zdarzenie losowe (0-1)", SZANSA_NA_ZDARZENIE, float,
                                    "Jak często dzieje się coś nieoczekiwanego.",
                                    minimum=0, maksimum=1),
    }
    symulacja = Symulacja()
    symulacja.start(parametry)


if __name__ == "__main__":  # zabezpiecznie
    main()
