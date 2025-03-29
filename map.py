import customtkinter as ctk
from tkintermapview import TkinterMapView
import requests


class PollutionMapPage(ctk.CTkFrame):
    def __init__(self, parent, api_key, geocoding_api_key):
        super().__init__(parent)
        self.api_key = api_key
        self.geocoding_api_key = geocoding_api_key
        self.configure(fg_color='#ADD8E6')
        self.create_map_page()

    def show_pollution_alert(self, location_name, pollution_text, temperature):
        """Wyświetla okno z informacją o stanie powietrza i temperaturze."""
        alert = ctk.CTkToplevel(self)
        alert.title("Informacje o lokalizacji")
        alert.geometry("600x300")
        alert.configure(fg_color='#FFFFFF')

        label = ctk.CTkLabel(
            alert,
            text=f"Lokalizacja: {location_name}\n\nTemperatura: {temperature}°C\n\nStan powietrza:\n\n{pollution_text}",
            font=("Arial", 14),
            text_color="#000000",
            wraplength=550
        )
        label.pack(pady=20)

        button = ctk.CTkButton(
            alert,
            text="Zamknij",
            font=("Arial", 12, "bold"),
            fg_color="#4682B4",
            text_color="white",
            command=alert.destroy
        )
        button.pack(pady=10)

    def on_map_click(self, coordinates):
        """Obsługuje kliknięcie na mapie i pobiera dane o temperaturze i zanieczyszczeniu."""
        lat, lon = coordinates

        self.map_view.delete_all_marker()
        self.map_view.set_marker(lat, lon)

        weather_data = self.get_weather_data(lat, lon)
        location_name = self.get_location_name(lat, lon)

        if weather_data:
            temperature = weather_data["temperature"]
            pollution_text = (
                f"CO (czad): {weather_data['pollution'].get('co', 'Brak danych')} µg/m³\n"
                f"NO₂ (dwutlenek azotu): {weather_data['pollution'].get('no2', 'Brak danych')} µg/m³\n"
                f"PM2.5: {weather_data['pollution'].get('pm2_5', 'Brak danych')} µg/m³\n"
                f"PM10: {weather_data['pollution'].get('pm10', 'Brak danych')} µg/m³"
            )
        else:
            temperature = "Brak danych"
            pollution_text = "Brak danych o zanieczyszczeniach"

        self.show_pollution_alert(location_name, pollution_text, temperature)

    def get_weather_data(self, latitude, longitude):
        """Pobiera dane o temperaturze i jakości powietrza z OpenWeather API."""
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={self.api_key}"
        pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={self.api_key}"

        try:
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            temperature = round(weather_data["main"]["temp"], 1)

            pollution_response = requests.get(pollution_url)
            pollution_response.raise_for_status()
            pollution_data = pollution_response.json()
            pollution = pollution_data.get('list', [{}])[0].get('components', {})

            return {"temperature": temperature, "pollution": pollution}
        except requests.RequestException as e:
            print(f"Błąd pobierania danych pogodowych: {e}")
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
            text="Kliknij na mapie, aby sprawdzić temperaturę i stan powietrza.",
            font=("Arial", 14, "bold"),
            text_color="#000000"
        )
        instruction_label.pack(pady=10)

        self.map_view = TkinterMapView(self, width=750, height=450, corner_radius=10)
        self.map_view.set_position(52.2297, 21.0122)
        self.map_view.set_zoom(10)
        self.map_view.pack(pady=20)

        self.map_view.add_left_click_map_command(self.on_map_click)


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Mapa Temperatury i Zanieczyszczenia Powietrza")
    app.geometry("900x650")
    app.configure(fg_color='#ADD8E6')

    api_key = "fb9e5c164b6e64b6ea40f8d266f20499"
    geocoding_api_key = "054f1743e6714d5da5471ceea86bfb33"
    pollution_page = PollutionMapPage(app, api_key, geocoding_api_key)
    pollution_page.pack(fill="both", expand=True)

    app.mainloop()
