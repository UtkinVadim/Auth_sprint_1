from dataclasses import dataclass

import aiohttp
import pytest
from multidict import CIMultiDictProxy

import config

SERVICE_URL = f"http://{config.SERVER_HOST}:{config.SERVER_PORT}"


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(path: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f"{SERVICE_URL}{path}"
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
