import pygame

from pos import Pos
from info_text import InfoText


class LifeDisplay:
    image_save_frequency = 10  # 10 cycles

    def __init__(self, land, sim_surface, stats, logger):
        pygame.init()
        self.sim_surface = sim_surface
        self.display = pygame.display.set_mode(sim_surface.surface_array.shape[:2])
        pygame.display.set_caption("It's alive")

        self.stats = stats
        self.infoText = InfoText()
        self.logger = logger

        self.land = land

        self.show_entity = True
        self.show_aspect_1 = False
        self.show_aspect_2 = False
        self.show_aspect_3 = False
        self.show_sparkles = True
        self.show_stats_overlay = False
        self.show_land = True

        self.changed_cells = []
    # end def

    def start(self):
        game_running = True
        last_mouse_pos = Pos(0, 0)

        self.logger.info('display started')
        while game_running:
            surface_array = self.sim_surface.get_surface_array()
            life_surface = pygame.surfarray.make_surface(surface_array)

            self.display.blit(life_surface, (0, 0))
            pygame.display.update()
            self.logger.refresh_terminal()

            # save periodic image
            if self.stats.cycles % LifeDisplay.image_save_frequency == 0:
                filename = 'life-%07d.jpg' % self.stats.cycles
                #pygame.image.save(self.surface, filename)
            # end if

            self.stats.increment_display_iterations()
            #self.logger.info('display refreshes: %d' % self.stats.display_iterations)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_running = False
                        break
                    elif event.key == pygame.K_e:
                        self.show_entity = not self.show_entity
                    elif event.key == pygame.K_1:
                        self.show_aspect_1 = not self.show_aspect_1
                    elif event.key == pygame.K_2:
                        self.show_aspect_2 = not self.show_aspect_2
                    elif event.key == pygame.K_3:
                        self.show_aspect_3 = not self.show_aspect_3
                    elif event.key == pygame.K_b:
                        self.show_sparkles = not self.show_sparkles
                    elif event.key == pygame.K_n:
                        self.show_land = not self.show_land
                    elif event.key == pygame.K_o:
                        self.show_stats_overlay = not self.show_stats_overlay
                # end if
            # end for

            mouse_pos = Pos(tuple_pos=pygame.mouse.get_pos())
            if mouse_pos != last_mouse_pos:
                last_mouse_pos = mouse_pos
                #self.terminal.add_message('mouse position %s' % repr(mouse_pos))
                self.infoText.set_entity(self.land.get_entity(mouse_pos), mouse_pos)
        # end while

        self.logger.shutdown()
        pygame.quit()
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
