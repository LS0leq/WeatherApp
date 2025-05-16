import unittest
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt


class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Załaduj dane testowe
        cls.df = pd.read_csv('ml_dataset.csv').dropna(subset=['t+1'])
        cls.X = cls.df[['t-6','t-5', 't-4', 't-3', 't-2', 't-1']]
        cls.y = cls.df['t+1']

        # Załaduj wytrenowany model
        with open('model.pkl', 'rb') as f:
            cls.model = pickle.load(f)




    def test_model_instance(self):
        # Sprawdź czy model to LinearRegression
        self.assertIsInstance(self.model, LinearRegression)

    def test_model_prediction_shape(self):
        y_pred = self.model.predict(self.X)
        self.assertEqual(len(y_pred), len(self.X))

    def generate_synthetic_data(num_samples=100):
        data = {
            't-6': np.random.randn(num_samples),
            't-5': np.random.randn(num_samples),
            't-4': np.random.randn(num_samples),
            't-3': np.random.randn(num_samples),
            't-2': np.random.randn(num_samples),
            't-1': np.random.randn(num_samples),
        }

        df = pd.DataFrame(data)

        df['t+1'] = df.sum(axis=1) + np.random.normal(0, 0.1, size=num_samples)

        return df


    def generate_weather_like_data(num_samples=800, base_temp=15):
        np.random.seed(42)

        temps = [base_temp]

        for i in range(1, num_samples + 6):
            delta = np.random.normal(loc=0, scale=1)
            new_temp = temps[-1] + delta
            temps.append(new_temp)

        data = {
            't-6': temps[0:num_samples],
            't-5': temps[1:num_samples + 1],
            't-4': temps[2:num_samples + 2],
            't-3': temps[3:num_samples + 3],
            't-2': temps[4:num_samples + 4],
            't-1': temps[5:num_samples + 5],
        }

        df = pd.DataFrame(data)

        df['t+1'] = temps[6:num_samples + 6] + np.random.normal(0, 0.5, size=num_samples)

        return df

    df_weather = generate_weather_like_data(1000)
    print(df_weather.head())
    print(df_weather.tail())
    result_df = pd.DataFrame({'Prawdziwa': y_test[:5].values, 'Przewidziana': y_pred[:5]})
    print(result_df)

    synthetic_df = generate_synthetic_data(200)
    # print(synthetic_df.head())




    def test_model_mse_reasonable(self):
        # Sprawdź czy MSE nie jest zbyt wysokie (prosty sanity check)
        y_pred = self.model.predict(self.X)
        mse = mean_squared_error(self.y, y_pred)
        self.assertLess(mse, 100)  # wartość graniczna do dostosowania pod dane

if __name__ == '__main__':
    unittest.main()
