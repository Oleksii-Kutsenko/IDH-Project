import pandas as pd

from country_name_solver import CountryNameSolver
from db import Session
from models.competitiveness_dimension import CompetitivenessDimension
from models.country_statistics import CountryStatistics
from models.time_dimension import TimeDimension
from models.trade_dimension import TradeDimension


def load_all_trade_data():
    country_name_solver = CountryNameSolver()

    export_dataframe = pd.read_excel("etl/data/export_trade_data.xlsx", skiprows=2)
    import_dataframe = pd.read_excel("etl/data/import_trade_data.xlsx", skiprows=2)

    export_dataframe = export_dataframe[export_dataframe["Product/Sector"] == "SI3_AGG - TO - Total merchandise"]
    export_dataframe = export_dataframe.drop(columns=["Product/Sector", "Partner Economy"])

    export_dataframe = export_dataframe.melt(id_vars=["Reporting Economy"], var_name="Year", value_name="Export Value")

    import_dataframe = import_dataframe[import_dataframe["Product/Sector"] == "SI3_AGG - TO - Total merchandise"]
    import_dataframe = import_dataframe.drop(columns=["Product/Sector", "Partner Economy"])

    import_dataframe = import_dataframe.melt(id_vars=["Reporting Economy"], var_name="Year", value_name="Import Value")

    import_export_dataframe = pd.merge(export_dataframe, import_dataframe, on=["Reporting Economy", "Year"])

    import_export_dataframe["Year"] = import_export_dataframe["Year"].astype(int)

    data_years = set(import_export_dataframe["Year"].unique())
    with Session() as session:
        existed_years = set(year[0] for year in session.query(TimeDimension.year).all())
        not_existed_years = set(data_years) - existed_years

        to_create_time_dimension = [TimeDimension(year=int(year)) for year in not_existed_years]
        session.add_all(to_create_time_dimension)

        session.commit()

    with Session() as session:
        year_2_time_id = dict(session.query(TimeDimension.year, TimeDimension.time_id).all())

    with Session() as session:
        for _, row in import_export_dataframe.iterrows():
            time_id = year_2_time_id[row["Year"]]
            country_id = country_name_solver.solve(row["Reporting Economy"])
            if country_id is None:
                continue

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

            export_value = row["Export Value"] if not pd.isna(row["Export Value"]) else 0
            import_value = row["Import Value"] if not pd.isna(row["Import Value"]) else 0

            competitiveness_dim_object = CompetitivenessDimension(export_value=export_value)
            session.add(competitiveness_dim_object)
            session.flush()
            country_statistics.competitiveness_id = competitiveness_dim_object.competitiveness_id

            trade_dim_object = TradeDimension(total_trade=export_value + import_value)
            session.add(trade_dim_object)
            session.flush()
            country_statistics.trade_id = trade_dim_object.trade_id

            session.add(country_statistics)
        session.commit()
