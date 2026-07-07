from src.logger import Logger


def przykladowy_log():
    return {
        "dzien": 5,
        "pogoda": "deszcz",
        "narodziny": ["Karol"],
        "martwe": ["Marek", "Bartosz"],
        "powod_smierci": {"Marek": "glod", "Bartosz": "drapieznik"},
        "zjadly": ["Łaciata", "Andrzej"],
        "glodne": ["Hiszpan"],
        "drapiezniki": [(3, 4)],
        "stan_krow": [
            {"symbol": "K", "gatunek": "krowa", "imie": "Łaciata",
             "najedzenie": 80, "zjadla": True, "zyje": True},
            {"symbol": "K", "gatunek": "krowa", "imie": "Andrzej",
             "najedzenie": 70, "zjadla": True, "zyje": True},
            {"symbol": "K", "gatunek": "krowa", "imie": "Hiszpan",
             "najedzenie": 20, "zjadla": False, "zyje": True},
        ],
        "kepki_trawy": [(1, 1), (2, 2)],
        "finanse": {
            "budzet": 120,
            "przychod": 40,
            "koszt": 50,
            "bilans": -10,
            "bankrut": False,
        },
        "zdarzenia": ["Pora deszczowa - leje od kilku dni"],
    }


def test_czy_log_zawiera_pogodei_naglowek(capsys):
    Logger().drukuj_log(przykladowy_log())
    wynik = capsys.readouterr().out
    assert "DZIEŃ 5" in wynik
    assert "deszcz" in wynik


def test_czy_log_pokazuje_smierc_z_powodem(capsys):
    Logger().drukuj_log(przykladowy_log())
    wynik = capsys.readouterr().out
    assert "Marek" in wynik
    assert "glod" in wynik
    assert "Bartosz" in wynik
    assert "drapieznik" in wynik


def test_czy_log_drukuje_statystyki_stada(capsys):
    Logger().drukuj_log(przykladowy_log())
    wynik = capsys.readouterr().out
    assert "ŻYWE KROWY: 3" in wynik  # 3 zywe krowy
    assert "najedzonych: 2" in wynik  # 2 najedzone
    assert "głodnych: 1" in wynik  # 1 glodna


def test_czy_log_bez_zdarzen_pomija_naglowek(capsys):
    log = przykladowy_log()
    log["zdarzenia"] = []
    Logger().drukuj_log(log)
    wynik = capsys.readouterr().out
    assert "Zdarzenia:" not in wynik


def test_czy_loger_pokazuje_podsumowanie_koncowe(capsys):
    Logger().drukuj_podsumowanie_koncowe(5, "bankructwo", {"budzet": 0})
    wynik = capsys.readouterr().out
    assert "KONIEC" in wynik
    assert "bankructwo" in wynik
