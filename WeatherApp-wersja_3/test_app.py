import unittest
from modules.info_component import InfoComponent
from modules.map_component import MapComponent
import customtkinter as ctk


class TestInfoComponent(unittest.TestCase):
    def setUp(self):
        self.root = ctk.CTk()
        self.info_component = InfoComponent(self.root)

    def test_initial_label_text(self):
        """Sprawdza, czy początkowy tekst etykiety jest poprawny."""
        self.assertEqual(self.info_component.info_label.cget("text"), "Wybierz lokalizację na mapie")

    def test_update_info(self):
        """Sprawdza etykiete, (czyli te informacje ktore mamy o zanieczyszczeniach) czy aktualizuje się poprawnie po wywołaniu update_info."""
        pollution_data = {'co': 1200, 'no2': 50, 'pm2_5': 30}
        self.info_component.update_info("Warszawa", pollution_data)
        self.assertIn("Lokalizacja: Warszawa", self.info_component.info_label.cget("text"))
        self.assertIn("CO: Bardzo wysoki poziom! Możliwe zatrucie.", self.info_component.info_label.cget("text"))


class TestMapComponent(unittest.TestCase):
    def setUp(self):
        self.root = ctk.CTk()
        self.info_component = InfoComponent(self.root)
        self.map_component = MapComponent(self.root, self.info_component)

    def test_map_initial_position(self):
        """Sprawdza początkową pozycję ustawioną na Warszawę."""
        lat, lon = self.map_component.map_view.get_position()
        self.assertAlmostEqual(lat, 52.2297, places=2)
        self.assertAlmostEqual(lon, 21.0122, places=2)


if __name__ == "__main__":
    unittest.main()
