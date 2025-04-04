import tkinter as tk
from tkinter import messagebox
import requests
import geocoder


class WeatherApp:
    def __init__(self, root, weather_api_key):
        self.root = root
        self.root.title("Pogoda i zalecenia")
        self.root.geometry("500x400")
        self.weather_api_key = weather_api_key

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=20)

        self.fetch_button = tk.Button(self.root, text="Sprawdź pogodę", command=self.fetch_weather)
        self.fetch_button.pack(pady=10)

        self.exit_button = tk.Button(self.root, text="Zamknij", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def fetch_weather(self):
        g = geocoder.ip('me')
        latitude = g.latlng[0]
        longitude = g.latlng[1]

        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={self.weather_api_key}&units=metric&lang=pl"

        try:
            response = requests.get(weather_url)
            response.raise_for_status()
            data = response.json()

            if data:

                temperature = data['main']['temp']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                weather_description = data['weather'][0]['description']
                city_name = data['name']

                outfit = self.get_outfit_suggestion(temperature)
                activity = self.get_activity_suggestion(temperature, wind_speed)
                hazard = self.get_hazard_suggestion(temperature, humidity, wind_speed)

                result_text = (
                    f"Lokalizacja: {city_name}\n"
                    f"Pogoda: {weather_description.capitalize()}\n"
                    f"Temperatura: {temperature}°C\n"
                    f"Wilgotność: {humidity}%\n"
                    f"Wiatr: {wind_speed} km/h\n\n"
                    f"Ubiór: {outfit}\n"
                    f"Aktywności: {activity}\n"
                    f"Zagrożenia: {hazard}"
                )
                self.result_label.config(text=result_text)

            else:
                messagebox.showerror("Błąd", "Brak danych pogodowych dla Twojej lokalizacji.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")
            print(e)

    def get_outfit_suggestion(self, temperature):
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

    def get_activity_suggestion(self, temperature, wind_speed):
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

    def get_hazard_suggestion(self, temperature, humidity, wind_speed):
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


if __name__ == "__main__":
    weather_api_key = "fb9e5c164b6e64b6ea40f8d266f20499"
    root = tk.Tk()
    app = WeatherApp(root, weather_api_key)
    root.mainloop()
