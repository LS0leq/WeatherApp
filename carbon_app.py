import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

FILENAME = "favorite_locations.json"

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
        if wind_speed > 20:
            return "Zaleca się krótki spacer, ale ubierz się ciepło, aby uniknąć wychłodzenia."
        return "Idealna pogoda na spacer lub krótki bieg."
    elif 10 < temperature <= 20:
        if wind_speed > 20:
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

class CarbonApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#ADD8E6')

        self.selected_state = tk.StringVar()
        self.selected_city = tk.StringVar()
        self.favorite_locations = self.load_favorite_locations()

        self.countries_and_cities = [
            {"country": "Polska", "state": "Pomorskie",
             "cities": ["Bytów", "Gdańsk", "Gdynia", "Kościerzyna", "Pogórze", "Sopot"]},
            {"country": "Polska", "state": "Mazowieckie", "cities": ["Warszawa", "Radom", "Płock"]},
            {"country": "Polska", "state": "Kujawsko-Pomorskie",
             "cities": ["Bydgoszcz", "Grudziądz", "Inowrocław", "Nakło nad Notecią", "Świecie", "Toruń", "Wilcze",
                        "Włocławek"]},
            {"country": "Polska", "state": "Małopolskie",
             "cities": ["Kraków", "Muszyna", "Myslenice", "Niepolomice", "Nowy Targ", "Olkusz", "Rabka-Zdroj",
                        "Sucha Beskidzka", "Uście Gorlickie", "Zabierzów", "Zaborze"]},
            {"country": "Polska", "state": "Łódzkie",
             "cities": ["Ksawerów", "Kutno", "Lask", "Łódź", "Pabianice", "Piotrków Trybunalski", "Radomsko",
                        "Zgierz"]},
            {"country": "Polska", "state": "Lubelskie",
             "cities": ["Biała Podlaska", "Chełm", "Lublin", "Łódź", "Łuków", "Radzyń Podlaski", "Zamość"]},
            {"country": "Polska", "state": "Lubuskie", "cities": ["Lubsko", "Nowa Sól", "Olbrachcice", "Zielona Góra"]},
            {"country": "Polska", "state": "Opolskie", "cities": ["Lubsko", "Nowa Sól", "Olbrachcice", "Zielona Góra"]},
            {"country": "Polska", "state": "Podlasie",
             "cities": ["Białystok", "Grajewo", "Nowa Świdziałówka", "Suwałki"]},
            {"country": "Polska", "state": "Śląskie",
             "cities": ["Bielsko-Biała", "Goczałkowice-Zdrój", "Jastrzębie-Zdrój", "Katowice", "Lubliniec",
                        "Międzybrodzie Żywieckie", "Orzesze", "Racibórz", "Rybnik", "Sosnicowice", "Sosnowiec", "Tychy",
                        "Zawiercie"]},
            {"country": "Polska", "state": "Podkarpackie",
             "cities": ["Boguchwała", "Dębica", "Jarosław", "Krempna", "Krosno", "Mielec", "Nisko", "Przemyśl",
                        "Rudna Wielka", "Rymanów-Zdrój", "Rzeszów", "Sanok", "Tarnobrzeg"]},
            {"country": "Polska", "state": "Świętokrzyskie",
             "cities": ["Kępie", "Kielce", "Łagów", "Małogoszcz", "Skarżysko-Kamienna", "Starachowice", "Wodzisław",
                        "Wymysłów"]},
            {"country": "Polska", "state": "Warmińsko Mazurskie",
             "cities": ["Działdowo", "Ełk", "Gołdap", "Olsztyn", "Ostróda", "Wygryny"]},
            {"country": "Polska", "state": "Zachodnio Pomorskie",
             "cities": ["Darłowo", "Kołobrzeg", "Szczecin", "Szczecinek"]}
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

        tk.Label(self, text="Województwo:", bg='#87CEEB', font=('Arial', 14, 'bold')).pack(pady=5)
        self.state_combobox = ttk.Combobox(self, textvariable=self.selected_state, font=('Arial', 12))
        self.state_combobox['values'] = [item['state'] for item in self.countries_and_cities]
        self.state_combobox.bind("<<ComboboxSelected>>", self.on_state_selected)
        self.state_combobox.pack(pady=5)

        tk.Label(self, text="Miasto:", bg='#87CEEB', font=('Arial', 14, 'bold')).pack(pady=5)
        self.city_combobox = ttk.Combobox(self, textvariable=self.selected_city, font=('Arial', 12))
        self.city_combobox.pack(pady=5)

        tk.Button(self, text="Sprawdź pogodę", command=self.fetch_data, font=('Arial', 14, 'bold'),
                  bg='#4682B4', fg='white').pack(pady=10)

        self.result_label = tk.Label(self, text="", bg='#FFFFFF', font=('Arial', 14), wraplength=350)
        self.result_label.pack(pady=5)

        tk.Button(self, text="Zapisz lokalizację", command=self.save_favorite_location, font=('Arial', 12, 'bold'),
                  bg='#4682B4', fg='white').pack(pady=5)

        tk.Label(self, text="Ulubione lokalizacje:", bg='#87CEEB', font=('Arial', 14, 'bold')).pack(pady=5)
        self.fav_locations_combobox = ttk.Combobox(self, font=('Arial', 12))
        self.fav_locations_combobox['values'] = [f"{loc['state']}, {loc['city']}" for loc in self.favorite_locations]
        self.fav_locations_combobox.bind("<<ComboboxSelected>>", self.on_favorite_selected)
        self.fav_locations_combobox.pack(pady=5)

        # Przycisk usuwania ulubionej lokalizacji
        tk.Button(self, text="Usuń lokalizację", command=self.remove_favorite_location, font=('Arial', 12, 'bold'),
                  bg='#B22222', fg='white').pack(pady=5)

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

        api_key = "fb9e5c164b6e64b6ea40f8d266f20499"
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},PL&limit=1&appid={api_key}"

        try:
            geo_response = requests.get(geocoding_url)
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            if not geo_data:
                messagebox.showerror("Błąd", "Nie znaleziono współrzędnych dla podanego miasta.")
                return

            lat, lon = geo_data[0]['lat'], geo_data[0]['lon']

            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']

            outfit_suggestion = get_outfit_suggestion(temperature)
            activity_suggestion = get_activity_suggestion(temperature, wind_speed)
            hazard_suggestion = get_hazard_suggestion(temperature, humidity, wind_speed)

            weather_info = (f"Temperatura: {temperature}°C\n"
                            f"Wilgotność: {humidity}%\n"
                            f"Wiatr: {wind_speed} m/s\n\n"
                            f"Ubiór: {outfit_suggestion}\n"
                            f"Aktywność: {activity_suggestion}\n"
                            f"Zagrożenia: {hazard_suggestion}")

            self.result_label.config(text=weather_info)

        except requests.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

    def save_favorite_location(self):
        location = {"state": self.selected_state.get(), "city": self.selected_city.get()}
        self.favorite_locations.append(location)
        with open(FILENAME, "w") as file:
            json.dump(self.favorite_locations, file)
        self.fav_locations_combobox['values'] = [f"{loc['state']}, {loc['city']}" for loc in self.favorite_locations]
        messagebox.showinfo("Sukces", "Lokalizacja zapisana!")

    def load_favorite_locations(self):
        try:
            with open(FILENAME, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def on_favorite_selected(self, event):
        selected = self.fav_locations_combobox.get()
        state, city = selected.split(", ")
        self.selected_state.set(state)
        self.on_state_selected(None)
        self.selected_city.set(city)

    def remove_favorite_location(self):
        """ Funkcja usuwająca wybraną lokalizację z listy ulubionych i pliku """
        selected_location = self.fav_locations_combobox.get()

        if selected_location:
            state, city = selected_location.split(", ")
            # Usuwamy lokalizację z listy
            self.favorite_locations = [loc for loc in self.favorite_locations if not (loc['state'] == state and loc['city'] == city)]

            # Zapisujemy zaktualizowaną listę do pliku
            with open(FILENAME, "w") as file:
                json.dump(self.favorite_locations, file)

            # Aktualizujemy combobox z ulubionymi lokalizacjami
            self.fav_locations_combobox['values'] = [f"{loc['state']}, {loc['city']}" for loc in self.favorite_locations]

            messagebox.showinfo("Sukces", f"Lokalizacja '{selected_location}' została usunięta.")
        else:
            messagebox.showwarning("Brak lokalizacji", "Proszę wybrać lokalizację do usunięcia.")
