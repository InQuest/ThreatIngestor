try:
    import ConfigParser as configparser
except:
    #py3
    import configparser

import sources.twitter
import sources.rss
import operators.threatkb
import operators.csv

SOURCE_MAP = {
    'twitter': sources.twitter.Twitter,
    'rss': sources.rss.RSS,
}

OPERATOR_MAP = {
    'threatkb': operators.threatkb.ThreatKB,
    'csv': operators.csv.CSV,
}

INTERNAL_OPTIONS = [
    'saved_state',
    'module',
]

class Config:

    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def daemon(self):
        """Returns boolean, are we daemonizing?"""
        return self.config.getboolean('main', 'daemon')

    def sleep(self):
        """Returns number of seconds to sleep between iterations, if daemonizing"""
        return self.config.getint('main', 'sleep')

    def sources(self):
        """Return a list of (name, Source class, {kwargs}) tuples"""
        sources = []
        for section in self.config.sections():
            if section.startswith('source:'):
                kwargs = {}
                for option in self.config.options(section):
                    if option not in INTERNAL_OPTIONS:
                        kwargs[option] = self.config.get(section, option)
                sources.append((section, SOURCE_MAP[self.config.get(section, 'module')], kwargs))
        return sources

    def operators(self):
        """Return a list of (name, Operator class, {kwargs}) tuples"""
        operators = []
        for section in self.config.sections():
            if section.startswith('operator:'):
                kwargs = {}
                for option in self.config.options(section):
                    if option not in INTERNAL_OPTIONS:
                        kwargs[option] = self.config.get(section, option)
                operators.append((section, OPERATOR_MAP[self.config.get(section, 'module')], kwargs))
        return operators

    def save_state(self, source, saved_state):
        """Save the state for a given source"""
        self.config.set(source, 'saved_state', saved_state)

        # write it out immediately
        with open(self.filename, 'w+') as f:
            self.config.write(f)

    def get_state(self, source):
        """Return saved_state for a given source"""
        # refresh the config
        self.config.read(self.filename)
        return self.config.get(source, 'saved_state')
