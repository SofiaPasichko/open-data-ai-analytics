import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine


def load_and_prepare_data():
    db_user = os.getenv('POSTGRES_USER', 'user')
    db_password = os.getenv('POSTGRES_PASSWORD', 'password')
    db_db = os.getenv('POSTGRES_DB', 'mydb')
    db_host = os.getenv('POSTGRES_HOST', 'db')
    db_port = os.getenv('POSTGRES_PORT', '5432')

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_db}"
    engine = create_engine(connection_string)

    try:
        df = pd.read_sql("air_data", engine)
    except Exception as e:
        print(f"Помилка при читанні з БД: {e}")
        return pd.DataFrame()

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
    if df_long.empty:
        print("Немає даних для візуалізації")
        return

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

    output_path = "static/plot.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    print(f"Графік успішно збережено за шляхом: {output_path}")

    plt.close()


def main():
    df_long = load_and_prepare_data()
    visualize_pollution_data(df_long)


if __name__ == "__main__":
    main()