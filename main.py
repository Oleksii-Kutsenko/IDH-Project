from etl.load_country_dimension import load_country_dimension
from etl.load_economic_dimension import load_economic_dimension
from etl.load_education_dimension import load_education_dimension

# Execute ETL process
if __name__ == "__main__":
    load_country_dimension()
    load_education_dimension()
    load_economic_dimension()
