import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the correct path to your cleaned data folder
DATA_FOLDER = "/Users/Elissa/Documents/garmin_data_analysis/cleaned_data"

# Load relevant datasets
files = {
    "calories": "Calories.csv",
    "intensity": "Intensity Minutes.csv",
    "floors": "Floors Climbed.csv",
    "sleep": "Sleep.csv"
}

data = {name: pd.read_csv(os.path.join(DATA_FOLDER, filename)) for name, filename in files.items()}

# Standardize column names
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

data = {name: clean_column_names(df) for name, df in data.items()}

# Ensure date column is formatted correctly
def convert_date_column(df, column="date"):
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], format="%B %Y", errors="coerce")
    return df

data = {name: convert_date_column(df) for name, df in data.items()}

# Sort by date
for name, df in data.items():
    df.sort_values("date", inplace=True)

# --- 📊 Monthly Calorie Burn Trend ---
def plot_calorie_burn_trend():
    df = data["calories"].sort_values("date")

    # Normalize colors based on total calories burned
    norm = (df["total_calories"] - df["total_calories"].min()) / (df["total_calories"].max() - df["total_calories"].min())
    colors = sns.color_palette("Reds", as_cmap=True)(norm)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=df["date"].dt.strftime('%B %Y'), y=df["total_calories"], palette=colors)
    plt.xticks(rotation=45)
    plt.ylabel("Total Calories Burned")
    plt.xlabel("Month")
    plt.title("Monthly Calorie Burn Trend")
    plt.show()

plot_calorie_burn_trend()

# --- 🔥 Correlation: Intensity Minutes vs. Calories Burned ---
def plot_intensity_vs_calories():
    df = data["calories"].merge(data["intensity"], on="date", how="inner")

    plt.figure(figsize=(10, 6))
    sns.regplot(x=df["actual"], y=df["total_calories"], scatter_kws={"color": "orange"}, line_kws={"color": "red"}, ci=95)
    plt.xlabel("Intensity Minutes")
    plt.ylabel("Total Calories Burned")
    plt.title("Correlation: Intensity Minutes vs. Calories Burned")
    plt.show()

plot_intensity_vs_calories()

# --- 🏋️ Impact of Stair Climbing on Calories Burned ---
def plot_floors_vs_calories():
    df = data["calories"].merge(data["floors"], on="date", how="inner")

    plt.figure(figsize=(10, 6))
    sns.regplot(x=df["climbed_floors"], y=df["total_calories"], scatter_kws={"color": "orange"}, line_kws={"color": "blue"}, ci=95)
    plt.xlabel("Floors Climbed")
    plt.ylabel("Total Calories Burned")
    plt.title("Impact of Stair Climbing on Calories Burned")
    plt.show()

plot_floors_vs_calories()

# --- 🌙 Fixed Sleep Analysis: Convert Sleep Duration to Minutes ---
def plot_activity_vs_sleep():
    df = data["intensity"].merge(data["sleep"], on="date", how="inner")

    # Convert sleep duration from "8h 29min" to total minutes
    def convert_duration_to_minutes(duration_str):
        try:
            hours, minutes = 0, 0
            if "h" in duration_str:
                hours = int(duration_str.split("h")[0].strip())
            if "min" in duration_str:
                minutes = int(duration_str.split("h")[-1].replace("min", "").strip())
            return hours * 60 + minutes
        except:
            return None  # If conversion fails, return None

    df["avg_duration"] = df["avg_duration"].apply(convert_duration_to_minutes)

    # Ensure data is numeric & drop NaNs
    df = df.dropna(subset=["avg_duration", "actual"])

    plt.figure(figsize=(10, 6))
    sns.regplot(x=df["actual"], y=df["avg_duration"], scatter_kws={"color": "orange"}, line_kws={"color": "green"}, ci=95)
    plt.xlabel("Intensity Minutes")
    plt.ylabel("Average Sleep Duration (minutes)")
    plt.title("Impact of Activity on Sleep Duration")
    plt.grid(True)
    plt.show()

plot_activity_vs_sleep()

# Ensure Plots Do Not Block Terminal Execution
plt.show(block=False)
