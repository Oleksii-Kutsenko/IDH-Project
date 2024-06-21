import os

import dotenv

dotenv.load_dotenv(".db_env")

if int(os.getenv("DEBUG")):
    DATABASE_URI = f"mssql+pyodbc://{os.getenv('MSSQL_DEV_USER')}:{os.getenv('MSSQL_DEV_PASSWORD')}@{os.getenv('MSSQL_DEV_HOST')}/{os.getenv('MSSQL_DEV_DB')}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=no"
else:
    DATABASE_URI = (
        f"mssql+pyodbc://{os.getenv('MSSQL_USER')}:{os.getenv('MSSQL_PASSWORD')}@db-mssql/s31841?"
        "driver=SQL+Server+Native+Client+11.0&Trusted_Connection=yes"
    )
