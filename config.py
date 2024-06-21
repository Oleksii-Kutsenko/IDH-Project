import os

if True:
    DATABASE_URI = (
        "mssql+pyodbc://s31841:pQ-7_3Zs@db-mssql/s31841?" "driver=SQL+Server+Native+Client+11.0&Trusted_Connection=yes"
    )
else:
    import dotenv

    dotenv.load_dotenv(".db_env")
    DATABASE_URI = f"mssql+pyodbc://{os.getenv('MSSQL_USER')}:{os.getenv('MSSQL_PASSWORD')}@{os.getenv('MSSQL_HOST')}/{os.getenv('MSSQL_DB')}?driver=ODBC+Driver+17+for+SQL+Server"
