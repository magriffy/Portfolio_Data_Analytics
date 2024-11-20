import pandas as pd

bc_df = pd.read_csv("BCHAIN-MKPRU.csv")
gold_df = pd.read_csv("LBMA-GOLD.csv")

print(bc_df.head())
print(gold_df.head())
