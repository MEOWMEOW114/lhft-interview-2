from fastapi import BackgroundTasks, FastAPI, WebSocket
import random
import asyncio
import time
import string
from http import HTTPStatus
from pydantic import BaseModel, Field
from typing import Dict
from uuid import UUID, uuid4
import multiprocessing
from fastapi.middleware.cors import CORSMiddleware


class Configure(BaseModel):
    elements_per_update: int = 50
    update_frequency_milliseconds: int = 1000


# Create application
app = FastAPI(title='WebSocket Example')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

# server configuration
NUMBER_OF_SYMBOLS = 500
N = 4
symbols = list(set([''.join(random.choices(string.ascii_uppercase, k=N))
                    for x in range(NUMBER_OF_SYMBOLS)]))

# server configuration
app.state.timeout = 0.5
app.state.symbols = symbols
app.state.last_ts = int(time.time() * 100)
app.state.resp = []
app.state.historial_values = initial_history_dict = {x: [] for x in symbols}
app.state.elements_per_update = 3
app.state.task = None

print(app.state.historial_values)


async def background_work():

    while True:
        current_ts = int(time.time() * 100)
        diff = (current_ts - app.state.last_ts)

        app.state.last_ts = current_ts
        target_symbols = random.sample(app.state.symbols,
                                       app.state.elements_per_update)

        min_ts = current_ts - 5 * 60 * 100
        resp = list(map(lambda sym: {
            # 'ts': ts,
            'symbol': sym,
            'price': int(random.uniform(0, 1) * 10000)}, target_symbols))

        for ele_update in resp:
            try:
                filtered = [
                    d for d in app.state.historial_values[ele_update['symbol']] if d['ts'] > min_ts]

                filtered.append({
                    'price': ele_update['price'],
                    'ts': current_ts
                })
                app.state.historial_values[ele_update['symbol']] = filtered
            except Exception as err:
                print(err)
                print(ele_update['symbol'])
            # print(filtered)
        # print(resp)
        app.state.resp = resp

        completed_ts = int(time.time() * 100)

        timeout = app.state.timeout - (completed_ts - current_ts) * 1.0/100
        print(timeout)
        await asyncio.sleep(timeout)


@app.post("/new_task", status_code=HTTPStatus.ACCEPTED)
async def task_handler(configure: Configure, background_tasks: BackgroundTasks):
    # print(configure)
    minsecond = configure.update_frequency_milliseconds
    if minsecond >= 100:
        app.state.timeout = minsecond / 1000

    if configure.elements_per_update <= len(app.state.symbols):
        app.state.elements_per_update = configure.elements_per_update

    return {}


@app.on_event("startup")
async def startup_event():
    print(' on startup')
    app.state.task = asyncio.ensure_future(background_work())


@app.on_event("shutdown")
async def on_shutdown():
    if not app.state.task.cancelled():
        app.state.task.cancel()


@app.get("/symbols")
async def read_main():
    import os
    print(os.getpid())
    # print(worker.getpid())

    return {"symbols": app.state.symbols}


@app.get("/historic/{symbol}/{since}/{last}")
async def historic(symbol: str, since: int, last: int):
    current_ts = int(time.time() * 100)
    max_ts = current_ts - since * 100
    last_ts = max_ts - last * 100
    try:
        symbol_history = app.state.historial_values[symbol]
        symbol_history = [
            d for d in symbol_history if d['ts'] <= max_ts and d['ts'] >= last_ts]
    except Exception as err:
        symbol_history = []
    return {"historic": symbol_history}


@app.get("/")
async def read_main():
    return {"msg": 'hello world', 'time': app.state.timeout}


# // https: // stackoverflow.com/questions/67947099/send-receive-in-parallel-using-websockets-in-python-fastapi


@app.websocket("/ws/samples_update")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    last_ts = time.time()
    while True:
        try:
            # Wait for any message from the client
            # time.sleep(1000)
            echo = await websocket.receive_text()

            # only send json if there is any update
            if app.state.resp:
                await websocket.send_json(app.state.resp)
            app.state.resp = []
        except Exception as e:
            print('error:', e)
            break
    print('Bye..')
