import pandas as pd
import os
from sqlalchemy import create_engine

db_user = os.getenv('POSTGRES_USER', 'user')
db_password = os.getenv('POSTGRES_PASSWORD', 'password')
db_db = os.getenv('POSTGRES_DB', 'mydb')
db_host = os.getenv('POSTGRES_HOST', 'db')
db_port = os.getenv('POSTGRES_PORT', '5432')

url = "https://data.gov.ua/dataset/1c1d0513-a2f1-46c9-8130-b6ee5ebcc9c9/resource/aa48911d-b696-450b-ac94-8d08fb13d0f9/download/shchodenni-za-sichen-2026.csv"

try:
    df = pd.read_csv(url, sep=';', decimal=',', na_values='null')

    df.columns = df.columns.str.strip()
    if 'city' in df.columns:
        df['city'] = df['city'].astype(str).str.strip()
    if 'nameImpurity' in df.columns:
        df['nameImpurity'] = df['nameImpurity'].astype(str).str.strip()

    print("Data loaded from URL")

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_db}"
    engine = create_engine(connection_string)

    df.to_sql("air_data", engine, if_exists="replace", index=False)
    print("Saved to database successfully")

except Exception as e:
    print(f"Error occurred: {e}")