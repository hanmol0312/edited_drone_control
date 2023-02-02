import asyncio
from awaits import awaitable
import aioify

# @aioify
def do():
    print("I am doing!")
    print("I am done.")

async def do_not():
    do()
    print("I am not done")

asyncio.run(do_not())