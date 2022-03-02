import asyncio


async def async_generator():
    # for i in range(3):
    i = 1
    await asyncio.sleep(1)

    async def g():

        yield 1

        yield 2
    async for k in g():
        yield k
    yield i*i


async def main():
    async for i in async_generator():
        print(i)

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        # see: https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.shutdown_asyncgens
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
