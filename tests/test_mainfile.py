# test_api.py
import pytest

from supporting_files.support_methods import SupportMethods


class TestAapiVvod:

    support = SupportMethods()

    @pytest.mark.asyncio
    async def test_get_post(self):
        response = await self.support.call_get_method()
        assert response.status_code == 200
        assert response.json()["id"] == 1

    @pytest.mark.asyncio
    async def test_post(self):
        response = await self.support.call_post_method()
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
        assert response.status_code == 201, "Expected status code 201"