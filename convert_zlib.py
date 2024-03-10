import json
import zlib
import base64
import glob
import os

def compress_coordinates(input_file, output_file):
    # Read the JSON data from the input file
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    # Iterate through each feature in the GeoJSON
    for feature in data['features']:
        # Extract the coordinates
        coordinates = feature['geometry']['coordinates']
        
        # Convert the coordinates to a JSON string and then to bytes
        coordinates_bytes = json.dumps(coordinates).encode('utf-8')
        
        # Compress the coordinates bytes using zlib
        compressed_coordinates = zlib.compress(coordinates_bytes)
        
        # Convert the compressed bytes to a base64 string to store in JSON
        compressed_base64 = base64.b64encode(compressed_coordinates).decode('utf-8')
        
        # Replace the original coordinates with the compressed base64 string
        feature['geometry']['compressed_coordinates'] = compressed_base64
        del feature['geometry']['coordinates']  # Optionally remove the original to save space
    
    # Write the modified data to the output file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

def compress_all_in_folder(input_folder, output_folder):
    # Ensure output_folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Find all JSON files in the input_folder
    input_files = glob.glob(os.path.join(input_folder, '*.json'))
    
    for input_file in input_files:
        # Construct the output file path
        output_file = os.path.join(output_folder, os.path.basename(input_file))
        # Compress the coordinates for this file
        compress_coordinates(input_file, output_file)
        print(f'Processed {input_file}')

# Example usage - adjust 'input' and 'output' to your folder paths
input_folder = 'input'
output_folder = 'output'
compress_all_in_folder(input_folder, output_folder)

