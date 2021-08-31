from threading import Timer


class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs):
        self.timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.timer = Timer(self.interval, self.run)
            self.timer.start()
            self.is_running = True

    def stop(self):
        self.timer.cancel()
        self.is_running = False
