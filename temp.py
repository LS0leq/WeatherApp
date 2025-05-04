import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import urllib.parse

from future.backports.datetime import timedelta


class CarbonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wybierz województwo i miasto")
        self.root.geometry("500x400")

        self.selected_state = tk.StringVar()
        self.selected_city = tk.StringVar()

        self.countries_and_cities = [
            {"country": "Polska", "state": "Pomorskie", "cities": ["Bytów", "Gdańsk", "Gdynia", "Kościerzyna", "Pogórze", "Sopot"]},
            {"country": "Polska", "state": "Mazowieckie", "cities": ["Warszawa", "Radom", "Płock"]},
            {"country": "Polska", "state": "Kujawsko-Pomorskie", "cities": ["Bydgoszcz", "Grudziądz", "Inowrocław", "Nakło nad Notecią", "Świecie", "Toruń", "Wilcze", "Włocławek"]},
            {"country": "Polska", "state": "Małopolskie", "cities": ["Kraków", "Muszyna", "Myslenice", "Niepolomice", "Nowy Targ", "Olkusz", "Rabka-Zdroj", "Sucha Beskidzka", "Uście Gorlickie", "Zabierzów", "Zaborze"]},
            {"country": "Polska", "state": "Łódzkie", "cities": ["Ksawerów", "Kutno", "Lask", "Łódź", "Pabianice", "Piotrków Trybunalski", "Radomsko", "Zgierz"]},
            {"country": "Polska", "state": "Lubelskie", "cities": ["Biała Podlaska", "Chełm", "Lublin", "Łódź", "Łuków", "Radzyń Podlaski", "Zamość"]},
            {"country": "Polska", "state": "Lubuskie", "cities": ["Lubsko", "Nowa Sól", "Olbrachcice", "Zielona Góra"]},
            {"country": "Polska", "state": "Opolskie", "cities": ["Lubsko", "Nowa Sól", "Olbrachcice", "Zielona Góra"]},
            {"country": "Polska", "state": "Podlasie", "cities": ["Białystok", "Grajewo", "Nowa Świdziałówka", "Suwałki"]},
            {"country": "Polska", "state": "Śląskie", "cities": ["Bielsko-Biała", "Goczałkowice-Zdrój", "Jastrzębie-Zdrój", "Katowice", "Lubliniec", "Międzybrodzie Żywieckie", "Orzesze", "Racibórz", "Rybnik", "Sosnicowice", "Sosnowiec", "Tychy", "Zawiercie"]},
            {"country": "Polska", "state": "Podkarpackie", "cities": ["Boguchwała", "Dębica", "Jarosław", "Krempna", "Krosno", "Mielec", "Nisko", "Przemyśl", "Rudna Wielka", "Rymanów-Zdrój", "Rzeszów", "Sanok", "Tarnobrzeg"]},
            {"country": "Polska", "state": "Świętokrzyskie", "cities": ["Kępie", "Kielce", "Łagów", "Małogoszcz", "Skarżysko-Kamienna", "Starachowice", "Wodzisław", "Wymysłów"]},
            {"country": "Polska", "state": "Warmińsko Mazurskie", "cities": ["Działdowo", "Ełk", "Gołdap", "Olsztyn", "Ostróda", "Wygryny"]},
            {"country": "Polska", "state": "Zachodnio Pomorskie", "cities": ["Darłowo", "Kołobrzeg", "Szczecin", "Szczecinek"]}
        ]

        self.state_to_api_mapping = {
            "Mazowieckie": "Mazovia",
            "Małopolskie": "Lesser%Poland%Voivodeship",
            "Pomorskie": "Pomerania",
            "Łódzkie": "Lodz%Voivodeship",
            "Lubelskie": "Lublin",
            "Lubuskie": "Lubusz",
            "Opolskie": "Opole%Voivodeship",
            "Śląskie": "Silesia",
            "Podkarpackie": "Subcarpathian%Voivodeship",
            "Świętokrzyskie": "Swietokrzyskie",
            "Warmińsko Mazurskie": "Warmia-Masuria",
            "Zachodnio Pomorskie": "West%Pomerania"
        }

        self.favorite_locations = []
        self.open_from_file()
        self.create_widgets()
        self.update_favorites_listbox()
        self.favorites_listbox.bind("<Double-Button-1>", self.selected_favorite)

    def save_to_file(self):
        with open("favorites.txt", "w") as f:
            f.write("\n".join(self.favorite_locations))

    def open_from_file(self):
        try:
            with open("favorites.txt") as f:
                self.favorite_locations = f.read().splitlines()
        except FileNotFoundError:
            self.favorite_locations = []

    def fetch_forecast_data(self):
        city = self.selected_city.get()
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        x=0
        current_Hour=int(now.strftime("%H"))


        if not city:
            messagebox.showerror("Błąd", "Proszę wybrać miasto.")
            return

        api_key = "YLN4LMRPLRV8HQF7KVCGC4MCK"
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{date}?key={api_key}&include=hours"


        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            hours = data["days"][0]["hours"]
            target=[
                f"{(current_Hour - 5):02d}:00:00",
                f"{(current_Hour - 4):02d}:00:00",
                f"{(current_Hour - 3):02d}:00:00",
                f"{(current_Hour - 2):02d}:00:00",
                f"{(current_Hour - 1):02d}:00:00",
                f"{current_Hour}:00:00"
            ]
            results=[]

            for hours_data in hours:
                if hours_data["datetime"] in target:
                    hoursData= hours_data
                    temp = hours_data .get("temp", "brak")
                    humidity = hours_data  .get("humidity", "brak")
                    conditions = hours_data .get("conditions", "brak")
                    results.append(f"{hoursData} - Temp: {temp}°C, Wilgotność: {humidity}%, Warunki: {conditions}")

            with open("weather_data.txt", "w") as f:
                for result in results:
                    f.write(result + "\n")

        except requests.exceptions.RequestException as e:
            messagebox.showerror(e)


    def create_widgets(self):
        self.state_label = tk.Label(self.root, text="Województwo:")
        self.state_label.pack()

        self.state_combobox = ttk.Combobox(self.root, textvariable=self.selected_state)
        self.state_combobox['values'] = [item['state'] for item in self.countries_and_cities]
        self.state_combobox.bind("<<ComboboxSelected>>", self.on_state_selected)
        self.state_combobox.pack()

        self.city_label = tk.Label(self.root, text="Miasto:")
        self.city_label.pack()

        self.city_combobox = ttk.Combobox(self.root, textvariable=self.selected_city)
        self.city_combobox.pack()

        self.search_button = tk.Button(self.root, text="Sprawdź jakość powietrza", command=self.fetch_data)
        self.search_button.pack()

        self.add_to_favorites_button = tk.Button(self.root, text="Dodaj do ulubionych", command=self.add_favorite)
        self.add_to_favorites_button.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        self.favorites_label = tk.Label(self.root, text="Ulubione lokalizacje:")
        self.favorites_label.pack()

        self.favorites_listbox = tk.Listbox(self.root, height=5, width=40)
        self.favorites_listbox.pack()
        self.delete_button = tk.Button(self.root, text="Usuń", command=self.delete_favorite)
        self.delete_button.pack()
        self.forecast_button=tk.Button(self.root, text="Sprawdź prognozę pogody(AI)", command=self.fetch_forecast_data)
        self.forecast_button.pack()
        self.update_favorites_listbox()
        self.favorites_listbox.bind("<Double-1>", self.selected_favorite)

    def on_state_selected(self, event):
        selected_state = self.selected_state.get()
        cities = next((item['cities'] for item in self.countries_and_cities if item['state'] == selected_state), [])
        self.city_combobox['values'] = cities
        self.city_combobox.set("")

    def add_favorite(self):
        state = self.selected_state.get()
        city = self.selected_city.get()

        try:
            with open("favorites.txt") as f:
                self.favorite_locations = f.read().splitlines()
        except FileNotFoundError:
            self.favorite_locations = []

        if(f"{state}, {city}" in self.favorite_locations):
            messagebox.showwarning("Błąd", "Lokalizacja jest już na liście ulubionych.")
            return
        else:
            if state and city:

                self.favorite_locations.append(f"{state}, {city}")
                self.update_favorites_listbox()
                self.save_to_file()
                messagebox.showinfo("Sukces", f"Lokalizacja {state}, {city} została dodana do ulubionych.")
            else:
                messagebox.showwarning("Błąd", "Proszę wybrać zarówno województwo, jak i miasto.")



    def update_favorites_listbox(self):
        self.favorites_listbox.delete(0, tk.END)
        for location in self.favorite_locations:
            self.favorites_listbox.insert(tk.END, location)

    def selected_favorite(self, event):
        selected = self.favorites_listbox.curselection()
        if selected:
            location = self.favorite_locations[selected[0]]
            state, city = location.split(", ")
            self.selected_state.set(state)
            self.selected_city.set(city)

    def fetch_data(self):
        city = self.selected_city.get()
        state = self.selected_state.get()
        if not city or not state:
            messagebox.showerror("Błąd", "Proszę wybrać województwo i miasto.")
            return

        state_code = self.state_to_api_mapping.get(state, state)
        if city == "Warszawa":
            city = "Warsaw"

        api_url = f"http://api.airvisual.com/v2/city?city={city}&state={state_code}&country=POLAND&key=102d3598-ce56-4825-a71b-60d520a6535e"

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json().get('data')

            if data:
                aqi = data['current']['pollution']['aqius']
                color = self.get_color_based_on_aqi(aqi)
                weather = data['current']['weather']
                time = weather['ts']
                dt = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
                date_only = dt.date()
                result_text = (
                    f"AQI: {aqi} ({color})\n"
                    f"Temperatura: {weather['tp']}°C\n"
                    f"Wilgotność: {weather['hu']}%\n"
                    f"Ciśnienie: {weather['pr']} hPa\n"
                    f"Data: {date_only}"
                )
                self.result_label.config(text=result_text)
            else:
                messagebox.showerror("Błąd", "Brak danych dla wybranej lokalizacji.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

    def delete_favorite(self):
        selected = self.favorites_listbox.curselection()
        if selected:
            location = self.favorite_locations[selected[0]]
            self.favorite_locations.remove(location)
            self.update_favorites_listbox()
            self.save_to_file()
            messagebox.showinfo("Sukces", f"Lokalizacja {location} została usunięta z ulubionych.")
        else:
            messagebox.showwarning("Błąd", "Proszę wybrać lokalizację do usunięcia.")
    def get_color_based_on_aqi(self, aqi):
        if aqi <= 50:
            return "green"
        elif aqi <= 100:
            return "yellow"
        elif aqi <= 150:
            return "orange"
        elif aqi <= 200:
            return "red"
        else:
            return "dark"


if __name__ == "__main__":
    root = tk.Tk()
    app = CarbonApp(root)
    root.mainloop()
