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
        ctk.CTkLabel(self, text="Kliknij na mapie, aby sprawdzić jakość powietrza", font=("Arial", 14, "bold")).pack(pady=5)

        # Mapa
        self.map_view = TkinterMapView(self, width=750, height=450, corner_radius=10)
        self.map_view.set_position(52.2297, 21.0122)
        self.map_view.set_zoom(10)
        self.map_view.pack(pady=20)

        self.map_view.add_left_click_map_command(self.on_map_click)

        # Przycisk powrotu
        ctk.CTkButton(self, text="Wróć do wyboru miasta", font=("Arial", 12, "bold"),
                      command=lambda: controller.show_frame("CarbonApp")).pack(pady=10)

    def on_map_click(self, coordinates):
        """ Pobiera dane o temperaturze i jakości powietrza po kliknięciu na mapie """
        lat, lon = coordinates
        self.map_view.set_marker(lat, lon)

        api_key = "YOUR_API_KEY"
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"

        try:
            response = requests.get(weather_url)
            response.raise_for_status()
            weather_data = response.json()
            temperature = round(weather_data["main"]["temp"], 1)

            messagebox.showinfo("Informacje", f"Temperatura: {temperature}°C")
        except requests.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")
