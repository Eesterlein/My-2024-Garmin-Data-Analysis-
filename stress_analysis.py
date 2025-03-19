import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- ✅ Load Data ---
DATA_FOLDER = "/Users/Elissa/Documents/garmin_data_analysis/cleaned_data"

files = {
    "stress": "Stress.csv",
    "intensity": "Intensity Minutes.csv",
    "steps": "Steps.csv",
    "floors": "Floors Climbed.csv"
}

# Load all datasets
data = {name: pd.read_csv(os.path.join(DATA_FOLDER, filename)) for name, filename in files.items()}

# Standardize column names
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

data = {name: clean_column_names(df) for name, df in data.items()}

# Convert date column to datetime format
for df in data.values():
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], format="%B %Y", errors="coerce")

# --- 📊 Monthly Stress Level Trends ---
def plot_stress_trends():
    """Plots how stress fluctuates over time."""
    df = data["stress"].sort_values("date")

    plt.figure(figsize=(10, 5))
    sns.lineplot(x=df["date"], y=df["stress"], marker="o", color="red")
    plt.xticks(rotation=45)
    plt.ylabel("Average Stress Level")
    plt.xlabel("Month")
    plt.title("📊 Monthly Stress Level Trends")
    plt.grid(True)
    plt.show()

plot_stress_trends()

# --- 🏆 Find Highest & Lowest Stress Months ---
def analyze_stress_extremes():
    """Finds the months with highest and lowest stress levels."""
    df = data["stress"]

    highest_stress_month = df.loc[df["stress"].idxmax(), "date"]
    lowest_stress_month = df.loc[df["stress"].idxmin(), "date"]

    print("\n🏆 Most Stressful Month:", highest_stress_month.strftime('%B %Y'))
    print("💤 Least Stressful Month:", lowest_stress_month.strftime('%B %Y'))

analyze_stress_extremes()

# --- 📊 Correlation Between Stress & Physical Activity ---
def plot_stress_vs_activity():
    """Analyzes how stress correlates with steps, intensity, and floors climbed."""
    df = data["stress"].merge(data["intensity"], on="date", how="inner")
    df = df.merge(data["steps"], on="date", how="inner")
    df = df.merge(data["floors"], on="date", how="inner")

    # Calculate correlations
    stress_intensity_corr = df["stress"].corr(df["actual"])
    stress_steps_corr = df["stress"].corr(df["steps"])
    stress_floors_corr = df["stress"].corr(df["climbed_floors"])

    print("\n📊 Correlation Results:")
    print(f"   🔹 Stress vs. Intensity Minutes: {stress_intensity_corr:.2f}")
    print(f"   🔹 Stress vs. Steps: {stress_steps_corr:.2f}")
    print(f"   🔹 Stress vs. Floors Climbed: {stress_floors_corr:.2f}")

    # --- 📊 Scatter Plots ---
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Intensity vs Stress
    sns.regplot(x=df["actual"], y=df["stress"], scatter_kws={"color": "blue"}, line_kws={"color": "black"}, ax=axes[0])
    axes[0].set_title(f"📊 Stress vs. Intensity Minutes (r={stress_intensity_corr:.2f})")
    axes[0].set_xlabel("Intensity Minutes")
    axes[0].set_ylabel("Average Stress Level")

    # Steps vs Stress
    sns.regplot(x=df["steps"], y=df["stress"], scatter_kws={"color": "green"}, line_kws={"color": "black"}, ax=axes[1])
    axes[1].set_title(f"📊 Stress vs. Steps (r={stress_steps_corr:.2f})")
    axes[1].set_xlabel("Steps")
    axes[1].set_ylabel("Average Stress Level")

    # Floors Climbed vs Stress
    sns.regplot(x=df["climbed_floors"], y=df["stress"], scatter_kws={"color": "purple"}, line_kws={"color": "black"}, ax=axes[2])
    axes[2].set_title(f"📊 Stress vs. Floors Climbed (r={stress_floors_corr:.2f})")
    axes[2].set_xlabel("Floors Climbed")
    axes[2].set_ylabel("Average Stress Level")

    plt.tight_layout()
    plt.show()

plot_stress_vs_activity()

# ✅ Ensure plots do not block execution
plt.show(block=False)
