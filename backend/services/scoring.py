import pandas as pd

def load_benchmark_data(file_path:str):
  # This function is for loading data store inside /data
  df = pd.read_csv(file_path)
  return df
  
def get_avg_price(ville: str, df: pd.Dataframe) -> float:
  # This function is for retrieving the avg price stored in the database 
  # given the name of the city
  result = df[df["Commune"] == ville]

  # This is for preparing the case of input mismatch and user's ivalid input 
  if result.empty:
    raise ValueError(f"Invalid input for column city:{ville}")
  return float(result["avg_price_m2"].values[0])

  
  
