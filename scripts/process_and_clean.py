import os
import pandas as pd

# Set folder paths
DATA_FOLDER = "data"
CLEANED_FOLDER = "cleaned_data"
os.makedirs(CLEANED_FOLDER, exist_ok=True)

# ✅ Helper function: Convert dates to "Month YYYY" safely
def format_month_year(date_series, add_year=True):
    """Converts date column to 'Month YYYY' format while preserving original values on failure."""
    try:
        # **Only add year if it's missing**
        if add_year and not date_series.str.contains(r'\d{4}', regex=True, na=False).any():
            date_series = date_series.str[:3] + " 2024"  # Extract first 3 letters & append "2024"
        
        formatted_dates = pd.to_datetime(date_series, format="%b %Y", errors="coerce").dt.strftime("%B %Y")

        # **Fix:** If conversion fails, return original values instead of "Unknown"
        formatted_dates[formatted_dates.isna()] = date_series

        return formatted_dates

    except Exception as e:
        print(f"⚠️ Date formatting error: {e}")
        return date_series

# ✅ More precise function for datasets already in YYYY-MM-DD format
def format_yyyy_mm_dd_to_month_year(date_series):
    """Converts 'YYYY-MM-DD' dates into 'Month YYYY' format."""
    return pd.to_datetime(date_series, errors="coerce").dt.strftime("%B %Y")

# ✅ Convert numeric columns safely
def convert_to_numeric(df, columns):
    """Converts specified columns to numeric values, handling errors."""
    df[columns] = df[columns].apply(pd.to_numeric, errors="coerce")
    return df

# ✅ Convert time (HH:MM AM/PM) to minutes
def convert_time_to_minutes(time_str):
    """Converts time in 'HH:MM AM/PM' format to minutes since midnight."""
    try:
        time_obj = pd.to_datetime(time_str, format="%I:%M %p")
        return time_obj.hour * 60 + time_obj.minute
    except:
        return None

# ✅ Convert sleep duration (e.g., "8h 29min") to total minutes
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
        return None

# 🛠 **Cleaning Functions**
def clean_activities(df):
    """Standardizes month names and retains activity type."""
    df.columns = ["month", "activity_type"]
    if df.iloc[0].str.contains("Month", case=False, na=False).any():
        df = df.iloc[1:]  # Remove first row if it's a header
    df["month"] = format_month_year(df["month"], add_year=True)
    return df

def clean_average_heart_rate(df):
    """Formats date and removes 'bpm' from values."""
    df.columns = ["date", "heart_rate"]
    df["date"] = format_yyyy_mm_dd_to_month_year(df["date"])  # ✅ Use correct date function
    df["heart_rate"] = df["heart_rate"].str.replace(" bpm", "", regex=True)
    return df.dropna(subset=["date"])  # Ensure dates are retained

def clean_max_heart_rate(df):
    """Formats date and removes 'bpm' from values."""
    df.columns = ["date", "max_heart_rate"]
    df["date"] = format_yyyy_mm_dd_to_month_year(df["date"])  # ✅ Use correct date function
    df["max_heart_rate"] = df["max_heart_rate"].str.replace(" bpm", "", regex=True)
    return df.dropna(subset=["date"])

def clean_calories(df):
    """Formats date, converts calories to numeric, and aggregates by month."""
    df.columns = ["date", "active_calories", "resting_calories", "total_calories"]
    df["date"] = format_month_year(df["date"], add_year=True)
    df = convert_to_numeric(df, ["active_calories", "resting_calories", "total_calories"])
    return df.groupby("date", as_index=False).sum()

def clean_floors_climbed(df):
    """Formats date, converts floors climbed, and aggregates by month."""
    df.columns = ["date", "climbed_floors", "descended_floors"]
    df["date"] = format_month_year(df["date"], add_year=True)
    df = convert_to_numeric(df, ["climbed_floors", "descended_floors"])
    return df.groupby("date", as_index=False).sum()

def clean_intensity_minutes(df):
    """Formats dates, converts actual intensity minutes to numeric, and aggregates by month."""
    df.columns = ["date", "actual", "goal"]
    df["date"] = format_yyyy_mm_dd_to_month_year(df["date"])  # ✅ Use correct date function
    df = convert_to_numeric(df, ["actual"]).drop(columns=["goal"])
    return df.groupby("date", as_index=False).sum()

def clean_stress(df):
    """Formats date, converts stress values to numeric, and computes the average stress per month."""
    df.columns = ["date", "stress"]
    df["date"] = format_month_year(df["date"], add_year=True)
    df = convert_to_numeric(df, ["stress"])
    return df.groupby("date", as_index=False).mean()

def clean_sleep(df):
    """Formats sleep data: converts dates, durations, and times to minutes, then averages per month."""
    df = df.iloc[:, :4]  # Keep only the first 4 columns
    df.columns = ["date", "avg_duration", "avg_bedtime", "avg_wake_time"]

    df["date"] = format_month_year(df["date"], add_year=True)

    df["avg_duration"] = df["avg_duration"].apply(convert_duration_to_minutes)
    df["avg_bedtime"] = df["avg_bedtime"].apply(convert_time_to_minutes)
    df["avg_wake_time"] = df["avg_wake_time"].apply(convert_time_to_minutes)

    df = df.groupby("date", as_index=False).mean()

    df["avg_duration"] = df["avg_duration"].apply(lambda x: f"{int(x // 60)}h {int(x % 60)}min" if pd.notna(x) else "Unknown")
    return df

# ✅ Process CSV files
def process_csv(filename, cleaning_function):
    file_path = os.path.join(DATA_FOLDER, filename)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, dtype=str)
        print(f"\n🔹 Cleaning {filename}...")
        df = cleaning_function(df)
        cleaned_path = os.path.join(CLEANED_FOLDER, filename)
        print(f"✅ Saving {filename} to {cleaned_path}")
        df.to_csv(cleaned_path, index=False)
    else:
        print(f"⚠️ {filename} not found. Skipping.")

# ✅ Process all datasets
datasets = {
    "Activities.csv": clean_activities,
    "Average Heart Rate.csv": clean_average_heart_rate,
    "Max Heart Rate.csv": clean_max_heart_rate,
    "Calories.csv": clean_calories,
    "Floors Climbed.csv": clean_floors_climbed,
    "Intensity Minutes.csv": clean_intensity_minutes,
    "Stress.csv": clean_stress,
    "Sleep.csv": clean_sleep,
}

for filename, function in datasets.items():
    process_csv(filename, function)
