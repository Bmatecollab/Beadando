import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def create_linear_model(df: pd.DataFrame, x_col: str, y_col: str) -> LinearRegression:
    """
    Lineáris regressziós modell számítása az összes adatból
    :param df: a megadott DataFrame
    :param x_col: x oszlop, ami alapján felállítja a modellt
    :param y_col: y oszlop, amit próbál prediktálni
    :return: a modell
    """
    # Lineáris regresszió
    X = df[[x_col]].values  # a DataFrame bemeneti adatainak elkérése
    y = df[y_col].values  # az x-ekhez tartozó értékek elkérése

    # Lineáris regresszió modell betanítása
    model = LinearRegression()  # a modell létrehozása
    model.fit(X, y)  # a modell betanítása
    return model  # a függvény visszatér a modellel.


def calculate_linear_accuracy(df: pd.DataFrame, x_col: str, y_col: str, random_seed: int) -> float:
    """
    Lineáris regressziós modell számítása az összes adatból
    :param df: a megadott DataFrame
    :param x_col: x oszlop, ami alapján felállítja a modellt
    :param y_col: y oszlop, amit próbál prediktálni
    :param random_seed: seed a véletlenszám-generátor számára, így determinisztikus értéket számol
    :return: a modell
    """
    # Lineáris regresszió
    X = df[[x_col]].values  # a DataFrame bemeneti adatainak elkérése
    y = df[y_col].values  # az x-ekhez tartozó értékek elkérése

    # Adatok osztása tréningre és tesztelésre
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_seed)

    # Lineáris regresszió modell betanítása a training adatokon
    model = LinearRegression()  # a modell létrehozása
    model.fit(X_train, y_train)  # a modell betanítása

    y_pred = model.predict(X_test)  # predikciók kiszámítása az ismert helyeken
    y_errors = abs(y_pred - y_test)  # hibák abszolútértékének kiszámítása (lehetne négyzetes hiba is)
    return np.average(y_errors)  # visszatérés az átlagukkal


def calculate_multiple_models(df: pd.DataFrame, x_col: str, y_col: str) -> float:
    N = 10  # lineáris modellek száma, ennyi darabon átlagol a számításkor
    # modellek átlagos hibáinak listája
    errors = [calculate_linear_accuracy(df, x_col, y_col, i) for i in range(N)]
    return np.average(errors)  # ezek átlaga az eredmény
