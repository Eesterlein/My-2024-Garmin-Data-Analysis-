import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🔹 Set the correct path to the cleaned data folder
DATA_FOLDER = "/Users/Elissa/Documents/garmin_data_analysis/cleaned_data"

# 🔹 Load the Steps dataset
file_path = os.path.join(DATA_FOLDER, "Steps.csv")
steps_df = pd.read_csv(file_path)

# 🔹 Standardize column names
steps_df.columns = steps_df.columns.str.strip().str.lower().str.replace(" ", "_")

# 🔹 Convert date column to datetime format
steps_df["date"] = pd.to_datetime(steps_df["date"], format="%B %Y", errors="coerce")

# 🔹 Sort data by date
steps_df = steps_df.sort_values("date")

# --- 📊 Plot Monthly Step Count ---
plt.figure(figsize=(10, 5))
sns.barplot(x=steps_df["date"].dt.strftime('%B %Y'), y=steps_df["steps"], palette="Blues")
plt.xticks(rotation=45)
plt.ylabel("Total Steps")
plt.xlabel("Month")
plt.title("Monthly Step Count Trend")
plt.show()
