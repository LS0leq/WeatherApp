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

    def test_carbon_app_favorites_add_and_remove(self):
        """Test dodawania i usuwania ulubionych lokalizacji."""
        initial_count = len(self.carbon_app.favorite_locations)
        self.carbon_app.selected_state.set("Mazowieckie")
        self.carbon_app.selected_city.set("Warszawa")
        self.carbon_app.add_favorite()
        self.assertIn("Mazowieckie, Warszawa", self.carbon_app.favorite_locations)
        self.carbon_app.favorites_listbox.selection_set(0)
        self.carbon_app.delete_favorite()
        self.assertEqual(len(self.carbon_app.favorite_locations), initial_count)

    def test_carbon_app_update_favorites_listbox(self):
        """Test aktualizacji listy ulubionych."""
        self.carbon_app.favorite_locations = ["Mazowieckie, Warszawa"]
        self.carbon_app.update_favorites_listbox()
        self.assertEqual(self.carbon_app.favorites_listbox.get(0), "Mazowieckie, Warszawa")

    def test_carbon_app_selected_favorite(self):
        """Test wyboru ulubionej lokalizacji."""
        self.carbon_app.favorite_locations = ["Mazowieckie, Warszawa"]
        self.carbon_app.update_favorites_listbox()
        self.carbon_app.favorites_listbox.selection_set(0)
        event = type('Event', (object,), {'widget': self.carbon_app.favorites_listbox})()
        self.carbon_app.selected_favorite(event)
        self.assertEqual(self.carbon_app.selected_state.get(), "Mazowieckie")

    def test_pollution_map_info_label_text(self):
        """Test czy etykieta info_label zawiera odpowiedni tekst."""
        self.assertIn("Informacje o jakości powietrza", self.pollution_map.info_label.cget("text"))

    def test_pollution_map_info_text_default(self):
        """Test domyślnego tekstu info_text."""
        self.assertIn("Wybierz punkt na mapie", self.pollution_map.info_text.cget("text"))

    def test_pollution_map_get_pollution_level(self):
        """Test metody get_pollution_level."""
        pollution = {'co': 10, 'no2': 10, 'pm2_5': 5, 'pm10': 10}
        level = self.pollution_map.get_pollution_level(pollution)
        self.assertIn("dobra", level)

if __name__ == "__main__":
    unittest.main()
