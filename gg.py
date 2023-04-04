import pandas as pd

df = pd.read_csv('./data/check.csv')
print(df.time[2])