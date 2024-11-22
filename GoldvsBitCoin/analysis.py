import pandas as pd
from IPython.core.pylabtools import figsize
from matplotlib import pyplot as plt

bc_df = pd.read_csv("BCHAIN-MKPRU.csv")
gold_df = pd.read_csv("LBMA-GOLD.csv")

print(bc_df.head())
print(gold_df.head())

divisor = len(bc_df["Date"]) // 5

for date in bc_df["Date"]:
    print(date)

print(len(gold_df["Date"]))
b_xtcks = [bc_df["Date"][0], bc_df["Date"][365], bc_df["Date"][730], bc_df["Date"][1095], bc_df["Date"][1460], bc_df["Date"][1825]]

g_xtcks = [gold_df["Date"][0], gold_df["Date"][253], gold_df["Date"][506], gold_df["Date"][759], gold_df["Date"][1012], gold_df["Date"][1264]]

for date in gold_df["Date"]:
    print(bc_df[])

for i in range(100):
    print(f"GOLD: {gold_df["Date"][i]}\nBTC: {bc_df["Date"][i]}\n")

figure, axis = plt.subplots(2,1)
figure.set_figwidth(12)
figure.set_figheight(10)

# Bitcoin plot
axis[0].plot(bc_df["Date"], bc_df["Value"])
axis[0].set_xticks(b_xtcks)
axis[0].set_xlabel("Date")
axis[0].set_ylabel("Price of 1 Bitcoin")

# Gold plot
axis[1].plot(gold_df["Date"], gold_df["Value"])
axis[1].set_xticks(g_xtcks)
axis[1].set_xlabel("Date")
axis[1].set_ylabel("Price of 1 Troy Oz. of Gold")

figure.suptitle("Price of 1 Bitcoin vs. 1 Troy Oz. of Gold")
plt.show()

"""
plt.figure(figsize=(12, 4))
plt.plot(bc_df["Date"], bc_df["Value"])
plt.xticks(xtcks)
plt.xlabel("Date")
plt.ylabel("Price of 1 Bitcoin")
plt.title("Price of 1 BTC Over Time")
plt.show()
"""
