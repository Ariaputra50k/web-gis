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
required_columns = ['Titik', 'Year', 'Latitude', 'Longitude', 'Skor', 'Klasifikasi', 'Periode']
for column in required_columns:
    if column not in periode_headers:
        raise ValueError(f"Missing required column in periode.xlsx: {column}")

# Initialize the data structure
data = {}

def determine_category(entry):
    # Implement logic to determine the category
    # For example, based on some attribute in the entry
    if 'Tengah' in entry['Titik']:
        return 'Titik_Tengah'
    elif 'Hulu' in entry['Titik']:
        return 'Titik_Hulu'
    elif 'Hilir' in entry['Titik']:
        return 'Titik_Hilir'
    else:
        return 'Unknown'

# Populate the data structure
for entry in periode_dicts:
    titik = entry['Titik']
    year = entry['Year']
    latitude = entry['Latitude']
    longitude = entry['Longitude']
    skor = entry['Skor']
    klasifikasi = entry['Klasifikasi']
    periode = entry['Periode']  # Read the 'Periode' column
    
    if titik not in data:
        data[titik] = {}
    
    if year not in data[titik]:
        data[titik][year] = {
            'Latitude': latitude,
            'Longitude': longitude,
            'Titik': titik,
            'Year': year,
            'Titik_Tengah': {},
            'Titik_Hulu': {},
            'Titik_Hilir': {}
        }
    
    category = determine_category(entry)
    
    if category not in data[titik][year]:
        data[titik][year][category] = {}
    
    data[titik][year][category][periode] = {
        'Skor': skor,
        'Klasifikasi': klasifikasi
    }

# Save the data to a JavaScript file
with open('map_data.js', 'w') as js_file:
    js_file.write('var data = ')
    json.dump(data, js_file, indent=4)
    js_file.write(';')

# Print a sample of the data to debug
print("Data Sample:", list(data.items())[:5])