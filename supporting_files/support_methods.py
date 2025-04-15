from http.client import responses

import httpx

from supporting_files.common_variables import CommonVariables
from supporting_files.utils import utils_pt

class SupportMethods:
    url = CommonVariables()
    utils = utils_pt()

    async def payload_for_post(self):
        payload = {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        return payload

    async def call_post_method(self):
        payload = await self.payload_for_post()
        response = await self.utils.api_methods("POST", self.url.url ,payload)
        return response

    async def call_get_method(self):
        urls = f"{self.url.url}/1"
        response = await self.utils.api_methods("GET", urls, "")
        return response
