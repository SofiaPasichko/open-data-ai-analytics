import pandas as pd

df = pd.read_csv('shchodenni-za-sichen-2026.csv', sep=';', decimal=',', na_values='null')

df.columns = df.columns.str.strip()
df['city'] = df['city'].str.strip()
df['nameImpurity'] = df['nameImpurity'].str.strip()

print("Перші 5 рядків таблиці:")
print(df.head())

print("\nІнформація про типи даних:")
print(df.info())
