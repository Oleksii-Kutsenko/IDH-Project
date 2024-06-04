from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URI
from models.base import Base

# all models should be imported in order to be created with `Base.metadata.create_all(engine)` statement
from models.country_dimension import CountryDimension  # pylint: disable=unused-import
from models.country_statistics import CountryStatistics  # pylint: disable=unused-import
from models.education_dimension import (
    EducationDimension,  # pylint: disable=unused-import
)
from models.time_dimension import TimeDimension  # pylint: disable=unused-import

engine = create_engine(DATABASE_URI)


Session = sessionmaker(bind=engine)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
