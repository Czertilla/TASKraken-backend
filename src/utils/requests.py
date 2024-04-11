import aiohttp
import asyncio
import logging
if __name__ != "__main__":
    from .exceptor import Exceptor
else:
    from exceptor import Exceptor
exc = Exceptor()

DESERIALIZE_HTTP = 'https://recruit.rtuitlab.dev/deserialize'
DESERIALIZE_HEADERS = {
    'accept': 'application/json'
}

SERIALIZE_HTTP = 'https://recruit.rtuitlab.dev/serialize'
SERIALIZE_HEADERS = {
    'accept': 'application/octet-stream', 
    'Content-Type': 'application/json'
}

logger = logging.getLogger(__name__)


@exc.aiotect
async def deserialize(bytecode: bytes) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(DESERIALIZE_HTTP, data=bytecode, headers=DESERIALIZE_HEADERS) as response:
            logger.info("Status: %s", response.status)
            logger.info("Content-type: %s", response.headers['content-type'])
            data = await response.json()
    return data


@exc.aiotect
async def serialize(data: dict) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.post(SERIALIZE_HTTP, json=data, headers=SERIALIZE_HEADERS) as response:
            logger.info("Status: %s", response.status)
            logger.info("Content-type: %s", response.headers['content-type'])
            data = await response.content.read()
    return data

if __name__ == "__main__":
    testdata = {"abc": 123,
                "123": 123,
                "dfd": {
                    'a': 'as',
                    'v': 'fdf'
                }}
    bytecode = asyncio.run(serialize(testdata))
    print(bytecode)
    print(asyncio.run(deserialize(bytecode)))
    