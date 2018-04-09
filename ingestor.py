import sys
import time

import config

class Ingestor:

    def __init__(self, config_file):
        self.config = config.Config(config_file)
        self.sources = dict([(name, source(**kwargs)) for name, source, kwargs in self.config.sources()])
        self.operators = dict([(name, operator(**kwargs)) for name, operator, kwargs in self.config.operators()])

    def run(self):
        if self.config.daemon():
            self.run_forever()
        else:
            self.run_once()

    def run_once(self):
        for source in self.sources:
            saved_state, artifacts = self.sources[source].run(self.config.get_state(source))
            self.config.save_state(source, saved_state)

            for operator in self.operators:
                self.operators[operator].process(artifacts)

    def run_forever(self):
        while True:
            self.run_once()
            time.sleep(self.config.sleep())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You must specify a config file")
        sys.exit(1)

    app = Ingestor(sys.argv[1])
    app.run()
