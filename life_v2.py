import argparse
from importlib import import_module
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from life_display import LifeDisplay
from stats_container import StatsContainer
from terminal_display import TerminalDisplay
from logger import Logger
from entity_engine import EntityEngine
from safe_set import SafeSet

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Life Simulation')
    parser.add_argument('-s', '--simulation-name', default='phenotypes', help='simulation model')
    parser.add_argument('-l', '--log-file', help='log file')

    args = parser.parse_args()

    display_size = (600, 300)
    change_queue = SafeSet()

    stats = StatsContainer(change_queue)
    terminal = TerminalDisplay(stats)
    terminal.run()
    logger = Logger(terminal, LifeDisplay.__name__, args.log_file)

    sim_name = args.simulation_name
    land_module = import_module(sim_name + '.land')
    sim_module = import_module(sim_name + '.simulation')
    land = eval('land_module.Land(display_size, logger.get_logger(land_module.Land.__name__))')
    simulation = eval('sim_module.Simulation(land, change_queue, stats, logger.get_logger(sim_module.Simulation.__name__))')

    engine = EntityEngine(simulation, stats, logger.get_logger(EntityEngine.__name__))
    engine.daemon = True
    engine = engine
    engine.start()

    life_display = LifeDisplay(land, change_queue, display_size, stats, logger)
    life_display.display()
#end if
