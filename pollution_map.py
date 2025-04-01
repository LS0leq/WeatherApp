import customtkinter as ctk
from tkintermapview import TkinterMapView
from tkinter import messagebox
import requests


class PollutionMapPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color='#ADD8E6')

        # Instrukcja obsługi
        ctk.CTkLabel(self, text="Kliknij na mapie, aby sprawdzić jakość powietrza", font=("Arial", 14, "bold")).pack(
            pady=5)

        # Mapa
        self.map_view = TkinterMapView(self, width=750, height=450, corner_radius=10)
        self.map_view.set_position(52.2297, 21.0122)
        self.map_view.set_zoom(10)
        self.map_view.pack(pady=20)

        self.map_view.add_left_click_map_command(lambda coord: self.on_map_click(*coord))

        # Przycisk powrotu
        ctk.CTkButton(self, text="Wróć do wyboru miasta", font=("Arial", 12, "bold"),
                      command=lambda: controller.show_frame("CarbonApp")).pack(pady=10)

    def on_map_click(self, lat, lon):
        """ Pobiera dane o temperaturze i jakości powietrza po kliknięciu na mapie """
        self.map_view.set_marker(lat, lon)

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

            # Wyświetlanie wyników w oknie
            messagebox.showinfo("Informacje", f"Temperatura: {temperature}°C\n\nStan powietrza:\n\n{pollution_text}")

        except requests.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")
