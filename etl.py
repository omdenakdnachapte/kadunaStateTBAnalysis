# import necessary libraries
import pandas as pd
from thefuzz import process # for string similarity or to correct/standardize the LGAs names


# List of proper names for Local Government Areas (LGAs)
lga_names = ['Birnin-Gwari', 'Chikun', 'Giwa', 'Igabi', 'Ikara', 'Jaba',
             "Jema'a", 'Kachia', 'Kaduna North', 'Kaduna South', 'Kagarko',
             'Kajuru', 'Kaura', 'Kauru', 'Kubau', 'Kudan', 'Lere', 'Markafi',
             'Sabon-Gari', 'Sanga', 'Soba', 'Zango-Kataf', 'Zaria']

# Dictionary mapping each block to a dictionary of quarters and their corresponding COLUMN indices
column_indices = {
    'block1a': {1: [18, 19],
                2: [79, 80],
                3: [140, 141],
                4: [201, 202]},
    'block2a': {1: [28, 29],
                2: [89, 90],
                3: [150, 151],
                4: [211, 212]},
    'block2b': {1: [32, 34],
                2: [93, 95],
                3: [154, 156],
                4: [215, 217]},
    'block2c': {1: [38, 40],
                2: [99, 101],
                3: [160, 162],
                4: [221, 223]},
    'block2d': {1: [44, 46],
                2: [105, 107],
                3: [166, 168],
                4: [227, 229]},
    'block2e': {1: [57, 58],
                2: [118, 119],
                3: [179, 180],
                4: [240, 241]}
}

# Dictionary mapping each block to a dictionary of quarters and their corresponding ROW indices
row_indices = {
    'block1a': [1,28],
    'block2a': [2,13],
    'block2b': [1,11],
    'block2c': [1,11],
    'block2d': [1,11],
    'block2e': [2,12]
}

# For 2019 to 2021 excel raw files
older_data_column_names = {
    'block1a': ["Year", "Quarter", "LGA", "Total Presumptives",
                "Presumptive DS-TB", "Presumptive DR-TB", "Examined for Diagnosis", "Total Examined with Xpert",
                "Total Examined with AFB", "Total Examined with TB LAMP/LF-LAM", "Screened with X-ray", "MTB Detected",
                "Smear Positive", "TB Lamp/LF LAM", "Chest X-ray Suggestive", "Total Diagnosed",
                "Rifampicin Resistant", "HIV Positive", "HIV Negative", "HIV Unknown",
                "No. of Presumptives that are HCWS", "Referred from the Community", "Referred from the PPM" # 20
                ],
    'block2a': ["Year", "Quarter", "LGA", "PTB Xpert Positive",
                "PTB Smear Positive", "PTB TB Lamp", "PTB LF-LAM", "PTB Clinically Diagnosed",
                "EPTB Xpert Positive", "EPTB Clinically Diagnosed", "Total TB Cases notified", "All TB cases who had Xpert test", # 9
                ]
}

