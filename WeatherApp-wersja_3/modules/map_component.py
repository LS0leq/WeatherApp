import customtkinter as ctk
from tkintermapview import TkinterMapView
import requests
from modules import config


class MapComponent(ctk.CTkFrame):
    def __init__(self, master, info_component):
        super().__init__(master, fg_color="#3A3A3A")
        self.info_component = info_component

        self.map_view = TkinterMapView(self, width=500, height=500, corner_radius=10)
        self.map_view.set_position(52.2297, 21.0122)  # Warszawa
        self.map_view.set_zoom(10)
        self.map_view.pack(expand=True, fill="both", padx=10, pady=10)

        self.map_view.add_left_click_map_command(self.on_map_click)

    def on_map_click(self, event):
        lat, lon = self.map_view.get_position()
        pollution_data = self.get_pollution_data(lat, lon)
        location_name = self.get_location_name(lat, lon)

        self.map_view.delete_all_marker()
        self.map_view.set_marker(lat, lon)

        self.info_component.update_info(location_name, pollution_data)

    def get_pollution_data(self, latitude, longitude):
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={config.API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['list'][0]['modules']
        except (requests.RequestException, KeyError):
            return None

    def get_location_name(self, latitude, longitude):
        url = f"https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={config.GEOCODING_API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data["results"][0]["formatted"] if data["results"] else "Nieznana lokalizacja"
        except requests.RequestException:
            return "Nieznana lokalizacja"
