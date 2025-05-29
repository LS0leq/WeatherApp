import unittest
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os


class TestModel(unittest.TestCase):
    test_results = {'passed': [], 'failed': [], 'mse': None}

    @classmethod
    def setUpClass(cls):
        # Załaduj dane testowe
        cls.df = pd.read_csv('ml_dataset.csv').dropna(subset=['t+1'])
        cls.feature_columns = ['t-6', 't-5', 't-4', 't-3', 't-2', 't-1', 't']
        cls.X = cls.df[cls.feature_columns].copy()
        cls.y = cls.df['t+1']

        with open('model.pkl', 'rb') as f:
            cls.model = pickle.load(f)

    def setUp(self):
        self._startTime = datetime.now()

    def tearDown(self):
        self._endTime = datetime.now()
        self._elapsedTime = self._endTime - self._startTime
        self.test_results[self._testMethodName] = {
            'time': self._elapsedTime.total_seconds(),
            'status': 'passed' if self._outcome.success else 'failed'
        }

    def test_model_instance(self):
        self.assertIsInstance(self.model, LinearRegression)

    def test_model_prediction_shape(self):
        y_pred = self.model.predict(self.X)
        self.assertEqual(len(y_pred), len(self.X))

    def test_model_mse_reasonable(self):
        X_test = self.X.copy()
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(self.y, y_pred)
        TestModel.test_results['mse'] = mse
        self.assertLess(mse, 100)

    @classmethod
    def generate_report(cls):
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_filename = f'test_report_{current_time}.txt'

        temp_range = {
            'min': cls.df[cls.feature_columns].min().min(),
            'max': cls.df[cls.feature_columns].max().max()
        }

        report_content = f"""
RAPORT Z WYKONANIA TESTÓW MODELU PREDYKCYJNEGO

Data wykonania: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Status: {'POZYTYWNY ✓' if all(test['status'] == 'passed' for test in cls.test_results.values() if isinstance(test, dict)) else 'NEGATYWNY ✗'}

WYKONANE TESTY:
1. test_model_instance - {'✓' if cls.test_results['test_model_instance']['status'] == 'passed' else '✗'} ({cls.test_results['test_model_instance']['time']:.3f}s)
   - Weryfikacja typu modelu (LinearRegression)

2. test_model_prediction_shape - {'✓' if cls.test_results['test_model_prediction_shape']['status'] == 'passed' else '✗'} ({cls.test_results['test_model_prediction_shape']['time']:.3f}s)
   - Sprawdzenie wymiarów predykcji

3. test_model_mse_reasonable - {'✓' if cls.test_results['test_model_mse_reasonable']['status'] == 'passed' else '✗'} ({cls.test_results['test_model_mse_reasonable']['time']:.3f}s)
   - Weryfikacja jakości predykcji (MSE < 100)
   - Uzyskane MSE: {cls.test_results['mse']:.4f}

ANALIZA DANYCH TESTOWYCH:
- Zakres temperatur: {temp_range['min']:.2f}°C - {temp_range['max']:.2f}°C
- Liczba próbek: {len(cls.df)}
- Wykorzystane cechy: {', '.join(cls.feature_columns)}

WNIOSKI:
1. Model {'jest' if cls.test_results['test_model_instance']['status'] == 'passed' else 'nie jest'} poprawnie załadowany i skonfigurowany
2. Predykcje {'są' if cls.test_results['test_model_prediction_shape']['status'] == 'passed' else 'nie są'} generowane zgodnie z oczekiwaniami
3. Błąd predykcji {'jest' if cls.test_results['test_model_mse_reasonable']['status'] == 'passed' else 'nie jest'} w akceptowalnym zakresie

Status końcowy: {'OK - wszystkie testy zakończone sukcesem' if all(test['status'] == 'passed' for test in cls.test_results.values() if isinstance(test, dict)) else 'BŁĄD - niektóre testy nie powiodły się'}
"""

        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"Raport został zapisany do pliku: {report_filename}")


if __name__ == '__main__':
    # Uruchomienie testów
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestModel)
    result = runner.run(suite)

    # Generowanie raportu
    TestModel.generate_report()