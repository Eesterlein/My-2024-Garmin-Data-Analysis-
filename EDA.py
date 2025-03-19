import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set folder path for cleaned data
CLEANED_FOLDER = "cleaned_data"

# List of cleaned CSV files
files = [
    "Activities.csv",
    "Average Heart Rate.csv",
    "Max Heart Rate.csv",
    "Calories.csv",
    "Floors Climbed.csv",
    "Intensity Minutes.csv",
    "Stress.csv",
    "Sleep.csv"
]

# Load all datasets into a dictionary
data = {}
for file in files:
    file_path = os.path.join(CLEANED_FOLDER, file)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        data[file] = df
        print(f"✅ Loaded {file} with shape {df.shape}")
    else:
        print(f"⚠️ {file} not found, skipping...")

# Function to display basic information about datasets
def summarize_datasets(data):
    """Prints basic information, missing values, and statistics for each dataset."""
    for name, df in data.items():
        print(f"\n📊 Summary for {name}:")
        print(df.info())  # Column types and non-null values
        print("\n🔍 Missing Values:\n", df.isnull().sum())  # Missing values
        print("\n📈 Basic Statistics:\n", df.describe())  # Summary statistics

# Run initial summaries
summarize_datasets(data)

# Exploratory Visualizations
def plot_time_series(df, x_col, y_col, title, ylabel):
    """Plots a time series chart."""
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df, x=x_col, y=y_col, marker="o")
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

# Plot key metrics
if "Average Heart Rate.csv" in data:
    plot_time_series(data["Average Heart Rate.csv"], "date", "heart_rate", "Average Heart Rate Over Time", "Heart Rate (bpm)")

if "Max Heart Rate.csv" in data:
    plot_time_series(data["Max Heart Rate.csv"], "date", "max_heart_rate", "Max Heart Rate Over Time", "Max Heart Rate (bpm)")

if "Calories.csv" in data:
    plot_time_series(data["Calories.csv"], "date", "total_calories", "Total Calories Burned Over Time", "Calories Burned")

if "Floors Climbed.csv" in data:
    plot_time_series(data["Floors Climbed.csv"], "date", "climbed_floors", "Floors Climbed Over Time", "Floors Climbed")

if "Intensity Minutes.csv" in data:
    plot_time_series(data["Intensity Minutes.csv"], "date", "actual", "Intensity Minutes Over Time", "Minutes")

if "Stress.csv" in data:
    plot_time_series(data["Stress.csv"], "date", "stress", "Average Stress Levels Over Time", "Stress Score")

if "Sleep.csv" in data:
    plot_time_series(data["Sleep.csv"], "date", "avg_duration", "Average Sleep Duration Over Time", "Sleep Duration (minutes)")

print("\n✅ EDA complete! Visualizations and summaries generated.")
