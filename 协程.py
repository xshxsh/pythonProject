import asyncio
import time


async def func1():
    print('你好啊，func1-1')
    # time.sleep(1)
    await asyncio.sleep(1)
    print('你好啊，func1-2')


async def func2():
    print('你好啊，func2-1')
    # time.sleep(1)
    await asyncio.sleep(1)
    print('你好啊，func2-2')


async def func3():
    print('你好啊，func3-1')
    # time.sleep(1)
    await asyncio.sleep(1)
    print('你好啊，func3-2')


async def main():
    tasks = [
        asyncio.create_task(func1()),
        asyncio.create_task(func2()),
        asyncio.create_task(func2())
    ]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    # asyncio.run(func1())
    t1 = time.time()
    asyncio.run(main())
    print('耗时', time.time() - t1)
