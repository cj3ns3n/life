from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import argparse
from life_display import LifeDisplay
from stats_container import StatsContainer
from terminal_display import TerminalDisplay
from logger import Logger
from phenotypes.terra_firma import Land
from phenotypes.simulation import Simulation
from entity_engine import EntityEngine


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Life Simulation')
    parser.add_argument('-l', '--log-file', help='log file')

    args = parser.parse_args()

    stats = StatsContainer()
    terminal = TerminalDisplay(stats)
    terminal.run()
    logger = Logger(terminal, LifeDisplay.__name__, args.log_file)

    display_size =  (600, 300)
    land = Land(display_size, logger.get_logger(Land.__name__))
    simulation = Simulation(land, stats, logger.get_logger(Simulation.__name__))
    engine = EntityEngine(simulation, stats, logger.get_logger(EntityEngine.__name__))
    engine.daemon = True
    engine = engine
    engine.start()

    life_display = LifeDisplay(land, simulation, display_size, stats, logger)
    life_display.display()
#end if
