import json
from typing import Dict, List

from db import Session
from models.country_dimension import CountryDimension

DATA_PATH = "etl/data/countries.json"


def serialize_countries_data(raw_countries_data: List[Dict[str, str]]) -> None:
    countries_data = []

    for raw_country_data in raw_countries_data:
        country_name = raw_country_data["name"]
        country_id = raw_country_data["id"]
        countries_data.append({"country_id": country_id, "country_name": country_name})

    with open(DATA_PATH, "w") as f:
        json.dump(countries_data, f)


def load_country_dimension():
    raw_countries_data = json.loads(open(DATA_PATH).read())

    countries_dim_objects = []
    with Session() as session:
        session.query(CountryDimension).delete()
        for raw_country_data in raw_countries_data:
            country_dim_object = CountryDimension(
                country_code=raw_country_data["alpha-3"],
                country_name=raw_country_data["name"],
            )
            countries_dim_objects.append(country_dim_object)
        session.bulk_save_objects(countries_dim_objects)
        session.commit()
