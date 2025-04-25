import row

from supporting_files.common_variables import CommonVariables
from supporting_files.utils import utils_pt
import pandas as pd
import requests
import json
import time

class SupportMethods:

    def __init__(self, token):
        self.token = token
        self.url = CommonVariables()
        self.utils = utils_pt()
        self.header = {"Authorization": self.token, "x-service-id": "vod"}
        self.CSV_FILE_PATH = 'supporting_files/test_case/assets_dump.csv'

    async def payload_for_post(self):
        return {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }

    async def call_post_method(self):
        payload = await self.payload_for_post()
        response = await self.utils.api_methods("POST", self.url.url, payload, self.header)
        return response

    async def call_get_method(self):
        urls = f"{self.url.url}/1"
        response = await self.utils.api_methods("GET", urls, "", self.header)
        return response

    async def read_csv_data(self, CSV_FILE_PATH):
        try:
            # Read only the specified columns from CSV
            df = await pd.read_csv(CSV_FILE_PATH,
                             usecols=['amg_id', 'asset_id', 'platform_id', 'is_mdu_redelivery', 'not_billable'])
            return df
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None

    async def create_json_payload(row):
    # Construct JSON payload from row data
        payload = [{
        "amg_id": row['amg_id'],
        "asset_id": row['asset_id'],
        "platform_id": row['platform_id'],
        "is_mdu_redelivery": row['is_mdu_redelivery'],
        "not_billable": row['not_billable']
        }]
        return payload

    async def create_for_post_delivery(self):
        df = await self.read_csv_data(self.CSV_FILE_PATH)
        if df is None:
            return
        # Process each row
        for index, row in df.iterrows():
            # Create JSON payload
            payload = await self.create_json_payload(row)

            # Make POST request
            response = await self.make_post_request(self.url.url, payload, self.token)

            # Optional: Process response if needed
            if response:
                print(f"Response for amg_id {row['amg_id']}: {response}")
                return response
            # Delay to avoid overwhelming the API
            time.sleep(1)

    async def make_post_request(self, url, payload, token):
        payload = await self.create_json_payload()
        response = await self.utils.api_methods("POST", self.url.url, payload, self.header)
        return response