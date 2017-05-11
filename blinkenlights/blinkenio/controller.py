import concurrent.futures
import functools
import threading


class Controller:

    def __init__(self):
        self.ok = False

    def start(self):
        self.ok = True

    def stop(self):
        self.ok = False


