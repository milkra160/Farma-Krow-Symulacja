from src.config import *
from src.symulacja import Symulacja


# pyta uzytkownika o jeden parametr. Enter = wartosc domyslna
def zapytaj(tekst, domyslne, typ):
    odpowiedz = input(f"{tekst} [{domyslne}]: ").strip()
    if odpowiedz == "":
        return domyslne
    return typ(odpowiedz)


def main():
    print("--- FARMA KROW ---")
    print("SKONFIGURUJ SYMULACJE!!")
    parametry = {
        "nazwa_farmy": zapytaj("Nazwa farmy", "Moja Farma", str),
        "liczba_krow_start": zapytaj("liczba krow startowych", 5, int),
        "budzet_start": zapytaj("Budżet startowy", BUDZET_START, float),
        "szansa_drapieznik": zapytaj(
            "Szansa na drapieznika (0-1)", SZANSA_DRAPIEZNIK, float
        ),
        "maks_drapieznikow": zapytaj(
            "Maksymalna liczba drapieznikow", MAKS_DRAPIEZNIKOW, int
        ),
        "max_dni": zapytaj("Maksymalna liczba dni", MAX_DNI, int),
        "szansa_zdarzenia": zapytaj(
            "Szansa na zdarzenie losowe (0-1)", SZANSA_NA_ZDARZENIE, int
        ),
    }
    symulacja = Symulacja()
    symulacja.start(parametry)


if __name__ == "__main__":  # zabezpiecznie
    main()
