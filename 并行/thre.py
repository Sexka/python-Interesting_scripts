import aiohttp
import asyncio
from gevent import monkey
monkey.patch_all()

async def request(url):
    print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response)

# <并行>
async def main_async():
    # 准备请求列表
    urls = ['http://www.baidu.com', 'http://www.163.com', 'http://www.bing.com']
    # 使用异步IO, 等待三个请求都都完成
    await asyncio.wait([request(url) for url in urls])
    print('结束了')



# 串行
async def main_sync():
    # 依次等待每一个请求
    await request('http://www.baidu.com')
    await request('http://www.163.com')
    await request('http://www.bing.com')
    print('结束了')

if __name__ == '__main__': 
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main_sync())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_async())