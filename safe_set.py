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
            if len(self.data_set) > 0:
                return self.data_set.pop()
            return None
    # end def

    def __len__(self):
        return len(self.data_set)
    # end def
# end class

