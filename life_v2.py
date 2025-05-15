import argparse
from life_display import LifeDisplay
from stats_container import StatsContainer
from terminal_display import TerminalDisplay
from logger import Logger
from phenotypes.terra_firma import Land
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
    engine = EntityEngine(land, stats, logger.get_logger(EntityEngine.__name__))
    engine.daemon = True

    life_display = LifeDisplay(land, engine, display_size, stats, logger)
    life_display.display()
#end if
