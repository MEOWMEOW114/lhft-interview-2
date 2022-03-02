import asyncio
from collections.abc import Iterable, Iterator, Generator, Coroutine


class T:
    __iter__ = ...
    #  def __iter__(self):
    #      return ...
    __next__ = ...
    send = ...
    throw = ...
    close = ...

    # def __await__(self):
    #     # yield from asyncio.sleep(2)
    #     return new_sleep().__await__()


#  iter(T())
print(f'{isinstance(T(), Iterable)  = }')
print(f'{isinstance(T(), Iterator)  = }')
print(f'{isinstance(T(), Generator) = }')
print(f'{isinstance(T(), Coroutine) = }')


async def new_sleep():
    await asyncio.sleep(1)


class Waiting:
    def __await__(self):
        yield from new_sleep().__await__()
        print('first sleep')
        yield from new_sleep().__await__()
        print('second sleep')
        return 'done'


async def ticker(delay, to):
    """Yield numbers from 0 to `to` every `delay` seconds."""
    for i in range(to):
        yield i
        await asyncio.sleep(delay)


async def main():
    # tick = ticker(0, 10)
    # tick.next()

    await Waiting()


async def main2():
    async for i in ticker(2, 10):
        print(i)

    # foo = ticker(2, 10)
    # a = await foo.__anext__()
    # print(a)


if __name__ == "__main__":
    # asyncio.run(ticker(1, 4))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # loop.run_until_complete(main())
