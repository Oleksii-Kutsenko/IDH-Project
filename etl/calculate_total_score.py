import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from db import Session
from models.competitiveness_dimension import CompetitivenessDimension
from models.country_dimension import CountryDimension
from models.country_statistics import CountryStatistics
from models.economic_dimension import EconomicDimension
from models.education_dimension import EducationDimension
from models.military_dimension import MilitaryDimension
from models.time_dimension import TimeDimension
from models.trade_dimension import TradeDimension

dimensions = [
    EducationDimension,
    EconomicDimension,
    MilitaryDimension,
    TradeDimension,
    CompetitivenessDimension,
]

dimension_values = {
    EducationDimension: EducationDimension.pisa_average_score,
    EconomicDimension: EconomicDimension.country_gdp,
    MilitaryDimension: MilitaryDimension.military_spending,
    TradeDimension: TradeDimension.total_trade,
    CompetitivenessDimension: CompetitivenessDimension.export_value,
}


def calculate_total_score():
    with Session() as session:
        time_dimensions = session.query(TimeDimension).all()

        for time in time_dimensions:
            dimension_objects_to_db = []

            for dimension in dimensions:
                dimension_value = dimension_values[dimension]
                country_statistics = (
                    session.query(CountryStatistics, dimension)
                    .join(dimension)
                    .filter(CountryStatistics.time_id == time.time_id)
                    .all()
                )

                if len(country_statistics) == 0:
                    continue

                country_statistics_df = pd.DataFrame(
                    [(cs[0], cs[1], getattr(cs[1], dimension_value.name)) for cs in country_statistics],
                    columns=["country_statistics", "dimension", "dimension_value"],
                )

                country_statistics_df["normalized_value"] = MinMaxScaler().fit_transform(
                    country_statistics_df["dimension_value"].values.reshape(-1, 1)
                )

                for _, row in country_statistics_df.iterrows():
                    dimension_object = row["dimension"]
                    score = row["normalized_value"]
                    dimension_object.normalized_score = score
                    dimension_objects_to_db.append(dimension_object)

            if dimension_objects_to_db:
                session.add_all(dimension_objects_to_db)
                session.commit()

        for time in time_dimensions:
            country_statistics = (
                session.query(
                    CountryStatistics,
                    EducationDimension.normalized_score.label("education_score"),
                    EconomicDimension.normalized_score.label("economic_score"),
                    MilitaryDimension.normalized_score.label("military_score"),
                    TradeDimension.normalized_score.label("trade_score"),
                    CompetitivenessDimension.normalized_score.label("competitiveness_score"),
                )
                .outerjoin(EducationDimension, CountryStatistics.education_id == EducationDimension.education_id)
                .outerjoin(EconomicDimension, CountryStatistics.economic_id == EconomicDimension.economic_id)
                .outerjoin(MilitaryDimension, CountryStatistics.military_id == MilitaryDimension.military_id)
                .outerjoin(TradeDimension, CountryStatistics.trade_id == TradeDimension.trade_id)
                .outerjoin(
                    CompetitivenessDimension,
                    CountryStatistics.competitiveness_id == CompetitivenessDimension.competitiveness_id,
                )
                .filter(CountryStatistics.time_id == time.time_id)
                .all()
            )

            if len(country_statistics) == 0:
                continue

            country_statistics_df = pd.DataFrame(
                [(cs[0], cs[1], cs[2], cs[3], cs[4], cs[5]) for cs in country_statistics],
                columns=[
                    "country_statistics",
                    "education",
                    "economic",
                    "military",
                    "trade",
                    "competitiveness",
                ],
            )
            country_statistics_df = country_statistics_df.fillna(0)
            country_statistics_df["total_score"] = country_statistics_df[
                ["education", "economic", "military", "trade", "competitiveness"]
            ].mean(axis=1)
            for _, row in country_statistics_df.iterrows():

                country_stat = row["country_statistics"]
                country_stat.total_score = row["total_score"]
                session.add(country_stat)

        session.commit()
