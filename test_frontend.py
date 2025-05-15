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

    def test_carbon_app_buttons(self):
        """Test działania przycisków w CarbonApp."""
        for button in self.carbon_app.buttons:
            button.invoke()
            # Sprawdzenie, czy aplikacja nie rzuca błędów po kliknięciu przycisku.

    def test_pollution_map_marker_update(self):
        """Test aktualizacji markera na mapie."""
        lat, lon = 50.0647, 19.9450
        self.pollution_map.on_map_click(lat, lon)
        self.assertEqual(self.pollution_map.current_marker['lat'], lat)
        self.assertEqual(self.pollution_map.current_marker['lon'], lon)

    def test_pollution_map_no_marker(self):
        """Test zachowania mapy bez kliknięcia."""
        self.assertIsNone(self.pollution_map.current_marker)

    def test_map_click_invalid_coordinates(self):
        """Test obsługi kliknięcia na mapie z nieprawidłowymi współrzędnymi."""
        with self.assertRaises(ValueError):
            self.pollution_map.on_map_click("invalid", 21.0122)
        with self.assertRaises(ValueError):
            self.pollution_map.on_map_click(52.2297, "invalid")
        with self.assertRaises(ValueError):
            self.pollution_map.on_map_click(None, None)

    def test_carbon_app_button_labels(self):
        """Test poprawności etykiet przycisków w CarbonApp."""
        expected_labels = ["Przycisk 1", "Przycisk 2", "Przycisk 3"]  # Przykładowe etykiety
        actual_labels = [button.cget("text") for button in self.carbon_app.buttons]
        self.assertEqual(expected_labels, actual_labels)

    def test_pollution_map_error_handling(self):
        """Test obsługi błędów w PollutionMapPage."""
        try:
            self.pollution_map.on_map_click(999, 999)  # Nieprawidłowe współrzędne
        except Exception as e:
            self.fail(f"Metoda on_map_click rzuciła nieoczekiwany wyjątek: {e}")

    def test_pollution_map_marker_removal(self):
        """Test usuwania markera z mapy."""
        lat, lon = 50.0647, 19.9450
        self.pollution_map.on_map_click(lat, lon)
        self.pollution_map.remove_marker()
        self.assertIsNone(self.pollution_map.current_marker)

if __name__ == "__main__":
    unittest.main()
