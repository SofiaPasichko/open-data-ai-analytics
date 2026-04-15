from flask import Flask, render_template, send_from_directory
from sqlalchemy import create_engine
import pandas as pd
import os

app = Flask(__name__)

db_user = os.getenv('POSTGRES_USER', 'user')
db_password = os.getenv('POSTGRES_PASSWORD', 'password')
db_db = os.getenv('POSTGRES_DB', 'mydb')
db_host = os.getenv('POSTGRES_HOST', 'db')
db_port = os.getenv('POSTGRES_PORT', '5432')

connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_db}"
engine = create_engine(connection_string)


@app.route("/")
def home():
    try:
        df = pd.read_sql("SELECT * FROM air_data", engine)

        days_to_show = ['1', '2', '3', '4', '5']
        cols_to_show = ['city', 'nameImpurity'] + [d for d in days_to_show if d in df.columns]

        df_preview = df[cols_to_show].iloc[::12]

        columns = df_preview.columns.tolist()
        data = df_preview.values.tolist()

        return render_template("index.html", columns=columns, data=data)
    except Exception as e:
        return f"Помилка завантаження даних з БД: {e}"


@app.route("/report")
def report():
    try:
        quality = "Звіт про якість ще не створено."
        research = "Звіт про дослідження ще не створено."

        if os.path.exists("/reports/quality_report.txt"):
            with open("/reports/quality_report.txt", "r", encoding="utf-8") as f:
                quality = f.read()

        if os.path.exists("/reports/research_report.txt"):
            with open("/reports/research_report.txt", "r", encoding="utf-8") as f:
                research = f.read()

        content = f"{quality}\n\n{'=' * 40}\n\n{research}"
    except Exception as e:
        content = f"Помилка при читанні звітів: {e}"

    return f"<pre style='padding: 20px; background: #f4f4f4;'>{content}</pre>"


@app.route("/plot")
def plot():
    return """
        <div style='text-align: center; font-family: Arial, sans-serif; padding: 20px;'>
            <h1>Аналітичні графіки (Seaborn)</h1>
            <img src='/static/plot.png' width='900' style='border: 1px solid #ddd; border-radius: 8px;'/>
        </div>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)