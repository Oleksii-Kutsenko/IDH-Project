import pandas as pd

def load_population_dimension():
    data = pd.read_csv("etl/data/population_data.csv")
    
    data.columns
    import pdb; pdb.set_trace()
