import pytest
from supporting_files.support_api_methods import SupportMethods

@pytest.fixture(scope="class")
def support_methods_fixture(bearer_token):
    return SupportMethods(token=bearer_token)

@pytest.mark.usefixtures("support_methods_fixture")
class TestAapiVvod:

    @pytest.fixture(autouse=True)
    def setup_support(self, support_methods_fixture):
        self.support = support_methods_fixture

    @pytest.mark.asyncio
    async def test_get_post(self):
        response = await self.support.call_get_method()
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_post(self):
        response = await self.support.call_post_method()
        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_delivery_post_api(self):
        responses = await self.support.create_for_post_delivery()
        assert responses.status_code == 200

