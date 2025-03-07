import tkinter as tk
from tkinter import ttk
import requests
import io
import datetime

# Funkcja do pobierania pogody i ikony
def get_weather():
    city = combo.get()
    api_key = "62aaa211c27926a7c8b71c67b1394826"  # Twój klucz API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pl"

    # Wykonanie zapytania do API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Pobranie informacji o pogodzie
        city_name = combo.get()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Wyświetlenie wyników w oknie
        result_label.config(text=f"Pogoda w {city_name}:\n"
                                 f"Temperatura: {temperature}°C\n"
                                 f"Opis: {description.capitalize()}\n"
                                 f"Wilgotność: {humidity}%\n"
                                 f"Wiatr: {wind_speed} m/s")

        # Pobranie ikony pogody
        icon_code = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        icon_response = requests.get(icon_url)

        if icon_response.status_code == 200:
            # Konwersja obrazu do formatu PhotoImage
            image_data = io.BytesIO(icon_response.content)
            image = tk.PhotoImage(data=image_data.read())  # Wczytanie obrazu bez Pillow

            # Ustawienie obrazu w etykiecie
            icon_label.config(image=image)
            icon_label.image = image  # Zapewnienie, że obraz nie zostanie usunięty przez garbage collector
    else:
        result_label.config(text="Błąd podczas pobierania danych o pogodzie.")

# Funkcja do aktualizowania zegara i daty
def update_clock():
    # Pobranie aktualnej daty i godziny
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S")
    formatted_date = current_time.strftime("%d-%m-%Y")  # Format daty: dzień-miesiąc-rok

    # Aktualizacja tekstu zegara i daty
    clock_label.config(text=f"Godzina: {formatted_time}\nData: {formatted_date}")

    # Wywołanie funkcji co 1000 ms (1 sekunda)
    root.after(1000, update_clock)

# Tworzenie głównego okna aplikacji
root = tk.Tk()
root.title("Aplikacja Pogodowa")
root.geometry("600x600")  # Zwiększone okno
root.configure(bg="#f0f0f0")  # Kolor tła aplikacji

# Ustawienie czcionki na całej aplikacji
default_font = ("Helvetica", 12)
large_font = ("Helvetica", 16)

# Dodawanie responsywności - główne okno
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(0, weight=1)

# Tworzenie etykiety zegara i daty (u góry)
clock_label = tk.Label(root, font=("Helvetica", 20), justify="center", bg="#f0f0f0", fg="black")
clock_label.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

# Tworzenie etykiety z instrukcją
instruction_label = tk.Label(root, text="Podaj nazwę miasta:", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
instruction_label.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

# Lista dostępnych miast
opcje = ["Gdańsk", "Warszawa", "Kraków"]

# Tworzenie comboboxa (mniejszy rozmiar)
combo = ttk.Combobox(root, values=opcje, font=("Helvetica", 10), state="readonly")
combo.set("Wybierz miasto")  # Ustawiamy domyślną wartość
combo.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

# Tworzenie przycisku do pobierania danych pogodowych
get_weather_button = tk.Button(root, text="Pobierz pogodę", command=get_weather, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="solid", bd=1)
get_weather_button.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

# Etykieta do wyświetlania wyników
result_label = tk.Label(root, text="", font=("Helvetica", 12), justify="left", bg="#f0f0f0")
result_label.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")

# Tworzenie etykiety do wyświetlania ikony pogody pod opisem pogody
icon_label = tk.Label(root, bg="#f0f0f0")
icon_label.grid(row=5, column=0, pady=10, padx=10, sticky="nsew")

# Uruchomienie aktualizacji zegara i daty
update_clock()

# Ustawianie ikonki na pasku
root.iconbitmap('zdj/Logo.ico')

# Uruchomienie aplikacji
root.mainloop()
