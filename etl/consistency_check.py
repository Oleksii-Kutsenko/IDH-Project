from db import Session
from models.country_dimension import CountryDimension
from models.country_statistics import CountryStatistics
from models.time_dimension import TimeDimension


def consistency_check():
    # render the time and country dimensions for all countries and years
    with Session() as session:
        time_dimensions = session.query(TimeDimension).all()
        country_dimensions = session.query(CountryDimension).all()

        to_create_country_statistics = []

        for time in time_dimensions:
            for country in country_dimensions:
                existing_stats = (
                    session.query(CountryStatistics).filter_by(time_id=time.time_id, country_id=country.country_id).first()
                )

                if not existing_stats:
                    new_stat = CountryStatistics(
                        time_id=time.time_id,
                        country_id=country.country_id,
                    )
                    to_create_country_statistics.append(new_stat)

        if to_create_country_statistics:
            session.bulk_save_objects(to_create_country_statistics)
            session.commit()
