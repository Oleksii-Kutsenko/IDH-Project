import math
from pathlib import Path

import pandas as pd

from country_name_solver import CountryNameSolver
from db import Session
from models.country_statistics import CountryStatistics
from models.military_dimension import MilitaryDimension
from models.time_dimension import TimeDimension


def load_military_dimension():
    country_name_solver = CountryNameSolver()
    file = Path("etl/data/military_expeditures.xlsx").resolve()

    sheet = pd.read_excel(file, sheet_name="Constant (2022) US$", header=5)
    sheet.drop(columns=["Unnamed: 1", "Notes"], inplace=True)
    sheet.dropna(inplace=True)
    sheet.replace({"...": 0, "xxx": 0}, inplace=True)
    sheet = pd.melt(sheet, id_vars=["Country"], var_name="year", value_name="value")

    data_years = set(sheet["year"].unique())
    with Session() as session:
        existed_years = set(year[0] for year in session.query(TimeDimension.year).all())
        not_existed_years = data_years - existed_years

        to_create_time_dimension = [TimeDimension(year=year) for year in not_existed_years]
        if to_create_time_dimension:
            session.bulk_save_objects(to_create_time_dimension)
            session.commit()

        year_2_time_id = dict(session.query(TimeDimension.year, TimeDimension.time_id).all())

    country_statistics_to_insert = []

    with Session() as session:
        for _, row in sheet.iterrows():
            country_name = row["Country"]
            if isinstance(country_name, float) and math.isnan(country_name):
                continue

            country_id = country_name_solver.solve(country_name)
            if country_id is None:
                print(f"Country {country_name} not found in the database")
                continue

            time_id = year_2_time_id[row["year"]]
            military_spending = row["value"]

            country_statistics = (
                session.query(CountryStatistics)
                .filter(CountryStatistics.country_id == country_id, CountryStatistics.time_id == time_id)
                .one_or_none()
            )
            if country_statistics is None:
                country_statistics = CountryStatistics(
                    country_id=country_id,
                    time_id=time_id,
                )

            military_dimension = MilitaryDimension(military_spending=military_spending)
            session.add(military_dimension)
            session.flush()

            country_statistics.military_id = military_dimension.military_id
            country_statistics_to_insert.append(country_statistics)

        session.bulk_save_objects(country_statistics_to_insert)
        session.commit()
