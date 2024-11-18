import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import ttest_ind

df = pd.read_excel("Problem_C_Data_Wordle.xlsx", usecols="B:M")
# Date, Contest #, Word, # of reported results, # in hard mode, 1 try, 2 tries, 3 tries..
df.columns = ["date", "contest", "word", "reported", "hard", "1", "2", "3", "4", "5", "6", "X"]

# Changes the dates all to the form of year-month-day
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

# makes another column called 'day_of_week' and uses the date from the 'date' column to detemine which day of the week it is
df['day_of_week'] = df['date'].dt.day_name()


df.set_index("date", inplace=True)
daily_results = df["reported"]

# calculates the mean by total reported for each day of the week
reported_by_day = df.groupby('day_of_week')['reported'].mean()
# calculates the mean by total mean for each day of the week
reported_by_day_hard = df.groupby('day_of_week')['hard'].mean()

# print(reported_by_day)
# print(reported_by_day_hard)
# print(df)

# Order the days of the week correctly
ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
reported_by_day = reported_by_day.reindex(ordered_days)
reported_by_day_hard = reported_by_day_hard.reindex(ordered_days)

# Plot the bar chart
plt.figure(figsize=(10, 6))
reported_by_day.plot(kind='bar', color='skyblue')
# reported_by_day_hard.plot(kind='bar', color='blue')
plt.title("Number of Reported Results by Day of the Week")
plt.xticks(rotation=45)
# plt.show()


# Prepare lagged features
df_rf = pd.DataFrame(daily_results)
for lag in range(1, 8):  # Using past 7 days as features
    df_rf[f'lag_{lag}'] = df_rf['reported'].shift(lag)

# Remove rows with NaN values (caused by shifting)
df_rf.dropna(inplace=True)

# Split data into features (X) and target (y)
X = df_rf.drop('reported', axis=1)
y = df_rf['reported']

# Train the Random Forest model, reserving the last 30 days for testing
model_rf = RandomForestRegressor()
model_rf.fit(X[:-30], y[:-30])

# Predict for the last available day in the test set (March 1, 2023, assumed to be 30 days ahead)
future_values = X[-1:]  # Taking the latest feature row for prediction
predicted_value_rf = model_rf.predict(future_values)

print(f"Predicted reported results on March 1, 2023 (Random Forest): {predicted_value_rf[0]}")


"""
Try to establish variation in data from number of consonants/vowels in word
"""
vowels = ["a", "e", "i", "o", "u"]

i = 1



def c_count(word):
    """
    Utility function that returns number of consonants in a word

    :param word: Wordle word
    :return: Number of consonants in word
    """

    consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y",
                  "z"]
    cs = 0
    #loops through each work to detect number of consonants
    for l in word:
        if l in consonants:
            cs += 1
    return cs

c_list = []
#loops through every word in data and runs the c_count function on them and adds them to a list
for word in df["word"]:
    c_list.append(c_count(word))

# Add number of consonants in word as column
df["consonants"] = c_list

#groups the average number of reports by the number of consonants found in the word
reported_by_consonants = df.groupby('consonants')['reported'].mean()
#groups the average number of hard reports by the number of consonants found in the word
reported_by_consonants_hard = df.groupby('consonants')['hard'].mean()
print(reported_by_consonants)
print(reported_by_consonants_hard)

#graphs the consonant data
plt.figure(figsize=(10, 6))
reported_by_consonants_hard.plot(kind='bar', color='skyblue')
# reported_by_day_hard.plot(kind='bar', color='blue')
plt.title("Number of Reported Results by Number of Consonants in Word")
plt.xticks(rotation=45)
plt.show()

easy = []
hard = []
e_perc = (df["reported"], df["2"] + df["3"] + df["4"])
h_perc = (df["reported"], df["5"] + df["6"] + df["X"])

h_avg = 0

for index, row in df.iterrows():

    e_perc = row["2"] + row["3"] + row["4"]
    h_perc = row["5"] + row["6"] + row["X"]

    if e_perc >= 50:
        easy.append(row["hard"])
    if h_perc >= 50:
        hard.append(row["hard"])

h_avg = sum(hard) / len(hard)
e_avg = sum(easy) / len(easy)

print(f"Easy: {e_avg}")
print(f"Hard: {h_avg}")

#t test
# Sample data
data1 = [1, 2, 3, 4, 5]
data2 = [6, 7, 8, 9, 10]

# Perform t-test
t_statistic, p_value = ttest_ind(easy, hard)

print("p-value:", p_value, " >.05 therefore not statistically significant")