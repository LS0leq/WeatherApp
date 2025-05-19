import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime, timedelta
import pandas as pd
import re
from dotenv import load_dotenv
from urllib.parse import quote





def get_outfit_suggestion(temperature):
    if temperature <= 0:
        return "Ciepły płaszcz, szalik, czapka, rękawiczki."
    elif 0 < temperature <= 10:
        return "Kurtka zimowa lub ciepły sweter."
    elif 10 < temperature <= 20:
        return "Lekka kurtka lub bluza."
    elif 20 < temperature <= 30:
        return "T-shirt, lekka odzież."
    else:
        return "Woda, krem z filtrem, lekkie ubrania."


def get_activity_suggestion(temperature, wind_speed):
    if temperature <= 0:
        return "Zaleca się unikanie długich spacerów na zewnątrz. Możesz rozważyć aktywności w zamkniętych pomieszczeniach."
    elif 0 < temperature <= 10:
        if wind_speed > 5:
            return "Zaleca się krótki spacer, ale ubierz się ciepło, aby uniknąć wychłodzenia."
        return "Idealna pogoda na spacer lub krótki bieg."
    elif 10 < temperature <= 20:
        if wind_speed > 5:
            return "Możesz uprawiać różne aktywności na świeżym powietrzu, ale bądź przygotowany na silny wiatr."
        return "Idealna pogoda na spacer, jogging lub jazdę na rowerze."
    elif 20 < temperature <= 30:
        return "Idealna pogoda na aktywności na świeżym powietrzu: spacer, jogging, rower."
    else:
        return "Możesz uprawiać aktywności na świeżym powietrzu, ale pamiętaj o odpowiedniej ochronie przed słońcem."


def get_hazard_suggestion(temperature, humidity, wind_speed):
    if temperature <= 0:
        return "Zimno, możliwe oblodzenia. Uważaj na śliskie drogi."
    elif 0 < temperature <= 10:
        return "Chłodno, możliwe przymrozki. Uważaj na wypadki na drodze."
    elif 10 < temperature <= 20:
        if wind_speed > 20:
            return "Wiatr może być silny, bądź ostrożny na zewnątrz."
        return "Brak zagrożeń. Warto korzystać z pogody."
    elif 20 < temperature <= 30:
        if humidity > 70:
            return "Wysoka wilgotność może powodować dyskomfort. Pamiętaj o nawadnianiu organizmu."
        return "Brak zagrożeń. Ciesz się pogodą!"
    else:
        return "Wysokie temperatury. Pamiętaj o ochronie przed słońcem."


load_dotenv()

class CarbonApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.check_api_keys()

        self.selected_state = tk.StringVar()
        self.selected_city = tk.StringVar()

        self.countries_and_cities = [
            {"country": "Polska", "state": "Pomorskie",
             "cities": ["Bytow", "Gdansk", "Gdynia", "Koscierzyna", "Pogorze", "Sopot"]},
            {"country": "Polska", "state": "Mazowieckie", "cities": ["Warszawa", "Radom", "Plock"]},
            {"country": "Polska", "state": "Kujawsko-Pomorskie",
             "cities": ["Bydgoszcz", "Grudziadz", "Inowroclaw", "Naklo nad Notecia", "Swiecie", "Torun", "Wilcze",
                        "Wloclawek"]},
            {"country": "Polska", "state": "Małopolskie",
             "cities": ["Krakow", "Muszyna", "Myslenice", "Niepolomice", "Nowy Targ", "Olkusz", "Rabka-Zdroj",
                        "Sucha Beskidzka", "Uscie Gorlickie", "Zabierzow", "Zaborze"]},
            {"country": "Polska", "state": "Łódzkie",
             "cities": ["Ksawerow", "Kutno", "Lask", "Lodz", "Pabianice", "Piotrkow Trybunalski", "Radomsko",
                        "Zgierz"]},
            {"country": "Polska", "state": "Lubelskie",
             "cities": ["Biala Podlaska", "Chelm", "Lublin", "Lodz", "Lukow", "Radzyn Podlaski", "Zamosc"]},
            {"country": "Polska", "state": "Lubuskie", "cities": ["Lubsko", "Nowa Sol", "Olbrachcice", "Zielona Gora"]},
            {"country": "Polska", "state": "Opolskie", "cities": ["Lubsko", "Nowa Sol", "Olbrachcice", "Zielona Gora"]},
            {"country": "Polska", "state": "Podlasie",
             "cities": ["Bialystok", "Grajewo", "Nowa Swidzialowka", "Suwalki"]},
            {"country": "Polska", "state": "Śląskie",
             "cities": ["Bielsko-Biala", "Goczalkowice-Zdroj", "Jastrzebie-Zdroj", "Katowice", "Lubliniec",
                        "Miedzybrodzie Zywieckie", "Orzesze", "Raciborz", "Rybnik", "Sosnicowice", "Sosnowiec", "Tychy",
                        "Zawiercie"]},
            {"country": "Polska", "state": "Podkarpackie",
             "cities": ["Boguchwala", "Debica", "Jaroslaw", "Krempna", "Krosno", "Mielec", "Nisko", "Przemysl",
                        "Rudna Wielka", "Rymanow-Zdroj", "Rzeszow", "Sanok", "Tarnobrzeg"]},
            {"country": "Polska", "state": "Świętokrzyskie",
             "cities": ["Kepie", "Kielce", "Lagow", "Malogoszcz", "Skarzysko-Kamienna", "Starachowice", "Wodzislaw",
                        "Wymyslow"]},
            {"country": "Polska", "state": "Warmińsko Mazurskie",
             "cities": ["Dzialdowo", "Elk", "Goldap", "Olsztyn", "Ostroda", "Wygryny"]},
            {"country": "Polska", "state": "Zachodnio Pomorskie",
             "cities": ["Darlowo", "Kolobrzeg", "Szczecin", "Szczecinek"]}
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
        self.aiPred = "Prognoza AI: brak danych"

        self.favorite_locations = []
        self.open_from_file()
        self.create_widgets()
        self.update_favorites_listbox()
        self.favorites_listbox.bind("<Double-Button-1>", self.selected_favorite)

    def check_api_keys(self):
        """Sprawdź czy klucze API są dostępne"""
        required_keys = {
            'VISUALCROSSING_API_KEY': 'Visual Crossing Weather',
            'AIRVISUAL_API_KEY': 'AirVisual'
        }

        missing_keys = []
        for key, service in required_keys.items():
            if not os.getenv(key):
                missing_keys.append(service)

        if missing_keys:
            messagebox.showerror(
                "Błąd konfiguracji",
                f"Brak kluczy API dla następujących serwisów: {', '.join(missing_keys)}\n"
                "Sprawdź plik .env"
            )
            self.destroy()
    def save_to_file(self):
        with open("favorites.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(self.favorite_locations))
    def generate(self):
        try:
            x=1
            with open("weather_data.txt", "r") as file:
                lines = file.readlines()

            if len(lines) == 0:
                messagebox.showwarning("Błąd", "Plik weather_data.txt jest pusty.")
                return

            temperatures = []

            for line in lines:
                match = re.search(r"Temp: ([\d.]+)", line)
                if match:
                    temp = float(match.group(1))
                    temperatures.append(temp)


            if len(temperatures) < 7:
                raise ValueError("Za mało danych pogodowych (minimum 7 temperatur potrzebne)")

            rows = []
            for i in range(len(temperatures) - 6):
                row = temperatures[i:i + 8]
                rows.append(row)


            columns = ['t-6','t-5', 't-4', 't-3', 't-2', 't-1', 't', 't+1']
            df = pd.DataFrame(rows, columns=columns)

            df.to_csv("ml_dataset.csv", index=False)



        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd przy generowaniu datasetu: {str(e)}")
    def open_from_file(self):
        try:
            try:
                with open("favorites.txt", encoding='utf-8') as f:
                    self.favorite_locations = f.read().splitlines()
            except UnicodeDecodeError:
                for encoding in ['cp1250', 'iso-8859-2', 'windows-1250']:
                    try:
                        with open("favorites.txt", encoding=encoding) as f:
                            self.favorite_locations = f.read().splitlines()
                        break
                    except UnicodeDecodeError:
                        continue
        except FileNotFoundError:
            self.favorite_locations = []
    def fetch_forecast_data(self):
        import pickle
        import pandas as pd
        from pathlib import Path
        import sys
        city = self.selected_city.get()
        now = datetime.now()
        current_Hour = int(now.strftime("%H"))
        weather_data = []
        api_key = os.getenv('VISUALCROSSING_API_KEY')


        if not city:
            messagebox.showerror("Błąd", "Proszę wybrać miasto.")
            return

        for day_offset in range(4):
            date = (datetime.now() - timedelta(days=day_offset)).strftime("%Y-%m-%d")
            url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{date}?key={api_key}&include=hours"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                hours = data["days"][0]["hours"]
                target = [
                    f"{(current_Hour - 6):02d}:00:00",
                    f"{(current_Hour - 5):02d}:00:00",
                    f"{(current_Hour - 4):02d}:00:00",
                    f"{(current_Hour - 3):02d}:00:00",
                    f"{(current_Hour - 2):02d}:00:00",
                    f"{(current_Hour - 1):02d}:00:00",
                    f"{current_Hour}:00:00"
                ]

                temps = []
                for hour_data in hours:
                    if hour_data["datetime"] in target:
                        temp = hour_data.get("temp", "brak")
                        humidity = hour_data.get("humidity", "brak")
                        conditions = hour_data.get("conditions", "brak")
                        temps.append(temp)
                        weather_data.append({
                            "date": date,
                            "time": hour_data["datetime"],
                            "temperature": temp,
                            "humidity": humidity,
                            "conditions": conditions
                        })

                if len(temps) == 7:
                    df = pd.DataFrame([temps], columns=[f"t-{6 - i}" for i in range(7)])
                    df["date"] = date
                    df.to_csv("ml_dataset.csv", mode='a', header=not os.path.exists("ml_dataset.csv"), index=False)


            except requests.exceptions.RequestException as e:
                print(f"Nie udało się pobrać danych dla {date}: {e}")
            with open("weather_data.txt", "w") as f:
                for data in weather_data:
                    f.write(
                        f"{data['date']} {data['time']} - Temp: {((data['temperature'])-32)/1.8}°C, Wilgotność: {data['humidity']}%, Warunki: {data['conditions']}\n")

        self.generate()

        try:
            subprocess.run([sys.executable, 'trainAI.py'], check=True)
            if len(temps) >= 6 and Path("model.pkl").exists():
                with open("model.pkl", "rb") as f:
                    model = pickle.load(f)

                df = pd.DataFrame(
                    [temps],
                    columns=[f"t" if (6 - i) == 0 else f"t-{6 - i}" for i in range(len(temps))]
                )
                with open("pred.txt", "r") as file:
                    predAI = file.readlines()
                    predAI = str(round(float(predAI[0]), 1))


                self.aiPred = f"Prognozowana temperatura za godzinę: {predAI}°C"
                self.ai.config(text=self.aiPred)

            elif not Path("model.pkl").exists():
                messagebox.showwarning("AI", "Brak modelu AI. Wytrenuj najpierw model (plik model.pkl).")
            else:
                messagebox.showwarning("AI", "Brak wystarczających danych pogodowych do prognozy.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas trenowania modelu: {e}")
    def create_widgets(self):
        self.state_label = tk.Label(self, text="Województwo:")
        self.state_label.pack()

        self.state_combobox = ttk.Combobox(self, textvariable=self.selected_state)
        self.state_combobox['values'] = [item['state'] for item in self.countries_and_cities]
        self.state_combobox.bind("<<ComboboxSelected>>", self.on_state_selected)
        self.state_combobox.pack()

        self.city_label = tk.Label(self, text="Miasto:")
        self.city_label.pack()

        self.city_combobox = ttk.Combobox(self, textvariable=self.selected_city)
        self.city_combobox.pack()

        self.search_button = tk.Button(self, text="Sprawdź jakość powietrza", command=self.fetch_data)
        self.search_button.pack()

        self.add_to_favorites_button = tk.Button(self, text="Dodaj do ulubionych", command=self.add_favorite)
        self.add_to_favorites_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        self.favorites_label = tk.Label(self, text="Ulubione lokalizacje:")
        self.favorites_label.pack()

        self.favorites_listbox = tk.Listbox(self, height=5, width=40)
        self.favorites_listbox.pack()
        self.delete_button = tk.Button(self, text="Usuń", command=self.delete_favorite)
        self.delete_button.pack()
        self.forecast_button=tk.Button(self, text="Sprawdź prognozę pogody(AI)", command=self.fetch_forecast_data)
        self.forecast_button.pack()
        self.update_favorites_listbox()
        self.favorites_listbox.bind("<Double-1>", self.selected_favorite)
        self.ai = tk.Label(self, text=self.aiPred)
        self.ai.pack()
    def on_state_selected(self, event):
        selected_state = self.selected_state.get()
        cities = next((item['cities'] for item in self.countries_and_cities if item['state'] == selected_state), [])
        self.city_combobox['values'] = cities
        self.city_combobox.set("")
    def add_favorite(self):
        state = self.selected_state.get()
        city = quote(self.selected_city.get())

        try:
            with open("favorites.txt", encoding="utf-8") as f:
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
        api_key = os.getenv('AIRVISUAL_API_KEY')

        if not city or not state:
            messagebox.showerror("Błąd", "Proszę wybrać województwo i miasto.")
            return

        state_code = self.state_to_api_mapping.get(state, state)
        if city == "Warszawa":
            city = "Warsaw"

        api_url = f"https://api.airvisual.com/v2/city?city={city}&state={state_code}&country=POLAND&key={api_key}"
        print(api_url)

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
                outfit = get_outfit_suggestion(weather['tp'])
                act = get_activity_suggestion(weather['tp'],weather['ws'])
                hazard = get_hazard_suggestion(weather['tp'],weather['hu'],weather['ws'])
                result_text = (
                    f"Data: {date_only}\n"
                    f"AQI: {aqi} ({color})\n"
                    f"Temperatura: {weather['tp']}°C\n"
                    f"Wilgotność: {weather['hu']}%\n"
                    f"Ciśnienie: {weather['pr']} hPa\n"
                    f"Proponowany ubiór: {outfit}\n"
                    f"Proponowana aktywność: {act}\n"
                    f"Możliwe zagrożenia: {hazard}\n"
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




# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Aplikacja Pogodowa")
    root.geometry("400x600")
    app = CarbonApp(root)
    app.pack(expand=True, fill="both")
    root.mainloop()
