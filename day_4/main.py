from time import time_ns

from fastapi import FastAPI
import redis.asyncio as redis


app = FastAPI()
redis_client = redis.Redis(host='redis')

@app.get('/ping')
async def read_root():
    return {'response': 'pong'}


def func(number: int):
    if number <= 1:
        return number
    return func(number - 1) + func(number - 2)


@app.get('/calc/{number}')
async def calc(number: int):
    start_time = time_ns()
    result = await redis_client.get(number)
    if not result:
        result = func(number)
        await redis_client.set(number, result)
    return {
        'result': result,
        'time': (time_ns() - start_time) / 10**9,
    }
