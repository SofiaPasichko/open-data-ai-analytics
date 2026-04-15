import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine


def run_data_research(df):
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
        coef = model.coef_[0]
    else:
        trend = "немає даних"
        coef = None

    stability_analysis = so2_data.groupby('city')['value'].agg(['mean', 'std'])
    stability_analysis['variability_%'] = (
        stability_analysis['std'] / stability_analysis['mean']
    ) * 100

    unstable_cities = stability_analysis.sort_values('variability_%', ascending=False)

    with open("/reports/research_report.txt", "w", encoding="utf-8") as f:
        f.write("ДОСЛІДЖЕННЯ ДАНИХ\n\n")
        f.write("1. Топ-5 міст за SO2:\n")
        f.write(str(city_rating.head()))
        f.write("\n\n")
        f.write("2. Тренд Києва (Завислі речовини):\n")
        if coef is not None:
            f.write(f"Коефіцієнт: {coef:.5f}\n")
            f.write(f"Тренд: {trend}\n")
        else:
            f.write("Немає даних для Києва\n")
        f.write("\n3. Нестабільні міста (SO2):\n")
        f.write(str(unstable_cities[['mean', 'variability_%']].head()))

    print("\n1. Топ-5 міст за середнім рівнем SO2:")
    print(city_rating.head())

    print("\n2. Київ тренд:")
    if coef is not None:
        print(f"Коефіцієнт: {coef:.5f}")
        print(f"Результат: {trend}")
    else:
        print("Немає даних для Києва.")

    print("\n3. Нестабільні міста:")
    print(unstable_cities[['mean', 'variability_%']].head())

    return df_long


if __name__ == "__main__":
    db_user = os.getenv('POSTGRES_USER', 'user')
    db_password = os.getenv('POSTGRES_PASSWORD', 'password')
    db_db = os.getenv('POSTGRES_DB', 'mydb')
    db_host = os.getenv('POSTGRES_HOST', 'db')
    db_port = os.getenv('POSTGRES_PORT', '5432')

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_db}"
    engine = create_engine(connection_string)

    try:
        df = pd.read_sql("air_data", engine)
        run_data_research(df)
        print("\nLoaded from database")
    except Exception as e:
        print(f"Error: {e}")