import csv
import requests
import json
import time

# Configuration
CSV_FILE = 'supporting_files/test_case/assets_dump.csv'  # Your CSV file path
API_ENDPOINT = 'https://cf-test.lab.amagi.com/api/deliveries'  # Replace with your API endpoint
API_KEY = 'your_api_key_here'  # Replace with your API key if needed
DELAY_SECONDS = 1  # Delay between API calls to avoid rate limiting


def read_csv_data(file_path):
    """Read specified columns from CSV file."""
    data = []
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Extract only the required columns
                record = {
                    'amg_id': row.get('amg_id'),
                    'asset_id': row.get('asset_id'),
                    'platform_id': row.get('platform_id'),
                    'is_mdu_redelivery': row.get('is_mdu_redelivery'),
                    'not_billable': row.get('not_billable')
                }
                data.append(record)
        return data
    except FileNotFoundError:
        print(f"Error: CSV file {file_path} not found")
        return []
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return []


def create_json_payload(record):
    """Create JSON payload for API call from CSV record."""
    # Modify this structure to match your API's expected JSON format
    payload = {
        "data": {
            "amg_id": record['amg_id'],
            "asset_id": record['asset_id'],
            "platform_id": record['platform_id'],
            "is_mdu_redelivery": record['is_mdu_redelivery'] == 'True',  # Convert to boolean
            "not_billable": record['not_billable'] == 'True'  # Convert to boolean
        }
    }
    return payload


def make_api_call(payload):
    """Make POST API call with the given payload."""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'  # Modify based on your API's auth requirements
    }

    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {str(e)}")
        return None


def main():
    # Read CSV data
    records = read_csv_data(CSV_FILE)

    if not records:
        print("No data to process")
        return

    # Process each record
    for index, record in enumerate(records, 1):
        print(f"Processing record {index}/{len(records)}")

        # Create JSON payload
        payload = create_json_payload(record)

        # Make API call
        response = make_api_call(payload)

        if response:
            print(f"Success for record {index}: {json.dumps(response, indent=2)}")
        else:
            print(f"Failed for record {index}")

        # Delay between API calls
        time.sleep(DELAY_SECONDS)


if __name__ == '__main__':
    main()