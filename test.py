import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from temp import CarbonApp

class TestCarbonApp(unittest.TestCase):
    def setUp(self):
        """Inicjalizacja aplikacji przed każdym testem."""
        self.root = tk.Tk()
        self.app = CarbonApp(self.root)

    def tearDown(self):
        """Zamykanie okna aplikacji po każdym teście."""
        self.root.destroy()

    def test_initial_state(self):
        """Test sprawdzający, czy aplikacja poprawnie inicjalizuje interfejs użytkownika."""
        self.assertEqual(self.app.selected_state.get(), "")
        self.assertEqual(self.app.selected_city.get(), "")

    def test_on_state_selected(self):
        """Test sprawdzający, czy lista miast zmienia się po wyborze województwa."""
        self.app.selected_state.set("Pomorskie")
        self.app.on_state_selected(None)
        expected_cities = ["Bytów", "Gdańsk", "Gdynia", "Kościerzyna", "Pogórze", "Sopot"]
        self.assertEqual(list(self.app.city_combobox["values"]), expected_cities)

    @patch("requests.get")
    def test_fetch_data_success(self, mock_get):
        """Test sprawdzający poprawne pobieranie danych z API."""
        self.app.selected_state.set("Mazowieckie")
        self.app.selected_city.set("Warszawa")

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "current": {
                    "pollution": {"aqius": 42},
                    "weather": {"tp": 20, "hu": 60, "pr": 1015, "ts": "2024-03-17T10:00:00"}
                }
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        self.app.fetch_data()
        self.assertIn("AQI: 42", self.app.result_label.cget("text"))

    @patch("requests.get")
    def test_fetch_data_api_error(self, mock_get):
        """Test obsługi błędu API."""
        self.app.selected_state.set("Mazowieckie")
        self.app.selected_city.set("Warszawa")

        mock_get.side_effect = Exception("Błąd połączenia")

        with patch("tkinter.messagebox.showerror") as mock_error:
            self.app.fetch_data()
            mock_error.assert_called_with("Błąd", "Wystąpił błąd: Błąd połączenia")

    def test_get_color_based_on_aqi(self):
        """Test sprawdzający poprawność funkcji zwracającej kolor AQI."""
        self.assertEqual(self.app.get_color_based_on_aqi(30), "green")
        self.assertEqual(self.app.get_color_based_on_aqi(75), "yellow")
        self.assertEqual(self.app.get_color_based_on_aqi(125), "orange")
        self.assertEqual(self.app.get_color_based_on_aqi(175), "red")
        self.assertEqual(self.app.get_color_based_on_aqi(250), "dark")


if __name__ == "__main__":
    unittest.main()
