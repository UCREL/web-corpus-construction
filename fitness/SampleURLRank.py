from .URLRank import URLRank


class SampleURLRank(URLRank):

    def __init__(self, scale=1):
        URLRank.__init__(self, "Sample URL Rank", scale)

    def goodness(self, url):
        '''Overrides URLRank#goodness.

        Have a look at the practical document for examples of what this could
        be.'''

        return 0
