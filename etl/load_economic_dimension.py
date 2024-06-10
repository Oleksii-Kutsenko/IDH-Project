import math

import pandas as pd

from country_name_solver import CountryNameSolver
from db import Session
from models.country_dimension import CountryDimension
from models.country_statistics import CountryStatistics
from models.economic_dimension import EconomicDimension
from models.time_dimension import TimeDimension


def load_economic_dimension():
    country_name_solver = CountryNameSolver()

    dataframe = pd.read_excel("etl/data/economic_data.xlsx", sheet_name="NGDPD")
    # drop last two rows with credits
    dataframe = dataframe.iloc[:-2]
    # group by country name and year
    dataframe = dataframe.rename(columns={"GDP, current prices (Billions of U.S. dollars)": "country_name"})
    dataframe = pd.melt(dataframe, id_vars=["country_name"], var_name="year", value_name="value")

    # create needed time dimension objects
    data_years = set(dataframe["year"].unique())
    with Session() as session:
        existed_years = set(year[0] for year in session.query(TimeDimension.year).all())
        not_existed_years = set(data_years) - existed_years

        to_create_time_dimension = [TimeDimension(year=year) for year in not_existed_years]
        session.add_all(to_create_time_dimension)

        session.commit()

    with Session() as session:
        year_2_time_id = dict(session.query(TimeDimension.year, TimeDimension.time_id).all())

    for _, row in dataframe.iterrows():
        if isinstance(row["country_name"], float) and math.isnan(row["country_name"]):
            continue

        country_id = country_name_solver.solve(row["country_name"])
        try:
            if country_id is None:
                raise ValueError(f"Country {row['country_name']} not found in the database")
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

            country_gdp = row["value"]
            if country_gdp == "no data":
                country_gdp = 0
            economic_dimension = EconomicDimension(country_gdp=country_gdp)
            country_statistics.economic_dimension = economic_dimension
            session.add(economic_dimension)
            session.add(country_statistics)
            session.commit()
