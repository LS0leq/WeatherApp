import tkinter as tk
from tkinter import ttk, messagebox
import requests


class CarbonApp:
    def __init__(self, root):
        # Inicjalizacja głównego okna aplikacji
        self.root = root
        self.root.title("Wybierz województwo i miasto")
        self.root.geometry("1600x1900")
        self.root.configure(bg='#ADD8E6')  # Kolor tła

        # Zmienne do przechowywania wybranego województwa i miasta
        self.selected_state = tk.StringVar()
        self.selected_city = tk.StringVar()

        # Lista województw, miast oraz mapowanie do API
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

        # Mapa województw na odpowiedniki API
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

        # Tworzenie elementów interfejsu
        self.create_widgets()

    def create_widgets(self):
        """
        Tworzenie widgetów aplikacji, takich jak etykiety, comboboxy i przyciski.
        """
        # Stylizacja etykiet
        label_style = {'bg': '#87CEEB', 'font': ('Arial', 14, 'bold')}

        # Etykieta i combobox dla województwa
        self.state_label = tk.Label(self.root, text="Województwo:", **label_style)
        self.state_label.pack(pady=(10, 5))

        self.selected_state = tk.StringVar()
        self.state_combobox = ttk.Combobox(self.root, textvariable=self.selected_state, font=('Arial', 12))
        self.state_combobox['values'] = [item['state'] for item in self.countries_and_cities]  # Lista województw
        self.state_combobox.bind("<<ComboboxSelected>>", self.on_state_selected)  # Obsługa wyboru województwa
        self.state_combobox.pack(pady=5)

        # Etykieta i combobox dla miasta
        self.city_label = tk.Label(self.root, text="Miasto:", **label_style)
        self.city_label.pack(pady=(10, 5))

        self.selected_city = tk.StringVar()
        self.city_combobox = ttk.Combobox(self.root, textvariable=self.selected_city, font=('Arial', 12))
        self.city_combobox.pack(pady=5)

        # Przycisk do sprawdzenia jakości powietrza
        self.search_button = tk.Button(self.root, text="Sprawdź jakość powietrza", command=self.fetch_data,
                                       font=('Arial', 14, 'bold'), bg='#4682B4', fg='white', padx=12, pady=8)
        self.search_button.pack(pady=15)

        # Etykieta dla wyników, początkowo ukryta
        self.result_label = tk.Label(self.root, text="", bg='#FFFFFF', font=('Arial', 14), wraplength=350, bd=2,
                                     relief="solid", padx=12, pady=12)
        self.result_label.pack(pady=5)
        self.result_label.pack_forget()  # Ukrywanie etykiety na początku

    def on_state_selected(self, event):
        """
        Funkcja wywoływana po wybraniu województwa.
        Zmienia dostępne miasta w zależności od wybranego województwa.
        """
        selected_state = self.selected_state.get()  # Pobranie wybranego województwa
        cities = next((item['cities'] for item in self.countries_and_cities if item['state'] == selected_state), [])
        self.city_combobox['values'] = cities  # Ustawienie dostępnych miast
        self.city_combobox.set("")  # Resetowanie wyboru miasta

    def fetch_data(self):
        """
        Funkcja pobiera dane z API AirVisual o jakości powietrza
        dla wybranego miasta i województwa.
        """
        city = self.selected_city.get()
        state = self.selected_state.get()

        # Sprawdzanie, czy wybrano województwo i miasto
        if not city or not state:
            messagebox.showerror("Błąd", "Proszę wybrać województwo i miasto.")
            return

        # Mapowanie województwa na kod zgodny z API
        state_code = self.state_to_api_mapping.get(state, state)

        # Specjalna obsługa dla Warszawy (zmiana na "Warsaw")
        if city == "Warszawa":
            city = "Warsaw"

        # Tworzenie URL do API z danymi o jakości powietrza
        api_url = f"http://api.airvisual.com/v2/city?city={city}&state={state_code}&country=POLAND&key=102d3598-ce56-4825-a71b-60d520a6535e"

        try:
            # Wysyłanie zapytania do API
            response = requests.get(api_url)
            response.raise_for_status()  # Sprawdzanie statusu odpowiedzi

            # Przetwarzanie danych z odpowiedzi
            data = response.json().get('data')

            if data:
                # Pobieranie danych o jakości powietrza
                aqi = data['current']['pollution']['aqius']  # Indeks jakości powietrza
                color = self.get_color_based_on_aqi(aqi)  # Kolor w zależności od AQI
                weather = data['current']['weather']  # Dane o pogodzie

                # Tworzenie tekstu z wynikami
                result_text = (
                    f"AQI: {aqi} ({color})\n"
                    f"Temperatura: {weather['tp']}°C\n"
                    f"Wilgotność: {weather['hu']}%\n"
                    f"Ciśnienie: {weather['pr']} hPa\n"
                    f"Czas: {weather['ts']}"
                )

                # Wyświetlanie wyników
                self.result_label.config(text=result_text)
                self.result_label.pack(pady=5)  # Pokazanie etykiety z wynikami
            else:
                # Obsługa przypadku, gdy brak danych
                messagebox.showerror("Błąd", "Brak danych dla wybranej lokalizacji.")
        except requests.exceptions.RequestException as e:
            # Obsługa błędów połączenia
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

    def get_color_based_on_aqi(self, aqi):
        """
        Funkcja zwraca kolor na podstawie wartości AQI.
        """
        if aqi <= 50:
            return "green"
        elif aqi <= 100:
            return "yellow"
        elif aqi <= 150:
            return "orange"
        elif aqi <= 200:
            return "red"
        else:
            return "dark"  # Kolor dla złej jakości powietrza


if __name__ == "__main__":
    root = tk.Tk()  # Tworzenie głównego okna aplikacji
    app = CarbonApp(root)  # Inicjalizacja aplikacji
    root.mainloop()  # Uruchomienie głównej pętli aplikacji
