import random
import tornado.ioloop
import tornado.web
import tornado.websocket

class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        print("A new client connected.")
        WebSocketServer.clients.add(self)

    def on_close(self):
        print("A client disconnected.")
        WebSocketServer.clients.remove(self)

    @classmethod
    def send_message(cls, message: str):
        print(f"Sending message '{message}' to {len(cls.clients)} client(s).")
        for client in cls.clients:
            client.write_message(message)

class RandomWordSelector:
    def __init__(self, word_list):
        self.word_list = word_list

    def sample(self):
        return random.choice(self.word_list)

def main():
    app = tornado.web.Application(
        [
            (r"/websocket/", WebSocketServer)
        ],
        websocket_ping_interval=10,  # Send ping every 10 seconds
        websocket_ping_timeout=30,   # Close connection if no pong received within 30 seconds
    )
    app.listen(8888)
    print("WebSocket server started on port 8888")

    io_loop = tornado.ioloop.IOLoop.current()

    # List of words to send periodically
    word_selector = RandomWordSelector(['apple', 'banana', 'orange', 'grape', 'melon'])

    # Send a random word to all connected clients every 3 seconds
    periodic_callback = tornado.ioloop.PeriodicCallback(
        lambda: WebSocketServer.send_message(word_selector.sample()), 3000
    )
    periodic_callback.start()

    try:
        io_loop.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        io_loop.stop()

if __name__ == "__main__":
    main()