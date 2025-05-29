# WeatherApp

## Opis projektu

WeatherApp to profesjonalna aplikacja napisana w języku Python, służąca do pobierania, analizy oraz prezentowania danych pogodowych. Projekt stworzony został z myślą o firmach i użytkownikach indywidualnych, którzy potrzebują niezawodnych i szczegółowych informacji pogodowych, z możliwością integracji w większych systemach lub własnych rozwiązaniach biznesowych. 

## Spis treści

- [Opis projektu](#opis-projektu)
- [Funkcjonalności](#funkcjonalności)
- [Wymagania systemowe](#wymagania-systemowe)
- [Instalacja](#instalacja)
- [Konfiguracja](#konfiguracja)
- [Sposób użycia](#sposób-użycia)
- [Architektura](#architektura)
- [Testowanie](#testowanie)
- [Bezpieczeństwo](#bezpieczeństwo)
- [Wsparcie i kontakt](#wsparcie-i-kontakt)
- [Licencja](#licencja)
- [Autorzy](#autorzy)

## Funkcjonalności

- Pobieranie aktualnych danych pogodowych dla dowolnej lokalizacji
- Obsługa wielu źródeł danych pogodowych (np. OpenWeatherMap, WeatherAPI)
- Historia oraz prognozy pogody
- Prezentacja prognozy pogody poprzez własne AI
- Integracja z innymi aplikacjami przez REST API
- Modułowa architektura umożliwiająca łatwą rozbudowę o nowe funkcjonalności
- Automatyczne testy jednostkowe i integracyjne
- Obsługa alertów pogodowych

## Wymagania systemowe

- Python 3.9 lub nowszy
- System operacyjny: Linux, macOS, Windows
- Dostęp do internetu (do pobierania danych pogodowych)
- Zalecane: wirtualne środowisko Pythona (venv, conda)

## Instalacja

```bash
git clone https://github.com/LS0leq/WeatherApp.git
cd WeatherApp
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Konfiguracja

1. Skopiuj plik konfiguracyjny:

   ```bash
   cp config.example.yaml config.yaml
   ```

2. Uzupełnij plik `.env` o własne klucze API i preferencje użytkownika.


## Sposób użycia

- Uruchom aplikację:
  
  ```bash
  python main.py
  ```

## Architektura

Projekt oparty jest na architekturze warstwowej:

- `main.py` – punkt wejścia aplikacji
- `weather/` – logika pobierania i przetwarzania danych pogodowych
- `api/` – warstwa komunikacji z zewnętrznymi API
- `config/` – zarządzanie konfiguracją
- `utils/` – funkcje pomocnicze
- `tests/` – testy jednostkowe i integracyjne

## Testowanie

- Wszystkie kluczowe funkcjonalności pokryte są testami jednostkowymi.
- Wyniki testów prezentowane są w postaci raportów.

## Bezpieczeństwo

- Klucze API oraz dane wrażliwe przechowywane są w pliku `.env`, który nie jest wersjonowany.
- Wrażliwe operacje są logowane.
- Zaleca się regularną aktualizację zależności (`pip list --outdated`).

## Wsparcie i kontakt

W przypadku problemów lub chęci rozwoju projektu:

- Otwórz issue na [GitHubie](https://github.com/LS0leq/WeatherApp/issues)

## Licencja

Projekt dostępny jest na licencji MIT.

## Autorzy

- Aleksander Wąsowicz
- Patryk Kryger
- Mateusz Żywicki

---

> Dokumentacja została przygotowana zgodnie ze standardami korporacyjnymi. Wszelkie uwagi i sugestie można zgłaszać przez system zgłoszeń. Aby utworzyć tą dokumentację użyto własnego oprogramowania (kreator.lsoleq.xaa.pl)
