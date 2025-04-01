import tkinter as tk
from tkinter import ttk, messagebox
import requests

class CarbonApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#ADD8E6')

        self.selected_state = tk.StringVar()
        self.selected_city = tk.StringVar()

        self.countries_and_cities = [
            {"state": "Pomorskie", "cities": ["Bytów", "Gdańsk", "Gdynia", "Kościerzyna", "Sopot"]},
            {"state": "Mazowieckie", "cities": ["Warszawa", "Radom", "Płock"]},
            {"state": "Małopolskie", "cities": ["Kraków", "Zakopane"]}
        ]

        tk.Label(self, text="Województwo:", bg='#87CEEB', font=('Arial', 14, 'bold')).pack(pady=5)
        self.state_combobox = ttk.Combobox(self, textvariable=self.selected_state, font=('Arial', 12))
        self.state_combobox['values'] = [item['state'] for item in self.countries_and_cities]
        self.state_combobox.bind("<<ComboboxSelected>>", self.on_state_selected)
        self.state_combobox.pack(pady=5)

        tk.Label(self, text="Miasto:", bg='#87CEEB', font=('Arial', 14, 'bold')).pack(pady=5)
        self.city_combobox = ttk.Combobox(self, textvariable=self.selected_city, font=('Arial', 12))
        self.city_combobox.pack(pady=5)

        tk.Button(self, text="Sprawdź jakość powietrza", command=self.fetch_data, font=('Arial', 14, 'bold'),
                  bg='#4682B4', fg='white').pack(pady=10)

        self.result_label = tk.Label(self, text="", bg='#FFFFFF', font=('Arial', 14), wraplength=350)
        self.result_label.pack(pady=5)

        tk.Button(self, text="Mapa Zanieczyszczeń", font=('Arial', 12, 'bold'),
                  command=lambda: controller.show_frame("PollutionMapPage"), bg='#4682B4', fg='white').pack(pady=10)

    def on_state_selected(self, event):
        selected_state = self.selected_state.get()
        cities = next((item['cities'] for item in self.countries_and_cities if item['state'] == selected_state), [])
        self.city_combobox['values'] = cities
        self.city_combobox.set("")

    def fetch_data(self):
        city = self.selected_city.get()

        if not city:
            messagebox.showerror("Błąd", "Proszę wybrać województwo i miasto.")
            return

        api_key = "fb9e5c164b6e64b6ea40f8d266f20499"  # OpenWeatherMap API
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},PL&limit=1&appid={api_key}"

        try:
            geo_response = requests.get(geocoding_url)
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            if not geo_data:
                messagebox.showerror("Błąd", "Nie znaleziono współrzędnych dla podanego miasta.")
                return

            lat, lon = geo_data[0]['lat'], geo_data[0]['lon']

            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
            pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            temperature = round(weather_data["main"]["temp"], 1)

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

            self.result_label.config(text=f"Temperatura: {temperature}°C\n\n{pollution_text}")

        except requests.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Aplikacja Jakości Powietrza")
    root.geometry("400x500")
    app = CarbonApp(root, None)
    app.pack(expand=True, fill="both")
    root.mainloop()
