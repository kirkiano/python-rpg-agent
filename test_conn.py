import socket
import asyncio
import time
from traceback import print_exc

# TODO: eventually get rid of this file


host = 'live_driver'
port = 11237


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("connecting")
    s.connect((host, port))
    print("cxn DONE")
except Exception:
    print_exc()


try:
    print("creating ioloop")
    ioloop = asyncio.get_event_loop()
    print("ioloop created")

    @asyncio.coroutine
    def f():
        r, w = yield from asyncio.open_connection(host, port, loop=ioloop)
    print("Creating tasks")
    tasks = [ioloop.create_task(f())]
    print("Running ioloop")
    ioloop.run_until_complete(asyncio.wait(tasks))
    print("ioloop DONE")
except Exception:
    print("We caught exception")
    print_exc()
finally:
    print("finally done")


# Gives enough time to log in to Docker container and test network
time.sleep(6000)
