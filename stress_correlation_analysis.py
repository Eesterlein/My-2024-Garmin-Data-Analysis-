import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🔹 Set correct path to the cleaned data folder
DATA_FOLDER = "/Users/Elissa/Documents/garmin_data_analysis/cleaned_data"

# 🔹 Define dataset filenames
files = {
    "stress": "Stress.csv",
    "intensity": "Intensity Minutes.csv",
    "sleep": "Sleep.csv",
    "heart_rate": "Average Heart Rate.csv",
}

# 🔹 Load datasets into pandas DataFrames
data = {name: pd.read_csv(os.path.join(DATA_FOLDER, filename)) for name, filename in files.items()}

# 🔹 Standardize column names and ensure date formatting
for name, df in data.items():
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    data[name] = df

# 🔹 Convert Sleep Duration (e.g., "8h 32min") to Total Minutes
def convert_sleep_to_minutes(duration):
    """Converts sleep duration from '8h 32min' format to total minutes."""
    try:
        parts = duration.split("h")
        hours = int(parts[0].strip()) if parts[0].strip().isdigit() else 0
        minutes = int(parts[1].replace("min", "").strip()) if "min" in parts[1] else 0
        return hours * 60 + minutes
    except:
        return None  # Handle errors gracefully

data["sleep"]["avg_duration"] = data["sleep"]["avg_duration"].apply(convert_sleep_to_minutes)

# 🔹 Merge datasets on 'date' to analyze correlations
merged_df = data["stress"].merge(data["intensity"], on="date", how="inner").merge(
    data["sleep"], on="date", how="inner"
).merge(data["heart_rate"], on="date", how="left")  # Left join to keep all stress records

# 🔹 Handle missing heart rate values by forward-filling
merged_df["heart_rate"] = merged_df["heart_rate"].ffill()

# --- 📊 Correlation Analysis ---
correlations = merged_df[["stress", "actual", "avg_duration", "heart_rate"]].corr()
print("\n📊 Correlation Matrix:")
print(correlations)

# --- 📈 Scatter Plot: Training Intensity vs. Stress ---
plt.figure(figsize=(8, 6))
sns.regplot(x=merged_df["actual"], y=merged_df["stress"], 
            scatter_kws={"color": "blue", "alpha": 0.6}, 
            line_kws={"color": "red"})
plt.xlabel("Intensity Minutes")
plt.ylabel("Stress Level")
plt.title("Relationship Between Training Intensity and Stress")
plt.grid(True)
plt.show()

# --- 📈 Scatter Plot: Resting Heart Rate vs. Stress ---
plt.figure(figsize=(8, 6))
sns.regplot(x=merged_df["heart_rate"], y=merged_df["stress"], 
            scatter_kws={"color": "green", "alpha": 0.6}, 
            line_kws={"color": "orange"})
plt.xlabel("Resting Heart Rate (bpm)")
plt.ylabel("Stress Level")
plt.title("Relationship Between Resting Heart Rate and Stress")
plt.grid(True)
plt.show()

# ✅ Ensure Plots Do Not Block Terminal Execution
plt.show(block=False)
