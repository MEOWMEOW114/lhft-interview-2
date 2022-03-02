from fastapi import BackgroundTasks, FastAPI, WebSocket
import random
import asyncio

# @app.websocket("/wsqueue")
# // https://stackoverflow.com/questions/67947099/send-receive-in-parallel-using-websockets-in-python-fastapi


async def read_and_send_to_client(data):
    print(f'reading {data} from client')
    await asyncio.sleep(10)  # simulate a slow call
    print(f'finished reading {data}, sending to websocket client')


async def read_webscoket(websocket: WebSocket):
    await websocket.accept()
    queue = asyncio.queues.Queue()

    async def read_from_socket(websocket: WebSocket):
        async for data in websocket.iter_json():
            print(f"putting {data} in the queue")
            queue.put_nowait(data)

    async def get_data_and_send():
        data = await queue.get()
        fetch_task = asyncio.create_task(read_and_send_to_client(data))
        while True:
            data = await queue.get()
            if not fetch_task.done():
                print(f'Got new data while task not complete, canceling.')
                fetch_task.cancel()
            fetch_task = asyncio.create_task(read_and_send_to_client(data))

    await asyncio.gather(read_from_socket(websocket), get_data_and_send())
