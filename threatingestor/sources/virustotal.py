import datetime, requests

from threatingestor.sources import Source

class Plugin(Source):
    """VirusTotal Comments Source Plugin"""
    def __init__(self, name, user, api_key):
        self.name = name
        self.user = user
        self.api_key = api_key

    def run(self, saved_state):
        """
        Returns a list of artifacts and the saved state
        """

        headers = {
            "x-apikey": self.api_key,
            "accept": "application/json"
        }

        response = requests.get(f"https://www.virustotal.com/api/v3/users/{self.user}/comments?limit=10", headers=headers)
        saved_state = datetime.datetime.utcnow()

        artifacts = []
        
        for comment in response.json()['data']:
            artifacts += self.process_element(content=comment['attributes']['text'], reference_link=comment['links']['self'])

        return saved_state, artifacts
