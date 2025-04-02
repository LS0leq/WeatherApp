import tkinter as tk
from tkinter import ttk, messagebox
import requests


class CarbonApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(
            bg='#ADD8E6')  # Ustawienie tła aplikacji na jasny niebieski

        self.selected_state = tk.StringVar()  # Zmienna do przechowywania wybranego województwa
        self.selected_city = tk.StringVar()  # Zmienna do przechowywania wybranego miasta

        # Lista województw i miast
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

        # Lista ulubionych lokalizacji
        self.favorites = []

        # Główny kontener aplikacji (ramka), która będzie zawierała wszystkie elementy
        main_frame = tk.Frame(self, bg='#ADD8E6')
        main_frame.pack(expand=True, fill="both",
                        anchor="center")

        # Wyświetlanie etykiety dla województwa
        tk.Label(main_frame, text="Województwo:",
                 bg='#87CEEB',
                 font=('Arial', 14, 'bold')).pack(
            pady=5)

        # Combobox do wyboru województwa
        self.state_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.selected_state,
            font=('Arial', 12))
        self.state_combobox['values'] = [
            item['state'] for item in
            self.countries_and_cities]  # Lista województw
        self.state_combobox.bind(
            "<<ComboboxSelected>>",
            self.on_state_selected)  # Po wybraniu województwa, aktualizuje miasta
        self.state_combobox.pack(pady=5)

        # Wyświetlanie etykiety dla miasta
        tk.Label(main_frame, text="Miasto:",
                 bg='#87CEEB',
                 font=('Arial', 14, 'bold')).pack(
            pady=5)

        # Combobox do wyboru miasta
        self.city_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.selected_city,
            font=('Arial', 12))
        self.city_combobox.pack(pady=5)

        # Przycisk do dodania wybranego miasta do ulubionych
        tk.Button(main_frame,
                  text="Dodaj do ulubionych",
                  command=self.add_to_favorites,
                  font=('Arial', 12, 'bold'),
                  bg='#4682B4', fg='white').pack(
            pady=5)

        # Etykieta dla ulubionych lokalizacji
        tk.Label(main_frame,
                 text="Ulubione lokalizacje:",
                 bg='#87CEEB',
                 font=('Arial', 14, 'bold')).pack(
            pady=5)

        # Combobox do wybrania ulubionej lokalizacji
        self.favorites_combobox = ttk.Combobox(
            main_frame, font=('Arial', 12))
        self.favorites_combobox[
            'values'] = self.favorites  # Lista ulubionych miast
        self.favorites_combobox.bind(
            "<<ComboboxSelected>>",
            self.on_favorite_selected)  # Po wybraniu lokalizacji, automatycznie pobiera dane
        self.favorites_combobox.pack(pady=5)

        # Przycisk do usunięcia wybranego miasta z ulubionych
        tk.Button(main_frame,
                  text="Usuń z ulubionych",
                  command=self.remove_from_favorites,
                  font=('Arial', 12, 'bold'),
                  bg='#4682B4', fg='white').pack(
            pady=5)

        # Przycisk do sprawdzenia jakości powietrza i pogody
        self.weather_button = tk.Button(
            main_frame,
            text="Sprawdź jakość powietrza",
            command=self.fetch_data,
            font=('Arial', 14, 'bold'),
            bg='#4682B4', fg='white')
        self.weather_button.pack(pady=10)

        # Ramka na wyniki (pogoda i jakość powietrza), początkowo ukryta
        self.result_frame = tk.Frame(main_frame,
                                     bg='#FFFFFF',
                                     bd=2,
                                     relief="solid",
                                     padx=10,
                                     pady=10)
        self.result_frame.pack_forget()  # Ukrycie ramki na początku

        # Etykieta do wyświetlania wyników pogody i jakości powietrza
        self.result_label = tk.Label(
            self.result_frame, text="",
            bg='#FFFFFF', font=('Arial', 14),
            wraplength=350)
        self.result_label.pack(pady=5)

        # Przycisk do przejścia do mapy zanieczyszczeń (przeniesienie do innej strony)
        tk.Button(main_frame,
                  text="Mapa Zanieczyszczeń",
                  font=('Arial', 12, 'bold'),
                  command=lambda: controller.show_frame(
                      "PollutionMapPage"),
                  bg='#4682B4', fg='white').pack(
            pady=10)

    # Funkcja obsługująca wybór województwa z listy
    def on_state_selected(self, event):
        selected_state = self.selected_state.get()
        cities = next((item['cities'] for item in
                       self.countries_and_cities
                       if item[
                           'state'] == selected_state),
                      [])
        self.city_combobox[
            'values'] = cities  # Aktualizowanie listy miast
        self.city_combobox.set(
            "")  # Czyszczenie wybranego miasta

    # Funkcja obsługująca wybór ulubionego miasta
    def on_favorite_selected(self, event):
        selected_favorite = self.favorites_combobox.get()
        if selected_favorite:
            # Po wybraniu lokalizacji z ulubionych, automatycznie ustawia miasto i pobiera dane
            self.selected_city.set(
                selected_favorite)
            self.fetch_data()

    # Funkcja do pobierania danych o pogodzie i jakości powietrza
    def fetch_data(self):
        city = self.selected_city.get()

        if not city:
            messagebox.showerror("Błąd",
                                 "Proszę wybrać województwo i miasto.")
            return

        api_key = "fb9e5c164b6e64b6ea40f8d266f20499"  # Klucz API do OpenWeatherMap
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},PL&limit=1&appid={api_key}"

        try:
            # Zapytanie o dane geolokalizacyjne (szerokość i długość geograficzną)
            geo_response = requests.get(
                geocoding_url)
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            if not geo_data:
                messagebox.showerror("Błąd",
                                     "Nie znaleziono współrzędnych dla podanego miasta.")
                return

            lat, lon = geo_data[0]['lat'], \
            geo_data[0]['lon']

            # Zapytanie o dane pogodowe
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
            # Zapytanie o dane dotyczące jakości powietrza
            pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"

            # Pobranie danych pogodowych
            weather_response = requests.get(
                weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            temperature = round(
                weather_data["main"]["temp"], 1)

            # Pobranie danych o zanieczyszczeniu powietrza
            pollution_response = requests.get(
                pollution_url)
            pollution_response.raise_for_status()
            pollution_data = pollution_response.json()
            pollution = \
            pollution_data.get('list', [{}])[
                0].get('components', {})

            # Formatowanie tekstu jakości powietrza
            pollution_text = (
                f"CO (czad): {pollution.get('co', 'Brak danych')} µg/m³\n"
                f"NO₂ (dwutlenek azotu): {pollution.get('no2', 'Brak danych')} µg/m³\n"
                f"PM2.5: {pollution.get('pm2_5', 'Brak danych')} µg/m³\n"
                f"PM10: {pollution.get('pm10', 'Brak danych')} µg/m³"
            )

            # Aktualizacja etykiety wyników i pokazanie ramki z wynikami
            self.result_label.config(
                text=f"Temperatura: {temperature}°C\n\n{pollution_text}")
            self.result_frame.pack(pady=5)

        except requests.RequestException as e:
            messagebox.showerror("Błąd",
                                 f"Wystąpił błąd: {e}")

    # Funkcja do dodania miasta do ulubionych
    def add_to_favorites(self):
        city = self.selected_city.get()

        if not city:
            messagebox.showerror("Błąd",
                                 "Proszę wybrać miasto.")
            return

        if city not in self.favorites:
            self.favorites.append(city)
            self.favorites_combobox[
                'values'] = self.favorites  # Aktualizacja listy ulubionych miast
            messagebox.showinfo("Sukces",
                                f"{city} dodano do ulubionych.")
        else:
            messagebox.showinfo("Informacja",
                                "To miasto jest już w ulubionych.")

    # Funkcja do usunięcia miasta z ulubionych
    def remove_from_favorites(self):
        city = self.favorites_combobox.get()

        if city in self.favorites:
            self.favorites.remove(city)
            self.favorites_combobox[
                'values'] = self.favorites  # Aktualizacja listy ulubionych miast
            messagebox.showinfo("Sukces",
                                f"{city} usunięto z ulubionych.")
        else:
            messagebox.showerror("Błąd",
                                 "To miasto nie znajduje się w ulubionych.")


# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Aplikacja Jakości Powietrza")
    root.geometry("400x600")

    app = CarbonApp(root, None)
    app.pack(expand=True, fill="both",
             anchor="center")

    root.mainloop()
