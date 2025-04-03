import customtkinter as ctk
from tkintermapview import TkinterMapView
from tkinter import messagebox
import requests


class PollutionMapPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color='#2E2E2E')  # Ustawienie ciemnego tła

        self.current_marker = None  # Zmienna do przechowywania referencji do aktualnego znacznika

        # Utworzenie ramki na mapę po lewej stronie
        self.map_frame = ctk.CTkFrame(self, fg_color="#2E2E2E")
        self.map_frame.grid(row=0, column=0, padx=10, pady=10)

        # Instrukcja obsługi
        ctk.CTkLabel(self, text="Kliknij na mapie, aby sprawdzić jakość powietrza", font=("Arial", 14, "bold"), text_color="white").grid(row=1, column=1, padx=10, pady=20)

        # Mapa
        self.map_view = TkinterMapView(self.map_frame, width=750, height=450, corner_radius=10)
        self.map_view.set_position(52.2297, 21.0122)
        self.map_view.set_zoom(10)
        self.map_view.pack(pady=20)

        self.map_view.add_left_click_map_command(lambda coord: self.on_map_click(*coord))

        # Utworzenie ramki na informacje po prawej stronie
        self.info_frame = ctk.CTkFrame(self, fg_color="#2E2E2E")
        self.info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Etykieta na informacje
        self.info_label = ctk.CTkLabel(self.info_frame, text="Informacje o jakości powietrza", font=("Arial", 12, "bold"), text_color="white")
        self.info_label.grid(row=0, column=0, padx=10, pady=5)

        self.info_text = ctk.CTkLabel(self.info_frame, text="Wybierz punkt na mapie, aby wyświetlić dane.", font=("Arial", 12), text_color="white", wraplength=300)
        self.info_text.grid(row=1, column=0, padx=10, pady=10)

        # Przycisk powrotu
        self.back_button = ctk.CTkButton(self.info_frame, text="Wróć do wyboru miasta", font=("Arial", 12, "bold"), command=lambda: controller.show_frame("CarbonApp"))
        self.back_button.grid(row=2, column=0, padx=10, pady=10)

    def on_map_click(self, lat, lon):
        """ Pobiera dane o temperaturze i jakości powietrza po kliknięciu na mapie """
        # Usuwamy istniejący znacznik, jeśli istnieje
        if self.current_marker:
            self.current_marker.delete()

        # Ustawiamy nowy znacznik
        self.current_marker = self.map_view.set_marker(lat, lon)

        # Klucze API
        weather_api_key = "fb9e5c164b6e64b6ea40f8d266f20499"
        geocoding_api_key = "054f1743e6714d5da5471ceea86bfb33"

        # URL do pobrania danych o pogodzie
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={weather_api_key}"
        pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={weather_api_key}"

        try:
            # Pobieranie danych o pogodzie
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            temperature = round(weather_data["main"]["temp"], 1)

            # Pobieranie danych o jakości powietrza
            pollution_response = requests.get(pollution_url)
            pollution_response.raise_for_status()
            pollution_data = pollution_response.json()
            pollution = pollution_data.get('list', [{}])[0].get('components', {})

            pollution_text = (
                f"CO (czad): {pollution.get('co', 'Brak danych')} µg/m³\n"
                f"NO₂ (dwutlenek azotu): {pollution.get('no2', 'Brak danych')} µg/m³\n"
                f"PM2.5: {pollution.get('pm2_5', 'Brak danych')} µg/m³\n"
                f"PM10: {pollution.get('pm10', 'Brak danych')} µg/m³"
            )

            # Określenie zagrożenia na podstawie poziomu zanieczyszczeń
            pollution_level = self.get_pollution_level(pollution)

            # Wyświetlanie wyników w oknie
            self.info_text.configure(text=f"Temperatura: {temperature}°C\n\nStan powietrza:\n\n{pollution_text}\n\nZagrożenie: {pollution_level}")

        except requests.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

    def get_pollution_level(self, pollution):
        """ Określenie zagrożenia zdrowotnego na podstawie poziomu zanieczyszczeń """
        # Wartości graniczne wg Światowej Organizacji Zdrowia (WHO) i innych wytycznych
        co_level = pollution.get('co', 0)
        no2_level = pollution.get('no2', 0)
        pm2_5_level = pollution.get('pm2_5', 0)
        pm10_level = pollution.get('pm10', 0)

        # Wskaźnik zagrożenia
        if pm2_5_level > 35 or pm10_level > 50:
            return "Wysokie zagrożenie dla zdrowia (Unikaj aktywności na zewnątrz)"
        elif no2_level > 200 or co_level > 1000:
            return "Umiarkowane zagrożenie (Zaleca się ograniczenie aktywności na zewnątrz)"
        elif pm2_5_level > 12 or pm10_level > 20:
            return "Niskie zagrożenie (Zaleca się ostrożność wrażliwych osób)"
        else:
            return "Jakość powietrza dobra (Brak zagrożeń)"
