import requests

from threatingestor.sources import Source

class Plugin(Source):
    """VirusTotal Comments Source Plugin"""
    def __init__(self, name, user, api_key, limit=10):
        self.name = name
        self.user = user
        self.api_key = api_key
        self.limit = limit

    def run(self, saved_state):
        """
        Returns a list of artifacts and the saved state
        """

        headers = {
            "x-apikey": self.api_key,
            "accept": "application/json"
        }

        # Collects the 10 most recent comments from a specific user on VT
        response = requests.get(f"https://www.virustotal.com/api/v3/users/{self.user}/comments?limit={self.limit}", headers=headers)

        artifacts = []
        
        for comment in response.json()['data']:
            if saved_state and int(saved_state) <= int(comment['attributes']['date']):
                continue

            saved_state = comment['attributes']['date']
            artifacts += self.process_element(content=comment['attributes']['text'], reference_link=comment['links']['self'])

        return saved_state, artifacts
