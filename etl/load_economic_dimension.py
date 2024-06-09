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

    import pdb

    pdb.set_trace()
