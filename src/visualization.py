import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

URL = "https://data.gov.ua/dataset/1c1d0513-a2f1-46c9-8130-b6ee5ebcc9c9/resource/aa48911d-b696-450b-ac94-8d08fb13d0f9/download/shchodenni-za-sichen-2026.csv"


def load_and_prepare_data():
    df = pd.read_csv(URL, sep=';', decimal=',', na_values='null')

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

    return df_long


def visualize_pollution_data(df_long):
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))

    kyiv_dust = df_long[
        (df_long['city'] == 'Київ') &
        (df_long['nameImpurity'] == 'Завислі речовини')
    ]

    plt.subplot(1, 2, 1)
    sns.lineplot(data=kyiv_dust, x='day', y='value', marker='o')
    plt.title('Тренд пилу в Києві (Січень 2026)')
    plt.xlabel('День місяця')
    plt.ylabel('Концентрація')

    target_cities = ['Київ', 'Херсон', 'Вінниця', 'Суми']
    comparison_data = df_long[
        (df_long['city'].isin(target_cities)) &
        (df_long['nameImpurity'] == 'Дiоксид сiрки')
    ]

    plt.subplot(1, 2, 2)
    sns.boxplot(data=comparison_data, x='city', y='value')
    plt.title('Розподіл SO2: Стабільність vs Сплески')
    plt.xlabel('Місто')
    plt.ylabel('Концентрація')

    plt.tight_layout()

    import os
    os.makedirs("artifacts/visualization", exist_ok=True)
    plt.savefig("artifacts/visualization/plot.png")

    plt.close()


def main():
    df_long = load_and_prepare_data()
    visualize_pollution_data(df_long)


if __name__ == "__main__":
    main()