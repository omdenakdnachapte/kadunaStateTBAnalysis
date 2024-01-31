import pandas as pd
import csv

# Assuming your CSV file is named 'your_file.csv'
file_path = 'Block2b_2023.csv'
df = pd.read_csv(file_path)

# Read the CSV file into a pandas DataFrame
with open(file_path, 'r+') as csv_file:
    totals = []
    # Create a CSV reader
    csv_reader = csv.reader(csv_file, delimiter='\t')  # Adjust the delimiter if needed

    # Iterate through each row in the CSV file
    index = 0
    for row in csv_reader:
        if(index != 0):
            result_array = row[0].split(',')
            total = int(float(result_array[4]))+int(float(result_array[5]))+int(float(result_array[6]))+int(float(result_array[7]))+int(float(result_array[8]))+int(float(result_array[9]))+int(float(result_array[10]))+int(float(result_array[11]))
            totals.append(total)
        
        
        index = index + 1
    df["Total"] = totals
    
    df.to_csv(file_path, index=False)


#cp Block2b_2023\ copy.csv Block2b_2023.csv 

