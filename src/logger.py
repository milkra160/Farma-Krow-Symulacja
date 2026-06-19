# klasa Logger formatuje i drukuje dzienny log w terminalu
class Logger:
    def drukuj_log(self, log: dict):
        # naglowek: pogoda i dzien
        print(f"--- Dzień {log['dzien']} | pogoda: {log['pogoda']} ---")

        # aktywne zdarzenia losowe
        if len(log["zdarzenia"]) > 0:
            print("Zdarzenia:")
            for opis in log["zdarzenia"]:
                print(f" - {opis}")

        # finanse
        finanse = log["finanse"]
        print(
            f"Finanse: przychód {finanse['przychod']}, koszt {finanse['koszt']}, "
            f"bilans {finanse['bilans']}, budżet {finanse['budzet']}"
        )

        # narodziny
        if len(log["narodziny"]) > 0:
            print(f"Narodziny: {', '.join(log['narodziny'])}")

        # dorastanie

        if log.get("dorastanie") and len(log["dorastanie"]) > 0:
            print(f"Dorastanie: {', '.join(log['dorastanie'])} juz jest duża krową")

        # smierc z powodem
        for imie in log["martwe"]:
            powod = log["powod_smierci"][imie]
            print(f"Zdechła: {imie} (powód: {powod})")

        # statystyka stada
        ile_zjadlo = len(log["zjadly"])
        ile_glodnych = len(log["glodne"])
        rozmiar_stada = ile_zjadlo + ile_glodnych
        print(
            f"Stado: {rozmiar_stada} krów (najedzonych: {ile_zjadlo}, głodnych: {ile_glodnych})"
        )
        print()  # pusta linia na koniec dnia

    def drukuj_podsumowanie_koncowe(self, dni: int, powod: str, finanse: dict):
        print("-" * 30)
        print("KONIEC SYMULACJI")
        print(f"Powód zakończenia: {powod}")
        print(f"Liczba przetrwanych dni: {dni}")
        print(f"Końcowy budżet: {finanse['budzet']}")
        print("-" * 30)
