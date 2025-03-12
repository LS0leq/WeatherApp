import customtkinter as ctk
from tkintermapview import TkinterMapView
import requests


# -----KOMPONENT 1: OBSLUGA MAPY I POBIERANIE DANYCH ZANIECZYSZCZEN------
class MapComponent(ctk.CTkFrame):
    def __init__(self, parent, api_key, geocoding_api_key, info_component):
        super().__init__(parent, fg_color="#3A3A3A")
        self.api_key = api_key
        self.geocoding_api_key = geocoding_api_key
        self.info_component = info_component

        self.map_view = TkinterMapView(self, width=500, height=500, corner_radius=10)
        self.map_view.set_position(52.2297, 21.0122)  # Domyślnie Warszawa
        self.map_view.set_zoom(10)
        self.map_view.pack(expand=True, fill="both", padx=10, pady=10)
        self.map_view.add_left_click_map_command(self.on_map_click)
#-----------Obsluga markea-------
    def on_map_click(self, event):
        lat, lon = self.map_view.get_position()
        pollution_data = self.get_pollution_data(lat, lon)
        location_name = self.get_location_name(lat, lon)
        self.map_view.delete_all_marker()
        self.map_view.set_marker(lat, lon)

        if pollution_data:
            pollution_text = self.get_pollution_description(pollution_data)
        else:
            pollution_text = "Brak danych o zanieczyszczeniach"

        self.info_component.update_info(location_name, pollution_text)

    def get_pollution_data(self, latitude, longitude):
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={self.api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['list'][0]['components']
        except (requests.RequestException, KeyError):
            return None

    def get_location_name(self, latitude, longitude):
        url = f"https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={self.geocoding_api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data["results"][0]["formatted"] if data["results"] else "Nieznana lokalizacja"
        except requests.RequestException:
            return "Nieznana lokalizacja"

#------------------Ponizej inforamcje o zanieczyszczeniach----------------------
#---WAZNE---W razie braku zanieczyszczen program nie bedzie wyswietlac pojedynczych informacji (jesli powietrze jest calkowicie czyste bedzie informacja o tym)-----
    def get_pollution_description(self, pollution_data):
        descriptions = []

        if pollution_data['co'] > 1000:
            descriptions.append("CO: Bardzo wysoki poziom! Możliwe zatrucie.")
        elif pollution_data['co'] > 500:
            descriptions.append("CO: Wysoki poziom, może powodować problemy oddechowe.")

        if pollution_data['no2'] > 200:
            descriptions.append("NO₂: Bardzo wysoki poziom, zagrożenie dla astmatyków.")
        elif pollution_data['no2'] > 100:
            descriptions.append("NO₂: Średni poziom, może pogarszać stan układu oddechowego.")

        if pollution_data['pm2_5'] > 100:
            descriptions.append("PM2.5: Bardzo wysoki poziom, ryzyko chorób serca.")
        elif pollution_data['pm2_5'] > 50:
            descriptions.append("PM2.5: Średni poziom, możliwe problemy oddechowe.")

        return "\n".join(descriptions) if descriptions else "Powietrze jest czyste!"



#--------------------------KOMPONENT 2 WYSWIETLANIE INFORMACJI---------------------------
class InfoComponent(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#3A3A3A")
        self.info_label = ctk.CTkLabel(self, text="Wybierz lokalizację na mapie", font=("Arial", 16),
                                       text_color="white")
        self.info_label.pack(pady=20)

    def update_info(self, location, pollution_text):
        self.info_label.configure(text=f"Lokalizacja: {location}\n\n{pollution_text}")

#------------KOMPONENT 3 OBSLUGA WSZYSTKIEGO/GLOWNA APLIKACJA--------------
class PollutionApp(ctk.CTk):
    def __init__(self, api_key, geocoding_api_key):
        super().__init__()
        self.api_key = api_key
        self.geocoding_api_key = geocoding_api_key
        self.title("Mapa Zanieczyszczenia Powietrza")
        self.geometry("1000x600")
        self.configure(bg="#2E2E2E")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.info_component = InfoComponent(self)
        self.info_component.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.map_component = MapComponent(self, self.api_key, self.geocoding_api_key, self.info_component)
        self.map_component.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    API_KEY = "fb9e5c164b6e64b6ea40f8d266f20499"
    GEOCODING_API_KEY = "054f1743e6714d5da5471ceea86bfb33"

    app = PollutionApp(API_KEY, GEOCODING_API_KEY)
    app.mainloop()
