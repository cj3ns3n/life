import curses
from threading import Lock

class TerminalDisplay:
    def __init__(self, stats_container):
        self.stats_container = stats_container
        self.scr = curses.initscr()
        self.size = self.scr.getmaxyx()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        if curses.has_colors():
            curses.start_color()

        self.terminal_lock = Lock()
        self.messages = []
    # end def

    def add_message(self, message):
        self.terminal_lock.acquire()
        try:
            if len(message) < self.size[0]:
                message = message + ' ' * (self.size[0] - len(message))

            self.messages.append(message)
            if len(self.messages) > 5:
                self.messages = self.messages[-5:]
        finally:
            self.terminal_lock.release()

    # end def

    def run(self):
        stats = self.stats_container.get_stats()

        self.scr.addstr(0, 0, "Cycles: %d" % stats['cycles'])

        pop_text_str = 'Population %03d; Males %03d; Females %03d' % (stats['births'] - stats['maternal_deaths'] - stats['natural_deaths'], stats['males'], stats['females'])
        self.scr.addstr(1, 0, pop_text_str)

        births = stats['births']
        m_deaths = stats['maternal_deaths']
        n_deaths = stats['natural_deaths']
        m_deathrate = 100.0 * float(m_deaths) / float(births) if births > 0 else 0.0
        n_deathrate = 100.0 * float(n_deaths) / float(births) if births > 0 else 0.0  # skewed because initial spawned entities are not in the birth count
        births_text_str = 'Births: %02d; Maternal Deaths: %02d (rate: %0.1f%%); Natural Deaths: %02d (rate: %0.1f%%)' % (births, m_deaths, m_deathrate, n_deaths, n_deathrate)
        self.scr.addstr(2, 0, births_text_str)

        self.scr.addstr(3, 0, 'Avg Age: %.1f, Stdv Age: %.1f' % (stats['age_avg'], stats['age_stdev']))

        self.scr.addstr(4, 0, 'Avg Health: %.1f, Stdv Health: %.1f' % (stats['health_avg'], stats['health_stdev']))

        self.scr.addstr(5, 0, 'Avg Size: %.1f, Stdv Size: %.1f' % (stats['size_avg'], stats['size_stdev']))

        self.scr.addstr(6, 0, 'Refreshes %d' % stats['display_iterations'])


        self.scr.addstr(8, 0, 'Key Commands:')
        self.scr.addstr(9, 0, '\tESC\t- Close program')
        self.scr.addstr(10, 0, '\ta\t- Toggle display of age as a color')
        self.scr.addstr(11, 0, '\tb\t- Toggle display of birth sparkle')
        self.scr.addstr(12, 0, '\th\t- Toggle display of health as a color')
        self.scr.addstr(13, 0, '\to\t- Toggle display of stats overlay')
        self.scr.addstr(14, 0, '\tp\t- Toggle display of phenotype color; overrides other entity colors')
        self.scr.addstr(15, 0, '\ts\t- Toggle display of sex as a color')

        self.terminal_lock.acquire()
        try:
            for i in range(len(self.messages)):
                self.scr.addstr(17+i, 0, self.messages[i])
        finally:
            self.terminal_lock.release()

        self.scr.refresh()
    # end def

    def shutdown(self):
        curses.nocbreak()
        curses.echo()
        curses.curs_set(True)
        # self.scr.keypad(False)
        curses.endwin()
    # end def
# end class

class DummyStats:
    def __init__(self):
        self.cycles = 0
        self.population = 0
# end class

if __name__ == "__main__":
    import time

    stats = DummyStats()
    terminal = TerminalDisplay()

    for i in range(10):
        terminal.run(stats)
        stats.cycles += 1
        stats.population += 10

        time.sleep(0.2)
    # end while

    terminal.shutdown()
# end if