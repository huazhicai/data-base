import redis

# r = redis.Redis(host='localhost', port=6379, db=2)

class Base(object):
    def __init__(self):
        self.r = redis.Redis(host)