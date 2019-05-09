from threading import Lock

mylock = Lock()
p = print

def print(*a, **b):
    with mylock:
            p(*a, **b)