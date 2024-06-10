import logging
from typing import Optional

from db import Session
from models.country_dimension import CountryDimension

logger = logging.getLogger(__name__)


class CountryNameSolver:
    """
    Helper class to get country id from country name
    """

    CITIES_MAPPING = {
        "jersey": "Jersey City",
        "malta": "Valletta",
        "cayman islands": "George Town",
        "guernsey": "St Peter Port",
        "bermuda": "Hamilton",
        "liechtenstein": "Vaduz",
        "gift city -gujarat": "Ahmedabad",
        "cyprus": "Nicosia",
        "isle of man": "Douglas",
        "bahrain": "Manama",
        "british virgin islands": "Road Town",
        "mauritius": "Port Louis",
        "bahamas": "Nassau",
        "trinidad and tobago": "Port of Spain",
        "barbados": "Bridgetown",
    }

    COUNTRIES_MAPPING = {
        "b-s-j-z (china)": "China",
        "bahamas, the": "Bahamas",
        "bahrain, kingdom of": "Kingdom of Bahrain",
        "baku (azerbaijan)": "Azerbaijan",
        "bolivia (plurinational state of)": "Bolivia, Plurinational State of",
        "burma": "Myanmar",
        "cape verde": "Republic of Cabo Verde",
        "china (beijing, shanghai, jiangsu, zhejiang)": "China",
        "china, people's republic of": "China",
        "congo (dem. rep.)": "Congo, The Democratic Republic of the",
        "congo, dem. rep.": "Congo, The Democratic Republic of the",
        "congo, dem. rep. of the": "Congo, The Democratic Republic of the",
        "congo, dr": "Congo, The Democratic Republic of the",
        "congo, rep.": "Republic of the Congo",
        "congo, republic": "Republic of the Congo",
        "congo, republic of": "Republic of the Congo",
        "cote d'ivoire (ivory coast)": "Republic of Côte d'Ivoire",
        "democratic republic of congo": "Congo, The Democratic Republic of the",
        "democratic republic of the congo": "Congo, The Democratic Republic of the",
        "east timor": "Timor-Leste",
        "egypt, arab rep.": "Egypt",
        "gambia, the": "Gambia",
        "iran (islamic republic of)": "Iran, Islamic Republic of",
        "iran, islamic rep.": "Iran, Islamic Republic of",
        "ivory coast": "Republic of Côte d'Ivoire",
        "korea (the republic of)": "Korea, Republic of",
        "korea, rep.": "Korea, Republic of",
        "korea, south": "Korea, Republic of",
        "kuwait, the state of": "State of Kuwait",
        "lao p.d.r.": "Lao People's Democratic Republic",
        "lao pdr": "Lao People's Democratic Republic",
        "laos": "Lao People's Democratic Republic",
        "liechtenstein*": "Liechtenstein",
        "marshall islands (the)": "Marshall Islands",
        "micronesia (federated states of)": "Micronesia, Federated States of",
        "micronesia, fed. states of": "Micronesia, Federated States of",
        "micronesia, fed. sts.": "Micronesia, Federated States of",
        "netherlands (the)": "Netherlands",
        "niger": "Republic of the Niger",
        "philippines (the)": "Philippines",
        "republic of congo": "Republic of the Congo",
        "republic of korea": "Korea, Republic of",
        "russian federation (the)": "Russian Federation",
        "saudi arabia, kingdom of": "Kingdom of Saudi Arabia",
        "south sudan, republic of": "South Sudan",
        "st. kitts and nevis": "Saint Kitts and Nevis",
        "st. lucia": "Saint Lucia",
        "st. vincent and the grenadines": "Saint Vincent and the Grenadines",
        "swaziland": "Eswatini",
        "timor leste": "Timor-Leste",
        "turkiye": "Turkey",
        "türkiye": "Turkey",
        "türkiye, republic of": "Turkey",
        "uae": "United Arab Emirates",
        "united arab emirates (the)": "United Arab Emirates",
        "united kingdom (uk)": "United Kingdom",
        "united kingdom of great britain and northern ireland (the)": "United Kingdom",
        "united states of america (the)": "United States",
        "united states of america (usa)": "United States",
        "venezuela (bolivarian republic of)": "Venezuela, Bolivarian Republic of",
        "venezuela, rb": "Venezuela, Bolivarian Republic of",
        "yemen, rep.": "Yemen",
        "russia": "Russian Federation",
        "czech republic": "Czechia",
        "korea": "Korea, Republic of",
        "slovak republic": "Slovakia",
        "united kingdom": "United Kingdom of Great Britain and Northern Ireland",
        "united states": "United States of America",
        "albania (2015)": "Albania",
        "argentina (2015)": "Argentina",
        "b-s-j-g (china)": "China",
        "kazakhstan (2015)": "Kazakhstan",
        "malaysia (2015)": "Malaysia",
        "moldova": "Moldova, Republic of",
        "ukraine (18 of 27 regions)": "Ukraine",
    }

    def __init__(self) -> None:
        try:
            session = Session()
            self.country_name_2_id = dict(
                session.query(CountryDimension.country_name, CountryDimension.country_id).all()
            )
            session.close()
        except Exception as e:
            logger.error(f"Error occurred while fetching country names: {e}")
            session.rollback()
            raise e

    @classmethod
    def get_country_name(cls, country_name: str) -> str:
        """
        Returns country name from COUNTRIES_MAPPING if it exists
        Args:
            country_name: problematic country name

        Returns:
            str: valid country name
        """
        if country_name.lower() in cls.COUNTRIES_MAPPING:
            return cls.COUNTRIES_MAPPING[country_name.lower()]
        return country_name

    def solve(self, country_name: str) -> Optional[int]:
        """
        Returns country id from country name
        Args:
            country_name: problematic country name

        Returns:
            Optional[int]: country id
        """
        country_name = self.get_country_name(country_name)
        return self.country_name_2_id.get(country_name)

    @classmethod
    def get_city_name(cls, city_name: str) -> str:
        """
        Returns city name from CITIES_MAPPING if it exists
        Args:
            city_name: possible problematic city name

        Returns:
            str: valid city name
        """
        if city_name.lower() in cls.CITIES_MAPPING:
            return cls.CITIES_MAPPING[city_name.lower()]
        return city_name


# List of territories, regions, and unrecognized countries
# These are not included in the country dimension table
territories_regions_unrecognized_countries = {
    "aruba",
    "chinese taipei",
    "cook islands",
    "faroe islands",
    "french polynesia",
    "gibraltar",
    "greenland",
    "guernsey",
    "hong kong",
    "hong kong (china)",
    "hong kong sar",
    "international",
    "kosovo",
    "macao",
    "macao (china)",
    "macao sar",
    "martinique",
    "palestinian territories",
    "puerto rico",
    "reunion",
    "taiwan",
    "taiwan, province of china",
    "vatican city",
    "vatican city state (holy see)",
    "virgin islands, british",
    "selected countries and jurisdictions",
    "palestinian authority",
    "international average (oecd)",
}
