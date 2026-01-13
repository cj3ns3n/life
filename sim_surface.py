import numpy as np
from threading import Lock

class SimulationSurface:
    def __init__(self, display_size):
        self.width = display_size[0]
        self.height = display_size[1]
        self.surface_array = np.zeros(shape=(self.width, self.height, 3))
        self.lock = Lock()
        
        # Double buffer system for efficient rendering
        # Each buffer is RGBA with Y-axis already flipped for Pyglet
        buffer_size = self.width * self.height * 4
        self.buffer_a = bytearray(buffer_size)
        self.buffer_b = bytearray(buffer_size)
        
        # Track which buffer is currently being written to
        self.write_buffer = self.buffer_a
        self.read_buffer = self.buffer_b
    # end def

    def get_surface_array(self):
      """Get RGB numpy array (for compatibility)."""
      self.acquire_lock()
      surface_array_cp = self.surface_array.astype('uint8')
      # random surface (for demo purpose)
      #surface_array_cp = np.random.random(self.surface_array.shape) * 255.0
      #surface_array_cp = surface_array_cp.astype('uint8')
      self.release_lock()

      return surface_array_cp
    # end def

    def get_surface_array_bytes(self):
      """Get RGBA bytes buffer (fast, no conversion needed)."""
      #self.acquire_lock()
      # Swap buffers - what was being written is now ready to read
      #self.read_buffer, self.write_buffer = self.write_buffer, self.read_buffer
      # Copy read buffer to return (so caller gets stable data)
      result = self.write_buffer
      #self.release_lock()
      
      return result
    # end def

    def set_color(self, pos, color):
      """Set color at position and update both numpy array and bytearray buffer."""
      # Update numpy array
      self.surface_array[pos.x, pos.y, :] = color
      
      # Update bytearray buffer with Y-axis flipped for Pyglet (bottom-left origin)
      # Pyglet expects: row 0 is bottom, row H-1 is top
      # Our numpy has: y=0 is top, y=H-1 is bottom (typically)
      flipped_y = self.height - 1 - pos.y
      
      # Calculate byte offset in the flipped buffer
      # Buffer layout: [row0_pixel0_RGBA, row0_pixel1_RGBA, ..., row1_pixel0_RGBA, ...]
      # Where row0 is the BOTTOM row in Pyglet coordinates
      pixel_index = flipped_y * self.width + pos.x
      byte_offset = pixel_index * 4
      
      # Set RGBA values in write buffer
      self.write_buffer[byte_offset + 0] = int(color[0])  # R
      self.write_buffer[byte_offset + 1] = int(color[1])  # G
      self.write_buffer[byte_offset + 2] = int(color[2])  # B
      self.write_buffer[byte_offset + 3] = 255             # A (fully opaque)
    # end def

    def acquire_lock(self):
      self.lock.acquire()
    # end def

    def release_lock(self):
      self.lock.release()
    # end def
# end class
