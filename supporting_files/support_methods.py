from supporting_files.common_variables import CommonVariables
from supporting_files.utils import utils_pt


class SupportMethods:

    def __init__(self, token):
        self.token = token
        self.url = CommonVariables()
        self.utils = utils_pt()
        self.header = {"Authorization": self.token, "x-service-id": "vod"}

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
