import time


class TaskState:

    def __init__(self):
        self.counter = 0
        self.last_ts = time.time()

    def background_work(self):
        while True:
            self.counter += 1
            print(items['s'])

            items['s'] = random.uniform(0, 1) * 10000
            time.sleep(1)

    def get_state(self):
        return self.counter
