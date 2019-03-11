import sys
import time
import traceback


import threatingestor.config
import threatingestor.state
from threatingestor.exceptions import IngestorError


class Ingestor:
    """ThreatIngestor main work logic.

    Handles reading the config file, calling sources, maintaining state, and
    sending artifacts to operators.
    """
    def __init__(self, config_file):
        # Load config.
        try:
            self.config = config.Config(config_file)
        except IngestorError as e:
            # Error loading config.
            sys.stderr.write(e)
            sys.exit(1)

        # Load state DB.
        try:
            self.statedb = threatingestor.state.State(self.config.state_path())
        except (OSError, IOError) as e:
            # Error loading state DB.
            sys.stderr.write(e)
            sys.exit(1)

        # Instantiate plugins.
        self.sources = {name: source(**kwargs)
                        for name, source, kwargs in self.config.sources()}
        self.operators = {name: operator(**kwargs)
                          for name, operator, kwargs in self.config.operators()}


    def run(self):
        """Run once, or forever, depending on config."""
        if self.config.daemon():
            self.run_forever()
        else:
            self.run_once()


    def run_once(self):
        """Run each source once, passing artifacts to each operator."""
        for source in self.sources:
            # Run the source to collect artifacts.
            try:
                saved_state, artifacts = self.sources[source].run(self.statedb.get_state(source))
            except Exception as e:
                sys.stderr.write("Unknown error in source {s}: {e}\n".format(s=source, e=e))
                sys.stderr.write(traceback.format_exc())
                continue

            # Save the source state.
            self.statedb.save_state(source, saved_state)

            # Process artifacts with each operator.
            for operator in self.operators:
                try:
                    self.operators[operator].process(artifacts)
                except Exception as e:
                    sys.stderr.write("Unknown error in operator {o}: {e}\n".format(o=operator, e=e))
                    sys.stderr.write(traceback.format_exc())
                    continue


    def run_forever(self):
        """Run forever, sleeping for the configured interval between each run."""
        while True:
            self.run_once()
            time.sleep(self.config.sleep())


def main():
    """CLI entry point, uses sys.argv directly."""
    if len(sys.argv) < 2:
        print("You must specify a config file")
        sys.exit(1)

    app = Ingestor(sys.argv[1])
    app.run()


if __name__ == "__main__":
    main()
