import sys
import time

import threatingestor.config
from threatingestor.exceptions import IngestorError
from threatingestor.state import State
class Ingestor:

    def __init__(self, config_file):
        try:
            self.config = config.Config(config_file)
        except IngestorError as e:
            # error loading config
            sys.stderr.write(e.message)
            sys.exit(1)
        
        self.statedb = State(self.config.state_path())

        self.sources = dict([(name, source(**kwargs)) for name, source, kwargs in self.config.sources()])
        self.operators = dict([(name, operator(**kwargs)) for name, operator, kwargs in self.config.operators()])

    def run(self):
        if self.config.daemon():
            self.run_forever()
        else:
            self.run_once()

    def run_once(self):
        for source in self.sources:
            saved_state, artifacts = self.sources[source].run(self.statedb.get_state(source))

            self.statedb.save_state(source, saved_state)


            for operator in self.operators:
                self.operators[operator].process(artifacts)

    def run_forever(self):
        while True:
            self.run_once()
            time.sleep(self.config.sleep())

def main():
    if len(sys.argv) < 2:
        print("You must specify a config file")
        sys.exit(1)

    app = Ingestor(sys.argv[1])
    app.run()

if __name__ == "__main__":
    main()
