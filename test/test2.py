import asyncio
import requests
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

async def entrypoint():
    url = 'https://leetcode.com/contest/api/ranking/weekly-contest-273/?pagination={}'
    await asyncio.wait([get(url.format(i)) for i in range(1, 1000)])
    # await asyncio.wait([
    #     get('https://www.google.com'),
    #     get('https://www.stackoverflow.com'),
    # ])

async def get(url):
    print(url)
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None, requests.get, url)
    print(url, res)

loop = asyncio.get_event_loop()
loop.run_until_complete(entrypoint())