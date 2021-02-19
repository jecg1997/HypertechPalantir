# import websockets
# import logging
# import asyncio
# from websockets import WebSocketClientProtocol
# #---------------------------------------------------------------------------
# logging.basicConfig(level = logging.INFO)

# async def consumer_handler(websocket: WebSocketClientProtocol) -> None:
#     async for message in websocket:
#         log_message(message)

# async def consume(hostname: str, port:int)-> None:
#     websocket_resource_url = f"ws://{hostname}:{port}"
#     async with websockets.connect(websocket_resource_url) as websocket:
#         await consumer_handler(websocket)

# async def produce(message: str, host: str, port: int) -> None:
#     async with websockets.connect(f"ws://{host}:{port}") as ws:
#         await ws.send(message)
#         await ws.recv()

# def log_message(message: str) -> None:
#     logging.info(f"Message: {message}")


# if __name__ =='__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(produce(message='hi', host='localhost', port=9001))
#     loop.run_forever()    



# import asyncio
# import websockets
 
# async def test():
 
#     async with websockets.connect('ws://localhost:9001') as websocket:
 
#         await websocket.send("hello")
 
#         response = await websocket.recv()
#         print(response)
#         await websocket.recv()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(test())
# # loop.run_forever()



from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect


class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        PeriodicCallback(self.keep_alive, 20000).start()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        print ("trying to connect")
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception as e:
            print ("connection error")
        else:
            print ("connected")
            self.run()

    @gen.coroutine
    def run(self):
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                print ("connection closed")
                self.ws = None
                break

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("Merwebo")

if __name__ == "__main__":
    client = Client("ws://localhost:8888", 5)
