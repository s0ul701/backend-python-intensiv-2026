from time import perf_counter_ns

from fastapi import FastAPI
import redis.asyncio as redis


app = FastAPI()
redis_client = redis.Redis(host='redis')

@app.get('/ping')
async def read_root():
    return {'response': 'pong'}


def long_time_func(number: int):
    if number <= 1:
        return number
    return long_time_func(number - 1) + long_time_func(number - 2)


@app.get('/calc/{number}')
async def calc(number: int):
    start_time = perf_counter_ns()
    result = await redis_client.get(number)
    if not result:
        result = long_time_func(number)
        await redis_client.set(number, result)
    return {
        'result': result,
        'time': (perf_counter_ns() - start_time) / 10**9,
    }
