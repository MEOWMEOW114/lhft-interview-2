from collections.abc import Generator


def averager() -> Generator[float, float, None]:  
    total = 0.0
    count = 0
    average = 0.0
    while True:  
        term = yield average  
        total += term
        count += 1
        average = total/count


# >>> coro_avg = averager()  1
#     >>> next(coro_avg)  2
#     0.0
#     >>> coro_avg.send(10)  3
#     10.0
#     >>> coro_avg.send(30)
#     20.0
#     >>> coro_avg.send(5)
#     15.0