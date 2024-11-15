import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

df = pd.read_excel("Problem_C_Data_Wordle.xlsx", usecols="B:M")
# Date, Contest #, Word, # of reported results, # in hard mode, 1 try, 2 tries, 3 tries..
df.columns = ["date", "contest", "word", "reported", "hard", "1", "2", "3", "4", "5", "6", "X"]

df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")

df['day_of_week'] = df['date'].dt.day_name()

df.set_index("date", inplace=True)
daily_results = df["reported"]

reported_by_day = df.groupby('day_of_week')['reported'].mean()
reported_by_day_hard = df.groupby('day_of_week')['hard'].mean()

print(reported_by_day)
print(reported_by_day_hard)
print(df)

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
plt.show()


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

#I think I did this completely wrong, Idk how to plot the # reported depending on 
# the percentage wins tries. 

# # Calculate the sum of "reported" for each of the columns ["1", "2", "3", "4", "5", "6", "X"]
# percentWinColumns = ["1", "2", "3", "4", "5", "6", "X"]
# reported_totals = [df[col].sum() for col in percentWinColumns]

# # Create the bar chart
# plt.figure(figsize=(10, 6))
# plt.bar(percentWinColumns, reported_totals, color='skyblue', edgecolor='black')

# # Add labels and title
# plt.xlabel("Columns (1, 2, 3, 4, 5, 6, X)")
# plt.ylabel("Total Reported Results")
# plt.title("Reported Results Distribution Across Tries")
# plt.show()