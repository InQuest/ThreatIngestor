import sys
import time
import traceback


from loguru import logger


import threatingestor.config
import threatingestor.state
import threatingestor.exceptions


class Ingestor:
    """ThreatIngestor main work logic.

    Handles reading the config file, calling sources, maintaining state, and
    sending artifacts to operators.
    """
    def __init__(self, config_file):
        # Load config.
        try:
            logger.debug(f"Reading config from '{config_file}'")
            self.config = config.Config(config_file)
        except (OSError, threatingestor.exceptions.IngestorError):
            # Error loading config.
            logger.exception("Couldn't read config")
            sys.exit(1)

        # Load state DB.
        try:
            logger.debug(f"Opening state database '{self.config.state_path()}'")
            self.statedb = threatingestor.state.State(self.config.state_path())
        except (OSError, IOError, threatingestor.exceptions.IngestorError):
            # Error loading state DB.
            logger.exception("Error reading state database")
            sys.exit(1)

        # Instantiate plugins.
        try:
            logger.debug("Initializing sources")
            self.sources = {name: source(**kwargs)
                            for name, source, kwargs in self.config.sources()}

            logger.debug("Initializing operators")
            self.operators = {name: operator(**kwargs)
                              for name, operator, kwargs in self.config.operators()}

        except (TypeError, ConnectionError, threatingestor.exceptions.PluginError):
            logger.exception("Error initializing plugins")
            sys.exit(1)


    def run(self):
        """Run once, or forever, depending on config."""
        if self.config.daemon():
            logger.debug("Running forever, in a loop")
            self.run_forever()
        else:
            logger.debug("Running once, to completion")
            self.run_once()


    def run_once(self):
        """Run each source once, passing artifacts to each operator."""
        for source in self.sources:
            # Run the source to collect artifacts.
            logger.debug(f"Running source '{source}'")
            try:
                saved_state, artifacts = self.sources[source].run(self.statedb.get_state(source))
            except Exception:
                logger.exception(f"Unknown error in source '{source}'")
                continue

            # Save the source state.
            self.statedb.save_state(source, saved_state)

            # Process artifacts with each operator.
            for operator in self.operators:
                print(source, operator)
                print(artifacts)
                logger.debug(f"Processing {len(artifacts)} artifacts from source '{source}' with operator '{operator}'")
                try:
                    self.operators[operator].process(artifacts)
                except Exception:
                    logger.exception(f"Unknown error in operator '{operator}'")
                    continue


    def run_forever(self):
        """Run forever, sleeping for the configured interval between each run."""
        while True:
            self.run_once()
            logger.debug(f"Sleeping for {self.config.sleep()} seconds")
            time.sleep(self.config.sleep())


def main():
    """CLI entry point, uses sys.argv directly."""
    if len(sys.argv) < 2:
        logger.error("You must specify a config file")
        sys.exit(1)

    app = Ingestor(sys.argv[1])
    app.run()


if __name__ == "__main__":
    main()
