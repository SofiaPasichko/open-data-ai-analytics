import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def run_data_research():
    file_path = "https://data.gov.ua/dataset/1c1d0513-a2f1-46c9-8130-b6ee5ebcc9c9/resource/aa48911d-b696-450b-ac94-8d08fb13d0f9/download/shchodenni-za-sichen-2026.csv"

    df = pd.read_csv(file_path, sep=';', decimal=',', na_values='null')

    day_cols = [col for col in df.columns if col.isdigit()]
    meta_cols = ['city', 'coordinateNumber', 'nameImpurity']

    df_long = pd.melt(
        df,
        id_vars=meta_cols,
        value_vars=day_cols,
        var_name='day',
        value_name='value'
    )

    df_long['day'] = df_long['day'].astype(int)
    df_long = df_long.dropna(subset=['value'])

    print("Дослідження даних:")

    so2_data = df_long[df_long['nameImpurity'] == 'Дiоксид сiрки']
    city_rating = so2_data.groupby('city')['value'].mean().sort_values(ascending=False)

    print("\n1. Топ-5 міст за середнім рівнем SO2:")
    print(city_rating.head())

    print("\n2. Побудова моделі тренду для Києва (Завислі речовини):")

    kyiv_data = df_long[
        (df_long['city'] == 'Київ') &
        (df_long['nameImpurity'] == 'Завислі речовини')
        ].sort_values('day')

    if not kyiv_data.empty:
        X = kyiv_data[['day']].values
        y = kyiv_data['value'].values

        model = LinearRegression()
        model.fit(X, y)

        trend = "зростає" if model.coef_[0] > 0 else "падає"
        print(f"Коефіцієнт нахилу: {model.coef_[0]:.5f}")
        print(f"Результат: Рівень забруднення протягом місяця в середньому {trend}.")
    else:
        print("Немає даних для Києва.")

    print("\n3. Аналіз міст з найбільш нестабільним рівнем забруднення (SO2):")

    stability_analysis = so2_data.groupby('city')['value'].agg(['mean', 'std'])
    stability_analysis['variability_%'] = (
                                                  stability_analysis['std'] / stability_analysis['mean']
                                          ) * 100

    unstable_cities = stability_analysis.sort_values('variability_%', ascending=False)
    print(unstable_cities[['mean', 'variability_%']].head())

    return df_long


if __name__ == "__main__":
    df_transformed = run_data_research()