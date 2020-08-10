import io
import importlib


import yaml
from loguru import logger


from threatingestor.exceptions import IngestorError, PluginError
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
NAME = 'name'


class Config:
    """Config read/write operations, and convenience methods."""
    def __init__(self, filename):
        """Read a config file."""
        self.filename = filename
        with io.open(self.filename, 'r') as f:
            try:
                self.config = yaml.safe_load(f.read())
            except yaml.error.YAMLError:
                raise IngestorError("YAML error in config")


    @staticmethod
    def _load_plugin(plugin_type, plugin):
        """Returns plugin class or raises an exception.

        :raises: threatingestor.exceptions.PluginError
        """
        try:
            module = importlib.import_module('.'.join([plugin_type, plugin]))
            return module.Plugin
        except (ImportError, AttributeError):
            raise PluginError("No valid plugin '{p}' in '{t}'".format(p=plugin, t=plugin_type))


    def daemon(self):
        """Returns boolean, are we daemonizing?"""
        return self.config['general']['daemon']


    def state_path(self):
        """Returns path of state.db file."""
        return self.config['general']['state_path']


    def sleep(self):
        """Returns number of seconds to sleep between iterations, if daemonizing."""
        return self.config['general']['sleep']


    def statsd(self):
        """Returns statsd config dictionary."""
        return self.config.get('statsd', {})


    def notifiers(self):
        """Returns notifiers config dictionary."""
        return self.config.get('notifiers', {})


    def logging(self):
        """Returns logging config dictionary."""
        return self.config.get('logging', {})


    def credentials(self, credential_name):
        """Return a dictionary with the specified credentials."""
        for credential in self.config['credentials']:
            for key, value in credential.items():
                if key == NAME and value == credential_name:
                    return credential
        return {}


    def sources(self):
        """Return a list of (name, Source class, {kwargs}) tuples.

        :raises: threatingestor.exceptions.PluginError
        """
        sources = []

        for source in self.config['sources']:
            kwargs = {}
            for key, value in source.items():
                if key not in INTERNAL_OPTIONS:
                    kwargs[key] = value

                elif key == 'credentials':
                    # Grab these named credentials
                    credential_name = value
                    for credential_key, credential_value in self.credentials(credential_name).items():
                        if credential_key != NAME:
                            kwargs[credential_key] = credential_value

            # load and initialize the plugin
            logger.debug(f"Found source '{source[NAME]}'")
            sources.append((source[NAME], self._load_plugin(SOURCE, source['module']), kwargs))

        logger.debug(f"Found {len(sources)} total sources")
        return sources


    def operators(self):
        """Return a list of (name, Operator class, {kwargs}) tuples.

        :raises: threatingestor.exceptions.PluginError
        """
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

                    elif key == NAME:
                        # exclude name key from operator kwargs, since it's not used
                        pass

                    else:
                        kwargs[key] = value

                elif key == 'credentials':
                    # Grab these named credentials
                    credential_name = value
                    for credential_key, credential_value in self.credentials(credential_name).items():
                        if credential_key != NAME:
                            kwargs[credential_key] = credential_value

            # load and initialize the plugin
            logger.debug(f"Found operator '{operator[NAME]}'")
            operators.append((operator[NAME], self._load_plugin(OPERATOR, operator['module']), kwargs))

        logger.debug(f"Found {len(operators)} total operators")
        return operators

    def whitelists(self):
        """Returns whitelist list."""
        return self.config.get("whitelists", [])