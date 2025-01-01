import json
import pandas as pd

# Load the Excel file using pandas
periode_df = pd.read_excel('periode.xlsx')

# Convert the DataFrame to a list of dictionaries
periode_dicts = periode_df.to_dict(orient='records')

# Extract headers
periode_headers = list(periode_df.columns)

# Print headers to debug
print("Periode Headers:", periode_headers)

# Ensure the required columns exist in periode
required_columns = ['Titik', 'Year', 'Periode', 'Latitude', 'Longitude', 'Skor', 'Klasifikasi']
for column in required_columns:
    if column not in periode_headers:
        raise ValueError(f"Missing required column in periode.xlsx: {column}")

# Filter the data to show only rows where 'Titik' refers to a child column
child_columns = ['Titik_Tengah', 'Titik_Hulu', 'Titik_Hilir']
filtered_data = []

for entry in periode_dicts:
    for child_column in child_columns:
        if child_column in entry and pd.notna(entry[child_column]):
            filtered_data.append(entry)
            break

# Save the filtered data to a JSON file
with open('filtered_data.json', 'w') as json_file:
    json.dump(filtered_data, json_file, indent=4)

# Print a sample of the filtered data to debug
print("Filtered Data Sample:", filtered_data[:5])