import customtkinter as ctk
from tkintermapview import TkinterMapView
import requests


class PollutionMapPage(ctk.CTkFrame):
    def __init__(self, parent, api_key, geocoding_api_key):
        super().__init__(parent)
        self.api_key = api_key
        self.geocoding_api_key = geocoding_api_key
        self.create_map_page()

    def show_pollution_alert(self, location_name, pollution_text):
        """Wyświetla okno z informacją o stanie powietrza."""
        alert = ctk.CTkToplevel(self)
        alert.title("Informacja o zanieczyszczeniu")
        alert.geometry("800x300")

        label = ctk.CTkLabel(
            alert,
            text=f"Lokalizacja: {location_name}\n\nStan powietrza:\n\n{pollution_text}",
            font=("Arial", 12),
            wraplength=700
        )
        label.pack(pady=40)

        button = ctk.CTkButton(
            alert,
            text="Zamknij",
            command=alert.destroy
        )
        button.pack(pady=10)

    def on_map_click(self, lat, lon):
        """Obsługuje kliknięcie na mapie i pobiera dane o zanieczyszczeniu."""
        self.map_view.delete_all_marker()
        self.map_view.set_marker(lat, lon)

        pollution_data = self.get_pollution_data(lat, lon)
        location_name = self.get_location_name(lat, lon)

        if pollution_data:
            pollution_text = (
                f"CO (czad): {pollution_data.get('co', 'Brak danych')} µg/m³\n"
                f"NO (tlenek azotu): {pollution_data.get('no', 'Brak danych')} µg/m³\n"
                f"NO₂ (dwutlenek azotu): {pollution_data.get('no2', 'Brak danych')} µg/m³\n"
                f"O₃ (ozon): {pollution_data.get('o3', 'Brak danych')} µg/m³\n"
                f"PM2.5: {pollution_data.get('pm2_5', 'Brak danych')} µg/m³\n"
                f"PM10: {pollution_data.get('pm10', 'Brak danych')} µg/m³"
            )
        else:
            pollution_text = "Brak danych o zanieczyszczeniach"

        self.show_pollution_alert(location_name, pollution_text)

    def get_pollution_data(self, latitude, longitude):
        """Pobiera dane o jakości powietrza z OpenWeather API."""
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('list', [{}])[0].get('components', {})
        except requests.RequestException as e:
            print(f"Błąd pobierania danych o zanieczyszczeniach: {e}")
            return None

    def get_location_name(self, latitude, longitude):
        """Pobiera nazwę lokalizacji na podstawie współrzędnych."""
        url = f"https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={self.geocoding_api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data["results"][0]["formatted"] if data.get("results") else "Nieznana lokalizacja"
        except requests.RequestException as e:
            print(f"Błąd pobierania nazwy lokalizacji: {e}")
            return "Nieznana lokalizacja"

    def create_map_page(self):
        """Tworzy widok mapy z instrukcjami."""
        instruction_label = ctk.CTkLabel(
            self,
            text="Kliknij na mapie, aby sprawdzić stan powietrza w wybranym miejscu.",
            font=("Arial", 14, "italic"),
            text_color="white"
        )
        instruction_label.pack(pady=10)

        self.map_view = TkinterMapView(self, width=700, height=400, corner_radius=10)
        self.map_view.set_position(52.2297, 21.0122)  # Domyślnie Warszawa
        self.map_view.set_zoom(10)
        self.map_view.pack(pady=20)

        self.map_view.add_left_click_map_command(self.on_map_click)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Mapa Zanieczyszczenia Powietrza")
    app.geometry("800x600")

    api_key = "fb9e5c164b6e64b6ea40f8d266f20499"
    geocoding_api_key = "054f1743e6714d5da5471ceea86bfb33"
    pollution_page = PollutionMapPage(app, api_key, geocoding_api_key)
    pollution_page.pack(fill="both", expand=True)

    app.mainloop()
