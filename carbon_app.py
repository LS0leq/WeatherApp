import tkinter as tk
from tkinter import Frame, Label, Button, ttk, messagebox
import requests, os

class CarbonApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#ADD8E6')  # Początkowe ustawienie tła na jasny niebieski
        self.controller = controller
        self.controller.current_theme = "light"
        self.selected_state = tk.StringVar()  # Zmienna do przechowywania wybranego województwa
        self.selected_city = tk.StringVar()  # Zmienna do przechowywania wybranego miasta

        # Lista województw i miast
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

        # Lista ulubionych lokalizacji
        self.favorites = []

        def toggle_theme(self):
            """ Funkcja zmieniająca motyw na przeciwny """
            if self.controller.current_theme == "dark":
                self.controller.current_theme = "light"
            else:
                self.controller.current_theme = "dark"
            self.controller.set_theme(self.controller.current_theme)

        def set_theme(self, theme):
            """ Funkcja ustawiająca motyw aplikacji """
            bg_color = '#333333' if theme == "dark" else '#ADD8E6'
            fg_color = '#FFFFFF' if theme == "dark" else '#000000'
            widget_bg_color = '#444444' if theme == "dark" else '#FFFFFF'

            self.configure(bg=bg_color)  # Ustawienie tła aplikacji
            for widget in self.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.configure(bg=bg_color)
                elif isinstance(widget, tk.Label):
                    widget.configure(bg=widget_bg_color, fg=fg_color)
                elif isinstance(widget, tk.Button):
                    widget.configure(bg=widget_bg_color, fg=fg_color)
                elif isinstance(widget, ttk.Combobox):
                    widget.configure(background=widget_bg_color, foreground=fg_color)

            self.result_frame.config(bg=widget_bg_color, bd=2, relief="solid", padx=10, pady=10)
            self.result_label.config(bg=widget_bg_color, fg=fg_color)
            self.clothing_advice_label.config(bg=widget_bg_color, fg=fg_color)

        # Główny kontener aplikacji (ramka), która będzie zawierała wszystkie elementy
        main_frame = tk.Frame(self, bg='#ADD8E6')
        main_frame.pack(expand=True, fill="both", anchor="center")

        # Wyświetlanie etykiety dla województwa
        tk.Label(main_frame, text="Województwo:", bg='#87CEEB', font=('Arial', 14, 'bold')).pack(pady=5)

        # Combobox do wyboru województwa
        self.state_combobox = ttk.Combobox(main_frame, textvariable=self.selected_state, font=('Arial', 12))
        self.state_combobox['values'] = [item['state'] for item in self.countries_and_cities]  # Lista województw
        self.state_combobox.bind("<<ComboboxSelected>>",
                                 self.on_state_selected)  # Po wybraniu województwa, aktualizuje miasta
        self.state_combobox.pack(pady=5)

        # Wyświetlanie etykiety dla miasta
        tk.Label(main_frame, text="Miasto:", bg='#87CEEB', font=('Arial', 14, 'bold')).pack(pady=5)

        # Combobox do wyboru miasta
        self.city_combobox = ttk.Combobox(main_frame, textvariable=self.selected_city, font=('Arial', 12))
        self.city_combobox.pack(pady=5)

        # Przycisk do dodania wybranego miasta do ulubionych
        tk.Button(main_frame, text="Dodaj do ulubionych", command=self.add_to_favorites, font=('Arial', 12, 'bold'),
                  bg='#4682B4', fg='white').pack(pady=5)

        # Etykieta dla ulubionych lokalizacji
        tk.Label(main_frame, text="Ulubione lokalizacje:", bg='#87CEEB', font=('Arial', 14, 'bold')).pack(pady=5)

        # Combobox do wybrania ulubionej lokalizacji
        self.favorites_combobox = ttk.Combobox(main_frame, font=('Arial', 12))
        self.favorites_combobox['values'] = self.favorites  # Lista ulubionych miast
        self.favorites_combobox.bind("<<ComboboxSelected>>",
                                     self.on_favorite_selected)  # Po wybraniu lokalizacji, automatycznie pobiera dane
        self.favorites_combobox.pack(pady=5)

        # Przycisk do usunięcia wybranego miasta z ulubionych
        tk.Button(main_frame, text="Usuń z ulubionych", command=self.remove_from_favorites, font=('Arial', 12, 'bold'),
                  bg='#4682B4', fg='white').pack(pady=5)

        # Przycisk do zmiany motywu
        self.theme_button = tk.Button(main_frame, text="Zmień motyw", command=self.toggle_theme,
                                      font=('Arial', 12, 'bold'), bg='#4682B4', fg='white')
        self.theme_button.pack(pady=10)

        # Przycisk do sprawdzenia jakości powietrza i pogody
        self.weather_button = tk.Button(main_frame, text="Sprawdź jakość powietrza", command=self.fetch_data,
                                        font=('Arial', 14, 'bold'), bg='#4682B4', fg='white')
        self.weather_button.pack(pady=10)

        # Ramka na wyniki (pogoda i jakość powietrza), początkowo ukryta
        self.result_frame = tk.Frame(main_frame, bg='#FFFFFF', bd=2, relief="solid", padx=10, pady=10)
        self.result_frame.pack_forget()  # Ukrycie ramki na początku

        # Etykieta do wyświetlania wyników pogody i jakości powietrza
        self.result_label = tk.Label(self.result_frame, text="", bg='#FFFFFF', font=('Arial', 14), wraplength=350)
        self.result_label.pack(pady=5)

        # Etykieta do wyświetlania zaleceń dotyczących odzieży
        self.clothing_advice_label = tk.Label(self.result_frame, text="", bg='#FFFFFF', font=('Arial', 12),
                                              wraplength=350)
        self.clothing_advice_label.pack(pady=5)

        # Przycisk do przejścia do mapy zanieczyszczeń (przeniesienie do innej strony)
        tk.Button(main_frame, text="Mapa Zanieczyszczeń", font=('Arial', 12, 'bold'),
                  command=lambda: controller.show_frame("PollutionMapPage"), bg='#4682B4', fg='white').pack(pady=10)

    def toggle_theme(self):
        """ Funkcja zmieniająca motyw na przeciwny """
        if self.controller.current_theme == "dark":
            self.controller.current_theme = "light"
        else:
            self.controller.current_theme = "dark"
        self.controller.set_theme(self.controller.current_theme)

    # Funkcja do pobierania danych o pogodzie i jakości powietrza
    def fetch_data(self):
        city = self.selected_city.get()

        if not city:
            messagebox.showerror("Błąd", "Proszę wybrać województwo i miasto.")
            return

        api_key = "fb9e5c164b6e64b6ea40f8d266f20499"  # Klucz API do OpenWeatherMap
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},PL&limit=1&appid={api_key}"

        try:
            # Zapytanie o dane geolokalizacyjne (szerokość i długość geograficzną)
            geo_response = requests.get(geocoding_url)
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            if not geo_data:
                messagebox.showerror("Błąd", "Nie znaleziono współrzędnych dla podanego miasta.")
                return

            lat, lon = geo_data[0]['lat'], geo_data[0]['lon']

            # Zapytanie o dane pogodowe
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
            # Zapytanie o dane dotyczące jakości powietrza
            pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

            # Pobranie danych pogodowych
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            temperature = round(weather_data["main"]["temp"], 1)
            description = weather_data["weather"][0]["description"]

            # Pobranie danych o jakości powietrza
            pollution_response = requests.get(pollution_url)
            pollution_response.raise_for_status()
            pollution_data = pollution_response.json()
            air_quality = pollution_data["list"][0]["main"]["aqi"]

            # Wyświetlanie danych w aplikacji
            self.display_weather_and_air_quality(temperature, description, air_quality)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Błąd", f"Nie udało się pobrać danych: {e}")

    # Funkcja do wyświetlania pogody i jakości powietrza
    def display_weather_and_air_quality(self, temperature, description, air_quality):
        # Wyświetlanie wyników na ekranie
        air_quality_str = self.get_air_quality_str(air_quality)

        # Podpowiedź odzieżowa
        clothing_advice = self.get_clothing_advice(temperature)

        self.result_label.config(
            text=f"Pogoda: {description.capitalize()}\nTemperatura: {temperature}°C\nJakość powietrza: {air_quality_str}")
        self.clothing_advice_label.config(text=clothing_advice)

        # Wyświetlanie ramki wyników
        self.result_frame.pack()

    def get_air_quality_str(self, air_quality):
        """Przekształca wartość AQI na opis jakości powietrza"""
        if air_quality == 1:
            return "Bardzo dobra"
        elif air_quality == 2:
            return "Dobra"
        elif air_quality == 3:
            return "Umiarkowana"
        elif air_quality == 4:
            return "Zła"
        elif air_quality == 5:
            return "Bardzo zła"
        return "Brak danych"

    def get_clothing_advice(self, temperature):
        """Zalecenia dotyczące odzieży w zależności od temperatury"""
        if temperature < 5:
            return "Zalecane: Ciepły płaszcz, rękawice, szalik."
        elif 5 <= temperature < 15:
            return "Zalecane: Kurtka, sweter, szalik."
        elif 15 <= temperature < 25:
            return "Zalecane: Lekkie ubrania, sweter, koszula."
        else:
            return "Zalecane: Letnia odzież, lekka koszulka."

    # Funkcje do obsługi ulubionych miast
    def load_favorites(self):
        """Funkcja wczytująca ulubione miasta z pliku"""
        if os.path.exists("favorites.txt"):
            with open("favorites.txt", "r", encoding="utf-8") as file:
                return [line.strip() for line in file.readlines()]
        return []  # Jeśli plik nie istnieje, zwróć pustą listę

    def save_favorites(self):
        """Funkcja zapisująca ulubione miasta do pliku"""
        with open("favorites.txt", "w", encoding="utf-8") as file:
            for city in self.favorites:
                file.write(f"{city}\n")

    def add_to_favorites(self):
        """Dodaje miasto do ulubionych"""
        city = self.selected_city.get()
        if city and city not in self.favorites:
            self.favorites.append(city)
            self.favorites_combobox['values'] = self.favorites
            self.save_favorites()  # Zapisz ulubione miasta po dodaniu
            messagebox.showinfo("Sukces", f"{city} dodane do ulubionych!")

    def remove_from_favorites(self):
        """Usuwa miasto z ulubionych"""
        city = self.favorites_combobox.get()
        if city and city in self.favorites:
            self.favorites.remove(city)
            self.favorites_combobox['values'] = self.favorites
            self.save_favorites()  # Zapisz ulubione miasta po usunięciu
            messagebox.showinfo("Sukces", f"{city} usunięte z ulubionych!")

    def on_state_selected(self, event):
        """Aktualizuje dostępne miasta na podstawie wybranego województwa"""
        selected_state = self.selected_state.get()
        cities = next(item["cities"] for item in self.countries_and_cities if item["state"] == selected_state)
        self.city_combobox['values'] = cities
        self.city_combobox.set("")  # Czyści pole miasta

    def on_favorite_selected(self, event):
        """Automatycznie wyświetla dane o pogodzie i jakości powietrza po wybraniu ulubionej lokalizacji"""
        city = self.favorites_combobox.get()
        if city:
            self.selected_city.set(city)
            self.fetch_data()
    def on_state_selected(self, event):
        """Aktualizuje dostępne miasta na podstawie wybranego województwa"""
        selected_state = self.selected_state.get()
        cities = next(item["cities"] for item in self.countries_and_cities if item["state"] == selected_state)
        self.city_combobox['values'] = cities
        self.city_combobox.set("")  # Czyści pole miasta

    def on_favorite_selected(self, event):
        """Automatycznie wyświetla dane o pogodzie i jakości powietrza po wybraniu ulubionej lokalizacji"""
        city = self.favorites_combobox.get()
        if city:
            self.selected_city.set(city)
            self.fetch_data()
