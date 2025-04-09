import os
import pandas as pd

# 🔹 Define file paths
RAW_DATA_FOLDER = "/Users/Elissa/Documents/garmin_data_analysis/data"
CLEANED_DATA_FOLDER = "/Users/Elissa/Documents/garmin_data_analysis/cleaned_data"

# 🔹 Load Steps dataset
steps_file = os.path.join(RAW_DATA_FOLDER, "Steps.csv")
steps_df = pd.read_csv(steps_file)

# 🔹 Debug: Check column names
print(f"🔍 Columns in Steps dataset: {steps_df.columns.tolist()}")

# 🔹 Standardize column names
steps_df.columns = steps_df.columns.str.strip().str.lower().str.replace(" ", "_")

# 🔹 Convert the date column to "Month YYYY"
steps_df["date"] = pd.to_datetime(steps_df["date"]).dt.strftime("%B %Y")

# 🔹 Aggregate step counts by month (SUM)
cleaned_steps = steps_df.groupby("date")["steps"].sum().reset_index()

# 🔹 Save cleaned data
cleaned_steps_file = os.path.join(CLEANED_DATA_FOLDER, "Steps.csv")
cleaned_steps.to_csv(cleaned_steps_file, index=False)

print(f"✅ Cleaned Steps data saved to {cleaned_steps_file}")
