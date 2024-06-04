import json
from typing import Dict, List

import requests

from db import Session
from models.country_dimension import CountryDimension

DATA_URL = "http://api.worldbank.org/v2/country/?format=json&per_page=300"
SERIALIZED_DATA_PATH = "etl/data/countries.json"


def serialize_countries_data(raw_countries_data: List[Dict[str, str]]) -> None:
    countries_data = []

    for raw_country_data in raw_countries_data:
        country_name = raw_country_data["name"]
        country_id = raw_country_data["id"]
        countries_data.append({"country_id": country_id, "country_name": country_name})

    with open(SERIALIZED_DATA_PATH, "w") as f:
        json.dump(countries_data, f)


def load_country_dimension():
    response = requests.get(DATA_URL)
    # Serialize response to JSON in case URL is not available
    if response.status_code == 200:
        data = response.json()
        assert len(data) == 2
        pages_info = data[0]
        assert pages_info["page"] == 1
        assert pages_info["pages"] == 1

        raw_countries_data = data[1]
        serialize_countries_data(raw_countries_data)
    else:
        raw_countries_data = json.loads(open(SERIALIZED_DATA_PATH).read())

    countries_dim_objects = []
    with Session() as session:
        session.query(CountryDimension).delete()
        for raw_country_data in raw_countries_data:
            country_dim_object = CountryDimension(
                country_code=raw_country_data["id"],
                country_name=raw_country_data["name"],
            )
            countries_dim_objects.append(country_dim_object)
        session.bulk_save_objects(countries_dim_objects)
