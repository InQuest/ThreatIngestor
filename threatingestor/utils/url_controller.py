"""
This script is a standalone utility available to all sources. Currently, this script is only being used for expanding Twitter (t.co) shorteners but can be integrated into other places where URLs are ingested.
"""

from pyshorteners import Shortener, exceptions

s = Shortener()

class UrlController:
    def expand_url(url):
        """
        Expand ingested URLs with this method.

        If a URL is unknown or cannot be expanded, you'll get a "None" response.

        @param: url (Example: https://inquest.net)

        @rtype: str
        """
        
        try:
            expanded_link = s.tinyurl.expand(url)
            return str(expanded_link)
        # If unable to expand the URL, this exception is thrown
        except exceptions.ExpandingErrorException:
            return "None"