import argparse
from life_display import LifeDisplay
from stats_container import StatsContainer
from terminal_display import TerminalDisplay
from logger import Logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Life Simulation')
    parser.add_argument('-l', '--log-file', help='log file')

    args = parser.parse_args()

    stats = StatsContainer()
    terminal = TerminalDisplay(stats)
    terminal.run()
    logger = Logger(terminal, LifeDisplay.__name__, args.log_file)

    life_display = LifeDisplay(stats, logger)
    life_display.display()
#end if