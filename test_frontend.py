import unittest
from tkinter import Tk
from carbon_app import CarbonApp
from pollution_map import PollutionMapPage

class TestFrontend(unittest.TestCase):
    def setUp(self):
        """Inicjalizacja głównego okna Tkinter i stron aplikacji."""
        self.root = Tk()
        self.root.geometry("400x600")
        self.carbon_app = CarbonApp(self.root, None)
        self.pollution_map = PollutionMapPage(self.root, None)

    def tearDown(self):
        """Zamykanie okna Tkinter po każdym teście."""
        self.root.destroy()

    def test_carbon_app_initialization(self):
        """Test inicjalizacji strony CarbonApp."""
        self.assertEqual(self.carbon_app.winfo_class(), "Frame")
        self.assertEqual(self.carbon_app.master, self.root)

    def test_pollution_map_initialization(self):
        """Test inicjalizacji strony PollutionMapPage."""
        self.assertEqual(self.pollution_map.winfo_class(), "Frame")
        self.assertEqual(self.pollution_map.master, self.root)

    def test_map_click(self):
        """Test obsługi kliknięcia na mapie."""
        lat, lon = 52.2297, 21.0122
        self.pollution_map.on_map_click(lat, lon)
        self.assertIsNotNone(self.pollution_map.current_marker)

    def test_back_button(self):
        """Test działania przycisku powrotu."""
        self.pollution_map.back_button.invoke()
        # Sprawdzenie, czy aplikacja nie rzuca błędów po kliknięciu przycisku.

if __name__ == "__main__":
    unittest.main()
