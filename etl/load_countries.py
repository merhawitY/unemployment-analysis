import requests
import pandas as pd
from sqlalchemy import create_engine

# MySQL connection
DB_USER = "etl_user"
DB_PASSWORD = "DataPipeline2026!"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "unemployment_analysis"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# World Bank Countries API
url = "https://api.worldbank.org/v2/country?format=json&per_page=300"

response = requests.get(url)
response.raise_for_status()

countries = response.json()[1]

rows = []

for country in countries:

    # Skip aggregate groups
    if country["region"]["value"] == "Aggregates":
        continue

    rows.append({
        "country_code": country["id"],
        "country_name": country["name"],
        "region": country["region"]["value"],
        "income_group": country["incomeLevel"]["value"]
    })

df = pd.DataFrame(rows)

print(df.head())

df.to_sql(
    "countries",
    con=engine,
    if_exists="append",
    index=False
)

print(f"{len(df)} countries loaded successfully!")