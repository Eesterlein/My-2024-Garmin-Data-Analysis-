import os
import pandas as pd

# Set the correct data folder path
DATA_FOLDER = "data"

# List all CSV files in the data folder
def list_data_files():
    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
    print("\n📂 Found CSV files:", files)
    return files

# Load and inspect all CSV files
def load_and_inspect_data():
    files = list_data_files()
    dataframes = {}  # Store loaded DataFrames
    
    for file in files:
        file_path = os.path.join(DATA_FOLDER, file)
        
        try:
            df = pd.read_csv(file_path)
            dataframes[file] = df  # Store DataFrame
            
            # Print file name and first few rows
            print(f"\n🔍 Inspecting: {file}")
            print(df.head(), "\n")
            
            # Print missing values summary
            print("🔎 Missing Values:")
            print(df.isnull().sum(), "\n")

        except Exception as e:
            print(f"❌ Error loading {file}: {e}")

    return dataframes

# Run script
if __name__ == "__main__":
    loaded_data = load_and_inspect_data()
