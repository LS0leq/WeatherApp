import tkinter as tk
from tkinter import ttk
import unittest

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test App")

        self.voivodeship_cb = ttk.Combobox(self, values=["Mazowieckie", "Małopolskie"])
        self.voivodeship_cb.pack()

        self.city_cb = ttk.Combobox(self, values=["Warszawa", "Kraków"])
        self.city_cb.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        self.button = tk.Button(self, text="Potwierdź", command=self.on_confirm)
        self.button.pack()

    def on_confirm(self):
        voivodeship = self.voivodeship_cb.get()
        city = self.city_cb.get()
        self.result_label.config(text=f"Wybrano: {voivodeship}, {city}")

class TestMyApp(unittest.TestCase):
    def setUp(self):
        self.app = MyApp()
        self.app.update()  # GUI update

    def tearDown(self):
        self.app.destroy()

    def test_user_flow(self):
        # Poprawny wybór obu wartości
        self.app.voivodeship_cb.set("Mazowieckie")
        self.app.city_cb.set("Warszawa")
        self.app.button.invoke()
        self.assertEqual(self.app.result_label.cget("text"), "Wybrano: Mazowieckie, Warszawa")

    def test_only_voivodeship_selected(self):
        # wybranie wojewodztwa z pustym miastem
        self.app.voivodeship_cb.set("Małopolskie")
        self.app.city_cb.set("")
        self.app.button.invoke()
        self.assertEqual(self.app.result_label.cget("text"), "Wybrano: Małopolskie, ")

    def test_only_city_selected(self):
        # odwrotnie do powyzszego czyli tylko miasto bez wojewodztwa
        self.app.voivodeship_cb.set("")
        self.app.city_cb.set("Kraków")
        self.app.button.invoke()
        self.assertEqual(self.app.result_label.cget("text"), "Wybrano: , Kraków")

    def test_nothing_selected(self):
        # nic nie wybrano
        self.app.voivodeship_cb.set("")
        self.app.city_cb.set("")
        self.app.button.invoke()
        self.assertEqual(self.app.result_label.cget("text"), "Wybrano: , ")

    def test_invalid_selection(self):
        # test sprawdzajacy wybranie warosci spoza listy
        self.app.voivodeship_cb.set("Pomorskie")  # nie ma takiej wartości
        self.app.city_cb.set("Gdańsk")            # nie ma takiej wartości
        self.app.button.invoke()
        self.assertEqual(self.app.result_label.cget("text"), "Wybrano: Pomorskie, Gdańsk")

    def test_default_state(self):
        # po uruchomieniu aplikacji powinno byc puste
        self.assertEqual(self.app.result_label.cget("text"), "")

if __name__ == "__main__":
    unittest.main()
