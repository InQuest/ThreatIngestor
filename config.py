try:
    import ConfigParser as configparser
except ImportError:
    #py3
    import configparser

import artifacts
import sources.twitter
import sources.rss
import sources.sqs
import sources.web
import sources.git
import operators.threatkb
import operators.csv
import operators.sqs

SOURCE_MAP = {
    # Add new source plugins here
    'twitter': sources.twitter.Twitter,
    'rss': sources.rss.RSS,
    'sqs': sources.sqs.SQS,
    'web': sources.web.Web,
    'git': sources.git.Git,
}

OPERATOR_MAP = {
    # Add new operator plugins here
    'threatkb': operators.threatkb.ThreatKB,
    'csv': operators.csv.CSV,
    'sqs': operators.sqs.SQS,
}

INTERNAL_OPTIONS = [
    'saved_state',
    'module',
]

ARTIFACT_TYPES = 'artifact_types'
FILTER_STRING = 'filter'
ALLOWED_SOURCES = 'allowed_sources'


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
                # initialize kwargs with required name argument
                kwargs = {'name': section.lstrip('source:')}
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
                        if option == ARTIFACT_TYPES:
                            # parse out special artifact_types option
                            types_list = self.config.get(section, option).split(',')
                            artifact_types = []
                            for artifact in types_list:
                                try:
                                    artifact_types.append(artifacts.STRING_MAP[artifact.lower().strip()])
                                except KeyError:
                                    # ignore invalid artifact types
                                    pass
                            kwargs[option] = artifact_types
                        elif option == FILTER_STRING:
                            # pass in special filter_string option
                            kwargs['filter_string'] = self.config.get(section, option)
                        elif option == ALLOWED_SOURCES:
                            kwargs[option] = [s.strip() for s in self.config.get(section, option).split(',')]
                        else:
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
