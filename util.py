import asyncio

async def run_every(seconds: float, func, *args, **kwargs):
    returned = 0
    while True:
        await asyncio.sleep(seconds)
        returned = await func(*args, returned, **kwargs)
        if returned is False:
            break