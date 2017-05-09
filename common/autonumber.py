from enum import Enum


class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class Enumerator():
    def __init__(self):
        self.number=0
    def next(self):
        self.number+=1
        return self.number
    def reset(self):
        self.number = 0

