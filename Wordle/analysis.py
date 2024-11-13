import pandas as pd
from datetime import datetime

df = pd.read_excel("Problem_C_Data_Wordle.xlsx", usecols="B:M")
# Date, Contest #, Word, # of reported results, # in hard mode, 1 try, 2 tries, 3 tries..
df.columns = ["date", "contest", "word", "reported", "hard", "1", "2", "3", "4", "5", "6", "X"]

print(df.head())
