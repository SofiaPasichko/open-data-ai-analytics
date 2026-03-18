import pandas as pd

url = "https://data.gov.ua/dataset/1c1d0513-a2f1-46c9-8130-b6ee5ebcc9c9/resource/aa48911d-b696-450b-ac94-8d08fb13d0f9/download/shchodenni-za-sichen-2026.csv"

df = pd.read_csv(url, sep=';', decimal=',', na_values='null')

df.columns = df.columns.str.strip()

if 'city' in df.columns:
    df['city'] = df['city'].astype(str).str.strip()

if 'nameImpurity' in df.columns:
    df['nameImpurity'] = df['nameImpurity'].astype(str).str.strip()

print("Перші 5 рядків таблиці:")
print(df.head())

print("\nІнформація про типи даних:")
print(df.info())