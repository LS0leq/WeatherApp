import tkinter as tk
from tkinter import ttk, messagebox
import requests


class CarbonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wybierz województwo i miasto")
        self.root.geometry("1600x1900")

        self.selected_state = tk.StringVar()
        self.selected_city = tk.StringVar()

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

        self.create_widgets()

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

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def on_state_selected(self, event):
        selected_state = self.selected_state.get()
        cities = next((item['cities'] for item in self.countries_and_cities if item['state'] == selected_state), [])
        self.city_combobox['values'] = cities
        self.city_combobox.set("")

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
                result_text = (
                    f"AQI: {aqi} ({color})\n"
                    f"Temperatura: {weather['tp']}°C\n"
                    f"Wilgotność: {weather['hu']}%\n"
                    f"Ciśnienie: {weather['pr']} hPa\n"
                    f"Czas: {weather['ts']}"
                )
                self.result_label.config(text=result_text)
            else:
                messagebox.showerror("Błąd", "Brak danych dla wybranej lokalizacji.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

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
