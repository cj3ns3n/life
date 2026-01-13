import ctypes
import pyglet
from pyglet import gl
from pyglet.window import key

from pos import Pos
from info_text import InfoText


class LifeDisplay:
    image_save_frequency = 10  # 10 cycles

    def __init__(self, land, sim_surface, stats, logger):
        self.sim_surface = sim_surface
        self.stats = stats
        self.infoText = InfoText()
        self.logger = logger
        self.land = land

        # Display options
        self.show_entity = True
        self.show_aspect_1 = False
        self.show_aspect_2 = False
        self.show_aspect_3 = False
        self.show_sparkles = True
        self.show_stats_overlay = True  # Changed default to True to show stats
        self.show_land = True

        self.changed_cells = []
        self.last_mouse_pos = Pos(0, 0)
        self.game_running = True

        # Get dimensions from sim_surface
        self.width = sim_surface.surface_array.shape[0]
        self.height = sim_surface.surface_array.shape[1]

        # Create main Pyglet window for simulation
        self.window = pyglet.window.Window(self.width, self.height, vsync=True, resizable=False)
        self.window.set_caption("It's alive")

        # Create separate stats window
        self.stats_window = pyglet.window.Window(500, 300, vsync=True, resizable=False)
        self.stats_window.set_caption("Simulation Stats")
        # Position stats window to the right of main window
        self.stats_window.set_location(self.window.get_location()[0] + self.width + 10, 
                                       self.window.get_location()[1])

        # Create RGBA buffer for Pyglet (needs alpha channel)
        self.buf = bytearray(self.width * self.height * 4)
        self.c_buf = (gl.GLubyte * (self.width * self.height * 4)).from_buffer(self.buf)

        # Create persistent GPU texture
        self.tex = pyglet.image.Texture.create(self.width, self.height)
        gl.glBindTexture(self.tex.target, self.tex.id)
        gl.glTexParameteri(self.tex.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(self.tex.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        # Create batch for text rendering
        self.text_batch = pyglet.graphics.Batch()

        # Register event handlers for main window
        self.window.on_draw = self.on_draw_main
        self.window.on_key_press = self.on_key_press
        self.window.on_mouse_motion = self.on_mouse_motion
        self.window.on_close = self.on_close

        # Register event handlers for stats window
        self.stats_window.on_draw = self.on_draw_stats
        self.stats_window.on_key_press = self.on_key_press
        self.stats_window.on_close = self.on_close

        self.logger.info('display initialized')
    # end def

    def upload_texture(self):
        """Upload the CPU buffer into the GPU texture."""
        gl.glBindTexture(self.tex.target, self.tex.id)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)

        gl.glTexSubImage2D(
            self.tex.target, 0,
            0, 0, self.width, self.height,
            gl.GL_RGBA,
            gl.GL_UNSIGNED_BYTE,
            ctypes.cast(self.c_buf, ctypes.c_void_p)
        )
    # end def

    def on_draw_main(self):
        """Pyglet draw event handler for main simulation window."""
        self.window.clear()
        
        # Draw the simulation texture
        self.tex.blit(0, 0, width=self.window.width, height=self.window.height)
    # end def

    def on_draw_stats(self):
        """Pyglet draw event handler for stats window."""
        self.stats_window.clear()
        
        # Draw stats if window is visible
        if self.show_stats_overlay and self.stats_window.visible:
            # Clear the batch and recreate labels
            self.text_batch = pyglet.graphics.Batch()
            self.infoText.blit(self.text_batch, self.stats)
            
            # Draw all text labels
            self.text_batch.draw()
    # end def

    def on_key_press(self, symbol, modifiers):
        """Pyglet keyboard event handler (works on both windows)."""
        if symbol == key.ESCAPE:
            self.game_running = False
            self.window.close()
            self.stats_window.close()
        elif symbol == key.E:
            self.show_entity = not self.show_entity
        elif symbol == key._1:
            self.show_aspect_1 = not self.show_aspect_1
        elif symbol == key._2:
            self.show_aspect_2 = not self.show_aspect_2
        elif symbol == key._3:
            self.show_aspect_3 = not self.show_aspect_3
        elif symbol == key.B:
            self.show_sparkles = not self.show_sparkles
        elif symbol == key.N:
            self.show_land = not self.show_land
        elif symbol == key.O:
            self.show_stats_overlay = not self.show_stats_overlay
            # Toggle stats window visibility
            self.stats_window.set_visible(self.show_stats_overlay)
    # end def

    def on_mouse_motion(self, x, y, dx, dy):
        """Pyglet mouse motion event handler."""
        mouse_pos = Pos(x, y)
        if mouse_pos != self.last_mouse_pos:
            self.last_mouse_pos = mouse_pos
            if self.land:
                self.infoText.set_entity(self.land.get_entity(mouse_pos), mouse_pos)
    # end def

    def on_close(self):
        """Pyglet window close event handler (closes both windows)."""
        self.game_running = False
        # Close both windows
        try:
            self.window.close()
        except:
            pass
        try:
            self.stats_window.close()
        except:
            pass
        self.logger.shutdown()
        return pyglet.event.EVENT_HANDLED
    # end def

    def update(self, dt):
        """Called periodically to update the display."""
        if not self.game_running:
            pyglet.app.exit()
            return

        # Get the simulation surface array as bytes
        new_data = self.sim_surface.get_surface_array_bytes()
        # Copy into our buffer
        self.buf[:] = new_data

        # Upload to GPU
        self.upload_texture()

        # Refresh terminal display
        self.logger.refresh_terminal()

        # Save periodic image
        if self.stats.cycles % LifeDisplay.image_save_frequency == 0:
            filename = 'life-%07d.jpg' % self.stats.cycles
            # Note: Pyglet image saving
            # pyglet.image.get_buffer_manager().get_color_buffer().save(filename)

        self.stats.increment_display_iterations()
    # end def

    def start(self):
        """Start the Pyglet application."""
        self.logger.info('display started')
        
        # Schedule the update function to run at 60 FPS
        pyglet.clock.schedule_interval(self.update, 1.0 / 60.0)
        
        # Start Pyglet event loop
        pyglet.app.run()
        
        # Cleanup after app exits
        self.logger.shutdown()
        exit()
    #end def
#end class

def nop(*args):
    pass

if __name__ == '__main__':
    from sim_surface import SimulationSurface
    sim_surface = SimulationSurface((600, 600))

    from stats_container import StatsContainer
    stats = StatsContainer(None)

    logger = lambda: None
    logger.shutdown = nop
    logger.refresh_terminal = nop
    logger.info = nop

    display = LifeDisplay(None, sim_surface, stats, logger)
    display.start()
