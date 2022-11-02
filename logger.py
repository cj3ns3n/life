import logging

class Logger:
    def __init__(self, terminal, name, filename = None):
        if filename:
            logging.basicConfig(filename = filename, format='%(asctime)s %(levelname)s: %(message)s - %(name)s', filemode='w', level=logging.INFO)

        self.terminal_display = terminal
        self.name = name
        self.logger = logging.getLogger(name)
    # end def

    def refresh_terminal(self):
        self.terminal_display.run()
    # end def

    def shutdown(self):
        self.terminal_display.shutdown()
    # end def

    def debug(self, message, terminal = False):
        self.logger.debug(message)
        if terminal:
            self.terminal_display.add_message(message)
    # end def

    def info(self, message, terminal = False):
        self.logger.info(message)
        if terminal:
            self.terminal_display.add_message(message)
    # end def

    def warn(self, message, terminal = False):
        self.logger.warning(message)
        if terminal:
            self.terminal_display.add_message(message)
    # end def

    def error(self, message, terminal = False):
        self.logger.error(message)
        if terminal:
            self.terminal_display.add_message(message)
    # end def

    def get_logger(self, name):
        return Logger(self.terminal_display, '%s.%s' % (self.name, name))
    # end def
# end class