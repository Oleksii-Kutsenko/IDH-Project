from etl.calculate_total_score import calculate_total_score
from etl.load_all_trade_dimension import load_all_trade_data
from etl.load_country_dimension import load_country_dimension
from etl.load_economic_dimension import load_economic_dimension
from etl.load_education_dimension import load_education_dimension
from etl.load_military_dimension import load_military_dimension

# Execute ETL process
if __name__ == "__main__":
    load_country_dimension()
    load_education_dimension()
    load_economic_dimension()
    load_military_dimension()
    load_all_trade_data()

    calculate_total_score()
