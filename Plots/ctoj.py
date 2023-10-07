import csv
import json
# Specify the input CSV file and the output JSON file
csv_file = 'nakamura_1979_sm_locations.csv'
json_file = 'nakamura_1979_sm_locations.json'

# Read the CSV file and convert it to a list of dictionaries
csv_data = []
with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        csv_data.append(row)

# Write the list of dictionaries to a JSON file
with open(json_file, mode='w') as file:
    json.dump(csv_data, file, indent=4)

print(f'CSV file "{csv_file}" has been converted to JSON file "{json_file}".')
