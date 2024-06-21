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

    column_names = [
        "Country",
        1981,
        1982,
        1983,
        1984,
        1985,
        1986,
        1987,
        1988,
        1989,
        1990,
        1991,
        1992,
        1993,
        1994,
        1995,
        1996,
        1997,
        1998,
        1999,
        2000,
        2001,
        2002,
        2003,
        2004,
        2005,
        2006,
        2007,
        2008,
        2009,
        2010,
        2011,
        2012,
        2013,
        2014,
        2015,
        2016,
        2017,
        2018,
        2019,
        2020,
        2021,
        2022,
    ]
    sheet = pd.read_excel(file, sheet_name="Sheet1", header=0, names=column_names)

    sheet = pd.melt(sheet, id_vars=["Country"], var_name="year", value_name="value")

    dictyears = {
        2016: "etl/data/2016tables-country.xlsx",
        2017: "etl/data/2017tables-country.xlsx",
        2018: "etl/data/2018tables-country.xlsx",
        2019: "etl/data/2019tables-country.xlsx",
        2020: "etl/data/2020tables-country.xlsx",
        2021: "etl/data/2021tables-country.xlsx",
        2022: "etl/data/2022tables-country.xlsx",
        2023: "etl/data/2023tables-country.xlsx",
    }

    data_years = set(sheet["year"].unique()).union(set(dictyears.keys()))
    with Session() as session:
        existed_years = set(year[0] for year in session.query(TimeDimension.year).all())
        not_existed_years = set(data_years) - existed_years

        to_create_time_dimension = [TimeDimension(year=year) for year in not_existed_years]
        session.add_all(to_create_time_dimension)

        session.commit()

    for year in dictyears:
        if year == 2016 or year == 2023:
            sheet_nature = pd.read_excel(year, sheet_name=str(year) + "-tables-country", header=0)
            sheet_nature = sheet_nature.drop(sheet_nature.columns[0], axis=1)
        else:
            sheet_nature = pd.read_excel(year, sheet_name=year + "-tables-country", header=0)
            columnsToDrop = [0,2,5]
            sheet_nature = sheet_nature.drop(sheet_nature.columns[columnsToDrop], axis=1)
        
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
