import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🔹 Set the correct path to the cleaned data folder
DATA_FOLDER = "/Users/Elissa/Documents/garmin_data_analysis/cleaned_data"

# 🔹 Define dataset filenames
files = {
    "activities": "Activities.csv",
    "heart_rate": "Average Heart Rate.csv",
    "calories": "Calories.csv",
    "floors": "Floors Climbed.csv",
    "intensity": "Intensity Minutes.csv",
    "max_hr": "Max Heart Rate.csv",
    "sleep": "Sleep.csv",
    "stress": "Stress.csv",
    "steps": "Steps.csv"
}

# 🔹 Load all datasets
data = {name: pd.read_csv(os.path.join(DATA_FOLDER, filename)) for name, filename in files.items()}

# 🔹 Standardize column names
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

data = {name: clean_column_names(df) for name, df in data.items()}

# 🔹 Ensure the date column is formatted correctly
def convert_date_column(df, column="date"):
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], format="%B %Y", errors="coerce")
    return df

data = {name: convert_date_column(df) for name, df in data.items()}

# --- 📊 Visualize Activity Trends ---
def plot_activity_trends():
    df = data["floors"].merge(data["intensity"], on="date", how="inner").sort_values("date")

    plt.figure(figsize=(10, 5))
    sns.lineplot(x=df["date"], y=df["climbed_floors"], label="Floors Climbed")
    sns.lineplot(x=df["date"], y=df["actual"], label="Intensity Minutes")
    plt.xticks(rotation=45)
    plt.ylabel("Activity Level")
    plt.xlabel("Month")
    plt.title("Total Activity Levels Over Time")
    plt.legend()
    plt.show()

plot_activity_trends()

# --- 📊 Bar Chart of Activity Levels by Month ---
def plot_activity_bar_chart():
    df = data["floors"].merge(data["intensity"], on="date", how="inner").sort_values("date")
    df["total_activity"] = df["climbed_floors"] + df["actual"]

    plt.figure(figsize=(10, 5))
    sns.barplot(x=df["date"].dt.strftime('%B %Y'), y=df["total_activity"], palette="coolwarm")
    plt.xticks(rotation=45)
    plt.ylabel("Total Activity Level")
    plt.xlabel("Month")
    plt.title("Monthly Activity Levels")
    plt.show()

plot_activity_bar_chart()

# --- 🏆 Most & Least Active Month (Excluding Steps) ---
def calculate_most_and_least_active_month():
    """Calculates the most and least active months using floors climbed, intensity, and calories (excluding steps)."""
    df = data["floors"].merge(data["intensity"], on="date", how="inner")
    df = df.merge(data["calories"], on="date", how="inner")

    # Create a Total Activity Score (Excluding Steps)
    df["total_activity_score"] = (
        (df["climbed_floors"] * 10) +  # Floors climbed (scaled for impact)
        df["actual"] +  # Intensity minutes
        df["total_calories"]  # Total calories burned
    )

    print("\n📊 Activity Metrics Per Month (Excluding Steps):")
    print(df[["date", "climbed_floors", "actual", "total_calories", "total_activity_score"]].sort_values("date"))

    # Find the most & least active months
    most_active_month = df.loc[df["total_activity_score"].idxmax(), "date"]
    least_active_month = df.loc[df["total_activity_score"].idxmin(), "date"]

    print("\n🏆 Most Active Month (Excluding Steps):", most_active_month.strftime('%B %Y'))
    print("💤 Least Active Month (Excluding Steps):", least_active_month.strftime('%B %Y'))

    # ✅ Mention step count trends separately
    step_df = data["steps"].sort_values("date")
    highest_steps_month = step_df.loc[step_df["steps"].idxmax(), "date"]
    print(f"🚶 High Step Count Alert: {highest_steps_month.strftime('%B %Y')} had an unusually high number of steps.")

calculate_most_and_least_active_month()

# --- 📊 How Consistent Have I Been With My Workout Frequency? (Fixed Coloring) ---
def plot_workout_frequency():
    """Analyzes how many days per month have logged activity correctly with fixed color scaling."""
    df = data["intensity"].copy()
    
    # ✅ Convert date back to datetime for sorting
    df["date"] = pd.to_datetime(df["date"], format="%B %Y", errors="coerce")

    # ✅ Estimate active days per month
    AVERAGE_MINUTES_PER_WORKOUT = 30  
    df["estimated_active_days"] = df["actual"] / AVERAGE_MINUTES_PER_WORKOUT

    # ✅ Cap active days at max days per month
    df["estimated_active_days"] = df.apply(lambda row: min(row["estimated_active_days"], row["date"].days_in_month), axis=1)

    # ✅ Sort the months correctly
    df = df.sort_values("date")

    # ✅ Normalize values for color scaling
    norm = (df["estimated_active_days"] - df["estimated_active_days"].min()) / (df["estimated_active_days"].max() - df["estimated_active_days"].min())
    colors = sns.color_palette("Blues", as_cmap=True)(norm)

    # ✅ Plot with corrected color mapping
    plt.figure(figsize=(10, 5))
    sns.barplot(x=df["date"].dt.strftime('%B %Y'), y=df["estimated_active_days"], palette=colors)

    plt.xticks(rotation=45)
    plt.ylabel("Estimated Active Days Per Month")
    plt.xlabel("Month")
    plt.title("Workout Frequency Consistency")
    plt.show()

    avg_active_days = df["estimated_active_days"].mean()
    print(f"📊 Average Estimated Active Days Per Month: {avg_active_days:.1f}")

plot_workout_frequency()

# --- 📊 Resting Heart Rate vs. Training Intensity ---
def plot_rhr_vs_intensity():
    """Compares Resting Heart Rate (RHR) with Training Intensity using dual y-axes."""
    df = data["heart_rate"].merge(data["intensity"], on="date", how="inner").sort_values("date")

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Primary Y-axis (Resting Heart Rate)
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Resting Heart Rate (bpm)", color="tab:blue")
    ax1.plot(df["date"], df["heart_rate"], label="Resting Heart Rate", color="tab:blue", marker="o")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    # Secondary Y-axis (Training Intensity Minutes)
    ax2 = ax1.twinx()
    ax2.set_ylabel("Training Intensity Minutes", color="tab:green")
    ax2.plot(df["date"], df["actual"], label="Intensity Minutes", color="tab:green", linestyle="dashed", marker="s")
    ax2.tick_params(axis="y", labelcolor="tab:green")

    # Legends
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # Title & Formatting
    plt.title("Resting Heart Rate vs. Training Intensity Over Time")
    plt.xticks(rotation=45)
    plt.show()

plot_rhr_vs_intensity()

# ✅ Ensure Plots Do Not Block Terminal Execution
plt.show(block=False)
