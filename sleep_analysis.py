import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🔹 Set the correct path to the cleaned data folder
DATA_FOLDER = "/Users/Elissa/Documents/garmin_data_analysis/cleaned_data"

# 🔹 Define dataset filenames
files = {
    "sleep": "Sleep.csv",
    "intensity": "Intensity Minutes.csv",
    "stress": "Stress.csv"
}

# 🔹 Load datasets
data = {name: pd.read_csv(os.path.join(DATA_FOLDER, filename)) for name, filename in files.items()}

# 🔹 Standardize column names
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

data = {name: clean_column_names(df) for name, df in data.items()}

# 🔹 Convert date columns to datetime format
def convert_date_column(df, column="date"):
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], format="%B %Y", errors="coerce")
    return df

data = {name: convert_date_column(df) for name, df in data.items()}

# 🔹 Convert sleep duration from "Xh Ymin" format to total minutes
def convert_duration_to_minutes(duration_str):
    """Converts sleep duration from 'Xh Ymin' format to total minutes."""
    try:
        hours, minutes = 0, 0
        if "h" in duration_str:
            hours = int(duration_str.split("h")[0].strip())
        if "min" in duration_str:
            minutes = int(duration_str.split("h")[-1].replace("min", "").strip())
        return hours * 60 + minutes
    except:
        return None  # Return None for invalid values

data["sleep"]["avg_duration"] = data["sleep"]["avg_duration"].apply(convert_duration_to_minutes)

# --- 📊 Sleep Duration Over Time ---
def plot_sleep_trends():
    """Plots sleep duration trends over time."""
    df = data["sleep"].sort_values("date")

    plt.figure(figsize=(10, 5))
    sns.lineplot(x=df["date"], y=df["avg_duration"], marker="o", label="Avg Sleep Duration")
    plt.xticks(rotation=45)
    plt.ylabel("Sleep Duration (minutes)")
    plt.xlabel("Month")
    plt.title("Sleep Duration Trends Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

plot_sleep_trends()

# --- 📊 Correlation Between Physical Activity & Sleep ---
def plot_activity_vs_sleep():
    """Analyzes correlation between intensity minutes and sleep duration."""
    df = data["sleep"].merge(data["intensity"], on="date", how="inner").sort_values("date")

    plt.figure(figsize=(8, 5))
    sns.regplot(x=df["actual"], y=df["avg_duration"], scatter_kws={"alpha": 0.6}, line_kws={"color": "red"})
    plt.xlabel("Intensity Minutes")
    plt.ylabel("Sleep Duration (minutes)")
    plt.title("Correlation: Physical Activity vs. Sleep Duration")
    plt.grid(True)
    plt.show()

    correlation = df["actual"].corr(df["avg_duration"])
    print(f"\n📊 Correlation between Intensity Minutes & Sleep Duration: {correlation:.3f}")

plot_activity_vs_sleep()

# --- 📊 Correlation Between Stress & Sleep ---
def plot_stress_vs_sleep():
    """Analyzes correlation between stress levels and sleep duration."""
    df = data["sleep"].merge(data["stress"], on="date", how="inner").sort_values("date")

    plt.figure(figsize=(8, 5))
    sns.regplot(x=df["stress"], y=df["avg_duration"], scatter_kws={"alpha": 0.6, "color": "red"}, line_kws={"color": "blue"})
    plt.xlabel("Average Stress Level")
    plt.ylabel("Sleep Duration (minutes)")
    plt.title("Correlation: Stress Levels vs. Sleep Duration")
    plt.grid(True)
    plt.show()

    correlation = df["stress"].corr(df["avg_duration"])
    print(f"\n📊 Correlation between Stress Levels & Sleep Duration: {correlation:.3f}")

plot_stress_vs_sleep()

# --- 📊 Compute Best & Worst Sleep Months ---
def analyze_best_worst_sleep():
    """Finds the best and worst sleep months and computes the average sleep duration."""
    avg_sleep = data["sleep"]["avg_duration"].mean()
    best_sleep_month = data["sleep"].loc[data["sleep"]["avg_duration"].idxmax(), ["date", "avg_duration"]]
    worst_sleep_month = data["sleep"].loc[data["sleep"]["avg_duration"].idxmin(), ["date", "avg_duration"]]

    print(f"\n💤 Average Sleep Duration: {avg_sleep:.1f} minutes (~{avg_sleep // 60:.0f}h {avg_sleep % 60:.0f}m)")
    print(f"🌟 Best Sleep Month: {best_sleep_month['date'].strftime('%B %Y')} ({best_sleep_month['avg_duration']:.0f} minutes)")
    print(f"📉 Worst Sleep Month: {worst_sleep_month['date'].strftime('%B %Y')} ({worst_sleep_month['avg_duration']:.0f} minutes)")

analyze_best_worst_sleep()

# ✅ Ensure Plots Do Not Block Terminal Execution
plt.show(block=False)
