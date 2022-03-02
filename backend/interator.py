class MyIterator:
    def __init__(self, max_num):
        self.max_num = max_num

    def __iter__(self):
        num = 1
        while num <= self.max_num:
            yield num
            num += 1


def infinite_seq():
    num = 0
    while True:
        yield num
        num += 1
        print(';dddd')


if __name__ == "__main__":
    dddd = infinite_seq()

    print(next(dddd))
    # print(next(dddd))
    print(next(dddd))
    print(next(dddd))

    dddd = (num**2 for num in range(5))
    print(dddd)
    print(next(dddd))
    print(next(dddd))
    print(next(dddd))
    print(next(dddd))