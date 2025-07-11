import threading


class SafeSet:
    def __init__(self, size=100):
        self.lock = threading.Lock()
        self.data_set = set()
    # end def

    def add(self, object):
        with self.lock:
          self.data_set.add(object)
    # end def

    def get(self):
        with self.lock:
            return self.data_set.pop()
    # end def

    def __len__(self):
        return len(self.data_set)
    # end def
# end class

