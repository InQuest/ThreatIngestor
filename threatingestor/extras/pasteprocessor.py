import sys


import requests


import threatingestor.extras.queueworker


class PasteProcessor(threatingestor.extras.queueworker.QueueWorker):
    """Read pastebin URLs from a queue, write raw content to a queue."""

    def do_work(self, job):
        """From a paste URL, get the raw contents."""
        try:
            url = job['url']

        except KeyError:
            print(f"Bad job: {job}")
            return

        # Pastebin.com
        if url.startswith("https://pastebin.com/raw/"):
            pass

        elif url.startswith("https://pastebin.com/"):
            start, end = url.split['.com/']
            url = '.com/raw/'.join([start, end])

        # Gist
        elif url.startswith("https://gist.github.com/") and not 'raw' in url:
            url = url + '/raw'

        # Fetch and return.
        response = requests.get(url)
        return {
            'content': response.content,
            'reference': response.url,
        }


if __name__ == "__main__":
    worker = PasteProcessor()
    worker.read_config(sys.argv[1])
    worker.run_forever()
