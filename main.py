import time

from etl.calculate_total_score import calculate_total_score
from etl.load_all_trade_dimension import load_all_trade_data
from etl.load_country_dimension import load_country_dimension
from etl.load_economic_dimension import load_economic_dimension
from etl.load_education_dimension import load_education_dimension
from etl.load_military_dimension import load_military_dimension
from etl.load_population_dimension import load_population_dimension
from etl.consistency_check import consistency_check

# Execute ETL process
if __name__ == "__main__":
    with open("performance_log.txt", "w") as f:
        f.write("Performance log\n")

    start = time.time()
    load_country_dimension()
    with open("performance_log.txt", "a") as f:
        f.write(f"Country dimension loaded in {((time.time() - start)/60)} minutes\n")

    # start = time.time()
    # load_education_dimension()
    # with open("performance_log.txt", "a") as f:
    #     f.write(f"Education dimension loaded in {((time.time() - start)/60)} minutes\n")

    # start = time.time()
    # load_economic_dimension()
    # with open("performance_log.txt", "a") as f:
    #     f.write(f"Economic dimension loaded in {((time.time() - start)/60)} minutes\n")

    start = time.time()
    load_military_dimension()
    with open("performance_log.txt", "a") as f:
        f.write(f"Military dimension loaded in {((time.time() - start)/60)} minutes\n")

    # start = time.time()
    # load_all_trade_data()
    # with open("performance_log.txt", "a") as f:
    #     f.write(f"Trade dimension loaded in {((time.time() - start)/60)} minutes\n")

    # start = time.time()
    # load_population_dimension()
    # with open("performance_log.txt", "a") as f:
    #     f.write(f"Population dimension loaded in {((time.time() - start)/60)} minutes\n")

    start = time.time()
    consistency_check()
    with open("performance_log.txt", "a") as f:
        f.write(f"Consistency check completed in {((time.time() - start)/60)} minutes\n")

    start = time.time()
    calculate_total_score()
    with open("performance_log.txt", "a") as f:
        f.write(f"Total score calculated in {((time.time() - start)/60)} minutes\n")
