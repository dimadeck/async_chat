from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpclient import TCPClient


@gen.coroutine
def send_message():
    stream = yield TCPClient().connect('127.0.0.1', 8000)
    message = input()
    yield stream.write((message + "\n").encode())
    print(f"Send : {message}")
    reply = yield stream.read_until(b"\n")
    print(f"Response: {reply.decode().strip()}")


if __name__ == "__main__":
    IOLoop.current().run_sync(send_message)
