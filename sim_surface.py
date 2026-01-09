import numpy as np
from threading import Lock

class SimulationSurface:
    def __init__(self, display_size):
        self.surface_array = np.zeros(shape=(display_size[0], display_size[1], 3))
        self.lock = Lock()
    # end def

    def get_surface_array(self):
      self.acquire_lock()
      surface_array_cp = self.surface_array.astype('uint8')
      # random surface (for demo purpose)
      #surface_array_cp = np.random.random(self.surface_array.shape) * 255.0
      #surface_array_cp = surface_array_cp.astype('uint8')
      self.release_lock()

      return surface_array_cp
    # end def

    def set_color(self, pos, color):
      self.surface_array[pos.x, pos.y, :] = color
    # end def

    def acquire_lock(self):
      self.lock.acquire()
    # end def

    def release_lock(self):
      self.lock.release()
    # end def
# end class
