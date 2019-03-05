import io
import sys
import time


import watchdog.events
import watchdog.observers


import threatingestor.extras.queueworker


class FSWatcher(
        watchdog.events.PatternMatchingEventHandler,
        threatingestor.extras.queueworker.QueueWorker):

    # Only match YARA rules.
    patterns = ["*.yar", "*.yara", "*.rule", "*.rules"]

    def process(self, event):
        """Handle a file event."""
        with io.open(event.src_path, 'r') as rule_source:
            rule_content = rule_source.read()
            self.write_one(rule_content)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


if __name__ == '__main__':
    observer = watchdog.observers.Observer()
    worker = FSWatcher()
    worker.read_config(sys.argv[1])
    observer.schedule(worker, worker.config['watch_path'])
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
