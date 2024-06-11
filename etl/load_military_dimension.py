import math

import pandas as pd

from country_name_solver import CountryNameSolver
from db import Session
from models.time_dimension import TimeDimension
from models.country_statistics import CountryStatistics
from models.military_dimension import MilitaryDimension

def load_military_dimension():
    country_name_solver = CountryNameSolver()
    file = '/home/kataha/New/IDH-Project/etl/data/SIPRI-Milex-data-1949-2023.xlsx'

    sheet = pd.read_excel(file, 
        sheet_name = "Constant (2022) US$", 
        header= 5)
    sheet = sheet.drop('Unnamed: 1', axis=1)
    sheet = sheet.drop('Notes', axis = 1)
    sheet.dropna(inplace=True)
    sheet.replace("...", 0, inplace=True)
    sheet.replace("xxx", 0, inplace=True)
    sheet = pd.melt(sheet, id_vars=["Country"], var_name="year", value_name="value")

    data_years = set(sheet["year"].unique())
    with Session() as session:
            existed_years = set(year[0] for year in session.query(TimeDimension.year).all())
            not_existed_years = set(data_years) - existed_years

            to_create_time_dimension = [TimeDimension(year=year) for year in not_existed_years]
            session.add_all(to_create_time_dimension)

            session.commit()

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

            military_spending = row["value"]
            military_dimension = MilitaryDimension(military_spending=military_spending)

            with Session() as session:
                session.add(military_dimension)
                session.flush()
                country_statistics.military_id = military_dimension.military_id
                session.add(military_dimension)
                session.add(country_statistics)
                session.commit()
