import pytest


@pytest.mark.asyncio
async def test_hello_world(make_get_request):
    response = await make_get_request(path="/")
    assert response.status == 200, response.body
    assert response.body == {'hello': 'world'}, response.body
