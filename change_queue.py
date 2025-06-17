from queue import Queue

class ChangeQueue:
    def __init__(self, maxsize=0):
      self.queue = Queue(maxsize=maxsize)
    # end def

    def add(self, cell):
      if not self.queue.full():
        self.queue.put(cell)
    # end def

    def get(self):
      cell = None

      if not self.queue.empty():
        cell = self.queue.get()
        self.queue.task_done()
      # end def

      return cell
    # end def

    def __len__(self):
      return self.queue.qsize()
# end class