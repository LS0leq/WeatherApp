import unittest
from unittest.mock import patch, Mock
import requests

# Funkcja do pobierania pogody i ikony
def get_weather(city):
    api_key = "62aaa211c27926a7c8b71c67b1394826"  # Twój klucz API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pl"

    # Wykonanie zapytania do API
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "city_name": city,
            "temperature": data['main']['temp'],
            "description": data['weather'][0]['description'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed'],
            "icon_code": data['weather'][0]['icon']
        }
    else:
        return None

class TestWeatherApp(unittest.TestCase):

    @patch('requests.get')
    def test_get_weather_success(self, mock_get):
        # Mockowanie odpowiedzi API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 20, "humidity": 50},
            "weather": [{"description": "clear sky", "icon": "01d"}],
            "wind": {"speed": 5}
        }
        mock_get.return_value = mock_response

        # Testowanie funkcji get_weather
        result = get_weather("Gdańsk")
        self.assertIsNotNone(result)
        self.assertEqual(result["city_name"], "Gdańsk")
        self.assertEqual(result["temperature"], 20)
        self.assertEqual(result["description"], "clear sky")
        self.assertEqual(result["humidity"], 50)
        self.assertEqual(result["wind_speed"], 5)
        self.assertEqual(result["icon_code"], "01d")

    @patch('requests.get')
    def test_get_weather_failure(self, mock_get):
        # Mockowanie odpowiedzi API
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Testowanie funkcji get_weather
        result = get_weather("NieistniejąceMiasto")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
