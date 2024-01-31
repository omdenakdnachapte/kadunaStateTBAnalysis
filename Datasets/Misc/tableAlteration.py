
import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'PTB_EPTB_Total_lab_clinical_historical_forecasts.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Split the 'Year-Quarter' column into 'Year' and 'Quarter' and add as new columns
df[['Year', 'Quarter']] = df['Year-Quarter'].str.split('Q', expand=True)

# Save the modified DataFrame back to the CSV file
df.to_csv(file_path, index=False)

print("Columns 'Year' and 'Quarter' added to the CSV file.")