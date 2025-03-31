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
            {"state": "Pomorskie", "cities": ["Gdańsk", "Gdynia", "Sopot"]},
            {"state": "Mazowieckie", "cities": ["Warszawa", "Radom"]},
            {"state": "Małopolskie", "cities": ["Kraków", "Zakopane"]}
        ]

        # Label i Combobox dla województwa
        tk.Label(self, text="Województwo:", bg='#87CEEB', font=('Arial', 14, 'bold')).pack(pady=5)
        self.state_combobox = ttk.Combobox(self, textvariable=self.selected_state, font=('Arial', 12))
        self.state_combobox['values'] = [item['state'] for item in self.countries_and_cities]
        self.state_combobox.bind("<<ComboboxSelected>>", self.on_state_selected)
        self.state_combobox.pack(pady=5)

        # Label i Combobox dla miasta
        tk.Label(self, text="Miasto:", bg='#87CEEB', font=('Arial', 14, 'bold')).pack(pady=5)
        self.city_combobox = ttk.Combobox(self, textvariable=self.selected_city, font=('Arial', 12))
        self.city_combobox.pack(pady=5)

        # Przycisk sprawdzający jakość powietrza
        tk.Button(self, text="Sprawdź jakość powietrza", command=self.fetch_data, font=('Arial', 14, 'bold'),
                  bg='#4682B4', fg='white').pack(pady=10)

        # Przycisk do przełączenia na mapę
        tk.Button(self, text="Przejdź do mapy", command=lambda: controller.show_frame("PollutionMapPage"),
                  font=('Arial', 14, 'bold'), bg='#32CD32', fg='white').pack(pady=10)

        # Wyniki jakości powietrza
        self.result_label = tk.Label(self, text="", bg='#FFFFFF', font=('Arial', 14), wraplength=350)
        self.result_label.pack(pady=5)

    def on_state_selected(self, event):
        """ Aktualizuje dostępne miasta na podstawie wybranego województwa """
        selected_state = self.selected_state.get()
        cities = next((item['cities'] for item in self.countries_and_cities if item['state'] == selected_state), [])
        self.city_combobox['values'] = cities
        self.city_combobox.set("")

    def fetch_data(self):
        """ Pobiera dane o jakości powietrza """
        city = self.selected_city.get()
        state = self.selected_state.get()

        if not city or not state:
            messagebox.showerror("Błąd", "Proszę wybrać województwo i miasto.")
            return

        api_url = f"http://api.airvisual.com/v2/city?city={city}&state={state}&country=POLAND&key=YOUR_API_KEY"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json().get('data', {})

            if data:
                aqi = data['current']['pollution']['aqius']
                self.result_label.config(text=f"AQI: {aqi}")
            else:
                messagebox.showerror("Błąd", "Brak danych dla tej lokalizacji.")
        except requests.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")
