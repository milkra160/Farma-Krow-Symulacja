from src.config import *
from src.symulacja import Symulacja
import os
import random

os.system("")

#kolory
ZIELONY ="\033[92m"
ZOLTY ="\033[93m"
CZERWONY="\033[91m"
RESET ="\033[0m"


#funkcja zmieniająca tekst na zielony
def zielony(tekst):
    return f"{ZIELONY}{tekst}{RESET}"

#funkcja zmieniająca tekst na zolty
def zolty(tekst):
    return f"{ZOLTY}{tekst}{RESET}"



#pytamy użytkownika o wprowadzenie seedu, jeśli nic nie poda to
#lostujemy losowy seed, tak żeby w przyszłości mozna było porównywac seedy
def zapytaj_o_seed():
    odpowiedz = input("Podaj seed (Enter = losowy): ").strip()
    if odpowiedz == "":
        seed = random.randrange(1, 1_000_000)
    else:
        seed = int(odpowiedz)
    random.seed(seed)
    print(zolty(f"Seed symulacji: {seed}"))
    return seed


# pyta uzytkownika o jeden parametr. Enter = wartosc domyslna
def zapytaj(tekst, domyslne, typ, opis=""):
    if opis:
        print(zielony(opis))
    odpowiedz = input(f"{tekst} [{domyslne}]: ").strip()
    if odpowiedz == "":
        return domyslne
    return typ(odpowiedz)

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
                                     "Ile dorosłych krów na start. Każda = +20 zł/dzień."),
        "budzet_start": zapytaj("Budżet startowy", BUDZET_START, float,
                                "Pieniądze na start. Dzień kosztuje 50 zł, więc 500 zł ~ 10 dni buforu."),
        "szansa_drapieznik": zapytaj("Szansa na drapieżnika (0-1)", SZANSA_DRAPIEZNIK, float,
                                     "0 = nigdy, 1 = codziennie. 0.15 = mniej więcej co tydzień."),
        "maks_drapieznikow": zapytaj("Maksymalna liczba drapieżników", MAKS_DRAPIEZNIKOW, int,
                                     "Ilu naraz może się pojawić (każdy może zabić 1 krowę)."),
        "max_dni": zapytaj("Maksymalna liczba dni", MAX_DNI, int,
                           "Po tylu dniach symulacja sama się kończy."),
        "szansa_zdarzenia": zapytaj("Szansa na zdarzenie losowe (0-1)", SZANSA_NA_ZDARZENIE, float,
                                    "Jak często dzieje się coś nieoczekiwanego. 0.10 = co ~10 dni."),
    }
    symulacja = Symulacja()
    symulacja.start(parametry)


if __name__ == "__main__":  # zabezpiecznie
    main()
