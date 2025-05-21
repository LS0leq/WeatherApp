import unittest
from carbon_app import get_outfit_suggestion, get_activity_suggestion, get_hazard_suggestion


class TestBackend(unittest.TestCase):

    def test_get_outfit_suggestion(self):
        self.assertEqual(get_outfit_suggestion(-5), "Ciepły płaszcz, szalik, czapka, rękawiczki.")
        self.assertEqual(get_outfit_suggestion(5), "Kurtka zimowa lub ciepły sweter.")
        self.assertEqual(get_outfit_suggestion(15), "Lekka kurtka lub bluza.")
        self.assertEqual(get_outfit_suggestion(25), "T-shirt, lekka odzież.")
        self.assertEqual(get_outfit_suggestion(35), "Woda, krem z filtrem, lekkie ubrania.")

    def test_get_outfit_suggestion_edge_cases(self):
        self.assertEqual(get_outfit_suggestion(0), "Kurtka zimowa lub ciepły sweter.")
        self.assertEqual(get_outfit_suggestion(10), "Lekka kurtka lub bluza.")
        self.assertEqual(get_outfit_suggestion(30), "T-shirt, lekka odzież.")

    def test_get_outfit_suggestion_invalid_input(self):
        """Test dla nieprawidłowych danych wejściowych w get_outfit_suggestion."""
        with self.assertRaises(ValueError):
            get_outfit_suggestion("invalid")
        with self.assertRaises(ValueError):
            get_outfit_suggestion(None)
        with self.assertRaises(ValueError):
            get_outfit_suggestion([])

    def test_get_outfit_suggestion_float(self):
        self.assertEqual(get_outfit_suggestion(0.0), "Kurtka zimowa lub ciepły sweter.")
        self.assertEqual(get_outfit_suggestion(10.1), "Lekka kurtka lub bluza.")
        self.assertEqual(get_outfit_suggestion(20.5), "T-shirt, lekka odzież.")

    def test_get_outfit_suggestion_large_negative(self):
        self.assertEqual(get_outfit_suggestion(-100), "Ciepły płaszcz, szalik, czapka, rękawiczki.")

    def test_get_activity_suggestion(self):
        self.assertIn("unikanie długich spacerów", get_activity_suggestion(-5, 10))
        self.assertIn("krótki spacer", get_activity_suggestion(5, 25))
        self.assertIn("jogging lub jazdę na rowerze", get_activity_suggestion(15, 10))
        self.assertIn("ochronie przed słońcem", get_activity_suggestion(35, 5))

    def test_get_activity_suggestion_edge_cases(self):
        self.assertIn("unikanie długich spacerów", get_activity_suggestion(-10, 5))
        self.assertIn("krótki spacer", get_activity_suggestion(10, 20))
        self.assertIn("ochronie przed słońcem", get_activity_suggestion(40, 5))

    def test_get_activity_suggestion_extreme_conditions(self):
        """Test dla ekstremalnych warunków pogodowych w get_activity_suggestion."""
        self.assertIn("unikanie aktywności na zewnątrz", get_activity_suggestion(-50, 100))
        self.assertIn("unikanie aktywności na zewnątrz", get_activity_suggestion(50, 100))
        self.assertIn("krótki spacer", get_activity_suggestion(20, 10))

    def test_get_activity_suggestion_high_wind(self):
        self.assertIn("silny wiatr", get_activity_suggestion(15, 10))

    def test_get_activity_suggestion_typical(self):
        self.assertIn("Idealna pogoda", get_activity_suggestion(18, 2))

    def test_get_hazard_suggestion(self):
        self.assertIn("możliwe oblodzenia", get_hazard_suggestion(-5, 50, 10))
        self.assertIn("możliwe przymrozki", get_hazard_suggestion(5, 50, 10))
        self.assertIn("Wiatr może być silny", get_hazard_suggestion(15, 50, 25))
        self.assertIn("Wysoka wilgotność", get_hazard_suggestion(25, 80, 10))
        self.assertIn("Wysokie temperatury", get_hazard_suggestion(35, 50, 10))

    def test_get_hazard_suggestion_edge_cases(self):
        self.assertIn("możliwe oblodzenia", get_hazard_suggestion(-10, 70, 15))
        self.assertIn("Wiatr może być silny", get_hazard_suggestion(20, 60, 30))
        self.assertIn("Wysokie temperatury", get_hazard_suggestion(40, 40, 5))

    def test_get_hazard_suggestion_no_hazards(self):
        self.assertEqual(get_hazard_suggestion(20, 50, 5), "Brak zagrożeń pogodowych.")

    def test_get_hazard_suggestion_extreme_conditions(self):
        """Test dla ekstremalnych warunków pogodowych w get_hazard_suggestion."""
        self.assertIn("Ekstremalne zimno", get_hazard_suggestion(-50, 10, 5))
        self.assertIn("Ekstremalne gorąco", get_hazard_suggestion(50, 10, 5))
        self.assertIn("Wiatr huraganowy", get_hazard_suggestion(20, 50, 100))

    def test_get_hazard_suggestion_invalid_input(self):
        """Test dla nieprawidłowych danych wejściowych w get_hazard_suggestion."""
        with self.assertRaises(ValueError):
            get_hazard_suggestion("invalid", 50, 10)
        with self.assertRaises(ValueError):
            get_hazard_suggestion(20, "invalid", 10)
        with self.assertRaises(ValueError):
            get_hazard_suggestion(20, 50, "invalid")

    def test_get_hazard_suggestion_high_humidity(self):
        self.assertIn("Wysoka wilgotność", get_hazard_suggestion(25, 90, 5))

    def test_get_hazard_suggestion_no_hazard(self):
        self.assertIn("Brak zagrożeń", get_hazard_suggestion(15, 50, 2))

    def test_get_hazard_suggestion_high_wind(self):
        self.assertIn("Wiatr może być silny", get_hazard_suggestion(15, 40, 25))

    def test_get_hazard_suggestion_high_temp(self):
        self.assertIn("Wysokie temperatury", get_hazard_suggestion(40, 20, 2))

    def test_get_hazard_suggestion_low_temp(self):
        self.assertIn("Zimno", get_hazard_suggestion(-2, 60, 2))

    def test_get_hazard_suggestion_type_errors(self):
        with self.assertRaises(Exception):
            get_hazard_suggestion({}, [], ())


if __name__ == "__main__":
    unittest.main()
