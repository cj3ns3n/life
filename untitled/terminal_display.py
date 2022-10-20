import curses
import sys

class TerminalDisplay:
    def __init__(self):
        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        if curses.has_colors():
            curses.start_color()
    # end def

    def run(self, stats):
        self.scr.addstr(0, 0, "Cycles: %d" % stats.cycles)
        self.scr.addstr(1, 0, "Population: %d" % stats.population)
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