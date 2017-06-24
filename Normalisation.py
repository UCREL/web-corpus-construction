
import logging

from url_normalize import url_normalize

class URLNormaliser:

    def normalise(self, url):
        """Normalise a URL"""

        return url_normalize(str(url))





