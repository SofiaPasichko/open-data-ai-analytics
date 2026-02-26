import pandas as pd

def run_data_quality_checks(file_path):
    df = pd.read_csv(file_path, sep=';', decimal=',', na_values='null')
    
    print(f"Звіт про якість даних: {file_path} ---")
    
    num_rows, num_cols = df.shape
    print(f"\n1. Розмірність даних:")
    print(f"- Кількість записів (рядків): {num_rows}")
    print(f"- Кількість ознак (стовпців): {num_cols}")

    missing_data = df.isnull().sum()
    total_missing = missing_data.sum()
    print(f"\n2. Пропущені значення:")
    if total_missing > 0:
        print(missing_data[missing_data > 0])
        print(f"Загальна кількість пропусків: {total_missing}")
    else:
        print("Пропущених значень не виявлено.")

    print("\n3. Типи даних ознак:")
    print(df.dtypes)

    duplicates = df.duplicated().sum()
    print(f"\n4. Кількість дублікатів: {duplicates}")

    return df

if __name__ == "__main__":
    file_name = 'shchodenni-za-sichen-2026.csv'
    df_clean = run_data_quality_checks(file_name)
