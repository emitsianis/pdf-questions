from queue import Queue
from threading import Thread

from flask import current_app

from app.chat.callbacks.stream import SteamingHandler


class StreamableChain:
    def stream(self, input):
        queue = Queue()
        handler = SteamingHandler(queue)

        def task(app_context):
            print("Starting task")
            app_context.push()
            self(input, callbacks=[handler])
            print("Ending task")

        Thread(target=task, args=[current_app.app_context()]).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token
