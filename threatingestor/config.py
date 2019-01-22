import io
import importlib
try:
    import ConfigParser as configparser
except ImportError:
    #py3
    import configparser

import yaml

from threatingestor.exceptions import PluginError
import threatingestor.artifacts

SOURCE = 'threatingestor.sources'
OPERATOR = 'threatingestor.operators'

INTERNAL_OPTIONS = [
    'saved_state',
    'module',
    'credentials',
]

ARTIFACT_TYPES = 'artifact_types'
FILTER_STRING = 'filter'
ALLOWED_SOURCES = 'allowed_sources'


class Config:

    def __init__(self, filename):
        self.filename = filename
        with io.open(self.filename, 'r') as f:
            self.config = yaml.load_safe(f.read())

    @staticmethod
    def _load_plugin(plugin_type, plugin):
        """Returns plugin class or raises an exception"""
        try:
            module = importlib.import_module('.'.join([plugin_type, plugin]))
            return module.Plugin
        except (ImportError, AttributeError):
            raise PluginError("No valid plugin '{p}' in '{t}'".format(p=plugin, t=plugin_type))

    def daemon(self):
        """Returns boolean, are we daemonizing?"""
        return self.config['general']['daemon']

    def state_path(self):
        """Returns path of state.db file"""
        return self.config['general']['state_path']

    def sleep(self):
        """Returns number of seconds to sleep between iterations, if daemonizing"""
        return self.config['general']['sleep']

    def credentials(self, credential_name):
        """Return a dictionary with the specified credentials"""
        for credential in self.config['credentials']:
            for key, value in credential.items():
                if key == 'name' and value == credential_name:
                    return credential

    def sources(self):
        """Return a list of (name, Source class, {kwargs}) tuples"""
        sources = []

        for source in self.config['sources']:
            # initialize kwargs with required name argument
            kwargs = {'name': source['name']}
            for key, value in source.items():
                if key not in INTERNAL_OPTIONS:
                    kwargs[key] = value

                elif key == 'credentials':
                    # Grab these named credentials
                    credential_name = value
                    for credential_key, credential_value in self.credentials(credential_name).items():
                        if credential_key != 'name':
                            kwargs[credential_key] = credential_value

            # load and initialize the plugin
            sources.append((source['name'], self._load_plugin(SOURCE, source['module']), kwargs))

        return sources

    def operators(self):
        """Return a list of (name, Operator class, {kwargs}) tuples"""
        operators = []
        for operator in self.config['operators']:
            kwargs = {}
            for key, value in operator.items():
                if key not in INTERNAL_OPTIONS:
                    if key == ARTIFACT_TYPES:
                        # parse out special artifact_types option
                        artifact_types = []
                        for artifact in value:
                            try:
                                artifact_types.append(threatingestor.artifacts.STRING_MAP[artifact.lower().strip()])
                            except KeyError:
                                # ignore invalid artifact types
                                pass
                        kwargs[key] = artifact_types

                    elif key == FILTER_STRING:
                        # pass in special filter_string option
                        kwargs['filter_string'] = value

                    elif key == ALLOWED_SOURCES:
                        kwargs[key] = [s.strip() for s in value]

                    else:
                        kwargs[key] = value

                elif key == 'credentials':
                    # Grab these named credentials
                    credential_name = value
                    for credential_key, credential_value in self.credentials(credential_name).items():
                        if credential_key != 'name':
                            kwargs[credential_key] = credential_value

            # load and initialize the plugin
            operators.append((operator["name"], self._load_plugin(OPERATOR, operator['module']), kwargs))

        return operators

    def save_state(self, source, saved_state):
        """Save the state for a given source"""
        self.config.set(source, 'saved_state', str(saved_state or ''))

        # write it out immediately
        with open(self.filename, 'w+') as f:
            self.config.write(f)

    def get_state(self, source):
        """Return saved_state for a given source"""
        # refresh the config
        self.config.read(self.filename)
        return self.config.get(source, 'saved_state')
