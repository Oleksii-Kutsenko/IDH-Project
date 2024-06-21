import math

import pandas as pd

from country_name_solver import CountryNameSolver
from db import Session
from models.time_dimension import TimeDimension
from models.country_statistics import CountryStatistics
from models.tech_dimension import TechDimension


def load_tech_dimension():

    country_name_solver = CountryNameSolver()
    file = "etl/data/rnd_spending.xlsx"
    column_names = ["Country"] + list(range(1981, 2023))

    sheet = pd.read_excel(file, sheet_name="Sheet1", header=0, names=column_names)
    sheet = pd.melt(sheet, id_vars=["Country"], var_name="year", value_name="value")
    
    dictyears = {
        year: f"etl/data/{year}-tables-country.xlsx"
        for year in range(2016, 2024)
    }

    data_years = set(sheet["year"].unique()).union(set(dictyears.keys()))
    with Session() as session:
        existed_years = set(year[0] for year in session.query(TimeDimension.year).all())
        not_existed_years = set(data_years) - existed_years

        to_create_time_dimension = [TimeDimension(year=year) for year in not_existed_years]
        session.add_all(to_create_time_dimension)

        session.commit()

    sheet_nature_dict = {}
    for year, file_path in dictyears.items():
        sheet_nature = pd.read_excel(file_path, sheet_name=f"{year}-tables-country", header=0)
        columns_to_drop = [0, 2, 5] if year not in {2016, 2023} else [0]
        sheet_nature = sheet_nature.drop(sheet_nature.columns[columns_to_drop], axis=1)
        sheet_nature_dict[year] = sheet_nature

        
    with Session() as session:

        year_2_time_id = dict(session.query(TimeDimension.year, TimeDimension.time_id).all())

    for _, row in sheet.iterrows():
        if isinstance(row["Country"], float) and math.isnan(row["Country"]):
            continue

        country_id = country_name_solver.solve(row["Country"])

        try:
            if country_id is None:
                raise ValueError(f"Country {row['Country']} not found in the database")
        except ValueError as e:
            print(e)
            continue

        time_id = year_2_time_id[row["year"]]

        with Session() as session:
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

        rnd_spending = row["value"]
        if rnd_spending == "NaN":
            rnd_spending = 0
        tech_dimension = TechDimension(rnd_spending=rnd_spending)

        with Session() as session:
            session.add(tech_dimension)
            session.flush()
            country_statistics.technology_id = tech_dimension.tech_id
            session.add(tech_dimension)
            session.add(country_statistics)
            session.commit()
