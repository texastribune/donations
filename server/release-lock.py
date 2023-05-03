from .batch import Lock

lock = Lock(key="charge-cards-lock")
lock.release()
