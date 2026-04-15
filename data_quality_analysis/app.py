import pandas as pd
import os
from sqlalchemy import create_engine


def run_data_quality_checks(df):
    print("Звіт про якість даних ---")
    num_rows, num_cols = df.shape
    missing_data = df.isnull().sum()
    total_missing = missing_data.sum()
    duplicates = df.duplicated().sum()

    print(f"\n1. Розмірність даних:")
    print(f"- Кількість записів (рядків): {num_rows}")
    print(f"- Кількість ознак (стовпців): {num_cols}")

    print(f"\n2. Пропущені значення:")
    if total_missing > 0:
        print(missing_data[missing_data > 0])
        print(f"Загальна кількість пропусків: {total_missing}")
    else:
        print("Пропущених значень не виявлено.")

    print("\n3. Типи даних ознак:")
    print(df.dtypes)

    print(f"\n4. Кількість дублікатів: {duplicates}")

    with open("/reports/quality_report.txt", "w", encoding="utf-8") as f:
        f.write("Звіт про якість даних ---\n\n")
        f.write(f"1. Розмірність даних:\n- Рядків: {num_rows}\n- Стовпців: {num_cols}\n\n")
        f.write(f"2. Пропущені значення:\n{str(missing_data[missing_data > 0])}\n")
        f.write(f"Загальна кількість пропусків: {total_missing}\n")
        f.write(f"\n3. Типи даних:\n{str(df.dtypes)}\n")
        f.write(f"\n4. Кількість дублікатів: {duplicates}\n")

    return df


if __name__ == "__main__":
    db_user = os.getenv('POSTGRES_USER', 'user')
    db_password = os.getenv('POSTGRES_PASSWORD', 'password')
    db_db = os.getenv('POSTGRES_DB', 'mydb')
    db_host = os.getenv('POSTGRES_HOST', 'db')
    db_port = os.getenv('POSTGRES_PORT', '5432')

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_db}"
    engine = create_engine(connection_string)

    try:
        df_clean = pd.read_sql("air_data", engine)
        run_data_quality_checks(df_clean)
        print("\nAnalysis completed and saved to /reports")
    except Exception as e:
        print(f"Error connecting to DB: {e}")