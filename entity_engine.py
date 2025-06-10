import threading

class EntityEngine(threading.Thread):
    def __init__(self, simulation, stats_container, logger):
        threading.Thread.__init__(self)

        self.simulation = simulation
        self.stats = stats_container
        self.logger = logger
    # end def

    def run(self):
        while True:
            stats_thread = None
            self.simulation.tick()

            self.stats.increment_cycles()
            self.logger.info('cycle completed: %d' % (self.stats.cycles))

            if stats_thread is None or not stats_thread.is_alive():
                stats_thread = threading.Thread(target=self.stats.calc_stats)
                stats_thread.start()
                stats_thread.join()  # forced to join until locking to implemented
        # end while
    # end def

    def get_processed_rows(self):
        return self.simulation.get_processed_rows()
    # end def
# end class
