import httpx

from supporting_files.common_variables import CommonVariables


class SupportMethods:
    url = CommonVariables()

    async def payload_for_post(self):
        payload = {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        return payload

    async def call_post_method(self):
        async with httpx.AsyncClient() as client:
            payload = await self.payload_for_post()
            response = await client.post(self.url.url, json= payload)
            return response

    async def call_get_method(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.url.url}/1")
            return response