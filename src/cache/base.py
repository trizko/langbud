class BaseCache:
    def get(self, key):
        raise NotImplementedError

    def set(self, key, value, timeout=None):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def push(self, key, *values):
        raise NotImplementedError

    def pop(self, key):
        raise NotImplementedError

    def length(self, key):
        raise NotImplementedError
