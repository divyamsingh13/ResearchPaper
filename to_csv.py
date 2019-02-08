import pandas as pd
import os

if os.path.exists("dataframe.pkl"):
    dt = pd.read_pickle("dataframe.pkl")
    print("creating csv")
    dt.to_csv("dataframe.csv")

else:
    print("dataframe does not exist")