import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle
df = pd.read_csv('ml_dataset.csv')


df['t+1'] = df['t'].shift(-1)

df = df.dropna(subset=['t+1'])


if len(df) > 1:
    X = df[['t-6','t-5', 't-4', 't-3', 't-2', 't-1', 't']]
    y = df['t+1']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)

    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