# Dictionary mapping each block to its corresponding column names
column_names = {
    'block1a': ["Year", "Quarter", "LGA", "Total Presumptives",
                        "Presumptive DS-TB", "Presumptive DR-TB", "Examined for Diagnosis",
                        "Total Examined with Xpert", "Total Examined with Truenat",
                        "Total Examined with AFB", "Total Examined with TB LAMP",
                        "Total Examined with LF-LAM and Others", "Screened with X-ray",
                        "MTB Detected", "Truenat Positive", "Smear Positive",
                        "TB Lamp Positive", "LF LAM Positive", "Chest X-ray Suggestive",
                        "Other Clinical Diagnosis", "Total Diagnosed", "Rifampicin Resistant",
                        "HIV Positive", "HIV Negative", "HIV Unknown",
                        "No. of Presumptives that are HCWS", "Referred from the Community",
                        "Referred from the PPM", "No. of Presumptives tested for COVID-19", #  27
                        "No. of Presumptives Positive for COVID-19"],
    'block2a': ["Year", "Quarter", "LGA", "PTB Xpert Positive", "PTB Truenat Positive",
                "PTB Smear Positive", "PTB TB Lamp", "PTB LF-LAM other", "PTB Clinically Diagnosed",
                "EPTB Xpert Positive", "EPTB Clinically Diagnosed", "Total TB Cases notified", "All TB cases who had Xpert test",
                "All TB cases who had Truenat test"], # 11
    'block2b': ["Year", "Quarter", "LGA", "Sex", "0 to 4", "5 to 14",
                   "15 to 24", "25 to 34", "35 to 44", "45 to 54", "55 to 64", "> 65", "Total"],
    'block2c': ["Year", "Quarter", "LGA", "Sex", "0 to 4", "5 to 14",
                   "15 to 24", "25 to 34", "35 to 44", "45 to 54", "55 to 64", "> 65", "Total"],
    'block2d': ["Year", "Quarter", "LGA", "Sex", "0 to 4", "5 to 14",
                   "15 to 24", "25 to 34", "35 to 44", "45 to 54", "55 to 64", "> 65", "Total"], 
    'block2e': ["Year", "Quarter", "LGA", "Male Total TB Cases Notified", "Female Total TB Cases Notified",
                "Male TB HIV Positive Cases", "Female TB HIV Positive Cases", "Male TB HIV Negative Cases", "Female TB HIV Negative Cases",
                "Male TB HIV Unknown Cases", "Female TB HIV Unknown Cases", "TB/HIV CPT", "TB/HIV ART"]
}
def process_lga_data(block, file_path, year):
    """
    This function processes LGA data from the given Excel file for the specified year and block.

    Parameters:
    block (str): The block for which the data is to be processed.
    file_path (str): The path to the Excel file.
    year (int): The year for which the data is to be processed.

    Returns:
    DataFrame: A DataFrame containing the processed data for the specified block and LGA in the specified year.
    """

    # Read the Excel file using pandas
    excel_file = pd.ExcelFile(file_path)

    # Extract all sheet names from the Excel file
    sheet_names = excel_file.sheet_names

    # Filter the sheet names to only include those that contain "_2", which are relevant for TB data
    relevant_sheet_names = [sheet_name for sheet_name in sheet_names if "_2" in sheet_name]

    # Initialize a DataFrame to store the processed data for the specified block
    # The columns of this DataFrame are defined by 'column_names[block]'
    columns = older_data_column_names[block] if block in ['block1a', 'block2a'] and year < 2022 else column_names[block]
    block_data = pd.DataFrame(columns=columns)

    # Loop over each relevant sheet name
    for lga_sheet_name in relevant_sheet_names:
        # Read the data from the current sheet into a DataFrame
        df = pd.read_excel(file_path, sheet_name=lga_sheet_name)

        # Loop over each quarter defined in 'column_indices[block]'
        for quarter in column_indices[block].keys():
            # Get the column and row indices for the current quarter
            i_col1 = column_indices[block][quarter][0]
            i_col2 = column_indices[block][quarter][1]
            i_row1 = row_indices[block][0]
            i_row2 = row_indices[block][1] - 7 if block == 'block1a' and year < 2022 else (row_indices[block][1] - 2 if block == 'block2a' and year < 2022 else row_indices[block][1])

            # Select the data for the current quarter using the column and row indices
            selected_data = df.iloc[i_col1:i_col2, i_row1:i_row2]

            # Add additional columns to the selected data for 'Year', 'Quarter', and 'LGA'
            selected_data.insert(0, "Year", year)
            selected_data.insert(1, "Quarter", quarter)
            selected_data.insert(2, "LGA", lga_sheet_name.split("_")[0])

            selected_data.columns = older_data_column_names[block] if block in ['block1a', 'block2a'] and year < 2022 else column_names[block]

            # Append the selected data to the main DataFrame
            block_data = pd.concat([block_data, selected_data], ignore_index=True)

    # Perform replacements in the DataFrame in a single call
    # Replace 'True' with 1 and '-' with 0
    block_data.replace({True: 1, '-': 0}, inplace=True)

    # Fill any remaining NaN values with 0
    block_data.fillna(0, inplace=True)

    # Perform string similarity to standardize the names of LGA
    block_data['LGA'] = block_data['LGA'].apply(lambda lga: process.extractOne(lga, lga_names)[0])

    # List of columns that should not be converted
    exclude_columns = ['Sex', 'LGA']

    # Convert all other columns to int
    block_data[block_data.columns.difference(exclude_columns)] = block_data[block_data.columns.difference(exclude_columns)].apply(pd.to_numeric, downcast='integer', errors='ignore')

    # Return the DataFrame containing the processed data
    return block_data
